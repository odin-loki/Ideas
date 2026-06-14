"""Signal-to-noise ratio models for ORCA detection."""

from __future__ import annotations

import numpy as np

from orca_sim.config import ORCAConfig, snr_threshold_linear


def electrode_noise_bandwidth_hz(integration_s: float) -> float:
    """Equivalent noise bandwidth for coherent integration window."""
    return max(1.0 / integration_s, 1e-6)


def noise_voltage_single_pair_v(
    electrode_noise_nv_rt_hz: float,
    bandwidth_hz: float,
) -> float:
    """
    Differential pair noise voltage.

    V_noise = √2 · electrode_noise · √BW   [Appendix A]
    """
    en = electrode_noise_nv_rt_hz * 1e-9
    return np.sqrt(2.0) * en * np.sqrt(bandwidth_hz)


def noise_voltage_matched_filter_v(
    cfg: ORCAConfig,
    *,
    dc_band: bool = True,
    integration_s: float | None = None,
    n_pairs: int | None = None,
) -> float:
    """
    Noise after matched spatial filter over N independent pairs.

    V_noise = √2 · electrode_noise · √BW / √N
    """
    node = cfg.node
    if dc_band:
        bw = cfg.dc_noise_bandwidth_hz
        en = node.electrode_noise_dc_nv_rt_hz
        n = n_pairs if n_pairs is not None else node.n_pairs
        integ = node.dc_integration_s
    else:
        integ = integration_s if integration_s is not None else node.demon_integration_s
        bw = electrode_noise_bandwidth_hz(integ)
        en = node.electrode_noise_elfe_nv_rt_hz
        n = node.n_electrodes  # spec §3.5: matched filter over 7 electrodes for ELFE

    base = noise_voltage_single_pair_v(en, bw)
    return base / np.sqrt(n)


def snr_linear(signal_v: float, noise_v: float) -> float:
    if noise_v <= 0:
        return float("inf")
    return signal_v / noise_v


def snr_db(signal_v: float, noise_v: float) -> float:
    ratio = snr_linear(signal_v, noise_v)
    if ratio <= 0:
        return -np.inf
    return 20.0 * np.log10(ratio)


def exceeds_detection_threshold(signal_v: float, noise_v: float, cfg: ORCAConfig) -> bool:
    return snr_linear(signal_v, noise_v) >= snr_threshold_linear(cfg)


def false_alarm_rate_per_week(cfg: ORCAConfig) -> float:
    """
    Approximate false-alarm rate at 10 dB threshold in Gaussian noise.

    Spec target: < 1 event / node / week. With 60 s integration and 10 dB threshold
    on a unit-variance normal statistic, P(false alarm per sample) ≈ erfc(3.162/√2)/2.
    Scale to weekly rate using integration cadence.
    """
    from scipy.special import erfc

    threshold = snr_threshold_linear(cfg)
    pfa_per_window = 0.5 * erfc(threshold / np.sqrt(2.0))
    windows_per_week = (7 * 24 * 3600) / cfg.node.dc_integration_s
    return float(pfa_per_window * windows_per_week)
