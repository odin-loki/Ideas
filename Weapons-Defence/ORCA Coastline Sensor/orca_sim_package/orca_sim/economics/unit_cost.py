"""Tier 1 acquisition and unit economics."""

from __future__ import annotations

from orca_sim.config import ORCAConfig, SPEC_TARGETS


def simulate_unit_cost(cfg: ORCAConfig) -> dict:
    eco = cfg.economics
    lo, hi = eco.node_cost_small_batch_usd
    tier1_acquisition = (
        eco.prototype_cost_usd
        + eco.tier1_production_usd
        + eco.deployment_usd
        + eco.shore_station_usd
        + eco.integration_usd
    )
    array_hardware_only = eco.tier1_nodes * eco.node_cost_nominal_usd
    p8a_ratio = eco.p8a_unit_cost_usd / tier1_acquisition

    return {
        "node_cost_range_usd": [lo, hi],
        "node_cost_nominal_usd": eco.node_cost_nominal_usd,
        "tier1_nodes": eco.tier1_nodes,
        "prototype_cost_usd": eco.prototype_cost_usd,
        "tier1_production_usd": eco.tier1_production_usd,
        "deployment_usd": eco.deployment_usd,
        "shore_station_usd": eco.shore_station_usd,
        "integration_usd": eco.integration_usd,
        "tier1_acquisition_usd": tier1_acquisition,
        "spec_tier1_acquisition_usd": SPEC_TARGETS["tier1_acquisition_usd"],
        "tier1_error_pct": abs(tier1_acquisition - SPEC_TARGETS["tier1_acquisition_usd"])
        / SPEC_TARGETS["tier1_acquisition_usd"]
        * 100.0,
        "array_hardware_only_usd": array_hardware_only,
        "p8a_unit_cost_usd": eco.p8a_unit_cost_usd,
        "orca_vs_p8a_acquisition_ratio": p8a_ratio,
        "orca_pct_of_p8a_cost": 100.0 / p8a_ratio,
    }
