#!/usr/bin/env python3
"""Run all Leviathan tank simulations and write reports."""

from __future__ import annotations

import os
import sys

# Allow running from repo without install
_PKG_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from leviathan_sim.aps.engagement import simulate_aps
from leviathan_sim.armament.main_gun import simulate_main_gun
from leviathan_sim.armament.secondary import simulate_secondary
from leviathan_sim.armour.effective import simulate_armour
from leviathan_sim.amphibious.flotation import simulate_amphibious
from leviathan_sim.config import DEFAULT_CONFIG
from leviathan_sim.cost.unit_cost import simulate_cost
from leviathan_sim.fcs.hit_probability import simulate_fcs
from leviathan_sim.logistics.maintenance import simulate_logistics
from leviathan_sim.mobility.performance import simulate_mobility
from leviathan_sim.powertrain.engine import simulate_powertrain
from leviathan_sim.reports.generate import generate_report
from leviathan_sim.suspension.ride import simulate_suspension
from leviathan_sim.weight.budget import simulate_weight


def run_all(cfg=DEFAULT_CONFIG):
    results = {
        "platform": cfg.name,
        "mobility": simulate_mobility(cfg),
        "armour": simulate_armour(cfg),
        "powertrain": simulate_powertrain(cfg),
        "suspension": simulate_suspension(cfg),
        "armament_main": simulate_main_gun(cfg),
        "armament_secondary": simulate_secondary(cfg),
        "aps": simulate_aps(cfg),
        "amphibious": simulate_amphibious(cfg),
        "fcs": simulate_fcs(cfg),
        "weight": simulate_weight(cfg),
        "logistics": simulate_logistics(cfg),
        "cost": simulate_cost(cfg),
    }
    report_path = generate_report(results, cfg)
    return results, report_path


def main():
    results, report_path = run_all()
    print(f"Leviathan simulation complete.")
    print(f"Report: {report_path}")
    print(f"JSON:   {os.path.join(os.path.dirname(report_path), 'leviathan_sim_results.json')}")
    w = results["weight"]
    print(f"Weight budget: {w['computed_total_kg']} kg (delta {w['delta_kg']:+} kg)")
    print(f"Power/weight:  {results['mobility']['power_to_weight_hp_t']} hp/t")
    print(f"Ground pressure: {results['mobility']['ground_pressure_kpa']} kPa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
