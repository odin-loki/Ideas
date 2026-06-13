"""Fire control system — first-round hit probability."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import LeviathanConfig


def simulate_fcs(cfg: LeviathanConfig) -> Dict[str, Any]:
    ranges_m = np.array([500, 1000, 1500, 2000, 2500, 3000], dtype=float)
    base_ceps_m = 0.15 + 0.00012 * ranges_m  # m at 50% (thermal + laser rangefinder)
    target_width_m = 3.5  # MBT frontal aspect
    target_length_m = 8.0

    def p_hit(cep, dim):
        # Circular error probable → hit on rectangular target (approx)
        return 1 - np.exp(-0.693 * (dim / (2 * cep)) ** 2)

    p_stationary = p_hit(base_ceps_m, target_width_m)
    p_moving = p_hit(base_ceps_m * 1.35, target_width_m)  # lead error penalty

    moving_target_speed_kmh = 40
    time_of_flight_s = ranges_m / cfg.main_gun.portfolio_muzzle_velocity_m_s

    return {
        "sensor_suite": [
            "commander's panoramic thermal (360°)",
            "gunner primary thermal / day channel",
            "laser rangefinder 200–9990 m",
            "wind sensor mast",
            "ballistic computer with muzzle reference",
        ],
        "first_round_hit_stationary": {
            int(r): float(p) for r, p in zip(ranges_m, np.round(p_stationary, 3))
        },
        "first_round_hit_moving_40kmh": {
            int(r): float(p) for r, p in zip(ranges_m, np.round(p_moving, 3))
        },
        "cep_m": {int(r): float(c) for r, c in zip(ranges_m, np.round(base_ceps_m, 2))},
        "time_of_flight_s": {
            int(r): float(t) for r, t in zip(ranges_m, np.round(time_of_flight_s, 2))
        },
        "max_direct_fire_range_m": 4000,
        "notes": "Uses portfolio MV for TOF; AMET would reduce TOF ~15%.",
    }
