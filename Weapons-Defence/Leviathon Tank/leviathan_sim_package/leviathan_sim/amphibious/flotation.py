"""Amphibious flotation and fording."""

from __future__ import annotations

from typing import Any, Dict

from leviathan_sim.config import G, RHO_WATER, LeviathanConfig


def simulate_amphibious(cfg: LeviathanConfig) -> Dict[str, Any]:
    amp = cfg.amphibious
    m = cfg.hull.combat_mass_kg
    displaced = amp.displacement_estimate_m3
    buoyancy_n = RHO_WATER * displaced * G
    weight_n = m * G
    reserve_buoyancy = (buoyancy_n - weight_n) / weight_n * 100

    sponson_kg = amp.sponson_buoyancy_L * RHO_WATER / 1000.0 * 2
    total_displaced_with_sponsons = displaced + amp.sponson_buoyancy_L / 1000.0

    # Propulsive power for swim speed (very simplified)
    v_swim = amp.swim_speed_kmh / 3.6
    # F_drag ≈ 0.5 * rho * Cd * A * v² ; water Cd~0.8, A~frontal 8 m²
    p_swim_kw = 0.5 * RHO_WATER * 0.8 * 8.0 * v_swim**3 / 1000 * 1.3  # margin

    return {
        "combat_mass_kg": m,
        "displacement_m3": displaced,
        "displacement_with_sponsons_m3": round(total_displaced_with_sponsons, 1),
        "buoyancy_margin_percent": round(reserve_buoyancy, 1),
        "floats_without_preparation": reserve_buoyancy > 0,
        "sponson_buoyancy_kg": round(sponson_kg, 0),
        "swim_speed_kmh": amp.swim_speed_kmh,
        "swim_power_kw": round(p_swim_kw, 0),
        "unprepared_ford_m": amp.unprepared_ford_m,
        "snorkel_depth_m": amp.snorkel_depth_m,
        "freeboard_forward_mm": amp.freeboard_forward_mm,
        "notes": (
            "Swim propulsion via track rotation; 6–8 km/h per specification. "
            "Reserve buoyancy must stay positive with full fuel and ammo."
        ),
    }
