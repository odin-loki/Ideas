"""Torsion-bar suspension and ride dynamics."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import G, LeviathanConfig


def simulate_suspension(cfg: LeviathanConfig) -> Dict[str, Any]:
    sus = cfg.suspension
    m = cfg.hull.combat_mass_kg
    wheels = sus.road_wheels_per_side * 2

    # Torsion bar stiffness: G * J / L ; steel G ≈ 80 GPa
    d = sus.torsion_bar_diam_mm / 1000.0
    L = sus.torsion_bar_length_mm / 1000.0
    J = np.pi * d**4 / 32
    G = 80e9
    k_bar = G * J / L  # N·m/rad

    mass_per_wheel = m / wheels
    lever_arm = sus.wheel_diam_mm / 2000.0 * 0.85
    k_linear = k_bar / lever_arm**2  # N/m per wheel (approx)
    fn = np.sqrt(k_linear / mass_per_wheel) / (2 * np.pi)

    travel_m = sus.wheel_travel_mm / 1000.0
    max_vert_accel_g = travel_m * fn**2 * 4 / G  # bump input proxy

    track_length_m = sus.links_per_track * sus.track_pitch_mm / 1000.0

    return {
        "road_wheels_total": wheels,
        "wheel_travel_mm": sus.wheel_travel_mm,
        "track_pitch_mm": sus.track_pitch_mm,
        "track_length_m": round(track_length_m, 2),
        "torsion_bar_diam_mm": sus.torsion_bar_diam_mm,
        "natural_frequency_Hz": round(fn, 2),
        "est_ground_clearance_mm": cfg.hull.ground_clearance_mm,
        "max_bump_acceleration_g": round(max_vert_accel_g, 2),
        "notes": "7+1 road wheels per side; hydropneumatic bump stops at full droop.",
    }
