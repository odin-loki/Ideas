"""Effective armour thickness and mass accounting."""

from __future__ import annotations

from typing import Any, Dict, List

from leviathan_sim.config import ArmourConfig, LeviathanConfig, effective_rha_mm


def simulate_armour(cfg: LeviathanConfig) -> Dict[str, Any]:
    armour: ArmourConfig = cfg.armour
    zones: List[Dict[str, Any]] = []

    for z in armour.zones:
        base_eff = effective_rha_mm(z.thickness_mm, z.angle_deg_from_vertical)
        with_era = base_eff + z.era_add_mm if z.has_era else base_eff
        area_m2 = _zone_area_estimate(z.name, cfg)
        mass_kg = (
            z.thickness_mm
            * area_m2
            * 1e-6
            * armour.material_density_g_cm3
            * 1000.0
        )
        if z.has_era:
            mass_kg += z.era_add_mm * area_m2 * 1e-6 * 2.7 * 1000.0 * 0.15

        zones.append(
            {
                "zone": z.name,
                "physical_mm": z.thickness_mm,
                "angle_deg_from_vertical": z.angle_deg_from_vertical,
                "effective_rha_mm": round(base_eff, 1),
                "with_era_mm": round(with_era, 1),
                "has_era": z.has_era,
                "estimated_mass_kg": round(mass_kg, 0),
            }
        )

    upper = next(z for z in zones if z["zone"] == "upper_glacis")
    turret = next(z for z in zones if z["zone"] == "turret_front_primary")
    pen_threat = cfg.main_gun.portfolio_pen_2000m_mm
    defeat = {z["zone"]: round(min(1.0, z["with_era_mm"] / pen_threat), 3) for z in zones}

    return {
        "zones": zones,
        "headline": {
            "upper_glacis_eff_mm": upper["effective_rha_mm"],
            "upper_glacis_with_era_mm": upper["with_era_mm"],
            "turret_front_eff_mm": turret["effective_rha_mm"],
            "turret_front_with_era_mm": turret["with_era_mm"],
            "total_armour_mass_kg": sum(z["estimated_mass_kg"] for z in zones),
        },
        "ke_defeat_margin_2km": defeat,
        "notes": (
            "AlNiCyN-5000 modelled 1:1 RHA equivalent per specification. "
            "ERA add-ons are nominal areal thickness credits."
        ),
    }


def _zone_area_estimate(zone_name: str, cfg: LeviathanConfig) -> float:
    w = cfg.hull.width_mm / 1000.0
    l = cfg.hull.length_mm / 1000.0
    areas = {
        "upper_glacis": 0.85 * w * 1.2,
        "lower_glacis": 0.6 * w * 0.9,
        "hull_side_upper": l * 0.35 * 2,
        "hull_side_lower": l * 0.25 * 2,
        "turret_front_primary": 1.8,
        "turret_front_cheek": 1.2,
        "turret_roof": 2.5,
        "hull_roof_crew": 3.0,
    }
    return areas.get(zone_name, 1.0)
