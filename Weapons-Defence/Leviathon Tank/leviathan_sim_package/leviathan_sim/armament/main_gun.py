"""140mm AMET main gun, autoloader, and dual penetration models."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from leviathan_sim.config import LeviathanConfig


def simulate_main_gun(cfg: LeviathanConfig) -> Dict[str, Any]:
    gun = cfg.main_gun
    l_cal = gun.barrel_length_mm / gun.calibre_mm
    rof_rpm = 60.0 / gun.autoloader_cycle_s
    total_ammo = gun.ready_rounds + gun.hull_stowage

    # Lanz-Odermatt style decay (portfolio-calibrated exponent)
    distances_m = np.array([0, 500, 1000, 1500, 2000, 2500, 3000], dtype=float)

    def pen_curve(v0, pen0, pen2k, dist):
        """Interpolate with exponential decay anchored at 0 and 2000 m."""
        k = -np.log(pen2k / pen0) / 2000.0 if pen0 > 0 else 0
        return pen0 * np.exp(-k * dist)

    spec_pen = pen_curve(
        gun.spec_muzzle_velocity_m_s,
        gun.spec_pen_0m_mm,
        gun.spec_pen_2000m_mm,
        distances_m,
    )
    port_pen = pen_curve(
        gun.portfolio_muzzle_velocity_m_s,
        gun.portfolio_pen_0m_mm,
        gun.portfolio_pen_2000m_mm,
        distances_m,
    )

    # Recoil impulse
    v = gun.portfolio_muzzle_velocity_m_s
    impulse_ns = gun.round_mass_kg * v * (1 - gun.muzzle_brake_reduction)
    recoil_force_kn = impulse_ns / (gun.recoil_stroke_mm / 1000.0) / 1000.0

    sustained_fire_min = gun.ready_rounds / rof_rpm

    return {
        "calibre_mm": gun.calibre_mm,
        "length_calibres": round(l_cal, 1),
        "autoloader_cycle_s": gun.autoloader_cycle_s,
        "rof_rpm": round(rof_rpm, 1),
        "ready_rounds": gun.ready_rounds,
        "hull_stowage": gun.hull_stowage,
        "total_ammo": total_ammo,
        "sustained_burst_min": round(sustained_fire_min, 2),
        "recoil_force_kN": round(recoil_force_kn, 0),
        "spec_amet": {
            "muzzle_velocity_m_s": gun.spec_muzzle_velocity_m_s,
            "muzzle_energy_MJ": gun.spec_muzzle_energy_MJ,
            "penetration_mm": {int(d): float(p) for d, p in zip(distances_m, np.round(spec_pen, 1))},
        },
        "portfolio_kew_ap": {
            "muzzle_velocity_m_s": gun.portfolio_muzzle_velocity_m_s,
            "muzzle_energy_MJ": gun.portfolio_muzzle_energy_MJ,
            "penetration_mm": {int(d): float(p) for d, p in zip(distances_m, np.round(port_pen, 1))},
            "pen_60deg_0m_mm": gun.portfolio_pen_60deg_0m_mm,
        },
        "penetration_discrepancy": {
            "warning": (
                "Specification AMET claims (1950 m/s, 1450 mm @ 0 m) exceed "
                "portfolio-validated KEW-AP (1698 m/s, 867 mm @ 0 m). "
                "Sim reports both; use portfolio for cross-weapon comparisons."
            ),
            "ratio_spec_to_portfolio_at_2km": round(
                gun.spec_pen_2000m_mm / gun.portfolio_pen_2000m_mm, 2
            ),
        },
    }
