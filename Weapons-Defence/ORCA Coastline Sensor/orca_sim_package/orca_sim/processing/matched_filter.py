"""Three-arm star matched spatial filter and bearing estimation."""

from __future__ import annotations

import numpy as np

from orca_sim.config import ORCAConfig, VesselType, depth_offset_m
from orca_sim.physics.corrosion_field import corrosion_field_lateral_v_m


def arm_response(field_v_m: float, vessel_bearing_deg: float, arm_bearing_deg: float) -> float:
    """Arm voltage proportional to field gradient component along arm axis."""
    delta = np.radians(vessel_bearing_deg - arm_bearing_deg)
    return field_v_m * np.cos(delta)


def star_arm_voltages(
    range_m: float,
    vessel_bearing_deg: float,
    vessel: VesselType,
    cfg: ORCAConfig,
) -> np.ndarray:
    e = corrosion_field_lateral_v_m(
        range_m,
        vessel.dipole_moment_am,
        cfg.node.seawater_conductivity_s_m,
        depth_offset_m(cfg, vessel),
    )
    baseline = cfg.node.baseline_m / 2.0  # arm half-span to tip electrode
    return np.array(
        [arm_response(e, vessel_bearing_deg, arm) * baseline for arm in cfg.node.arm_bearings_deg]
    )


def matched_filter_output_v(
    range_m: float,
    vessel_bearing_deg: float,
    vessel: VesselType,
    cfg: ORCAConfig,
) -> float:
    """
    Coherent combination of three independent arm pairs (√N gain in SNR).

    Weights normalised to unit template energy.
    """
    arms = star_arm_voltages(range_m, vessel_bearing_deg, vessel, cfg)
    weights = arms / (np.linalg.norm(arms) + 1e-30)
    return float(np.dot(weights, arms) * np.sqrt(cfg.node.n_pairs))


def estimate_bearing_deg(arm_voltages: np.ndarray, cfg: ORCAConfig) -> float:
    """
    Bearing from in-phase / quadrature arm components (spec §4.4).

    Uses arms at 0° and 120° as I/Q reference; accuracy ±8° at 10 dB threshold.
    """
    v0, v120, _v240 = arm_voltages
    bearing = np.degrees(np.arctan2(v120 - v0 * 0.5, v0 * np.sqrt(3) / 2.0))
    return float(bearing % 360.0)


def simulate_matched_filter(
    cfg: ORCAConfig,
    vessel: VesselType,
    range_km: float,
    true_bearing_deg: float = 45.0,
) -> dict:
    r_m = range_km * 1000.0
    arms = star_arm_voltages(r_m, true_bearing_deg, vessel, cfg)
    mf_out = matched_filter_output_v(r_m, true_bearing_deg, vessel, cfg)
    est_bearing = estimate_bearing_deg(arms, cfg)
    bearing_error = abs((est_bearing - true_bearing_deg + 180) % 360 - 180)

    return {
        "range_km": range_km,
        "true_bearing_deg": true_bearing_deg,
        "estimated_bearing_deg": est_bearing,
        "bearing_error_deg": bearing_error,
        "bearing_accuracy_spec_deg": cfg.node.bearing_accuracy_deg,
        "arm_voltages_v": arms.tolist(),
        "matched_filter_output_v": mf_out,
        "within_bearing_spec": bearing_error <= cfg.node.bearing_accuracy_deg,
    }
