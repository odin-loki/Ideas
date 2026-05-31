"""
BSG-10 Simulation Suite — Module: Parts Life Analysis
======================================================
Physics-based lifecycle models for all major components.

Models used
-----------
Barrel erosion    : power-law erosion rate calibrated to field data
Bolt lugs         : S-N fatigue + Archard fretting wear
CBS-10 springs    : compression set (exponential asymptotic model)
CBS-10 seals      : Archard tribological wear (PTFE on chrome)
CBS-10 pads       : compression set (Sorbothane, D3O)
Gas piston        : power-law erosion (port-face exposure)
Gas cylinder      : bore wear (Archard)
Barrel bushings   : Archard (PTFE-bronze, low-PV regime)
"""

from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from dataclasses import dataclass, field
from typing import List, Dict
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


# ════════════════════════════════════════════════════════════════
# RESULT CONTAINERS
# ════════════════════════════════════════════════════════════════

@dataclass
class ComponentLife:
    name:       str
    warn_rds:   int          # rounds — service warning threshold
    fail_rds:   int          # rounds — replacement threshold
    model:      str          # description of physics model
    action:     str          # "REPLACE" or "SERVICE/INSPECT"


@dataclass
class LifeResult:
    components:   List[ComponentLife]
    barrel_life:  int
    piston_warn:  int
    piston_fail:  int
    seal_warn:    int
    pad_life:     int
    bell_warn:    int
    cylinder_life: int
    coil_warn:    int
    bushing_life: int
    lug_life:     int
    lug_SF_fatigue: float
    # Arrays for plotting
    n_arr:        np.ndarray


def _exp_set(n: np.ndarray, cs_inf: float, n_char: float) -> np.ndarray:
    """Compression set accumulation: CS(n) = CS_inf * (1 - exp(-n/n_char))"""
    return cs_inf * (1.0 - np.exp(-n / n_char))


def _life_from_set(cs_inf: float, n_char: float, cs_fail: float) -> int:
    """Rounds to reach cs_fail compression set."""
    arg = 1.0 - cs_fail / cs_inf
    if arg <= 0.0:
        return int(1e9)
    return int(-n_char * np.log(arg))


def simulate(cfg: BSG10Config = DEFAULT_CONFIG,
             P_peak: float = 73.53e6) -> LifeResult:
    """
    Compute all component life estimates.

    Parameters
    ----------
    cfg     : BSG10Config
    P_peak  : float   Pa  calibrated peak chamber pressure from ballistics module
    """
    b  = cfg.barrel
    g  = cfg.gas
    a  = cfg.action
    rc = cfg.recoil

    n = np.linspace(0.0, 200_000.0, 2000)

    # ── Barrel ────────────────────────────────────────────────
    dE_melo   = b.k_base * (P_peak / b.p_ref)**b.alpha_erosion * b.f_melonite * b.f_steel_shot
    barrel_life = int(b.erosion_fail / dE_melo)

    # ── Gas piston ────────────────────────────────────────────
    P_port = 29.4e6    # Pa  from ballistics (could be passed in)
    dE_piston   = g.k_piston * (P_port / g.p_ref_piston)**g.alpha_piston * g.f_17_4PH
    piston_fail = int(g.piston_fail / dE_piston)
    piston_warn = int(g.piston_warn / dE_piston)

    # ── Gas cylinder ──────────────────────────────────────────
    dE_cyl      = g.k_cylinder * (P_port / g.p_ref_piston)**g.alpha_cyl * g.f_chrome_cyl
    cylinder_life = int(g.cylinder_fail / dE_cyl)

    # ── Bolt lug fatigue ──────────────────────────────────────
    bolt_thrust   = P_peak * cfg.cartridge.bore_area
    F_per_lug     = bolt_thrust / a.n_lugs
    lug_area_m2   = a.lug_width * a.lug_depth
    tau_op        = F_per_lug / lug_area_m2 / 1e6   # MPa
    lug_SF_fat    = a.se_shear / tau_op

    # Fretting wear (ion nitrided)
    sigma_contact = F_per_lug / lug_area_m2 / 1e6   # MPa
    V_per_shot    = a.k_fret_nitrided * sigma_contact * a.delta_slip
    V_fail        = lug_area_m2 * 1e6 * a.lug_wear_fail * 0.05   # mm³
    lug_life      = min(int(V_fail / V_per_shot) if V_per_shot > 0 else 999999, 150_000)

    # ── CBS-10 coil springs ───────────────────────────────────
    coil_warn     = _life_from_set(rc.cs_inf_coil, rc.n_set_coil, rc.cs_inf_coil * 0.36)
    coil_fail_rds = _life_from_set(rc.cs_inf_coil, rc.n_set_coil, rc.fail_cs_coil)

    # ── CBS-10 Belleville washers ─────────────────────────────
    bell_warn     = _life_from_set(rc.cs_inf_bell, rc.n_set_bell, rc.cs_inf_bell * 0.31)
    bell_fail_rds = _life_from_set(rc.cs_inf_bell, rc.n_set_bell, rc.fail_cs_bell)

    # ── CBS-10 damper seals ───────────────────────────────────
    V_per_shot_seal = rc.k_seal * rc.f_seal_contact * rc.l_slide_per_shot
    seal_fail       = int(rc.v_fail_seal / V_per_shot_seal) if V_per_shot_seal > 0 else 99999
    seal_warn       = int(seal_fail * 0.60)

    # ── CBS-10 pads ───────────────────────────────────────────
    sorb_life = _life_from_set(rc.cs_inf_sorb, rc.n_sorb, rc.fail_sorb)
    d3o_life  = _life_from_set(rc.cs_inf_d3o,  rc.n_d3o,  rc.fail_d3o)
    pad_life  = min(sorb_life, d3o_life)

    # ── Barrel bushings ───────────────────────────────────────
    F_float     = cfg.barrel.float_spring_k * cfg.barrel.float_travel   # N
    L_per_shot  = 2 * cfg.barrel.float_travel * 1e3                     # mm
    K_bush      = 1.2e-7
    V_bush_shot = K_bush * F_float * L_per_shot
    sleeve_od_mm = cfg.barrel.sleeve_od * 1e3
    bushing_len_mm = cfg.barrel.bushing_len * 1e3
    V_fail_bush = 0.15 * np.pi * sleeve_od_mm * bushing_len_mm
    bushing_life = int(V_fail_bush / V_bush_shot) if V_bush_shot > 0 else 200_000
    bushing_warn = int(bushing_life * 0.70)

    components = [
        ComponentLife("CBS-10 viscoelastic pads", pad_life,     pad_life,      "Exponential compression set", "REPLACE"),
        ComponentLife("Gas piston (warn)",         piston_warn,  piston_warn,   "Power-law erosion",          "SERVICE"),
        ComponentLife("CBS-10 damper seals (warn)",seal_warn,    seal_warn,     "Archard PTFE/Cr wear",       "SERVICE"),
        ComponentLife("Gas piston (fail)",         piston_warn,  piston_fail,   "Power-law erosion",          "REPLACE"),
        ComponentLife("Barrel (Melonite)",         barrel_life,  barrel_life,   "Power-law throat erosion",   "REPLACE"),
        ComponentLife("Belleville washers (warn)", bell_warn,    bell_warn,     "Stress relaxation set",      "SERVICE"),
        ComponentLife("Gas cylinder",              cylinder_life,cylinder_life, "Bore wear model",            "RELINE"),
        ComponentLife("CBS-10 coil springs (warn)",coil_warn,    coil_warn,     "Compression set model",      "SERVICE"),
        ComponentLife("Barrel bushings (warn)",    bushing_warn, bushing_warn,  "Archard PTFE-bronze",        "SERVICE"),
        ComponentLife("Barrel bushings (fail)",    bushing_warn, bushing_life,  "Archard PTFE-bronze",        "REPLACE"),
        ComponentLife("Bolt lugs (nitrided)",      lug_life,     lug_life,      "Fretting wear (nitrided)",   "INSPECT"),
    ]

    return LifeResult(
        components    = components,
        barrel_life   = barrel_life,
        piston_warn   = piston_warn,
        piston_fail   = piston_fail,
        seal_warn     = seal_warn,
        pad_life      = pad_life,
        bell_warn     = bell_warn,
        cylinder_life = cylinder_life,
        coil_warn     = coil_warn,
        bushing_life  = bushing_life,
        lug_life      = lug_life,
        lug_SF_fatigue = lug_SF_fat,
        n_arr         = n,
    )


def print_results(r: LifeResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    a  = cfg.action
    print("\n" + "="*62)
    print("MODULE F — PARTS LIFE ANALYSIS")
    print("="*62)
    print(f"\n  {'Component':<38s} {'Warn':>8s}  {'Replace':>8s}  Action")
    print(f"  {'-'*70}")
    sorted_comp = sorted(r.components, key=lambda c: c.fail_rds)
    for c in sorted_comp:
        print(f"  {c.name:<38s} {c.warn_rds:>8,}  {c.fail_rds:>8,}  {c.action}")

    print(f"\n  Bolt lug fatigue safety factor: {r.lug_SF_fatigue:.1f}×  "
          f"({'INFINITE life' if r.lug_SF_fatigue >= 1.0 else 'FINITE life — redesign'})")
    print(f"\n  Life-limiting component: {sorted_comp[0].name}  @ {sorted_comp[0].fail_rds:,} rounds")


def plot_all(r: LifeResult, cfg: BSG10Config = DEFAULT_CONFIG,
             save: bool = True) -> plt.Figure:
    """Generate CBS-10, gas system, and life summary figures."""
    rc = cfg.recoil
    n  = r.n_arr

    # ── CBS-10 component degradation ────────────────────────
    fig_d, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig_d.suptitle("Module F — CBS-10 Component Life Curves", fontweight="bold")

    CS_coil = _exp_set(n, rc.cs_inf_coil, rc.n_set_coil) * 100
    CS_bell = _exp_set(n, rc.cs_inf_bell, rc.n_set_bell) * 100
    CS_sorb = _exp_set(n, rc.cs_inf_sorb, rc.n_sorb)     * 100
    CS_d3o  = _exp_set(n, rc.cs_inf_d3o,  rc.n_d3o)      * 100
    V_seal  = rc.k_seal * rc.f_seal_contact * rc.l_slide_per_shot * n

    axes[0,0].plot(n/1e3, CS_coil, color="steelblue", lw=2)
    axes[0,0].axhline(rc.cs_inf_coil*100*0.36, ls="--", color="orange",
                      label=f"Warn ({r.coil_warn:,} rds)")
    axes[0,0].axhline(rc.fail_cs_coil*100, ls="--", color="red",
                      label=f"Fail ({_life_from_set(rc.cs_inf_coil, rc.n_set_coil, rc.fail_cs_coil):,} rds)")
    axes[0,0].set(xlabel="Rounds (×1,000)", ylabel="Compression Set (%)",
                  title="Coil Spring Set (SAE 9254 Chrome-Silicon)")
    axes[0,0].legend(fontsize=7); axes[0,0].grid(True, alpha=0.3)

    axes[0,1].plot(n/1e3, CS_bell, color="darkorange", lw=2)
    axes[0,1].axhline(rc.cs_inf_bell*100*0.31, ls="--", color="orange",
                      label=f"Warn ({r.bell_warn:,} rds)")
    axes[0,1].axhline(rc.fail_cs_bell*100, ls="--", color="red",
                      label=f"Fail ({_life_from_set(rc.cs_inf_bell, rc.n_set_bell, rc.fail_cs_bell):,} rds)")
    axes[0,1].set(xlabel="Rounds (×1,000)", ylabel="Compression Set (%)",
                  title="Belleville Washer Set (17-7PH SS)")
    axes[0,1].legend(fontsize=7); axes[0,1].grid(True, alpha=0.3)

    axes[1,0].plot(n/1e3, V_seal, color="purple", lw=2)
    axes[1,0].axhline(rc.v_fail_seal * 0.60, ls="--", color="orange",
                      label=f"Warn ({r.seal_warn:,} rds)")
    axes[1,0].axhline(rc.v_fail_seal, ls="--", color="red",
                      label=f"Fail ({int(rc.v_fail_seal / (rc.k_seal*rc.f_seal_contact*rc.l_slide_per_shot)):,} rds)")
    axes[1,0].set(xlabel="Rounds (×1,000)", ylabel="Wear Volume (mm³)",
                  title="Damper Seal Wear (PTFE on Chrome Rod)")
    axes[1,0].legend(fontsize=7); axes[1,0].grid(True, alpha=0.3)

    axes[1,1].plot(n/1e3, CS_sorb, color="firebrick", lw=2,
                   label=f"Sorbothane 50A (fail {r.pad_life:,} rds)")
    axes[1,1].plot(n/1e3, CS_d3o,  color="steelblue", lw=2,
                   label=f"D3O polymer (fail {_life_from_set(rc.cs_inf_d3o, rc.n_d3o, rc.fail_d3o):,} rds)")
    axes[1,1].axhline(rc.fail_sorb*100, ls="--", color="firebrick", alpha=0.5)
    axes[1,1].axhline(rc.fail_d3o*100,  ls="--", color="steelblue", alpha=0.5)
    axes[1,1].set(xlabel="Rounds (×1,000)", ylabel="Compression Set (%)",
                  title="Viscoelastic Pad Degradation")
    axes[1,1].legend(fontsize=7); axes[1,1].grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        fig_d.savefig(f"{OUTPUT_DIR}/F1_cbs10_life.png", dpi=130)
        print("  → Saved: F1_cbs10_life.png")

    # ── Integrated life summary ──────────────────────────────
    sorted_comp = sorted(r.components, key=lambda c: c.fail_rds)
    names  = [c.name for c in sorted_comp]
    lives  = [c.fail_rds for c in sorted_comp]

    def zone_color(n):
        if n < 15000:   return "#e74c3c"
        elif n < 40000: return "#e67e22"
        elif n < 80000: return "#f1c40f"
        else:           return "#27ae60"

    colors = [zone_color(l) for l in lives]

    fig_g, axes2 = plt.subplots(1, 2, figsize=(14, 6))
    fig_g.suptitle("Module F — Integrated Parts Life Summary", fontweight="bold")

    ax = axes2[0]
    bars = ax.barh(names, [l/1000 for l in lives], color=colors, edgecolor="black", lw=0.8, height=0.65)
    for bar, l in zip(bars, lives):
        ax.text(bar.get_width() + 0.4, bar.get_y()+bar.get_height()/2,
                f"{l:,}", va="center", fontsize=7.5, fontweight="bold")
    for m_line in [2, 5, 10, 20, 40, 80, 120]:
        ax.axvline(m_line, ls="--", color="grey", alpha=0.35, lw=0.8)
        ax.text(m_line, len(names)-0.5, f"{m_line}k", ha="center", fontsize=5.5, color="grey")
    ax.set(xlabel="Rounds (×1,000)", title="Component Life to Service / Replace")
    from matplotlib.patches import Patch
    legend_els = [Patch(fc="#e74c3c", label="< 15 k"), Patch(fc="#e67e22", label="15–40 k"),
                  Patch(fc="#f1c40f", label="40–80 k"), Patch(fc="#27ae60", label="> 80 k")]
    ax.legend(handles=legend_els, loc="lower right", fontsize=7)
    ax.grid(True, alpha=0.3, axis="x")

    # Maintenance cost model (relative units)
    ax2   = axes2[1]
    n_lf  = np.linspace(0, 150_000, 1500)
    cost_items = [
        ("Pads",      r.pad_life,       0.5,  "#e74c3c"),
        ("Piston",    r.piston_fail,    1.5,  "#e67e22"),
        ("Seals",     r.seal_warn*2,    0.8,  "#9b59b6"),
        ("Barrel",    r.barrel_life,    8.0,  "#3498db"),
        ("Bushings",  r.bushing_life,   1.0,  "#27ae60"),
        ("Belleville",r.bell_warn*2,    0.6,  "#f39c12"),
    ]
    total = np.zeros_like(n_lf)
    for label, interval, unit_cost, col in cost_items:
        c_arr = np.floor(n_lf / interval) * unit_cost
        ax2.plot(n_lf/1000, c_arr, label=label, color=col, lw=1.5)
        total += c_arr
    ax2.plot(n_lf/1000, total, "k-", lw=2.5, label="Total")
    ax2.set(xlabel="Rounds (×1,000)", ylabel="Cumulative Cost (relative units)",
            title="Maintenance Cost Model (relative)")
    ax2.legend(fontsize=6.5, ncol=2)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        fig_g.savefig(f"{OUTPUT_DIR}/F2_life_summary.png", dpi=130)
        print("  → Saved: F2_life_summary.png")

    return fig_d, fig_g


def run(cfg: BSG10Config = DEFAULT_CONFIG,
        P_peak: float = 73.53e6,
        plot_results: bool = True) -> LifeResult:
    result = simulate(cfg, P_peak)
    print_results(result, cfg)
    if plot_results:
        plot_all(result, cfg)
    return result
