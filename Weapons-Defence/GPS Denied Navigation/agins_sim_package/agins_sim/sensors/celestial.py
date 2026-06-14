"""Celestial position fix sensor models."""

from __future__ import annotations

import numpy as np

from agins_sim.config import CelestialConfig


def celestial_fix(
    true_pos: np.ndarray,
    rng: np.random.Generator,
    cfg: CelestialConfig,
    storm_factor: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    sigma = cfg.sigma_km * storm_factor
    z = true_pos + rng.normal(0, sigma, size=2)
    R = np.diag([sigma ** 2] * 2)
    return z, R
