"""
BSG-10 Simulation Suite — Module: Magazine Geometry
====================================================
Computes Tommy-style helical belt drum geometry, capacity,
feed spring force vs rounds remaining, and link kinematics.
"""

from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from dataclasses import dataclass
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


@dataclass
class MagazineResult:
    capacity:        int
    drum_depth_mm:   float
    n_coils:         float
    track_length_mm: float
    r_avg_mm:        float
    spring_rate:     float       # N·mm/rad
    feed_force_full: float       # N
    feed_force_last: float       # N
    feed_pass:       bool
    helix_x:         np.ndarray  # mm  for plotting
    helix_y:         np.ndarray  # mm


def compute(cfg: BSG10Config = DEFAULT_CONFIG) -> MagazineResult:
    """Compute drum geometry and verify feed reliability."""
    m = cfg.magazine
    shell_len = cfg.cartridge.shell_len

    n_coils      = m.usable_r / m.track_width
    r_avg        = m.hub_radius + m.usable_r / 2
    circ_avg     = 2.0 * np.pi * r_avg
    track_len    = circ_avg * n_coils
    capacity     = int(track_len / m.shell_pitch)
    drum_depth   = shell_len + 0.006  # m  (shell length + 6 mm clearance)

    # Spring rate from required feed force at average radius
    theta_max    = n_coils * 2.0 * np.pi
    k_spring     = m.f_feed_req * r_avg / theta_max   # N·m/rad → N·mm/rad if in mm

    # Feed force at last round (~1 revolution remaining)
    theta_last   = 2.0 * np.pi
    T_last       = k_spring * theta_last
    f_feed_last  = T_last / r_avg

    # Helix for plotting
    n_pts         = 500
    theta_arr     = np.linspace(0, n_coils * 2 * np.pi, n_pts)
    r_arr         = (m.hub_radius + (theta_arr / (2*np.pi)) * m.track_width) * 1e3
    helix_x       = r_arr * np.cos(theta_arr)
    helix_y       = r_arr * np.sin(theta_arr)

    return MagazineResult(
        capacity        = capacity,
        drum_depth_mm   = drum_depth * 1e3,
        n_coils         = n_coils,
        track_length_mm = track_len * 1e3,
        r_avg_mm        = r_avg * 1e3,
        spring_rate     = k_spring * 1e3,   # N·mm/rad
        feed_force_full = m.f_feed_req,
        feed_force_last = f_feed_last,
        feed_pass       = f_feed_last >= m.f_feed_min,
    helix_x = helix_x,
        helix_y         = helix_y,
    )


def print_results(r: MagazineResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    m = cfg.magazine
    print("\n" + "="*62)
    print("MODULE E — DRUM MAGAZINE GEOMETRY")
    print("="*62)
    print(f"  Drum outer diameter:  {m.drum_od*1e3:.0f} mm")
    print(f"  Drum depth:           {r.drum_depth_mm:.1f} mm")
    print(f"  Hub radius:           {m.hub_radius*1e3:.0f} mm")
    print(f"  Track width:          {m.track_width*1e3:.1f} mm")
    print(f"  Usable radial span:   {m.usable_r*1e3:.0f} mm")
    print(f"  Number of coil turns: {r.n_coils:.2f}")
    print(f"  Total belt length:    {r.track_length_mm:.0f} mm")
    print(f"  Shell capacity:       {r.capacity} rounds")
    print(f"  Spring rate:          {r.spring_rate:.2f} N·mm/rad")
    print(f"  Feed force (full):    {r.feed_force_full:.1f} N")
    print(f"  Feed force (last):    {r.feed_force_last:.1f} N  "
          f"(min {cfg.magazine.f_feed_min:.1f} N)  "
          f"{'PASS' if r.feed_pass else 'FAIL — upsize clock spring'}")


def plot(r: MagazineResult, cfg: BSG10Config = DEFAULT_CONFIG,
         save: bool = True) -> plt.Figure:
    m = cfg.magazine
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
    fig.suptitle(f"Module E — Helical Belt Drum Magazine  "
                 f"(∅{m.drum_od*1e3:.0f} mm, {r.capacity} rounds)",
                 fontweight="bold")

    # Helix cross-section
    ax = axes[0]
    ax.plot(r.helix_x, r.helix_y, color="steelblue", lw=1.2, label="Belt track")

    # Shell positions (one per shell_pitch along arc)
    arc = 0.0
    r_avg_m = r.r_avg_mm / 1e3
    sx, sy  = [], []
    for i in range(r.capacity):
        arc  += m.shell_pitch
        theta = arc / r_avg_m
        ri    = (m.hub_radius + (theta / (2*np.pi)) * m.track_width) * 1e3
        sx.append(ri * np.cos(theta))
        sy.append(ri * np.sin(theta))
    ax.scatter(sx, sy, c="firebrick", s=18, zorder=5, label=f"{r.capacity} shells")

    hub = plt.Circle((0, 0), m.hub_radius*1e3, fc="grey",   ec="black", lw=1.2)
    out = plt.Circle((0, 0), m.drum_od/2*1e3,  fc="none",   ec="black", lw=1.5, ls="--")
    ax.add_patch(hub); ax.add_patch(out)
    ax.set_aspect("equal")
    ax.set(xlabel="mm", ylabel="mm", title=f"Drum Cross-Section — {r.capacity} Rounds")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Feed force vs rounds remaining
    ax = axes[1]
    rounds_rem = np.arange(r.capacity, 0, -1)
    n_coils_rem = rounds_rem / (r.track_length_mm/m.shell_pitch*1e-3 / r.n_coils * 1e3 /
                                (m.shell_pitch*1e3)) if r.track_length_mm > 0 else np.ones_like(rounds_rem)

    # Simplified: force proportional to rounds remaining
    force_rem   = r.feed_force_full * rounds_rem / r.capacity

    ax.plot(rounds_rem, force_rem, color="darkorange", lw=2)
    ax.axhline(m.f_feed_min, ls="--", color="red",   label=f"Min feed ({m.f_feed_min:.0f} N)")
    ax.axhline(r.feed_force_full, ls="--", color="green",
               label=f"Full-drum ({r.feed_force_full:.0f} N)")
    ax.axhline(r.feed_force_last, ls=":", color="purple",
               label=f"Last round ({r.feed_force_last:.1f} N)")
    ax.set(xlabel="Rounds Remaining", ylabel="Feed Force (N)",
           title="Clock Spring Feed Force vs Rounds Remaining")
    ax.legend(fontsize=7)
    ax.invert_xaxis()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save:
        fig.savefig(f"{OUTPUT_DIR}/E_magazine.png", dpi=130)
        print("  → Saved: E_magazine.png")
    return fig


def run(cfg: BSG10Config = DEFAULT_CONFIG,
        plot_results: bool = True) -> MagazineResult:
    result = compute(cfg)
    print_results(result, cfg)
    if plot_results:
        plot(result, cfg)
    return result
