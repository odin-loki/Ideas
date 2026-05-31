"""
BSG-10 Simulation Suite — Module: Internal Ballistics
======================================================
Simulates chamber pressure, projectile velocity, and gas port timing
for the 10-gauge 3.5" magnum canister load with progressive powder.

Physics model
-------------
Rising phase  (0 → x_peak):  P = P_peak * (x/x_peak)^rise_exp
Expansion phase (x_peak → L): P = P_peak * (V_peak/V)^gamma
                               adiabatic-like with effective γ = 1.12

Calibration: binary search on P_peak until muzzle velocity = target.
"""

from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


@dataclass
class BallisticsResult:
    P_peak:       float          # Pa  calibrated peak pressure
    muzzle_vel:   float          # m/s
    transit_time: float          # s
    port_pressure: float         # Pa  at gas port
    port_velocity: float         # m/s at gas port
    port_time:    float          # s   time projectile reaches gas port
    muzzle_pressure: float       # Pa
    impulse_shot: float          # N·s
    impulse_gas:  float          # N·s
    impulse_total: float         # N·s
    x:            np.ndarray     # m   position array
    P:            np.ndarray     # Pa  pressure array
    v:            np.ndarray     # m/s velocity array
    t:            np.ndarray     # s   time array
    saami_pass:   bool


def _build_profile(P_peak: float, cfg: BSG10Config,
                   n_steps: int = 5000) -> tuple[np.ndarray, ...]:
    """Build pressure, velocity, and time arrays for a given P_peak."""
    c = cfg.cartridge
    b = cfg.barrel
    x  = np.linspace(0.0, b.length, n_steps)
    dx = x[1] - x[0]
    P  = np.zeros(n_steps)

    for i, xi in enumerate(x):
        if xi <= c.x_peak:
            P[i] = P_peak * (xi / c.x_peak) ** c.rise_exp if xi > 0 else 1e5
        else:
            Vi   = c.case_volume + c.bore_area * xi
            Vp   = c.case_volume + c.bore_area * c.x_peak
            P[i] = P_peak * (Vp / Vi) ** c.gamma

    # Velocity via work–energy theorem
    F = c.bore_area * np.maximum(P - 1.01325e5, 0.0) * 0.97   # 3% friction
    v = np.zeros(n_steps)
    for i in range(1, n_steps):
        KE   = 0.5 * c.payload_mass * v[i-1]**2 + 0.5*(F[i-1]+F[i])*dx
        v[i] = np.sqrt(max(2.0 * KE / c.payload_mass, 0.0))

    # Time
    t = np.zeros(n_steps)
    for i in range(1, n_steps):
        v_avg = max((v[i-1] + v[i]) / 2.0, 0.01)
        t[i]  = t[i-1] + dx / v_avg

    return x, P, v, t


def _muzzle_velocity(P_peak: float, cfg: BSG10Config) -> float:
    _, _, v, _ = _build_profile(P_peak, cfg)
    return float(v[-1])


def calibrate(cfg: BSG10Config = DEFAULT_CONFIG,
              tol: float = 0.05) -> BallisticsResult:
    """
    Binary-search calibrate P_peak to match cfg.cartridge.target_vel.

    Parameters
    ----------
    cfg : BSG10Config
    tol : float   convergence tolerance (m/s)

    Returns
    -------
    BallisticsResult
    """
    c = cfg.cartridge
    b = cfg.barrel

    lo, hi = 20e6, 130e6
    for _ in range(80):
        mid = (lo + hi) / 2.0
        vm  = _muzzle_velocity(mid, cfg)
        if vm < c.target_vel:
            lo = mid
        else:
            hi = mid

    P_peak = (lo + hi) / 2.0
    x, P, v, t = _build_profile(P_peak, cfg)

    ip  = int(np.argmin(np.abs(x - b.gas_port)))

    I_shot  = float(c.payload_mass * v[-1])
    I_gas   = float(c.powder_mass * 1.75 * v[-1])
    I_total = I_shot + I_gas

    return BallisticsResult(
        P_peak        = float(P_peak),
        muzzle_vel    = float(v[-1]),
        transit_time  = float(t[-1]),
        port_pressure = float(P[ip]),
        port_velocity = float(v[ip]),
        port_time     = float(t[ip]),
        muzzle_pressure = float(P[-1]),
        impulse_shot  = I_shot,
        impulse_gas   = I_gas,
        impulse_total = I_total,
        x             = x,
        P             = P,
        v             = v,
        t             = t,
        saami_pass    = bool(P_peak <= c.saami_limit),
    )


def print_results(r: BallisticsResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    c = cfg.cartridge
    b = cfg.barrel
    print("\n" + "="*62)
    print("MODULE A — INTERNAL BALLISTICS")
    print("="*62)
    print(f"  Peak pressure:        {r.P_peak/1e6:.2f} MPa  ({r.P_peak/6894.76:.0f} PSI)")
    print(f"  SAAMI 10-ga limit:    {c.saami_limit/1e6:.1f} MPa  (11,000 PSI)")
    print(f"  SAAMI margin:         {(c.saami_limit - r.P_peak)/c.saami_limit*100:.1f}%  "
          f"{'PASS' if r.saami_pass else 'FAIL *** REDESIGN ***'}")
    print(f"  Muzzle velocity:      {r.muzzle_vel:.1f} m/s  (target {c.target_vel} m/s)")
    print(f"  Transit time:         {r.transit_time*1e3:.2f} ms")
    print(f"  Gas port @ {b.gas_port*1e3:.0f} mm:")
    print(f"    Pressure            {r.port_pressure/1e6:.1f} MPa")
    print(f"    Velocity            {r.port_velocity:.1f} m/s")
    print(f"    Time                {r.port_time*1e6:.0f} μs")
    print(f"  Muzzle pressure:      {r.muzzle_pressure/1e6:.2f} MPa")
    print(f"  Impulse (shot):       {r.impulse_shot:.2f} N·s")
    print(f"  Impulse (gas):        {r.impulse_gas:.2f} N·s")
    print(f"  Impulse (total):      {r.impulse_total:.2f} N·s")


def plot(r: BallisticsResult, cfg: BSG10Config = DEFAULT_CONFIG,
         save: bool = True) -> plt.Figure:
    """Generate three-panel ballistics figure."""
    c = cfg.cartridge
    b = cfg.barrel
    ip = int(np.argmin(np.abs(r.x - b.gas_port)))

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle("Module A — Internal Ballistics (10-ga 3.5\" Magnum, γ=1.12)",
                 fontweight="bold")

    # Pressure vs position
    ax = axes[0]
    ax.plot(r.x*1e3, r.P/1e6, color="firebrick", lw=2)
    ax.axvline(b.gas_port*1e3, ls="--", color="navy", label=f"Gas port {b.gas_port*1e3:.0f} mm")
    ax.axhline(c.saami_limit/1e6, ls=":", color="orange", lw=2, label="SAAMI limit")
    ax.axhline(r.P_peak/1e6, ls="--", color="firebrick", alpha=0.4,
               label=f"P_peak {r.P_peak/1e6:.1f} MPa")
    ax.set(xlabel="Position (mm)", ylabel="Pressure (MPa)", title="Pressure vs Position")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Velocity vs position
    ax = axes[1]
    ax.plot(r.x*1e3, r.v, color="steelblue", lw=2)
    ax.axvline(b.gas_port*1e3, ls="--", color="navy")
    ax.axhline(c.target_vel, ls=":", color="green", label=f"Target {c.target_vel} m/s")
    ax.axhline(r.muzzle_vel, ls="--", color="steelblue", alpha=0.4,
               label=f"Muzzle {r.muzzle_vel:.0f} m/s")
    ax.set(xlabel="Position (mm)", ylabel="Velocity (m/s)", title="Payload Velocity vs Position")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Pressure vs time
    ax = axes[2]
    ax.plot(r.t*1e3, r.P/1e6, color="darkorange", lw=2)
    ax.axvline(r.port_time*1e3, ls="--", color="navy",
               label=f"Gas port t={r.port_time*1e3:.2f} ms")
    ax.axhline(c.saami_limit/1e6, ls=":", color="orange", lw=2, label="SAAMI limit")
    ax.set(xlabel="Time (ms)", ylabel="Pressure (MPa)", title="Pressure vs Time")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        path = f"{OUTPUT_DIR}/A_internal_ballistics.png"
        fig.savefig(path, dpi=130)
        print(f"  → Saved: A_internal_ballistics.png")
    return fig


def run(cfg: BSG10Config = DEFAULT_CONFIG, plot_results: bool = True) -> BallisticsResult:
    """Run the full internal ballistics simulation."""
    result = calibrate(cfg)
    print_results(result, cfg)
    if plot_results:
        plot(result, cfg)
    return result
