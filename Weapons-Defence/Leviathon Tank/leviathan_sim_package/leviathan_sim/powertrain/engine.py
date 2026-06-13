"""PPU-1300 boxer engine and fuel economy."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import LeviathanConfig

HP_TO_W = 745.7


def simulate_powertrain(cfg: LeviathanConfig) -> Dict[str, Any]:
    eng = cfg.engine
    rpm = np.linspace(800, 2400, 17)
    torque = _torque_curve(rpm, eng.torque_Nm, eng.torque_rpm, eng.power_rpm)
    power_hp = torque * rpm * 2 * np.pi / 60 / HP_TO_W

    power_w = eng.power_hp * HP_TO_W
    fuel_kg = eng.fuel_capacity_L * eng.fuel_density_kg_L
    bsfc = eng.bsfc_g_kwh / 1000.0

    load_points = [
        ("idle", 800, 0.05),
        ("cruise_45", 1600, 0.35),
        ("max_road", 2200, 0.85),
        ("sprint", 2200, 1.0),
    ]
    consumption = {}
    for name, rpm_pt, load in load_points:
        t = float(np.interp(rpm_pt, rpm, torque))
        p_kw = t * rpm_pt * 2 * np.pi / 60 / 1000 * load
        kg_h = p_kw * bsfc
        consumption[name] = {
            "rpm": rpm_pt,
            "power_kw": round(p_kw, 1),
            "fuel_kg_h": round(kg_h, 1),
            "fuel_L_h": round(kg_h / eng.fuel_density_kg_L, 1),
        }

    return {
        "designation": eng.designation,
        "layout": eng.layout,
        "cylinders": eng.cylinders,
        "displacement_L": eng.displacement_L,
        "rated_power_hp": eng.power_hp,
        "rated_torque_Nm": eng.torque_Nm,
        "dry_mass_kg": eng.dry_mass_kg,
        "fuel_capacity_L": eng.fuel_capacity_L,
        "fuel_mass_kg": round(fuel_kg, 0),
        "bsfc_g_kwh": eng.bsfc_g_kwh,
        "torque_curve": {
            "rpm": rpm.astype(int).tolist(),
            "torque_Nm": np.round(torque, 0).astype(int).tolist(),
            "power_hp": np.round(power_hp, 0).astype(int).tolist(),
        },
        "consumption": consumption,
        "transmission": {
            "gears_fwd": cfg.transmission.gears_forward,
            "gears_rev": cfg.transmission.gears_reverse,
            "final_drive": cfg.transmission.final_drive_ratio,
            "mass_kg": cfg.transmission.mass_kg,
        },
    }


def _torque_curve(rpm, peak_t, peak_rpm, power_rpm):
    t = np.zeros_like(rpm, dtype=float)
    for i, r in enumerate(rpm):
        if r <= peak_rpm:
            t[i] = peak_t * (0.6 + 0.4 * r / peak_rpm)
        else:
            t[i] = peak_t * (power_rpm / r)
    return t
