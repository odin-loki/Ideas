"""Markdown and JSON report generation for AGINS simulations."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, OUTPUT_DIR, SCENARIO_TITLES, SOLDIER_SCENARIOS, SHIP_SCENARIOS


def to_json_safe(obj: Any) -> Any:
    """Recursively convert numpy types and non-native keys for JSON."""
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return to_json_safe(obj.tolist())
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    return obj


def generate_report(results: Dict[str, Any], cfg: AGINSConfig = DEFAULT_CONFIG) -> str:
    md_path = os.path.join(OUTPUT_DIR, "agins_sim_report.md")
    json_path = os.path.join(OUTPUT_DIR, "agins_sim_results.json")

    lines = [
        "# AGINS — Simulation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Executive summary",
        "",
        _executive_summary(results),
        "",
        "## Soldier platform (MEMS)",
        "",
        _soldier_section(results.get("soldier", {})),
        "",
        "## Ship platform (FOG)",
        "",
        _ship_section(results.get("ship", {})),
        "",
        "## Spec targets (AGINS_full_report.md)",
        "",
        "| Platform | Scenario | Target mean | Target P90 |",
        "|----------|----------|-------------|------------|",
        "| Ship | Clear sky | 30 m | 50 m |",
        "| Ship | Storm | 57 m | 91 m |",
        "| Ship | DR only | 206 m | — |",
        "| Soldier | Open night | 26 m | 57 m |",
        "| Soldier | Urban | 61 m | 91 m |",
        "",
        "## Full JSON",
        "",
        "See `agins_sim_results.json` for machine-readable output.",
        "",
    ]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(to_json_safe(results), f, indent=2)

    return md_path


def _executive_summary(results: Dict[str, Any]) -> str:
    bullets = []
    soldier = results.get("soldier", {})
    ship = results.get("ship", {})

    for sc in SOLDIER_SCENARIOS:
        if sc in soldier:
            gh = soldier[sc]["filters"]["GH+PDR+compass"]
            bullets.append(
                f"- **Soldier {SCENARIO_TITLES[sc]}:** GH+PDR mean {gh['mean_m']:.1f} m, "
                f"P90 {gh['p90_m']:.1f} m"
            )

    for sc in SHIP_SCENARIOS:
        if sc in ship:
            gh = ship[sc]["filters"]["GH+compass"]
            bullets.append(
                f"- **Ship {SCENARIO_TITLES[sc]}:** GH mean {gh['mean_m']:.1f} m, "
                f"P90 {gh['p90_m']:.1f} m"
            )
            dr = ship[sc]["filters"]["DR (FOG IMU)"]
            bullets.append(f"  - DR (FOG IMU): mean {dr['mean_m']:.1f} m")

    return "\n".join(bullets) if bullets else "- No simulation results."


def _soldier_section(soldier: Dict[str, Any]) -> str:
    lines = [
        "| Scenario | Filter | Mean (m) | P90 (m) | Max (m) | Hdg° |",
        "|----------|--------|----------|---------|---------|------|",
    ]
    for sc in SOLDIER_SCENARIOS:
        if sc not in soldier:
            continue
        title = SCENARIO_TITLES[sc]
        for tag, stats in soldier[sc]["filters"].items():
            hdg = f"{stats['heading_deg']:.2f}" if "heading_deg" in stats else "—"
            lines.append(
                f"| {title} | {tag} | {stats['mean_m']:.1f} | {stats['p90_m']:.1f} | "
                f"{stats['max_m']:.1f} | {hdg} |"
            )
    return "\n".join(lines)


def _ship_section(ship: Dict[str, Any]) -> str:
    lines = [
        "| Scenario | Filter | Mean (m) | P90 (m) | Max (m) | Hdg° |",
        "|----------|--------|----------|---------|---------|------|",
    ]
    for sc in SHIP_SCENARIOS:
        if sc not in ship:
            continue
        title = SCENARIO_TITLES[sc]
        for tag, stats in ship[sc]["filters"].items():
            hdg = f"{stats['heading_deg']:.2f}" if "heading_deg" in stats else "—"
            lines.append(
                f"| {title} | {tag} | {stats['mean_m']:.1f} | {stats['p90_m']:.1f} | "
                f"{stats['max_m']:.1f} | {hdg} |"
            )
    return "\n".join(lines)


def generate_plots(results: Dict[str, Any], cfg: AGINSConfig = DEFAULT_CONFIG) -> str:
    """Generate consolidated PNG plots; returns output path."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec

    from agins_sim.config import DT, N_STEPS

    path = os.path.join(OUTPUT_DIR, "agins_sim_plots.png")
    t = np.arange(N_STEPS) * DT * 60
    CL = {"gh": "#0D47A1", "gh0": "#5C85D6", "kf": "#2E7D32", "dr": "#B71C1C", "pdr": "#E65100"}

    soldier = results.get("soldier", {})
    fig = plt.figure(figsize=(24, 34))
    gs = gridspec.GridSpec(4, 4, figure=fig, hspace=0.42, wspace=0.30)

    for row, sc in enumerate(SOLDIER_SCENARIOS):
        if sc not in soldier:
            continue
        r = soldier[sc]
        ts = r["time_series"]

        ax = fig.add_subplot(gs[row, 0])
        ax.plot(t, ts["position_error_gh_m"], "-", lw=2.5, color=CL["gh"], label="GH+PDR+compass")
        ax.plot(t, ts["position_error_gh0_m"], "--", lw=2, color=CL["gh0"], label="GH compass only", alpha=0.85)
        ax.plot(t, ts["position_error_kf_m"], "-.", lw=1.8, color=CL["kf"], label="KF+PDR+compass")
        ax.plot(t, ts["position_error_dr_pdr_m"], "--", lw=1.5, color=CL["pdr"], label="DR (PDR)", alpha=0.75)
        ax.plot(t, ts["position_error_dr_raw_m"], ":", lw=1.5, color=CL["dr"], label="DR (raw MEMS)", alpha=0.6)
        ax.set_title(f"{SCENARIO_TITLES[sc]}\nPosition Error (m)", fontsize=9, fontweight="bold")
        ax.set_xlabel("Time (min)", fontsize=8)
        ax.set_ylabel("Error (m)", fontsize=8)
        ax.legend(fontsize=7, loc="upper left")
        ax.grid(alpha=0.3)
        ax.set_ylim(0, None)

        ax = fig.add_subplot(gs[row, 1])
        traj = r["trajectory"]
        ax.plot(traj["truth_east_km"], traj["truth_north_km"], "k-", lw=2.5, label="Truth", alpha=0.85)
        ax.plot(traj["gh_east_km"], traj["gh_north_km"], "-", lw=1.8, color=CL["gh"], label="GH+PDR", alpha=0.85)
        ax.set_title("Trajectory (km)", fontsize=9, fontweight="bold")
        ax.set_xlabel("East", fontsize=8)
        ax.set_ylabel("North", fontsize=8)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)
        ax.set_aspect("equal")

        ax = fig.add_subplot(gs[row, 2])
        mp = np.array(ts["imm_probs"])
        ax.stackplot(t, mp[:, 0], mp[:, 1], mp[:, 2], labels=["CV", "CA", "HI"],
                     colors=["#42A5F5", "#66BB6A", "#FFA726"], alpha=0.85)
        ax.set_title("IMM Model Probs", fontsize=9, fontweight="bold")
        ax.set_xlabel("Time (min)", fontsize=8)
        ax.legend(fontsize=7, loc="upper right")
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.3)

        ax = fig.add_subplot(gs[row, 3])
        sky = np.array(ts["sky_fraction"])
        ax.fill_between(t, sky, alpha=0.4, color="#90CAF9", label="Sky fraction")
        urb = np.array(ts["urban_disturbance_nt"])
        if np.any(urb > 0):
            ax.fill_between(t, urb / 1000.0, alpha=0.3, color="#EF9A9A", label="Mag disturb /1000nT")
        ax.axhline(0.15, color="orange", lw=1, ls="--")
        ax.axhline(0.30, color="green", lw=1, ls="--")
        ax.set_title("Environment", fontsize=9, fontweight="bold")
        ax.set_xlabel("Time (min)", fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)

    plt.suptitle(
        "AGINS Soldier-Portable MEMS Navigation\n"
        "2hr patrol · 5 km/hr · GH-SR-IMM fusion",
        fontsize=11, fontweight="bold", y=0.999,
    )
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

    ship = results.get("ship", {})
    if ship:
        fig2, axes = plt.subplots(1, 2, figsize=(14, 5))
        for ax, sc in zip(axes, SHIP_SCENARIOS):
            if sc not in ship:
                continue
            ts = ship[sc]["time_series"]
            ax.plot(t, ts["position_error_gh_m"], "-", lw=2, color=CL["gh"], label="GH+compass")
            ax.plot(t, ts["position_error_kf_m"], "-.", lw=1.8, color=CL["kf"], label="KF+compass")
            ax.plot(t, ts["position_error_dr_m"], ":", lw=1.5, color=CL["dr"], label="DR (FOG IMU)")
            ax.set_title(SCENARIO_TITLES[sc], fontweight="bold")
            ax.set_xlabel("Time (min)")
            ax.set_ylabel("Error (m)")
            ax.legend(fontsize=8)
            ax.grid(alpha=0.3)
            ax.set_ylim(0, None)
        fig2.suptitle("AGINS Ship FOG Navigation — 2hr @ 15 kn", fontweight="bold")
        ship_path = os.path.join(OUTPUT_DIR, "agins_ship_plots.png")
        fig2.savefig(ship_path, dpi=150, bbox_inches="tight")
        plt.close(fig2)

    return path
