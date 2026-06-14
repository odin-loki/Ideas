"""8-knot submarine transit through coastal detection zone."""

from __future__ import annotations

from orca_sim.config import ORCAConfig, SPEC_TARGETS, VESSEL_TYPES
from orca_sim.array.track import simulate_transit_detections


def simulate_submarine_transit(
    cfg: ORCAConfig,
    detection_radius_km: float,
    *,
    speed_kn: float = 8.0,
    standoff_km: float = 20.0,
    seed: int = 42,
) -> dict:
    """
    Type-039 transit parallel to coast at 20 km standoff (spec §4.2 / §4.5).

    At 28.5 km detection boundary and 8 kn, dwell in zone ≈ 3.8 h (~228 × 60 s windows).
    """
    radius = detection_radius_km
    chord_km = 2.0 * (radius ** 2 - standoff_km ** 2) ** 0.5 if standoff_km < radius else 0.0
    speed_kmh = speed_kn * 1.852
    dwell_h = chord_km / speed_kmh if speed_kmh > 0 else 0.0
    n_windows = int(dwell_h * 3600 / cfg.node.dc_integration_s)

    baseline = simulate_transit_detections(
        cfg,
        radius,
        speed_kn=speed_kn,
        standoff_km=standoff_km,
        duration_h=max(dwell_h * 1.5, 6.0),
        seed=seed,
    )
    failure = simulate_transit_detections(
        cfg,
        radius,
        speed_kn=speed_kn,
        standoff_km=standoff_km,
        duration_h=max(dwell_h * 1.5, 6.0),
        failed_node_id=27,
        seed=seed,
    )

    return {
        "vessel": VESSEL_TYPES["type_039_ssk"].name,
        "speed_kn": speed_kn,
        "standoff_km": standoff_km,
        "detection_radius_km": radius,
        "spec_detection_radius_km": SPEC_TARGETS["submarine_uep_range_km"],
        "transit_chord_km": chord_km,
        "dwell_time_h": dwell_h,
        "spec_dwell_time_h": 3.8,
        "expected_detection_windows": n_windows,
        "spec_detection_windows": 228,
        "baseline_transit": baseline,
        "single_node_failure": failure,
        "detection_loss_on_failure": baseline["n_detections"] - failure["n_detections"],
    }
