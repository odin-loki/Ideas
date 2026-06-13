"""Coax MP-6.8 and 15.2 mm RWS."""

from __future__ import annotations

from typing import Any, Dict

from leviathan_sim.config import LeviathanConfig


def simulate_secondary(cfg: LeviathanConfig) -> Dict[str, Any]:
    return {
        "coax": {
            "weapon": "MP-6.8 coax machine gun",
            "calibre_mm": 6.8,
            "rate_of_fire_rpm": 750,
            "ready_ammo": 4000,
            "effective_range_m": 800,
            "role": "anti-personnel, suppressive fire",
        },
        "rws": {
            "weapon": "15.2 mm anti-tank sniper RWS",
            "calibre_mm": 15.2,
            "rate_of_fire_rpm": 30,
            "ready_ammo": 120,
            "effective_range_m": 2000,
            "penetration_mm_rha_500m": 45,
            "role": "precision anti-materiel, drone defeat",
        },
        "smoke_dischargers": {
            "tubes": 12,
            "salvo_coverage_s": 4,
        },
    }
