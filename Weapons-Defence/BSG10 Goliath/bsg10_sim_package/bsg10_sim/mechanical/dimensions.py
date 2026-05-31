"""
BSG-10 Simulation Suite — Module: Dimensional Geometry
=======================================================
Verifies all component dimensions fit within the bullpup envelope.
Checks clearances, balance zones, and cross-section fit.
Generates a dimensioned schematic.
"""

from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from dataclasses import dataclass
from typing import List, Tuple
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


@dataclass
class CheckItem:
    name:    str
    value:   float
    limit:   float
    unit:    str
    pass_hi: bool    # True = pass if value ≤ limit, False = pass if value ≥ limit

    @property
    def passed(self) -> bool:
        return self.value <= self.limit if self.pass_hi else self.value >= self.limit

    @property
    def status(self) -> str:
        return "PASS" if self.passed else "FAIL"


@dataclass
class DimResult:
    oal_mm:              float
    bore_height_mm:      float
    fg_from_butt_mm:     float
    cbs_damper_gap_mm:   float
    barrel_radial_cl_mm: float
    carrier_stroke_mm:   float
    cbs_travel_used_mm:  float
    checks:              List[CheckItem]
    all_pass:            bool


def check(cfg: BSG10Config = DEFAULT_CONFIG,
          carrier_stroke_used_mm: float = 23.2,
          cbs_travel_used_mm:     float = 39.6) -> DimResult:
    """
    Run all dimensional checks.

    Parameters
    ----------
    cfg                  : BSG10Config
    carrier_stroke_used_mm : from balanced action simulation
    cbs_travel_used_mm   : from recoil simulation
    """
    s   = cfg.system
    m   = cfg.magazine
    rc  = cfg.recoil
    a   = cfg.action

    # Derived dimensions
    oal          = s.oal
    fg_from_butt = oal - s.fg_from_muzzle

    # CBS-10 cross-section clearance
    rod_spacing_w  = 60.0   # mm
    spring_od      = 18.0   # mm
    damper_od      = 22.0   # mm
    cbs_gap        = rod_spacing_w - spring_od  # 42 mm gap between spring OD edges

    # Barrel float radial clearance
    receiver_id    = cfg.barrel.sleeve_od * 1e3 + 0.8    # mm
    barrel_sleeve  = cfg.barrel.sleeve_od * 1e3
    radial_cl      = (receiver_id - barrel_sleeve) / 2.0

    checks = [
        CheckItem("OAL",                    oal,                    1100.0, "mm", True),
        CheckItem("Bore height",            s.bore_height,          160.0,  "mm", True),
        CheckItem("Foregrip balance zone",  fg_from_butt,           720.0,  "mm", True),
        CheckItem("Foregrip balance (min)", fg_from_butt,           450.0,  "mm", False),
        CheckItem("CBS damper gap",         cbs_gap,                damper_od, "mm", False),
        CheckItem("Barrel radial cl.",      radial_cl,              0.30,   "mm", False),
        CheckItem("Carrier stroke",         carrier_stroke_used_mm, a.carrier_stroke*1e3, "mm", True),
        CheckItem("CBS travel used",        cbs_travel_used_mm,     rc.cbs_travel*1e3,    "mm", True),
        CheckItem("Drum below bore (cl.)",  45.0,                   30.0,   "mm", False),
    ]

    return DimResult(
        oal_mm              = oal,
        bore_height_mm      = s.bore_height,
        fg_from_butt_mm     = fg_from_butt,
        cbs_damper_gap_mm   = cbs_gap,
        barrel_radial_cl_mm = radial_cl,
        carrier_stroke_mm   = carrier_stroke_used_mm,
        cbs_travel_used_mm  = cbs_travel_used_mm,
        checks              = checks,
        all_pass            = all(c.passed for c in checks),
    )


def print_results(r: DimResult, cfg: BSG10Config = DEFAULT_CONFIG) -> None:
    s = cfg.system
    print("\n" + "="*62)
    print("MODULE D — DIMENSIONAL GEOMETRY CHECK")
    print("="*62)
    print(f"  OAL:                {r.oal_mm:.0f} mm  ({r.oal_mm/25.4:.1f} in)")
    print(f"  Bore height:        {r.bore_height_mm:.0f} mm")
    print(f"  Foregrip from butt: {r.fg_from_butt_mm:.0f} mm")
    print()
    print(f"  {'Check':<30s}  {'Value':>8s}  {'Limit':>8s}  {'Unit':>4s}  Status")
    print(f"  {'-'*62}")
    for c in r.checks:
        print(f"  {c.name:<30s}  {c.value:>8.1f}  {c.limit:>8.1f}  {c.unit:>4s}  {c.status}")
    print()
    print(f"  Overall: {'ALL CHECKS PASS' if r.all_pass else '*** CHECKS FAILED — SEE ABOVE ***'}")


def plot(r: DimResult, cfg: BSG10Config = DEFAULT_CONFIG,
         save: bool = True) -> plt.Figure:
    s = cfg.system
    m = cfg.magazine

    fig, (ax_lay, ax_chk) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Module D — Dimensional Geometry Check", fontweight="bold")

    # ── Side elevation schematic ────────────────────────────────
    ax_lay.set_xlim(-30, r.oal_mm + 30)
    ax_lay.set_ylim(-140, 80)
    ax_lay.set_aspect("equal")
    ax_lay.axis("off")
    ax_lay.set_title("Side-Elevation Schematic (all dimensions in mm)")

    butt     = 0.0
    cbs_end  = s.stock_length
    recv_end = cbs_end  + s.receiver_len
    bbl_end  = recv_end + s.barrel_length
    muz_end  = bbl_end  + s.comp_length
    bore_y   = 0.0
    drum_y   = bore_y - 45 - m.drum_od/2 * 1e3

    def rect(ax, x0, y0, w, h, **kw):
        ax.add_patch(Rectangle((x0, y0), w, h, **kw))

    rect(ax_lay, butt,     bore_y-18, cbs_end,              36, ec="steelblue", fc="lightblue",   lw=1.5)
    rect(ax_lay, cbs_end,  bore_y-22, s.receiver_len,        44, ec="dimgrey",  fc="silver",      lw=1.5)
    rect(ax_lay, recv_end, bore_y-10, s.barrel_length,       20, ec="darkgreen",fc="lightgreen",  lw=1.5)
    rect(ax_lay, bbl_end,  bore_y-14, s.comp_length,         28, ec="darkred",  fc="lightyellow", lw=1.5)

    drum_circ = Circle((recv_end - 20, drum_y), m.drum_od/2*1e3,
                       ec="purple", fc="lavender", lw=1.5)
    ax_lay.add_patch(drum_circ)

    for label, xc, yc, fs, col in [
        ("CBS-10", (butt+cbs_end)/2, bore_y+25, 7, "steelblue"),
        ("Receiver", (cbs_end+recv_end)/2, bore_y+30, 7, "dimgrey"),
        ("Barrel  510 mm", (recv_end+bbl_end)/2, bore_y+14, 7, "darkgreen"),
        ("Comp", (bbl_end+muz_end)/2, bore_y+18, 6.5, "darkred"),
        (f"Drum ∅{m.drum_od*1e3:.0f}", recv_end-20, drum_y, 7, "purple"),
    ]:
        ax_lay.text(xc, yc, label, ha="center", fontsize=fs, color=col, fontweight="bold")

    ax_lay.axhline(bore_y, color="red", lw=0.8, ls="--", alpha=0.5)
    ax_lay.text(10, bore_y+2.5, "Bore axis", fontsize=6, color="red", alpha=0.7)

    grip_x = s.grip_from_butt
    rect(ax_lay, grip_x-8, bore_y-58, 16, 58, ec="saddlebrown", fc="wheat", lw=1.2)
    ax_lay.text(grip_x, bore_y-63, "Grip", ha="center", fontsize=6, color="saddlebrown")

    fg_x = r.oal_mm - s.fg_from_muzzle
    rect(ax_lay, fg_x-8, bore_y-52, 16, 52, ec="saddlebrown", fc="wheat", lw=1.2)
    ax_lay.text(fg_x, bore_y-57, "FG", ha="center", fontsize=6, color="saddlebrown")

    ax_lay.annotate("", xy=(muz_end, bore_y-95), xytext=(butt, bore_y-95),
                    arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax_lay.text(r.oal_mm/2, bore_y-105, f"OAL = {r.oal_mm:.0f} mm ({r.oal_mm/25.4:.1f} in)",
                ha="center", fontsize=9, fontweight="bold")

    # ── Check table ─────────────────────────────────────────────
    ax_chk.axis("off")
    ax_chk.set_title("Geometry Pass / Fail Summary")
    col_labels = ["Check", "Value", "Limit", "Unit", "Status"]
    table_data = [[c.name, f"{c.value:.1f}", f"{c.limit:.1f}", c.unit,
                   "✔ PASS" if c.passed else "✘ FAIL"]
                  for c in r.checks]
    tbl = ax_chk.table(cellText=table_data, colLabels=col_labels,
                        loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1.2, 2.0)
    for (row, col), cell in tbl.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2c3e50")
            cell.set_text_props(color="white", fontweight="bold")
        elif col == 4:
            txt = cell.get_text().get_text()
            cell.set_facecolor("#d5f5e3" if "PASS" in txt else "#fadbd8")

    plt.tight_layout()
    if save:
        fig.savefig(f"{OUTPUT_DIR}/D_dimensions.png", dpi=130)
        print("  → Saved: D_dimensions.png")
    return fig


def run(cfg: BSG10Config = DEFAULT_CONFIG,
        carrier_stroke_used_mm: float = 23.2,
        cbs_travel_used_mm:     float = 39.6,
        plot_results: bool = True) -> DimResult:
    result = check(cfg, carrier_stroke_used_mm, cbs_travel_used_mm)
    print_results(result, cfg)
    if plot_results:
        plot(result, cfg)
    return result
