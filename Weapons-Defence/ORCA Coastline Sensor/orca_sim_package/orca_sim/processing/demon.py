"""DEMON cyclostationary propeller classification."""

from __future__ import annotations

import numpy as np

from orca_sim.config import ORCAConfig, VESSEL_TYPES, blade_rate_hz
from orca_sim.detection.snr import noise_voltage_matched_filter_v, snr_db
from orca_sim.physics.propeller_field import (
    demon_processing_gain_linear,
    harmonic_moment,
    propeller_voltage_v,
    skin_depth_m,
)


def demon_spectrum_peaks(vessel_key: str = "type_039_ssk", cfg: ORCAConfig | None = None) -> dict:
    cfg = cfg or __import__("orca_sim.config", fromlist=["DEFAULT_CONFIG"]).DEFAULT_CONFIG
    vessel = VESSEL_TYPES[vessel_key]
    f0 = blade_rate_hz(vessel)
    harmonics = []
    for k in range(1, 6):
        fk = f0 * k
        harmonics.append(
            {
                "harmonic": k,
                "frequency_hz": fk,
                "relative_amplitude": 1.0 / (k ** 1.5),
                "skin_depth_m": skin_depth_m(fk, cfg.node.seawater_conductivity_s_m),
            }
        )
    return {
        "vessel": vessel.name,
        "shaft_rpm": vessel.shaft_rpm,
        "blade_count": vessel.blade_count,
        "blade_rate_hz": f0,
        "demon_cyclic_hz": 2.0 * f0,
        "integration_s": cfg.node.demon_integration_s,
        "demon_gain_linear": demon_processing_gain_linear(cfg),
        "demon_gain_db": cfg.processing_gains.total_propeller_db,
        "harmonics": harmonics,
    }


def classify_propeller_at_range(
    range_km: float,
    cfg: ORCAConfig,
    vessel_key: str = "type_039_ssk",
) -> dict:
    vessel = VESSEL_TYPES[vessel_key]
    r_m = range_km * 1000.0
    raw_v = float(propeller_voltage_v(r_m, vessel, cfg))
    processed_v = raw_v * demon_processing_gain_linear(cfg)
    noise_v = noise_voltage_matched_filter_v(cfg, dc_band=False)
    snr = snr_db(processed_v, noise_v)
    threshold_db = cfg.node.snr_threshold_db
    classified = snr >= threshold_db

    return {
        "range_km": range_km,
        "raw_voltage_v": raw_v,
        "processed_voltage_v": processed_v,
        "noise_v": noise_v,
        "snr_db": snr,
        "threshold_db": threshold_db,
        "classified": classified,
        "blade_rate_hz": blade_rate_hz(vessel),
        "n_harmonics_used": 5,
        "fundamental_moment_am": vessel.propeller_moment_am,
        "harmonic_moments_am": [
            harmonic_moment(vessel.propeller_moment_am, k) for k in range(1, 6)
        ],
    }


def simulate_demon(cfg: ORCAConfig) -> dict:
    """Sweep classification SNR vs range around spec target."""
    target_km = 0.88
    ranges = np.linspace(0.3, 1.5, 25)
    sweep = [classify_propeller_at_range(float(r), cfg) for r in ranges]
    at_spec = classify_propeller_at_range(target_km, cfg)
    return {
        "spec_classification_range_km": target_km,
        "at_spec_range": at_spec,
        "sweep": sweep,
    }
