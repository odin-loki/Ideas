"""Northern coast array coverage geometry."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from orca_sim.config import ORCAConfig, SPEC_TARGETS


@dataclass
class CoverageResult:
    node_count: int
    node_spacing_km: float
    coast_length_km: float
    max_spacing_for_full_coverage_km: float
    detection_radius_km: float
    coverage_fraction: float
    blind_corridor_km: float
    nodes: list


def node_positions_km(cfg: ORCAConfig) -> np.ndarray:
    """Node positions at uniform spec spacing along threat axis."""
    arr = cfg.array
    return np.arange(arr.node_count, dtype=float) * arr.node_spacing_km


def simulate_coverage(cfg: ORCAConfig, detection_radius_km: float) -> CoverageResult:
    arr = cfg.array
    max_spacing = 2.0 * detection_radius_km
    positions = node_positions_km(cfg)
    actual_spacing = arr.node_spacing_km
    coast_span = float(positions[-1]) if len(positions) > 1 else 0.0

    # 100% coverage when spacing <= 2 * r_detect
    full_coverage = actual_spacing <= max_spacing + 1e-6
    coverage_fraction = 1.0 if full_coverage else max_spacing / actual_spacing

    # Single-node failure gap (spec §6.4): blind corridor width ≈ spacing when one node down
    blind_corridor_km = actual_spacing if arr.node_count > 1 else arr.coast_length_km

    nodes = [
        {
            "id": i + 1,
            "position_km": float(positions[i]),
            "detection_radius_km": detection_radius_km,
        }
        for i in range(len(positions))
    ]

    return CoverageResult(
        node_count=arr.node_count,
        node_spacing_km=actual_spacing,
        coast_length_km=coast_span,
        max_spacing_for_full_coverage_km=max_spacing,
        detection_radius_km=detection_radius_km,
        coverage_fraction=min(coverage_fraction, 1.0),
        blind_corridor_km=blind_corridor_km,
        nodes=nodes,
    )


def validate_array_params(cfg: ORCAConfig) -> dict:
    arr = cfg.array
    spacing_err = abs(arr.node_spacing_km - SPEC_TARGETS["node_spacing_km"]) / SPEC_TARGETS["node_spacing_km"]
    count_err = abs(arr.node_count - SPEC_TARGETS["node_count"]) / SPEC_TARGETS["node_count"]
    coast_err = abs(arr.coast_length_km - SPEC_TARGETS["coast_length_km"]) / SPEC_TARGETS["coast_length_km"]
    expected_nodes = int(np.ceil(arr.coast_length_km / arr.node_spacing_km)) + 1
    return {
        "node_spacing_km": arr.node_spacing_km,
        "node_count": arr.node_count,
        "coast_length_km": arr.coast_length_km,
        "expected_node_count_formula": expected_nodes,
        "spacing_within_1pct": spacing_err <= 0.01,
        "count_within_1pct": count_err <= 0.01,
        "coast_within_1pct": coast_err <= 0.01,
    }
