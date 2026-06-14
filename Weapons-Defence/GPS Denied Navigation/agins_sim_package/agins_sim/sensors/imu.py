"""IMU dead-reckoning sensor models (MEMS soldier / FOG ship)."""

from __future__ import annotations

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT, IMUConfig, N_STEPS


def simulate_imu(
    truth: np.ndarray,
    imu_cfg: IMUConfig,
    steps_per_min: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Return heading and speed measurements from IMU."""
    N = truth.shape[0]
    zh = np.zeros(N)
    zs = np.zeros(N)
    hb = 0.0
    gait = np.cumsum(
        rng.normal(0, np.radians(imu_cfg.gait_noise_deg) / np.sqrt(max(steps_per_min, 1)), N)
    ) if imu_cfg.gait_noise_deg > 0 else np.zeros(N)

    for k in range(N):
        th = np.arctan2(truth[k, 3], truth[k, 2])
        ts = np.sqrt(truth[k, 2] ** 2 + truth[k, 3] ** 2)
        hb += np.radians(imu_cfg.heading_drift_deg_hr) * DT + rng.normal(
            0, np.radians(imu_cfg.heading_noise_deg)
        )
        zh[k] = th + hb + gait[k] + rng.normal(0, np.radians(imu_cfg.heading_noise_deg))
        zs[k] = ts + imu_cfg.velocity_bias_kmh + rng.normal(0, imu_cfg.velocity_noise_kmh)
    return zh, zs


def dead_reckon_raw(
    zh: np.ndarray,
    zs: np.ndarray,
    x0: np.ndarray,
) -> np.ndarray:
    N = len(zh)
    est = np.zeros((N, 4))
    est[0] = x0.copy()
    for k in range(1, N):
        vn = zs[k] * np.cos(zh[k])
        ve = zs[k] * np.sin(zh[k])
        est[k] = [est[k - 1, 0] + vn * DT, est[k - 1, 1] + ve * DT, vn, ve]
    return est


def dead_reckon_ship(
    truth: np.ndarray,
    cfg: AGINSConfig,
    rng: np.random.Generator,
    x0: np.ndarray,
) -> np.ndarray:
    """
    FOG inertial DR without external fixes: gyro drift, random walk,
    velocity scale drift, and unknown ocean current (per AGINS spec ~206 m / 2 hr).
    """
    imu = cfg.ship.imu
    ship = cfg.ship
    N = truth.shape[0]
    est = np.zeros((N, 4))
    est[0] = x0.copy()

    hb = 0.0
    vel_scale = 1.0
    mag = ship.dr_ocean_current_kmh * rng.uniform(0.6, 1.0)
    angle = rng.uniform(0, 2 * np.pi)
    current_n = mag * np.cos(angle)
    current_e = mag * np.sin(angle)

    for k in range(1, N):
        th = np.arctan2(truth[k, 3], truth[k, 2])
        ts = np.sqrt(truth[k, 2] ** 2 + truth[k, 3] ** 2)

        hb += (
            np.radians(imu.heading_drift_deg_hr) * DT
            + rng.normal(0, np.radians(ship.dr_gyro_random_walk_deg_sqrt_hr) * np.sqrt(DT))
        )
        vel_scale *= 1.0 + rng.normal(0, ship.dr_velocity_scale_ppm_hr * 1e-6 * DT * 60)

        zh = th + hb + rng.normal(0, np.radians(imu.heading_noise_deg))
        zs = ts * vel_scale + imu.velocity_bias_kmh + rng.normal(0, imu.velocity_noise_kmh)

        vn = zs * np.cos(zh) + current_n
        ve = zs * np.sin(zh) + current_e
        est[k] = [est[k - 1, 0] + vn * DT, est[k - 1, 1] + ve * DT, vn, ve]
    return est


def dead_reckon_pdr(
    zh: np.ndarray,
    cfg: AGINSConfig,
    rng: np.random.Generator,
    x0: np.ndarray,
    nominal_speed_kmh: float | None = None,
) -> np.ndarray:
    from agins_sim.sensors.pdr import pdr_speed_measurement

    N = len(zh)
    est = np.zeros((N, 4))
    est[0] = x0.copy()
    for k in range(1, N):
        spd_pdr, _ = pdr_speed_measurement(cfg, rng, nominal_speed_kmh)
        vn = spd_pdr * np.cos(zh[k])
        ve = spd_pdr * np.sin(zh[k])
        est[k] = [est[k - 1, 0] + vn * DT, est[k - 1, 1] + ve * DT, vn, ve]
    return est
