"""
BSG-10 Simulation Suite — Module: Balanced Action Dynamics
==========================================================
Solves the coupled ODE for bolt carrier + counter-mass rack/pinion system.
Quantifies cycling impulse cancellation and carrier stroke.

Physics
-------
Effective mass for coupled system:
    m_eff = m_carrier + m_counter / R²

Gear constraint: v_counter = R * v_carrier (momentum balance)
Net cycling impulse on frame = (m_c - m_k/R) * v_max  (residual)
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


@dataclass
class ActionResult:
    carrier_stroke_mm:   float       # mm  max carrier travel
    carrier_vel_max:     float       # m/s
    counter_vel_max:     float       # m/s
    impulse_raw:         float       # N·s unbalanced cycling impulse
    impulse_balanced:    float       # N·s balanced residual
    reduction_pct:       float       # %
    stroke_pass:         bool        # within limit?
    t:  np.ndarray
    xc: np.ndarray                   # m   carrier position
    vc: np.ndarray                   # m/s carrier velocity
    xk: np.ndarray                   # m   counter-mass position
    vk: np.ndarray                   # m/s counter-mass velocity


def _gas_force_on_carrier(t: float) -> float:
    """
    Gas force on bolt face after shot exits.
    Modelled as triangular pulse: rise 1 ms, decay 4 ms.
    """
    t_rise  = 0.001
    t_decay = 0.004
    f_peak  = 8500.0    # N
    if t < t_rise:
        return f_peak * t / t_rise
    elif t < t_rise + t_decay:
        return f_peak * (1.0 - (t - t_rise) / t_decay)
    return 0.0


def simulate(cfg: BSG10Config = DEFAULT_CONFIG,
             t_end: float = 0.030) -> ActionResult:
    """
    Solve coupled carrier + counter-mass ODE.

    Parameters
    ----------
    cfg   : BSG10Config
    t_end : float   simulation duration (s)

    Returns
    -------
    ActionResult
    """
    a = cfg.action
    R     = a.gear_ratio
    m_eff = a.carrier_mass + a.counter_mass / R**2

    # Return spring on counter-mass
    k_ret = 5000.0   # N/m

    def ode(t, y):
        xc, vc, xk, vk = y
        Fg = _gas_force_on_carrier(t)

        # Buffer force
        F_buf = (a.buf_k * xc + a.buf_c * vc) if xc > 0 else 0.0

        # Net on combined system
        F_net = Fg - F_buf
        ac    = F_net / m_eff
        ak    = R * ac - (k_ret * xk) / a.counter_mass

        return [vc, ac, vk, ak]

    t_eval = np.linspace(0.0, t_end, 3000)
    sol = solve_ivp(ode, (0.0, t_end), [0.0, 0.0, 0.0, 0.0],
                    t_eval=t_eval, method="RK45", max_step=1e-5)

    xc = sol.y[0]; vc = sol.y[1]
    xk = sol.y[2]; vk = sol.y[3]

    stroke_mm    = float(np.max(np.abs(xc))) * 1e3
    vc_max       = float(np.max(np.abs(vc)))
    vk_max       = float(np.max(np.abs(vk)))
    I_raw        = a.carrier_mass * vc_max
    residual_f   = abs(a.carrier_mass - a.counter_mass / R)
    I_balanced   = residual_f * vc_max
    reduction    = (1.0 - I_balanced / I_raw) * 100.0 if I_raw > 0 else 0.0

    return ActionResult(
        carrier_stroke_mm  = stroke_mm,
        carrier_vel_max    = vc_max,
        counter_vel_max    = vk_max,
        impulse_raw        = I_raw,
        impulse_balanced   = I_balanced,
        reduction_pct      = reduction,
        stroke_pass        = stroke_mm <= a.carrier_stroke * 1e3,
        t = sol.t, xc=xc, vc=vc, xk=xk, vk=vk,
    )


def print_results(r: ActionResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    a = cfg.action
    print("\n" + "="*62)
    print("MODULE B — BALANCED ACTION DYNAMICS")
    print("="*62)
    print(f"  Gear ratio (momentum balance): {a.gear_ratio:.3f}")
    print(f"  Carrier stroke:       {r.carrier_stroke_mm:.1f} mm  "
          f"(limit {a.carrier_stroke*1e3:.0f} mm)  "
          f"{'PASS' if r.stroke_pass else 'FAIL'}")
    print(f"  Max carrier velocity: {r.carrier_vel_max:.2f} m/s")
    print(f"  Max counter velocity: {r.counter_vel_max:.2f} m/s")
    print(f"  Cycling impulse (raw):        {r.impulse_raw:.3f} N·s")
    print(f"  Cycling impulse (balanced):   {r.impulse_balanced:.3f} N·s")
    print(f"  Reduction:            {r.reduction_pct:.1f}%")


def plot(r: ActionResult, cfg: BSG10Config = DEFAULT_CONFIG,
         save: bool = True) -> plt.Figure:
    a = cfg.action
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle("Module B — Balanced Action Dynamics", fontweight="bold")

    axes[0].plot(r.t*1e3, r.xc*1e3,  color="firebrick", lw=2, label="Carrier (rearward)")
    axes[0].plot(r.t*1e3, r.xk*1e3,  color="steelblue", lw=2, label="Counter-mass (forward)")
    axes[0].axhline(a.carrier_stroke*1e3, ls="--", color="orange", label="Stroke limit")
    axes[0].set(xlabel="Time (ms)", ylabel="Displacement (mm)", title="Component Displacement")
    axes[0].legend(fontsize=7); axes[0].grid(True, alpha=0.3)

    axes[1].plot(r.t*1e3, r.vc, color="firebrick",  lw=2, label="Carrier")
    axes[1].plot(r.t*1e3, r.vk, color="steelblue",  lw=2, label="Counter-mass")
    axes[1].axhline(0, ls="--", color="grey", lw=0.8)
    axes[1].set(xlabel="Time (ms)", ylabel="Velocity (m/s)", title="Component Velocities")
    axes[1].legend(fontsize=7); axes[1].grid(True, alpha=0.3)

    p_c   = a.carrier_mass * r.vc
    p_k   = a.counter_mass * r.vk
    p_net = p_c + p_k
    axes[2].plot(r.t*1e3, p_c,   color="firebrick",  lw=2, label="Carrier momentum")
    axes[2].plot(r.t*1e3, -p_k,  color="steelblue",  lw=2, label="Counter momentum (−)")
    axes[2].plot(r.t*1e3, p_net, color="black",       lw=1.2, label="Net cycling")
    axes[2].set(xlabel="Time (ms)", ylabel="Momentum (N·s)", title="Momentum Cancellation")
    axes[2].legend(fontsize=7); axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        fig.savefig(f"{OUTPUT_DIR}/B_balanced_action.png", dpi=130)
        print("  → Saved: B_balanced_action.png")
    return fig


def run(cfg: BSG10Config = DEFAULT_CONFIG,
        plot_results: bool = True) -> ActionResult:
    result = simulate(cfg)
    print_results(result, cfg)
    if plot_results:
        plot(result, cfg)
    return result
