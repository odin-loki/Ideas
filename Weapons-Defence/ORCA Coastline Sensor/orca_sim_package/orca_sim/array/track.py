"""Shore-station track reconstruction and node-failure gap analysis."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from orca_sim.config import ORCAConfig, VESSEL_TYPES
from orca_sim.array.coverage import node_positions_km


@dataclass
class TrackPoint:
    time_h: float
    node_id: int
    range_km: float
    bearing_deg: float
    east_km: float
    north_km: float


def _bearing_to_offset(range_km: float, bearing_deg: float) -> tuple[float, float]:
    br = np.radians(bearing_deg)
    east = range_km * np.sin(br)
    north = range_km * np.cos(br)
    return east, north


def simulate_transit_detections(
    cfg: ORCAConfig,
    detection_radius_km: float,
    *,
    speed_kn: float = 8.0,
    standoff_km: float = 20.0,
    course_deg: float = 90.0,
    duration_h: float = 12.0,
    dt_min: float = 1.0,
    failed_node_id: int | None = None,
    seed: int = 42,
) -> dict:
    """
    Simplified track: vessel transits parallel to coast; nodes log detections
    when standoff range <= detection radius. Bearing noise ±8° at threshold.
    """
    rng = np.random.default_rng(seed)
    positions = node_positions_km(cfg)
    speed_kmh = speed_kn * 1.852
    dt_h = dt_min / 60.0
    n_steps = int(duration_h / dt_h) + 1

    # Vessel track: moves along coast (east) at fixed standoff from node line (north axis)
    start_x = -50.0
    detections: list[TrackPoint] = []
    truth: list[dict] = []

    for step in range(n_steps):
        t_h = step * dt_h
        x_km = start_x + speed_kmh * t_h
        y_km = standoff_km
        truth.append({"time_h": t_h, "east_km": x_km, "north_km": y_km})

        for idx, node_x in enumerate(positions):
            node_id = idx + 1
            if failed_node_id is not None and node_id == failed_node_id:
                continue

            dx = x_km - node_x
            dy = y_km
            r = np.hypot(dx, dy)
            if r > detection_radius_km:
                continue

            true_bearing = np.degrees(np.arctan2(dx, dy)) % 360.0
            bearing = true_bearing + rng.normal(0.0, cfg.node.bearing_accuracy_deg / 2.0)
            east, north = _bearing_to_offset(r, bearing)
            detections.append(
                TrackPoint(
                    time_h=t_h,
                    node_id=node_id,
                    range_km=r,
                    bearing_deg=bearing % 360.0,
                    east_km=node_x + east,
                    north_km=north,
                )
            )

    # Simple Kalman-style smoothing: mean speed from first/last detection times
    if len(detections) >= 2:
        t0 = detections[0].time_h
        t1 = detections[-1].time_h
        x0 = detections[0].east_km
        x1 = detections[-1].east_km
        est_speed_kmh = (x1 - x0) / max(t1 - t0, 1e-6)
    else:
        est_speed_kmh = speed_kmh

    gap_km = cfg.array.node_spacing_km if failed_node_id else 0.0

    return {
        "vessel": VESSEL_TYPES["type_039_ssk"].name,
        "speed_kn": speed_kn,
        "standoff_km": standoff_km,
        "detection_radius_km": detection_radius_km,
        "failed_node_id": failed_node_id,
        "n_detections": len(detections),
        "estimated_speed_kmh": est_speed_kmh,
        "estimated_speed_kn": est_speed_kmh / 1.852,
        "blind_corridor_km_on_failure": gap_km,
        "detections": [
            {
                "time_h": d.time_h,
                "node_id": d.node_id,
                "range_km": d.range_km,
                "bearing_deg": d.bearing_deg,
                "east_km": d.east_km,
                "north_km": d.north_km,
            }
            for d in detections
        ],
        "truth_samples": len(truth),
    }
