#!/usr/bin/env python3
"""AGINS — platform simulation entry point.

Runs the dedicated ``agins_sim`` package (ship + soldier scenarios, GH-SR-IMM
filter, multi-modal sensor fusion) and prints headline navigation numbers.

See ``SIM_README.md`` for methodology. Filter definition: ``../../Filtering/``.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PKG = _ROOT / "agins_sim_package"
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from run_all import run_all  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AGINS navigation simulation suite.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    args = parser.parse_args()

    results, report_path, plot_path = run_all(plots=False)
    ship = results.get("ship", {})
    soldier = results.get("soldier", {})
    summary = {
        "platform": results.get("platform", "AGINS"),
        "filter": "GH-SR-IMM",
        "ship_clear_sky_mean_m": ship.get("clear", {}).get("filters", {}).get("GH+compass", {}).get("mean_m"),
        "ship_clear_sky_p90_m": ship.get("clear", {}).get("filters", {}).get("GH+compass", {}).get("p90_m"),
        "ship_storm_mean_m": ship.get("storm", {}).get("filters", {}).get("GH+compass", {}).get("mean_m"),
        "ship_storm_p90_m": ship.get("storm", {}).get("filters", {}).get("GH+compass", {}).get("p90_m"),
        "soldier_open_night_mean_m": soldier.get("open_night", {}).get("filters", {}).get("GH+PDR+compass", {}).get("mean_m"),
        "soldier_open_night_p90_m": soldier.get("open_night", {}).get("filters", {}).get("GH+PDR+compass", {}).get("p90_m"),
        "soldier_urban_mean_m": soldier.get("urban", {}).get("filters", {}).get("GH+PDR+compass", {}).get("mean_m"),
        "soldier_urban_p90_m": soldier.get("urban", {}).get("filters", {}).get("GH+PDR+compass", {}).get("p90_m"),
        "soldier_pdr_dr_mean_m": soldier.get("open_night", {}).get("filters", {}).get("DR (PDR)", {}).get("mean_m"),
        "soldier_raw_mems_dr_mean_m": soldier.get("open_night", {}).get("filters", {}).get("DR (raw MEMS)", {}).get("mean_m"),
        "report": report_path,
        "plots": plot_path,
        "json_results": os.path.join(os.path.dirname(report_path), "agins_sim_results.json"),
    }

    print("AGINS — simulation complete")
    print(f"  Report: {report_path}")
    if summary["ship_clear_sky_mean_m"] is not None:
        print(f"  Ship clear sky: {summary['ship_clear_sky_mean_m']} m mean")
    if summary["ship_storm_mean_m"] is not None:
        print(f"  Ship storm: {summary['ship_storm_mean_m']} m mean")
    if summary["soldier_open_night_mean_m"] is not None:
        print(f"  Soldier open night: {summary['soldier_open_night_mean_m']} m mean")
    if summary["soldier_urban_mean_m"] is not None:
        print(f"  Soldier urban: {summary['soldier_urban_mean_m']} m mean")

    if args.json:
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
