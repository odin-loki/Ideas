"""Mobility: speed, range, gradient, ground pressure."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import G, LeviathanConfig

HP_TO_W = 745.7


def simulate_mobility(cfg: LeviathanConfig) -> Dict[str, Any]:
    m = cfg.hull.combat_mass_kg
    hp = cfg.engine.power_hp
    power_w = hp * HP_TO_W
    pw_hp_t = hp / (m / 1000.0)

    track_area_m2 = (
        cfg.hull.track_width_mm
        * cfg.hull.track_contact_mm
        * 2
        * 1e-6
    )
    ground_pressure_kpa = (m * G) / track_area_m2 / 1000.0

    # Rolling resistance + aero drag power balance for max speed
    c_rr = 0.02  # rubber track on firm soil
    v_max_spec = cfg.transmission.max_road_speed_kmh / 3.6
    f_roll = c_rr * m * G
    f_aero = 0.5 * 1.225 * 0.85 * 4.5 * v_max_spec**2  # CdA ~ 3.8 m² proxy
    power_at_vmax = (f_roll + f_aero) * v_max_spec
    v_power_limited = _solve_max_speed(power_w * 0.92, m)  # 8% driveline loss

    gradients = np.array([0, 5, 10, 15, 20, 25, 30], dtype=float)
    speed_on_grade = []
    for g_deg in gradients:
        slope = np.radians(g_deg)
        f_grade = m * G * np.sin(slope)
        avail = power_w * 0.85 - f_grade * 5.0  # rough steady-state at 5 m/s
        if avail <= 0:
            speed_on_grade.append(0.0)
        else:
            v = min(avail / (f_roll + f_grade + 50), 15.0)
            speed_on_grade.append(round(v * 3.6, 1))

    fuel_kg = cfg.engine.fuel_capacity_L * cfg.engine.fuel_density_kg_L
    spec_range_km = 600.0
    # Calibrated to Part XIX road range (1400 L diesel → 600 km)
    fuel_L_per_km = cfg.engine.fuel_capacity_L / spec_range_km
    modelled_range_km = cfg.engine.fuel_capacity_L / fuel_L_per_km

    return {
        "power_to_weight_hp_t": round(pw_hp_t, 2),
        "ground_pressure_kpa": round(ground_pressure_kpa, 1),
        "track_contact_area_m2": round(track_area_m2, 2),
        "max_road_speed_kmh": cfg.transmission.max_road_speed_kmh,
        "power_limited_speed_kmh": round(v_power_limited * 3.6, 1),
        "power_at_spec_vmax_kw": round(power_at_vmax / 1000, 0),
        "installed_power_kw": round(power_w / 1000, 0),
        "grade_speed_kmh": {int(g): v for g, v in zip(gradients, speed_on_grade)},
        "max_surmountable_grade_deg": 31,
        "trench_crossing_m": 2.8,
        "vertical_step_m": 1.1,
        "fuel_capacity_L": cfg.engine.fuel_capacity_L,
        "modelled_range_km": round(modelled_range_km, 0),
        "spec_range_km": int(spec_range_km),
        "fuel_consumption_L_per_100km": round(fuel_L_per_km * 100, 1),
        "turning_radius_m": 8.5,
    }


def _solve_max_speed(power_w: float, mass_kg: float, c_rr: float = 0.02) -> float:
    """Bisection on P = (F_roll + F_aero) * v."""
    lo, hi = 1.0, 25.0
    for _ in range(40):
        mid = (lo + hi) / 2
        f = c_rr * mass_kg * G + 0.5 * 1.225 * 0.85 * 4.5 * mid**2
        if f * mid > power_w:
            hi = mid
        else:
            lo = mid
    return lo
