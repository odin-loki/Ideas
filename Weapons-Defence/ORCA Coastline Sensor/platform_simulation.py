#!/usr/bin/env python3
"""ORCA — platform simulation entry point.

Runs the dedicated ``orca_sim`` package (dipole detection range, array coverage,
Tier 1 economics) and prints headline surveillance numbers.

See ``SIM_README.md`` for methodology.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_PKG = _ROOT / "orca_sim_package"
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from run_all import run_all  # noqa: E402


def _unpack_run_all(out: tuple) -> tuple[dict, str, str | None]:
    """Accept 2- or 3-tuple returns from ``run_all`` (results, report [, plots])."""
    if len(out) == 2:
        results, report_path = out
        plot_path = None
    elif len(out) == 3:
        results, report_path, plot_path = out
    else:
        raise ValueError(f"run_all returned {len(out)} values; expected 2 or 3")
    return results, report_path, plot_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ORCA coastline surveillance simulation suite.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary to stdout")
    args = parser.parse_args()

    out = run_all(plots=False)
    results, report_path, plot_path = _unpack_run_all(out)

    detection = results.get("detection", {})
    array = results.get("array", {})
    economics = results.get("economics", {})

    summary = {
        "platform": results.get("platform", "ORCA"),
        "submarine_uep_km": detection.get("submarine_uep_km"),
        "surface_vessel_uep_km": detection.get("surface_vessel_uep_km"),
        "propeller_demon_km": detection.get("propeller_demon_km"),
        "node_count": array.get("node_count"),
        "node_spacing_km": array.get("node_spacing_km"),
        "coastline_km": array.get("coastline_km"),
        "tier1_acquisition_usd": economics.get("tier1_acquisition_usd"),
        "annual_ops_usd": economics.get("annual_ops_usd"),
        "p8a_cost_fraction": economics.get("p8a_cost_fraction"),
        "report": report_path,
        "plots": plot_path,
        "json_results": os.path.join(os.path.dirname(report_path), "orca_sim_results.json"),
    }

    print("ORCA — simulation complete")
    print(f"  Report: {report_path}")
    if summary["submarine_uep_km"] is not None:
        print(f"  Submarine UEP: {summary['submarine_uep_km']} km")
    if summary["surface_vessel_uep_km"] is not None:
        print(f"  Surface vessel UEP: {summary['surface_vessel_uep_km']} km")
    if summary["node_count"] is not None:
        print(f"  Tier 1 array: {summary['node_count']} nodes")
    if summary["tier1_acquisition_usd"] is not None:
        print(f"  Tier 1 acquisition: ${summary['tier1_acquisition_usd']:,.0f}")
    if summary["p8a_cost_fraction"] is not None:
        print(f"  vs P-8A acquisition: {summary['p8a_cost_fraction']:.3%}")

    if args.json:
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
