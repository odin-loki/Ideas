"""Polarised sky compass heading sensor."""

from __future__ import annotations

import numpy as np

from agins_sim.config import PolarCompassConfig


def polar_compass_heading(
    true_heading: float,
    sky_fraction: float,
    rng: np.random.Generator,
    cfg: PolarCompassConfig,
    storm_factor: float = 1.0,
) -> tuple[float, float]:
    sigma = np.radians(cfg.sigma_deg * storm_factor) * (1 + 0.6 * (1 - sky_fraction))
    noise = rng.normal(0, sigma)
    if rng.random() < cfg.blunder_rate:
        noise += rng.choice([-1, 1]) * np.radians(cfg.blunder_deg)
    return true_heading + noise, float(sigma ** 2)
