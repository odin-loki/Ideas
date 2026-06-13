"""Maintenance intervals and logistics footprint."""

from __future__ import annotations

from typing import Any, Dict

from leviathan_sim.config import LeviathanConfig


def simulate_logistics(cfg: LeviathanConfig) -> Dict[str, Any]:
    return {
        "crew": {"commander": 1, "gunner": 1, "driver": 1, "loader": 0, "troops": 6},
        "autoloader_eliminates_loader": True,
        "maintenance_intervals_h": {
            "daily_checks": 1,
            "50h_service": 50,
            "250h_intermediate": 250,
            "500h_major": 500,
            "track_replacement_h": 3000,
        },
        "transport": {
            "rail_gauge_compatible": True,
            "c17_loads_per_sortie": 2,
            "a400m_loads_per_sortie": 1,
        },
        "fuel_consumption_L_per_100km_road": 180,
        "ammunition_resupply": {
            "main_gun_rounds_typical_load": 34,
            "coax_boxes": 8,
            "rws_rounds": 120,
        },
        "mean_time_between_failure_h": 450,
        "notes": "Logistics figures align with Part XX maintenance and support.",
    }
