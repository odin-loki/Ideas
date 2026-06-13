"""
MT-X Mk.II "Leviathan" — central simulation configuration.

All design parameters trace to papers/MT-X_Leviathan_Specification.md unless noted.
Edit this file to explore design variants (lighter armour, diesel-only fuel, etc.).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

G = 9.80665
RHO_WATER = 1000.0  # kg/m³


@dataclass
class HullConfig:
    length_mm: float = 8500.0
    width_mm: float = 3600.0
    width_skirts_mm: float = 4100.0
    height_turret_ring_mm: float = 1700.0
    height_overall_mm: float = 2380.0
    ground_clearance_mm: float = 450.0
    track_width_mm: float = 580.0
    track_contact_mm: float = 4800.0
    combat_mass_kg: float = 38000.0


@dataclass
class ArmourZone:
    name: str
    thickness_mm: float
    angle_deg_from_vertical: float
    has_era: bool = False
    era_add_mm: float = 0.0


@dataclass
class ArmourConfig:
    material_density_g_cm3: float = 3.05
    material_rha_equiv: float = 1.0  # 1:1 AlNiCyN-5000
    zones: List[ArmourZone] = field(default_factory=lambda: [
        ArmourZone("upper_glacis", 110, 78, True, 250),
        ArmourZone("lower_glacis", 130, 55, True, 250),
        ArmourZone("hull_side_upper", 80, 15, True, 250),
        ArmourZone("hull_side_lower", 60, 0, False, 0),
        ArmourZone("turret_front_primary", 200, 75, True, 300),
        ArmourZone("turret_front_cheek", 180, 70, True, 300),
        ArmourZone("turret_roof", 40, 10, False, 0),
        ArmourZone("hull_roof_crew", 50, 10, False, 0),
    ])


@dataclass
class EngineConfig:
    designation: str = "PPU-1300"
    cylinders: int = 12
    layout: str = "boxer"
    displacement_L: float = 38.4
    power_hp: float = 1300.0
    power_rpm: float = 2200.0
    torque_Nm: float = 4800.0
    torque_rpm: float = 1400.0
    dry_mass_kg: float = 2800.0
    bsfc_g_kwh: float = 210.0  # diesel design point
    fuel_capacity_L: float = 1400.0
    fuel_density_kg_L: float = 0.85


@dataclass
class TransmissionConfig:
    gears_forward: int = 6
    gears_reverse: int = 2
    final_drive_ratio: float = 5.8
    max_road_speed_kmh: float = 65.0
    max_reverse_kmh: float = 35.0
    mass_kg: float = 1800.0


@dataclass
class SuspensionConfig:
    torsion_bar_diam_mm: float = 65.0
    torsion_bar_length_mm: float = 2000.0
    road_wheels_per_side: int = 7
    wheel_diam_mm: float = 750.0
    wheel_travel_mm: float = 280.0
    track_pitch_mm: float = 164.0
    links_per_track: int = 92


@dataclass
class MainGunConfig:
    calibre_mm: float = 140.0
    barrel_length_mm: float = 9100.0
    round_mass_kg: float = 45.0
    # Spec-claimed AMET performance (MT-X_Leviathan_Specification.md Part VII)
    spec_muzzle_velocity_m_s: float = 1950.0
    spec_muzzle_energy_MJ: float = 57.0
    spec_pen_0m_mm: float = 1450.0
    spec_pen_2000m_mm: float = 1150.0
    # Portfolio-validated KEW-AP (140mm Tank KE Round — weapons_simulation.py)
    portfolio_muzzle_velocity_m_s: float = 1698.0
    portfolio_muzzle_energy_MJ: float = 9.23
    portfolio_pen_0m_mm: float = 867.1
    portfolio_pen_2000m_mm: float = 326.7
    portfolio_pen_60deg_0m_mm: float = 533.8
    autoloader_cycle_s: float = 7.5
    ready_rounds: int = 22
    hull_stowage: int = 12
    recoil_stroke_mm: float = 520.0
    muzzle_brake_reduction: float = 0.45


@dataclass
class APSConfig:
    radar_band: str = "Ka"
    detection_range_atgm_m: float = 400.0
    detection_range_rpg_m: float = 250.0
    engage_init_m: float = 250.0
    engage_min_m: float = 80.0
    reaction_time_s: float = 0.3
    track_update_hz: float = 50.0
    single_shot_pk: float = 0.80
    atgm_approach_speed_m_s: float = 200.0


@dataclass
class AmphibiousConfig:
    hull_seal_depth_m: float = 4.0
    unprepared_ford_m: float = 1.4
    snorkel_depth_m: float = 4.0
    swim_speed_kmh: float = 7.0  # midpoint 6–8
    freeboard_forward_mm: float = 200.0
    sponson_buoyancy_L: float = 1540.0  # both sides
    displacement_estimate_m3: float = 42.0  # hull volume below waterline at trim


@dataclass
class WeightBudget:
    """Component masses from Part XIX — must sum to combat_mass."""
    items: Dict[str, float] = field(default_factory=lambda: {
        "hull_structure": 8200,
        "turret_structure": 3100,
        "engine": 2800,
        "transmission_final_drives": 3200,
        "running_gear": 4400,
        "main_armament": 2600,
        "secondary_armament": 380,
        "aps_ew": 220,
        "electronics": 180,
        "crew": 300,
        "troop_payload": 960,
        "fuel": 1190,
        "ammunition": 2100,
        "era_panels": 640,
        "miscellaneous": 730,
    })


@dataclass
class CostConfig:
    """Central estimates from MT-X_Leviathan_Cost_Analysis.md — hybrid bonding, 100-unit run."""
    unit_price_ex_ammo_MUSD: float = 5.82
    unit_price_inc_ammo_MUSD: float = 6.14
    program_100_vehicles_BUSD: float = 1.293
    hybrid_saving_per_vehicle_USD: float = 340_000


@dataclass
class LeviathanConfig:
    hull: HullConfig = field(default_factory=HullConfig)
    armour: ArmourConfig = field(default_factory=ArmourConfig)
    engine: EngineConfig = field(default_factory=EngineConfig)
    transmission: TransmissionConfig = field(default_factory=TransmissionConfig)
    suspension: SuspensionConfig = field(default_factory=SuspensionConfig)
    main_gun: MainGunConfig = field(default_factory=MainGunConfig)
    aps: APSConfig = field(default_factory=APSConfig)
    amphibious: AmphibiousConfig = field(default_factory=AmphibiousConfig)
    weight: WeightBudget = field(default_factory=WeightBudget)
    cost: CostConfig = field(default_factory=CostConfig)
    name: str = "MT-X Mk.II Leviathan"


DEFAULT_CONFIG = LeviathanConfig()


def effective_rha_mm(thickness_mm: float, angle_deg_from_vertical: float) -> float:
    """Oblique plate: effective thickness = t / sin(angle from horizontal)."""
    angle_from_horizontal = 90.0 - angle_deg_from_vertical
    angle_rad = np.radians(max(angle_from_horizontal, 1.0))
    return thickness_mm / np.sin(angle_rad)
