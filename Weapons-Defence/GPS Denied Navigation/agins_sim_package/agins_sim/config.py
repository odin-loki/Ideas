"""
AGINS (Autonomous GPS-Independent Navigation System) — central simulation config.

Parameters trace to AGINS_full_report.md and nav_sim_soldier.py unless noted.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Shared timing ─────────────────────────────────────────────────────────────
DT = 1.0 / 60.0  # 1-minute steps
PATROL_DURATION_MIN = 120
N_STEPS = PATROL_DURATION_MIN  # 2-hour patrol / transit

SOLDIER_SCENARIOS = ["open_night", "open_day", "urban", "mixed"]
SHIP_SCENARIOS = ["clear", "storm"]

SCENARIO_TITLES: Dict[str, str] = {
    "open_night": "Open Terrain — Clear Night",
    "open_day": "Open Terrain — Daytime Overcast",
    "urban": "Urban Patrol — Sky/Mag Denied",
    "mixed": "Mixed (Open->Urban->Open)",
    "clear": "Maritime — Clear Sky Transit",
    "storm": "Maritime — 6hr Storm Conditions",
}


@dataclass
class IMUConfig:
    """Inertial measurement unit grade."""
    heading_drift_deg_hr: float
    heading_noise_deg: float
    velocity_bias_kmh: float
    velocity_noise_kmh: float
    gait_noise_deg: float = 0.0  # soldier only


@dataclass
class CelestialConfig:
    sigma_km: float
    interval_steps: int = 15
    sky_threshold: float = 0.30


@dataclass
class MagNavConfig:
    sigma_open_km: float
    sigma_urban_km: float
    interval_steps: int = 8
    urban_disturbance_nt: float = 500.0


@dataclass
class PolarCompassConfig:
    sigma_deg: float
    blunder_rate: float
    blunder_deg: float
    sky_threshold: float


@dataclass
class PDRConfig:
    steps_per_min: float = 100.0
    step_err: float = 0.02
    stride_err: float = 0.015
    speed_sigma_frac: float = 0.03


@dataclass
class FilterConfig:
    process_noise: Tuple[float, float, float] = (0.030, 0.20, 0.08)
    imm_transition: Tuple[Tuple[float, ...], ...] = (
        (0.92, 0.06, 0.02),
        (0.06, 0.92, 0.02),
        (0.25, 0.25, 0.50),
    )
    imm_initial_mu: Tuple[float, float, float] = (0.60, 0.28, 0.12)
    init_pos_var: float = 0.010
    init_vel_var: float = 0.25
    kf_process_noise: float = 0.035
    nig_forgetting: float = 0.02
    heading_gate_deg: float = 18.0
    nis_gate: float = 20.0


@dataclass
class SoldierPlatformConfig:
    speed_kmh: float = 5.0
    turn_rate_deg_s: float = 4.0
    initial_heading_deg: float = 20.0
    imu: IMUConfig = field(default_factory=lambda: IMUConfig(
        heading_drift_deg_hr=2.0,
        heading_noise_deg=0.05,
        velocity_bias_kmh=0.30,
        velocity_noise_kmh=0.05,
        gait_noise_deg=0.5,
    ))
    celestial: CelestialConfig = field(default_factory=lambda: CelestialConfig(sigma_km=0.35))
    magnav: MagNavConfig = field(default_factory=lambda: MagNavConfig(
        sigma_open_km=0.30,
        sigma_urban_km=0.55,
    ))
    polar: PolarCompassConfig = field(default_factory=lambda: PolarCompassConfig(
        sigma_deg=2.0,
        blunder_rate=0.06,
        blunder_deg=15.0,
        sky_threshold=0.15,
    ))
    pdr: PDRConfig = field(default_factory=PDRConfig)


@dataclass
class ShipPlatformConfig:
    speed_kn: float = 15.0
    turn_rate_deg_s: float = 2.0
    initial_heading_deg: float = 45.0
    dr_ocean_current_kmh: float = 0.20
    dr_gyro_random_walk_deg_sqrt_hr: float = 0.012
    dr_velocity_scale_ppm_hr: float = 4.0
    imu: IMUConfig = field(default_factory=lambda: IMUConfig(
        heading_drift_deg_hr=0.05,
        heading_noise_deg=0.01,
        velocity_bias_kmh=0.05,
        velocity_noise_kmh=0.02,
        gait_noise_deg=0.0,
    ))
    celestial: CelestialConfig = field(default_factory=lambda: CelestialConfig(
        sigma_km=0.085,
        interval_steps=10,
        sky_threshold=0.20,
    ))
    magnav: MagNavConfig = field(default_factory=lambda: MagNavConfig(
        sigma_open_km=0.065,
        sigma_urban_km=0.12,
        interval_steps=6,
        urban_disturbance_nt=80.0,
    ))
    polar: PolarCompassConfig = field(default_factory=lambda: PolarCompassConfig(
        sigma_deg=0.5,
        blunder_rate=0.005,
        blunder_deg=8.0,
        sky_threshold=0.05,
    ))


@dataclass
class AGINSConfig:
    soldier: SoldierPlatformConfig = field(default_factory=SoldierPlatformConfig)
    ship: ShipPlatformConfig = field(default_factory=ShipPlatformConfig)
    filter: FilterConfig = field(default_factory=FilterConfig)
    name: str = "AGINS GPS-Independent Navigation System"
    warmup_steps: int = 5
    default_seed: int = 42


DEFAULT_CONFIG = AGINSConfig()


def ship_speed_kmh(cfg: AGINSConfig) -> float:
    return cfg.ship.speed_kn * 1.852


def soldier_stride_km(cfg: AGINSConfig) -> float:
    s = cfg.soldier
    return s.speed_kmh / (s.pdr.steps_per_min * 60.0)
