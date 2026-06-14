"""Pedestrian dead reckoning speed measurement (heading-independent)."""

from __future__ import annotations

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT, soldier_stride_km


def pdr_speed_measurement(
    cfg: AGINSConfig,
    rng: np.random.Generator,
    nominal_speed_kmh: float | None = None,
) -> tuple[float, float]:
    s = cfg.soldier
    pdr = s.pdr
    spd = nominal_speed_kmh if nominal_speed_kmh is not None else s.speed_kmh
    step_err = rng.normal(0, pdr.step_err)
    stride = soldier_stride_km(cfg) * (1 + rng.normal(0, pdr.stride_err))
    spd_meas = pdr.steps_per_min * stride / DT * (1 + step_err)
    sigma = spd * pdr.speed_sigma_frac
    return float(spd_meas), float(sigma ** 2)
