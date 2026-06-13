#!/usr/bin/env python3
"""MT-X Mk.II Leviathan — platform simulation entry point.

Runs the dedicated ``leviathan_sim`` package (mobility, armour, powertrain,
armament, APS, amphibious, FCS, weight, logistics, cost) and optionally
cross-checks main-gun KE numbers against the portfolio ``140mm Tank KE Round``.

See ``SIM_README.md`` for methodology.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PKG = _ROOT / "leviathan_sim_package"
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from run_all import run_all  # noqa: E402


def _portfolio_ke_check() -> dict | None:
    """Optional cross-check against Weapons-Defence portfolio sim."""
    portfolio_root = _ROOT.parents[1]
    sim_path = portfolio_root / "weapons_simulation.py"
    if not sim_path.is_file():
        return None
    if str(portfolio_root) not in sys.path:
        sys.path.insert(0, str(portfolio_root))
    try:
        import weapons_simulation as ws  # type: ignore

        key = "140mm Tank KE Round"
        if key not in getattr(ws, "CARTRIDGES", {}):
            return {"status": "skipped", "reason": f"cartridge key {key!r} not found"}
        # Minimal headline pull if portfolio exposes penetration helper
        return {"status": "available", "cartridge_key": key, "note": "See 140mm Tank KE Round/SIM_README.md"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "reason": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Leviathan tank simulation suite.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    parser.add_argument("--portfolio-check", action="store_true", help="Include portfolio KE cross-check")
    args = parser.parse_args()

    results, report_path = run_all()
    summary = {
        "platform": results["platform"],
        "combat_mass_kg": results["weight"]["spec_combat_mass_kg"],
        "weight_budget_delta_kg": results["weight"]["delta_kg"],
        "power_to_weight_hp_t": results["mobility"]["power_to_weight_hp_t"],
        "ground_pressure_kpa": results["mobility"]["ground_pressure_kpa"],
        "max_road_speed_kmh": results["mobility"]["max_road_speed_kmh"],
        "upper_glacis_era_mm": results["armour"]["headline"]["upper_glacis_with_era_mm"],
        "main_gun_rof_rpm": results["armament_main"]["rof_rpm"],
        "portfolio_ke_2000m_mm": results["armament_main"]["portfolio_kew_ap"]["penetration_mm"][2000],
        "unit_cost_MUSD": results["cost"]["unit_price_ex_ammo_MUSD"],
        "report": report_path,
        "json_results": os.path.join(os.path.dirname(report_path), "leviathan_sim_results.json"),
    }

    if args.portfolio_check:
        summary["portfolio_ke_check"] = _portfolio_ke_check()

    print("MT-X Mk.II Leviathan — simulation complete")
    print(f"  Report: {report_path}")
    print(f"  Weight budget delta: {summary['weight_budget_delta_kg']:+} kg (see notes in report)")
    print(f"  Power/weight: {summary['power_to_weight_hp_t']} hp/t")
    print(f"  Ground pressure: {summary['ground_pressure_kpa']} kPa")
    print(f"  Portfolio KE @ 2 km: {summary['portfolio_ke_2000m_mm']} mm RHA")

    if args.json:
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
