"""Markdown report generation."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

from leviathan_sim.config import OUTPUT_DIR, LeviathanConfig


def generate_report(results: Dict[str, Any], cfg: LeviathanConfig) -> str:
    path = os.path.join(OUTPUT_DIR, "leviathan_sim_report.md")
    lines = [
        "# MT-X Mk.II Leviathan — Simulation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Executive summary",
        "",
        _executive_summary(results),
        "",
        "## Mobility",
        "",
        _dict_table(results["mobility"]),
        "",
        "## Armour (headline zones)",
        "",
        _armour_table(results["armour"]),
        "",
        "## Main armament",
        "",
        _main_gun_section(results["armament_main"]),
        "",
        "## APS",
        "",
        _dict_table(results["aps"]),
        "",
        "## Amphibious",
        "",
        _dict_table(results["amphibious"]),
        "",
        "## Weight budget",
        "",
        _weight_section(results["weight"]),
        "",
        "## Cost",
        "",
        _dict_table(results["cost"]),
        "",
        "## Full JSON",
        "",
        "See `leviathan_sim_results.json` for machine-readable output.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    json_path = os.path.join(OUTPUT_DIR, "leviathan_sim_results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return path


def _executive_summary(r: Dict[str, Any]) -> str:
    mob = r["mobility"]
    arm = r["armament_main"]
    w = r["weight"]
    return "\n".join(
        [
            f"- **Combat mass:** {w['spec_combat_mass_kg']:,} kg (budget delta {w['delta_kg']:+} kg)",
            f"- **Power-to-weight:** {mob['power_to_weight_hp_t']} hp/t",
            f"- **Max road speed:** {mob['max_road_speed_kmh']} km/h (modelled power limit {mob['power_limited_speed_kmh']} km/h)",
            f"- **Ground pressure:** {mob['ground_pressure_kpa']} kPa",
            f"- **Upper glacis (ERA):** {r['armour']['headline']['upper_glacis_with_era_mm']} mm eff. RHA",
            f"- **Main gun ROF:** {arm['rof_rpm']} rpm ({arm['total_ammo']} rounds stowed)",
            f"- **Portfolio KE @ 2 km:** {arm['portfolio_kew_ap']['penetration_mm'][2000]} mm RHA",
            f"- **Unit cost (ex ammo):** ${r['cost']['unit_price_ex_ammo_MUSD']:.2f}M",
        ]
    )


def _dict_table(d: Dict[str, Any], indent: int = 0) -> str:
    rows = []
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            rows.append(f"{prefix}- **{k}:**")
            rows.append(_dict_table(v, indent + 1))
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            rows.append(f"{prefix}- **{k}:** ({len(v)} entries)")
        else:
            rows.append(f"{prefix}- **{k}:** {v}")
    return "\n".join(rows)


def _armour_table(arm: Dict[str, Any]) -> str:
    lines = ["| Zone | Physical (mm) | Eff. RHA | With ERA |", "|------|---------------|----------|----------|"]
    for z in arm["zones"]:
        lines.append(
            f"| {z['zone']} | {z['physical_mm']} | {z['effective_rha_mm']} | {z['with_era_mm']} |"
        )
    return "\n".join(lines)


def _main_gun_section(g: Dict[str, Any]) -> str:
    lines = [
        f"- **ROF:** {g['rof_rpm']} rpm",
        f"- **Recoil force:** {g['recoil_force_kN']} kN",
        "",
        "**Portfolio KE penetration (mm RHA):**",
        "",
    ]
    for dist, pen in g["portfolio_kew_ap"]["penetration_mm"].items():
        lines.append(f"- {dist} m: {pen}")
    lines.extend(["", f"> {g['penetration_discrepancy']['warning']}", ""])
    return "\n".join(lines)


def _weight_section(w: Dict[str, Any]) -> str:
    lines = ["| Component | kg |", "|-----------|-----|"]
    for name, kg in w["items_kg"].items():
        lines.append(f"| {name} | {kg:,} |")
    lines.append(f"| **Total** | **{w['computed_total_kg']:,}** |")
    lines.append(f"| Spec target | {w['spec_combat_mass_kg']:,} |")
    return "\n".join(lines)
