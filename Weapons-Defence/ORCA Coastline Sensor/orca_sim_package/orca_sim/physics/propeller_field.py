"""Propeller (ELFE) oscillating dipole with skin-depth attenuation."""

from __future__ import annotations

import numpy as np

from orca_sim.config import MU0, ORCAConfig, VesselType, blade_rate_hz


def skin_depth_m(frequency_hz: float, conductivity_s_m: float) -> float:
    """
    Electromagnetic skin depth in seawater.

    δ(f) = √(2 / (ω · μ₀ · σ))
    """
    omega = 2.0 * np.pi * frequency_hz
    return np.sqrt(2.0 / (omega * MU0 * conductivity_s_m))


def propeller_field_v_m(
    range_m: float | np.ndarray,
    moment_am: float,
    frequency_hz: float,
    conductivity_s_m: float,
) -> float | np.ndarray:
    """
    Oscillating dipole field with exponential skin-depth attenuation.

    E(r, f) = (M · ω · μ₀) / (4π · r²) · exp(−r / δ(f))
    """
    r = np.maximum(np.asarray(range_m, dtype=float), 1.0)
    omega = 2.0 * np.pi * frequency_hz
    delta = skin_depth_m(frequency_hz, conductivity_s_m)
    return (moment_am * omega * MU0) / (4.0 * np.pi * r * r) * np.exp(-r / delta)


def harmonic_moment(moment_f0_am: float, harmonic_index: int) -> float:
    """Relative amplitude roll-off 1/k^1.5 for k-th harmonic."""
    if harmonic_index < 1:
        raise ValueError("harmonic_index must be >= 1")
    return moment_f0_am / (harmonic_index ** 1.5)


def combined_propeller_field_v_m(
    range_m: float | np.ndarray,
    vessel: VesselType,
    cfg: ORCAConfig,
    n_harmonics: int = 5,
) -> float | np.ndarray:
    """RSS combination of fundamental + harmonics at range r."""
    f0 = blade_rate_hz(vessel)
    sigma = cfg.node.seawater_conductivity_s_m
    fields = []
    for k in range(1, n_harmonics + 1):
        mk = harmonic_moment(vessel.propeller_moment_am, k)
        fk = f0 * k
        fields.append(propeller_field_v_m(range_m, mk, fk, sigma))
    return np.sqrt(np.sum(np.square(fields), axis=0))


def propeller_voltage_v(
    range_m: float | np.ndarray,
    vessel: VesselType,
    cfg: ORCAConfig,
    n_harmonics: int = 5,
) -> float | np.ndarray:
    """Spatially filtered electrode voltage before DEMON/coherent gains."""
    e = combined_propeller_field_v_m(range_m, vessel, cfg, n_harmonics)
    return e * cfg.node.baseline_m


def demon_processing_gain_linear(cfg: ORCAConfig) -> float:
    """Total linear gain from ELFE/DEMON processing chain (spec §3.5)."""
    return 10.0 ** (cfg.processing_gains.total_propeller_db / 20.0)


def propeller_voltage_processed_v(
    range_m: float | np.ndarray,
    vessel: VesselType,
    cfg: ORCAConfig,
) -> float | np.ndarray:
    """Propeller voltage after coherent integration, spatial filter, and DEMON."""
    return (
        propeller_voltage_v(range_m, vessel, cfg)
        * demon_processing_gain_linear(cfg)
        * cfg.propeller_gain_scale
    )
