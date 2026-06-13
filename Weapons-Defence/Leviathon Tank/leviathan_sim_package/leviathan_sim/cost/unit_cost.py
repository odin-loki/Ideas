"""Unit and program cost from cost analysis."""

from __future__ import annotations

from typing import Any, Dict

from leviathan_sim.config import LeviathanConfig


def simulate_cost(cfg: LeviathanConfig) -> Dict[str, Any]:
    c = cfg.cost
    return {
        "unit_price_ex_ammo_MUSD": c.unit_price_ex_ammo_MUSD,
        "unit_price_inc_ammo_MUSD": c.unit_price_inc_ammo_MUSD,
        "program_100_vehicles_BUSD": c.program_100_vehicles_BUSD,
        "hybrid_bonding_saving_per_vehicle_USD": c.hybrid_saving_per_vehicle_USD,
        "cost_drivers": [
            "AlNiCyN-5000 armour fabrication (hybrid bonding)",
            "140mm AMET and autoloader",
            "PPU-1300 boxer engine",
            "APS and sensor suite",
            "rubber track running gear",
        ],
        "notes": "Central case from MT-X_Leviathan_Cost_Analysis.md; 100-unit production run.",
    }
