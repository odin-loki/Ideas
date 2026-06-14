"""
ORCA (Ocean Resonant Coastal Array) — central simulation config.

Parameters trace to ORCA_System_Specification_v1.md Appendix A unless noted.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Tuple

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Physical constants
MU0 = 4.0 * np.pi * 1e-7  # H/m

# Spec-validated targets (Appendix A / §6)
SPEC_TARGETS = {
    "submarine_uep_range_km": 28.49,
    "surface_uep_range_km": 45.22,
    "propeller_demon_range_km": 0.88,
    "node_spacing_km": 57.0,
    "node_count": 54,
    "coast_length_km": 3000.0,
    "tier1_acquisition_usd": 775_676,
    "false_alarm_per_node_per_week": 1.0,
}

TOLERANCE_FRACTION = 0.01  # ±1% validation band for run_all.py


@dataclass
class VesselType:
    name: str
    dipole_moment_am: float  # corrosion UEP moment [A·m]
    propeller_moment_am: float  # ELFE fundamental moment M₀ [A·m]
    shaft_rpm: float = 120.0
    blade_count: int = 7
    depth_m: float = 50.0


@dataclass
class NodeConfig:
    depth_m: float = 15.0
    baseline_m: float = 200.0  # tip-to-tip electrode span
    n_pairs: int = 3  # independent long-baseline pairs (star arms)
    n_electrodes: int = 7
    electrode_noise_dc_nv_rt_hz: float = 1.0
    electrode_noise_elfe_nv_rt_hz: float = 0.5
    dc_integration_s: float = 60.0
    demon_integration_s: float = 300.0
    seawater_conductivity_s_m: float = 4.0
    snr_threshold_db: float = 10.0
    bearing_accuracy_deg: float = 8.0  # at threshold SNR
    arm_bearings_deg: Tuple[float, float, float] = (0.0, 120.0, 240.0)


@dataclass
class ArrayConfig:
    coast_length_km: float = 3000.0
    node_spacing_km: float = 57.0
    node_count: int = 54


@dataclass
class EconomicsConfig:
    node_cost_small_batch_usd: Tuple[float, float] = (5500.0, 6400.0)
    node_cost_nominal_usd: float = 6401.40
    prototype_nodes: int = 2
    prototype_cost_usd: float = 85_000.0
    tier1_nodes: int = 54
    tier1_production_usd: float = 345_676.0
    deployment_usd: float = 180_000.0
    shore_station_usd: float = 45_000.0
    integration_usd: float = 120_000.0
    p8a_unit_cost_usd: float = 345_000_000.0


@dataclass
class ProcessingGainsDB:
    """Cumulative processing gains from spec §3.5 table."""
    baseline_extension_db: float = 20.0
    matched_filter_dc_db: float = 4.8
    preamp_dc_db: float = 14.0
    coherent_integration_elfe_db: float = 17.8
    matched_filter_elfe_db: float = 8.5
    preamp_elfe_db: float = 12.0
    multi_harmonic_db: float = 0.7
    demon_db: float = 36.2

    @property
    def total_dc_db(self) -> float:
        return self.baseline_extension_db + self.matched_filter_dc_db + self.preamp_dc_db

    @property
    def total_propeller_db(self) -> float:
        return (
            self.coherent_integration_elfe_db
            + self.matched_filter_elfe_db
            + self.preamp_elfe_db
            + self.multi_harmonic_db
            + self.demon_db
        )


@dataclass
class ORCAConfig:
    name: str = "ORCA — Ocean Resonant Coastal Array"
    node: NodeConfig = field(default_factory=NodeConfig)
    array: ArrayConfig = field(default_factory=ArrayConfig)
    economics: EconomicsConfig = field(default_factory=EconomicsConfig)
    processing_gains: ProcessingGainsDB = field(default_factory=ProcessingGainsDB)
    # Effective noise bandwidth for DC corrosion detector (spec §6.1 uses √0.01 Hz)
    dc_noise_bandwidth_hz: float = 0.01
    # Optional scale on DEMON output — unity matches raw Appendix A gains; calibrate in run_all
    propeller_gain_scale: float = 1.0
    default_seed: int = 42


DEFAULT_CONFIG = ORCAConfig()

VESSEL_TYPES: Dict[str, VesselType] = {
    "type_039_ssk": VesselType(
        name="Type-039 SSK (Song/Yuan class)",
        dipole_moment_am=1500.0,
        propeller_moment_am=50.0,
        shaft_rpm=120.0,
        blade_count=7,
        depth_m=50.0,
    ),
    "surface_isr": VesselType(
        name="Surface ISR vessel (~5,000 t)",
        dipole_moment_am=6000.0,
        propeller_moment_am=200.0,
        shaft_rpm=90.0,
        blade_count=5,
        depth_m=8.0,
    ),
}


def depth_offset_m(cfg: ORCAConfig, vessel: VesselType) -> float:
    return abs(vessel.depth_m - cfg.node.depth_m)


def blade_rate_hz(vessel: VesselType) -> float:
    return (vessel.shaft_rpm / 60.0) * vessel.blade_count


def snr_threshold_linear(cfg: ORCAConfig) -> float:
    return 10.0 ** (cfg.node.snr_threshold_db / 20.0)
