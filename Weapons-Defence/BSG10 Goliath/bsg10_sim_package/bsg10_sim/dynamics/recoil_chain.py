"""
BSG-10 Simulation Suite — Module: Integrated Recoil Chain
==========================================================
Time-domain simulation of the full recoil path:
    firing impulse → compensator → floating barrel →
    balanced action → hydraulic buffer → CBS-10 → shoulder

Two models are run:
  1. Analytical bound  — gun arrives at CBS at full free-recoil velocity
  2. Time-domain ODE   — firing pulse applied while CBS acts simultaneously
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR
from .balanced_action import ActionResult


@dataclass
class RecoilResult:
    I_raw:              float       # N·s  total raw impulse
    I_after_comp:       float       # N·s  after compensator
    v0_gun:             float       # m/s  free-recoil velocity (post-comp)
    peak_force_bound:   float       # N    analytical bound (conservative)
    peak_force_td:      float       # N    time-domain result
    cbs_max_travel_mm:  float       # mm   CBS-10 max compression
    travel_pass:        bool
    t_peak_ms:          float       # ms   time of peak force
    ref_12ga_N:         float       # N    12-ga field reference
    raw_10ga_est_N:     float       # N    estimated raw 10-ga force
    reduction_pct:      float       # % vs raw 10-ga
    t:  np.ndarray
    v:  np.ndarray                  # m/s  gun velocity
    x:  np.ndarray                  # m    CBS compression
    F:  np.ndarray                  # N    shoulder force


def _cbs_analytical(I_eff: float, M_gun: float,
                    rc) -> tuple[float, float]:
    """
    Conservative analytical estimate: gun hits CBS at full free-recoil velocity.
    Returns (peak_force, max_travel).
    """
    v0 = I_eff / M_gun
    dt   = 1e-5
    t    = np.arange(0, 0.50, dt)
    x    = np.zeros_like(t)
    v    = np.zeros_like(t)
    v[0] = v0

    for i in range(1, len(t)):
        Fs = rc.spring_force(x[i-1])
        Fd = rc.damper_force(v[i-1])
        F_total = Fs + Fd
        a = -F_total / M_gun
        v[i] = v[i-1] + a * dt
        x[i] = x[i-1] + v[i] * dt
        if x[i] < 0:
            x[i] = 0.0

    F_shoulder = np.array([
        rc.spring_force(min(max(xi, 0), rc.cbs_travel)) +
        rc.damper_force(vi)
        for xi, vi in zip(x, v)
    ])
    return float(np.max(np.maximum(F_shoulder, 0))), float(np.max(x)) * 1e3


def simulate(cfg: BSG10Config = DEFAULT_CONFIG,
             I_total: float = 32.11,
             t_end: float = 0.50) -> RecoilResult:
    """
    Run both analytical bound and time-domain recoil simulation.

    Parameters
    ----------
    cfg     : BSG10Config
    I_total : float   total raw recoil impulse (N·s), from ballistics module
    t_end   : float   simulation duration (s)
    """
    rc  = cfg.recoil
    sys = cfg.system

    n_rounds    = cfg.magazine.drum_od  # dummy — use loaded mass directly
    M_gun       = sys.loaded_mass(45)   # 45-round drum

    I_eff       = I_total * (1.0 - rc.comp_efficiency)
    v0_gun      = I_eff / M_gun

    # Analytical bound
    F_bound, max_travel_bound = _cbs_analytical(I_eff, M_gun, rc)

    # Time-domain ODE
    # Firing impulse as half-sine over transit time
    t_fire   = 0.00221
    F_pk_fire = I_eff / (t_fire * np.pi / 2) * np.pi / 2

    def ode(t_sim, y):
        x_cbs, v_gun = y
        t_rel = t_sim

        # Firing force (half-sine pulse)
        F_fire = (F_pk_fire * np.sin(np.pi * t_rel / t_fire)
                  if t_rel < t_fire else 0.0)

        # CBS restoring force (only while compressed)
        if x_cbs > 0:
            Fs = rc.spring_force(min(x_cbs, rc.cbs_travel))
            Fd = rc.damper_force(v_gun)
            F_cbs = Fs + Fd
        else:
            F_cbs = 0.0

        F_net = F_fire - F_cbs
        a_gun = F_net / M_gun
        return [v_gun, a_gun]

    dt_eval = 5e-5
    t_eval  = np.arange(0.0, t_end, dt_eval)
    sol = solve_ivp(ode, (0.0, t_end), [0.0, 0.0],
                    t_eval=t_eval, method="RK45", max_step=1e-4)

    x_cbs = sol.y[0]
    v_gun = sol.y[1]

    F_sh = np.array([
        max(rc.spring_force(min(max(xi, 0), rc.cbs_travel)) +
            rc.damper_force(vi), 0.0)
        for xi, vi in zip(x_cbs, v_gun)
    ])

    peak_td      = float(np.max(F_sh))
    t_peak_ms    = float(sol.t[np.argmax(F_sh)]) * 1e3
    cbs_max_mm   = float(np.max(x_cbs)) * 1e3

    REF_12GA     = 1800.0
    RAW_10GA     = 4200.0
    reduction    = (1.0 - peak_td / RAW_10GA) * 100.0

    return RecoilResult(
        I_raw             = I_total,
        I_after_comp      = I_eff,
        v0_gun            = v0_gun,
        peak_force_bound  = F_bound,
        peak_force_td     = peak_td,
        cbs_max_travel_mm = cbs_max_mm,
        travel_pass       = cbs_max_mm <= rc.cbs_travel * 1e3,
        t_peak_ms         = t_peak_ms,
        ref_12ga_N        = REF_12GA,
        raw_10ga_est_N    = RAW_10GA,
        reduction_pct     = reduction,
        t = sol.t,
        v = v_gun,
        x = x_cbs,
        F = F_sh,
    )


def print_results(r: RecoilResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    rc = cfg.recoil
    print("\n" + "="*62)
    print("MODULE C — INTEGRATED RECOIL CHAIN")
    print("="*62)
    print(f"  Raw impulse:              {r.I_raw:.2f} N·s")
    print(f"  After compensator (−{cfg.recoil.comp_efficiency*100:.0f}%): "
          f"{r.I_after_comp:.2f} N·s")
    print(f"  Gun free-recoil vel:      {r.v0_gun:.3f} m/s")
    print(f"  CBS-10 max compression:   {r.cbs_max_travel_mm:.1f} mm  "
          f"(limit {rc.cbs_travel*1e3:.0f} mm)  "
          f"{'PASS' if r.travel_pass else 'FAIL'}")
    print(f"  Peak force (analytical):  {r.peak_force_bound:.0f} N  (conservative bound)")
    print(f"  Peak force (time-domain): {r.peak_force_td:.0f} N  (integrated result)")
    print(f"  Time of peak:             {r.t_peak_ms:.1f} ms")
    print(f"  12-ga reference:          {r.ref_12ga_N:.0f} N")
    print(f"  Raw 10-ga estimate:       {r.raw_10ga_est_N:.0f} N")
    print(f"  Reduction vs raw 10-ga:   {r.reduction_pct:.1f}%")
    cmp = "SOFTER" if r.peak_force_td < r.ref_12ga_N else "SIMILAR"
    print(f"  vs 12-ga field gun:       {cmp}")


def plot(r: RecoilResult, cfg: BSG10Config = DEFAULT_CONFIG,
         save: bool = True) -> plt.Figure:
    rc = cfg.recoil
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Module C — Integrated Recoil Simulation", fontweight="bold")

    axes[0,0].plot(r.t*1e3, r.v, color="firebrick", lw=2)
    axes[0,0].axhline(0, ls="--", color="grey", lw=0.8)
    axes[0,0].set(xlabel="Time (ms)", ylabel="Velocity (m/s)",
                  title="Gun Velocity (free recoil)")
    axes[0,0].grid(True, alpha=0.3)

    axes[0,1].plot(r.t*1e3, r.x*1e3, color="steelblue", lw=2)
    axes[0,1].axhline(rc.cbs_travel*1e3, ls="--", color="orange", label="Travel limit")
    axes[0,1].set(xlabel="Time (ms)", ylabel="Compression (mm)",
                  title="CBS-10 Compression vs Time")
    axes[0,1].legend(fontsize=7); axes[0,1].grid(True, alpha=0.3)

    axes[1,0].plot(r.t*1e3, r.F, color="darkorange", lw=2, label="BSG-10 (all mitigations)")
    axes[1,0].axhline(r.ref_12ga_N,  ls="--", color="green",
                      label=f"12-ga ref ({r.ref_12ga_N:.0f} N)")
    axes[1,0].axhline(r.raw_10ga_est_N, ls=":", color="red",
                      label=f"Raw 10-ga ({r.raw_10ga_est_N:.0f} N)")
    axes[1,0].axhline(r.peak_force_td, ls="--", color="navy",
                      label=f"BSG-10 peak ({r.peak_force_td:.0f} N)")
    axes[1,0].set(xlabel="Time (ms)", ylabel="Force (N)",
                  title="Shoulder Force vs Time", xlim=(0, 100))
    axes[1,0].legend(fontsize=7); axes[1,0].grid(True, alpha=0.3)

    scenarios = ["Raw\n10-ga\n(no mitigation)", "12-ga\nField Gun\n(reference)",
                 "BSG-10\n(all layers)"]
    forces    = [r.raw_10ga_est_N, r.ref_12ga_N, r.peak_force_td]
    clrs      = ["#e74c3c", "#f39c12", "#27ae60"]
    bars = axes[1,1].bar(scenarios, forces, color=clrs, edgecolor="black", lw=1.2)
    for bar, val in zip(bars, forces):
        axes[1,1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+40,
                       f"{val:.0f} N", ha="center", fontsize=9, fontweight="bold")
    axes[1,1].set(ylabel="Peak Shoulder Force (N)", title="Recoil Mitigation Comparison")
    axes[1,1].grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    if save:
        fig.savefig(f"{OUTPUT_DIR}/C_recoil_chain.png", dpi=130)
        print("  → Saved: C_recoil_chain.png")
    return fig


def run(cfg: BSG10Config = DEFAULT_CONFIG,
        I_total: float = 32.11,
        plot_results: bool = True) -> RecoilResult:
    result = simulate(cfg, I_total)
    print_results(result, cfg)
    if plot_results:
        plot(result, cfg)
    return result
