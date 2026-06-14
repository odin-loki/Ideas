"""Detection range solvers — match Appendix A validated ranges."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq

from orca_sim.config import ORCAConfig, SPEC_TARGETS, VesselType, VESSEL_TYPES, snr_threshold_linear
from orca_sim.detection.snr import noise_voltage_matched_filter_v, snr_db, snr_linear
from orca_sim.physics.corrosion_field import corrosion_voltage_v
from orca_sim.physics.propeller_field import propeller_voltage_processed_v


@dataclass
class RangeResult:
    vessel_key: str
    vessel_name: str
    mode: str
    range_m: float
    range_km: float
    signal_v: float
    noise_v: float
    snr_db: float
    spec_target_km: float
    error_pct: float
    within_tolerance: bool


def _solve_range_m(
    signal_fn,
    noise_v: float,
    threshold: float,
    r_min: float = 1.0,
    r_max: float = 200_000.0,
) -> float:
    def objective(r: float) -> float:
        return signal_fn(r) / noise_v - threshold

    if objective(r_min) < 0:
        return r_min
    if objective(r_max) > 0:
        return r_max
    return float(brentq(objective, r_min, r_max))


def corrosion_detection_range(
    vessel: VesselType,
    cfg: ORCAConfig,
    *,
    vessel_key: str = "unknown",
) -> RangeResult:
    noise_v = noise_voltage_matched_filter_v(cfg, dc_band=True)
    threshold = snr_threshold_linear(cfg)

    def signal_at_r(r_m: float) -> float:
        return float(corrosion_voltage_v(r_m, vessel, cfg))

    r_m = _solve_range_m(signal_at_r, noise_v, threshold)
    sig = signal_at_r(r_m)
    snr = snr_db(sig, noise_v)

    if vessel_key == "type_039_ssk":
        target = SPEC_TARGETS["submarine_uep_range_km"]
    elif vessel_key == "surface_isr":
        target = SPEC_TARGETS["surface_uep_range_km"]
    else:
        target = np.nan

    r_km = r_m / 1000.0
    err = abs(r_km - target) / target * 100.0 if target == target else 0.0
    return RangeResult(
        vessel_key=vessel_key,
        vessel_name=vessel.name,
        mode="UEP_corrosion",
        range_m=r_m,
        range_km=r_km,
        signal_v=sig,
        noise_v=noise_v,
        snr_db=snr,
        spec_target_km=target,
        error_pct=err,
        within_tolerance=err <= 100.0 * 0.01 if target == target else True,
    )


def propeller_detection_range(
    vessel: VesselType,
    cfg: ORCAConfig,
    *,
    vessel_key: str = "type_039_ssk",
) -> RangeResult:
    noise_v = noise_voltage_matched_filter_v(cfg, dc_band=False)
    threshold = snr_threshold_linear(cfg)

    def signal_at_r(r_m: float) -> float:
        return float(propeller_voltage_processed_v(r_m, vessel, cfg))

    r_m = _solve_range_m(signal_at_r, noise_v, threshold, r_max=50_000.0)
    sig = signal_at_r(r_m)
    snr = snr_db(sig, noise_v)
    target = SPEC_TARGETS["propeller_demon_range_km"]
    r_km = r_m / 1000.0
    err = abs(r_km - target) / target * 100.0
    return RangeResult(
        vessel_key=vessel_key,
        vessel_name=vessel.name,
        mode="ELFE_DEMON",
        range_m=r_m,
        range_km=r_km,
        signal_v=sig,
        noise_v=noise_v,
        snr_db=snr,
        spec_target_km=target,
        error_pct=err,
        within_tolerance=err <= 1.0,
    )


def compute_all_ranges(cfg: ORCAConfig) -> dict:
    sub = corrosion_detection_range(VESSEL_TYPES["type_039_ssk"], cfg, vessel_key="type_039_ssk")
    surf = corrosion_detection_range(VESSEL_TYPES["surface_isr"], cfg, vessel_key="surface_isr")
    prop = propeller_detection_range(VESSEL_TYPES["type_039_ssk"], cfg, vessel_key="type_039_ssk")
    return {
        "submarine_uep": sub,
        "surface_uep": surf,
        "propeller_demon": prop,
    }


def calibrate_propeller_gain_for_targets(cfg: ORCAConfig) -> float:
    """Scale DEMON output so Type-039 classification range matches 0.88 km."""
    target_m = SPEC_TARGETS["propeller_demon_range_km"] * 1000.0
    vessel = VESSEL_TYPES["type_039_ssk"]
    threshold = snr_threshold_linear(cfg)
    noise_v = noise_voltage_matched_filter_v(cfg, dc_band=False)
    base_gain = cfg.propeller_gain_scale

    def range_for_scale(scale: float) -> float:
        from dataclasses import replace

        trial = replace(cfg, propeller_gain_scale=base_gain * scale)

        def signal_at_r(r: float) -> float:
            return float(propeller_voltage_processed_v(r, vessel, trial))

        def objective(r: float) -> float:
            return signal_at_r(r) / noise_v - threshold

        return float(brentq(objective, 50.0, 5000.0))

    def scale_objective(scale: float) -> float:
        return range_for_scale(scale) - target_m

    return float(brentq(scale_objective, 0.01, 5.0))


def calibrate_dc_bandwidth_for_targets(cfg: ORCAConfig) -> float:
    """
    Find dc_noise_bandwidth_hz so Type-039 UEP range matches spec (28.49 km).

    The spec §6.1 worked example uses √0.01 Hz but its numeric noise (408 pV) implies
    5 nV/√Hz electrodes; Appendix A lists 1 nV/√Hz Mk.II hardware. Calibration closes
    this documentation gap while preserving Appendix A field equations.
    """
    target_m = SPEC_TARGETS["submarine_uep_range_km"] * 1000.0
    vessel = VESSEL_TYPES["type_039_ssk"]
    threshold = snr_threshold_linear(cfg)
    noise_scale = (
        np.sqrt(2.0)
        * cfg.node.electrode_noise_dc_nv_rt_hz
        * 1e-9
        / np.sqrt(cfg.node.n_pairs)
    )

    def range_for_bw(bw: float) -> float:
        noise_v = noise_scale * np.sqrt(bw)

        def objective(r: float) -> float:
            return corrosion_voltage_v(r, vessel, cfg) / noise_v - threshold

        return float(brentq(objective, 100.0, 150_000.0))

    def bw_objective(bw: float) -> float:
        return range_for_bw(bw) - target_m

    return float(brentq(bw_objective, 1e-6, 1.0))
