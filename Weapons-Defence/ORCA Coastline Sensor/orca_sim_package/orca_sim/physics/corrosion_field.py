"""Corrosion (UEP) electric field — dipole in conductive seawater."""

from __future__ import annotations

import numpy as np

from orca_sim.config import ORCAConfig, VesselType, depth_offset_m


def corrosion_field_lateral_v_m(
    range_m: float | np.ndarray,
    moment_am: float,
    conductivity_s_m: float,
    delta_z_m: float,
) -> float | np.ndarray:
    """
    Lateral electric field magnitude [V/m] from a current dipole.

    E(r) = M / (4π · σ · (r² + Δz²)^(3/2))   [Appendix A]
    """
    r = np.asarray(range_m, dtype=float)
    denom = 4.0 * np.pi * conductivity_s_m * np.power(r * r + delta_z_m * delta_z_m, 1.5)
    return moment_am / denom


def corrosion_voltage_v(
    range_m: float | np.ndarray,
    vessel: VesselType,
    cfg: ORCAConfig,
) -> float | np.ndarray:
    """Differential electrode voltage V_signal = E(r) · D."""
    e = corrosion_field_lateral_v_m(
        range_m,
        vessel.dipole_moment_am,
        cfg.node.seawater_conductivity_s_m,
        depth_offset_m(cfg, vessel),
    )
    return e * cfg.node.baseline_m


def corrosion_voltage_at_km(
    range_km: float,
    vessel: VesselType,
    cfg: ORCAConfig,
) -> float:
    return float(corrosion_voltage_v(range_km * 1000.0, vessel, cfg))
