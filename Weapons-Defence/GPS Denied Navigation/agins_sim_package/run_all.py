#!/usr/bin/env python3
"""Run all AGINS simulations and write consolidated reports."""

from __future__ import annotations

import argparse
import os
import sys

_PKG_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from agins_sim.config import DEFAULT_CONFIG, OUTPUT_DIR, SCENARIO_TITLES, SHIP_SCENARIOS, SOLDIER_SCENARIOS
from agins_sim.platforms.ship import simulate_ship
from agins_sim.platforms.soldier import simulate_soldier
from agins_sim.reports.generate import generate_plots, generate_report


def run_all(cfg=DEFAULT_CONFIG, plots: bool = True, seed: int | None = None):
    seed = seed if seed is not None else cfg.default_seed
    results = {"platform": cfg.name, "seed": seed, "soldier": {}, "ship": {}}

    print("Running AGINS soldier simulations...")
    for sc in SOLDIER_SCENARIOS:
        print(f"  {sc}...", end=" ", flush=True)
        results["soldier"][sc] = simulate_soldier(sc, cfg, seed)
        gh = results["soldier"][sc]["filters"]["GH+PDR+compass"]
        print(f"done - GH+PDR mean {gh['mean_m']:.1f} m")

    print("\nRunning AGINS ship simulations...")
    for sc in SHIP_SCENARIOS:
        print(f"  {sc}...", end=" ", flush=True)
        results["ship"][sc] = simulate_ship(sc, cfg, seed)
        gh = results["ship"][sc]["filters"]["GH+compass"]
        print(f"done - GH mean {gh['mean_m']:.1f} m")

    report_path = generate_report(results, cfg)
    plot_path = None
    if plots:
        plot_path = generate_plots(results, cfg)
        print(f"Plots:  {plot_path}")

    _print_summary(results)
    return results, report_path, plot_path


def _print_summary(results: dict) -> None:
    print("\n" + "=" * 88)
    print("AGINS SIMULATION RESULTS")
    print("=" * 88)
    print(f"{'Scenario':<32} {'Filter':<24} {'Mean(m)':>8} {'P90(m)':>8} {'Max(m)':>8}")
    print("-" * 88)

    for sc in SOLDIER_SCENARIOS:
        r = results["soldier"][sc]
        for tag, stats in r["filters"].items():
            lbl = SCENARIO_TITLES[sc] if tag == "GH+PDR+compass" else ""
            print(f"{lbl:<32} {tag:<24} {stats['mean_m']:>8.1f} {stats['p90_m']:>8.1f} {stats['max_m']:>8.1f}")
        print()

    print("-- Ship (FOG) --")
    for sc in SHIP_SCENARIOS:
        r = results["ship"][sc]
        for tag, stats in r["filters"].items():
            lbl = SCENARIO_TITLES[sc] if tag == "GH+compass" else ""
            print(f"{lbl:<32} {tag:<24} {stats['mean_m']:>8.1f} {stats['p90_m']:>8.1f} {stats['max_m']:>8.1f}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Run AGINS navigation simulations")
    parser.add_argument("--no-plots", action="store_true", help="Skip matplotlib plot generation")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (default: config default)")
    args = parser.parse_args()

    results, report_path, _ = run_all(plots=not args.no_plots, seed=args.seed)
    print(f"\nReport: {report_path}")
    print(f"JSON:   {os.path.join(OUTPUT_DIR, 'agins_sim_results.json')}")

    gh_night = results["soldier"]["open_night"]["filters"]["GH+PDR+compass"]
    gh_urban = results["soldier"]["urban"]["filters"]["GH+PDR+compass"]
    gh_clear = results["ship"]["clear"]["filters"]["GH+compass"]
    gh_storm = results["ship"]["storm"]["filters"]["GH+compass"]
    print(f"\nHeadline: Soldier night {gh_night['mean_m']:.0f}m | Urban {gh_urban['mean_m']:.0f}m | "
          f"Ship clear {gh_clear['mean_m']:.0f}m | Storm {gh_storm['mean_m']:.0f}m")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
