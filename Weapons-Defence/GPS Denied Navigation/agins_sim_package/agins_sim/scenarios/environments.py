"""Environment profiles for soldier and maritime scenarios."""

from __future__ import annotations

import numpy as np

from agins_sim.config import N_STEPS


def soldier_environment(scenario: str, seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return sky_fraction, urban_disturbance (nT), night flag arrays."""
    rng = np.random.default_rng(seed + 2)
    N = N_STEPS
    sky = np.zeros(N)
    urb = np.zeros(N)
    night = np.zeros(N, dtype=bool)

    for k in range(N):
        if scenario == "open_night":
            sky[k] = np.clip(0.75 + rng.normal(0, 0.08), 0, 1)
            night[k] = True
        elif scenario == "open_day":
            sky[k] = np.clip(0.30 + rng.normal(0, 0.12), 0, 0.65)
        elif scenario == "urban":
            sky[k] = np.clip(0.15 + 0.2 * np.sin(k * 0.3) + rng.normal(0, 0.08), 0, 0.4)
            urb[k] = np.clip(rng.normal(500, 150), 200, 900)
        elif scenario == "mixed":
            if k < 40:
                sky[k] = np.clip(0.70 + rng.normal(0, 0.08), 0, 1)
            elif k < 80:
                sky[k] = np.clip(0.15 + rng.normal(0, 0.08), 0, 0.35)
                urb[k] = np.clip(rng.normal(480, 150), 200, 900)
            else:
                sky[k] = np.clip(0.65 + rng.normal(0, 0.10), 0, 1)
                night[k] = True
        else:
            raise ValueError(f"Unknown soldier scenario: {scenario}")
    return sky, urb, night


def ship_environment(scenario: str, seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """
    Maritime environment: sky_fraction, swell (m), night flag, storm noise factor.
    """
    rng = np.random.default_rng(seed + 2)
    N = N_STEPS
    sky = np.zeros(N)
    swell = np.zeros(N)
    night = np.zeros(N, dtype=bool)
    storm_factor = 1.0

    if scenario == "clear":
        for k in range(N):
            sky[k] = np.clip(0.85 + rng.normal(0, 0.06), 0.5, 1.0)
            swell[k] = np.clip(rng.normal(1.5, 0.5), 0.5, 3.0)
            night[k] = k % 24 < 12  # half night for star fixes
        storm_factor = 1.0
    elif scenario == "storm":
        for k in range(N):
            sky[k] = np.clip(0.25 + rng.normal(0, 0.10), 0.05, 0.45)
            swell[k] = np.clip(rng.normal(5.5, 1.2), 3.0, 9.0)
            night[k] = k % 24 < 12
        storm_factor = 1.35
    else:
        raise ValueError(f"Unknown ship scenario: {scenario}")

    return sky, swell, night, storm_factor
