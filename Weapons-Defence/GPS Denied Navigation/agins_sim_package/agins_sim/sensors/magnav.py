"""Magnetic anomaly navigation (MagNav) position fix sensor."""

from __future__ import annotations

import numpy as np

from agins_sim.config import MagNavConfig


def magnav_fix(
    true_pos: np.ndarray,
    urban_disturbance: float,
    rng: np.random.Generator,
    cfg: MagNavConfig,
    storm_factor: float = 1.0,
) -> tuple[np.ndarray | None, np.ndarray | None]:
    d = np.sqrt((true_pos[0] - 3) ** 2 + (true_pos[1] - 3) ** 2)
    sigma = (cfg.sigma_open_km if d < 2.0 else cfg.sigma_urban_km) + urban_disturbance / 500.0
    sigma *= storm_factor
    if sigma > 1.0:
        return None, None
    z = true_pos + rng.standard_t(2.5, size=2) * sigma * np.sqrt(1.5 / 2.5)
    R = np.diag([sigma ** 2] * 2)
    return z, R
