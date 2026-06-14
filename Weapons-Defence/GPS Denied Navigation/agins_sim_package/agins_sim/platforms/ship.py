"""FOG-grade maritime navigation simulation."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT, N_STEPS, ship_speed_kmh
from agins_sim.filter.gh_sr_imm import GHSRIMM
from agins_sim.filter.standard_kf import StandardKF
from agins_sim.scenarios.environments import ship_environment
from agins_sim.sensors.celestial import celestial_fix
from agins_sim.sensors.imu import dead_reckon_ship
from agins_sim.sensors.magnav import magnav_fix
from agins_sim.sensors.polar_compass import polar_compass_heading


def generate_ship_truth(scenario: str, cfg: AGINSConfig = DEFAULT_CONFIG, seed: int = 42) -> np.ndarray:
    """2-hour transit at ~15 kn with course changes and swell-induced yaw."""
    rng = np.random.default_rng(seed)
    N = N_STEPS
    spd = ship_speed_kmh(cfg)
    turn_rate = np.radians(cfg.ship.turn_rate_deg_s)
    _, swell, _, _ = ship_environment(scenario, seed)

    T = np.zeros((N, 4))
    h = tgt = np.radians(cfg.ship.initial_heading_deg)
    n = e = 0.0

    for k in range(N):
        T[k] = [n, e, spd * np.cos(h), spd * np.sin(h)]
        if k == 30:
            tgt = h + np.radians(25)
        if k == 60:
            tgt = h - np.radians(15)
        if k == 90:
            tgt = h + np.radians(20)
        swell_yaw = np.radians(0.3 * swell[k] / 6.0) * rng.normal(0, 1)
        d = (tgt - h + np.pi) % (2 * np.pi) - np.pi
        h += np.clip(d, -turn_rate * DT, turn_rate * DT) + swell_yaw * DT
        n += spd * np.cos(h) * DT
        e += spd * np.sin(h) * DT
    return T


def _position_error(est: np.ndarray, truth: np.ndarray) -> np.ndarray:
    return np.sqrt((est[:, 0] - truth[:, 0]) ** 2 + (est[:, 1] - truth[:, 1]) ** 2) * 1000


def _heading_error(est: np.ndarray, truth: np.ndarray) -> np.ndarray:
    h = np.arctan2(est[:, 3], est[:, 2])
    ht = np.arctan2(truth[:, 3], truth[:, 2])
    return np.abs(np.degrees((h - ht + np.pi) % (2 * np.pi) - np.pi))


def _error_stats(pe: np.ndarray, he: np.ndarray | None, warmup: int) -> Dict[str, float]:
    w = pe[warmup:]
    stats = {
        "mean_m": float(np.mean(w)),
        "p90_m": float(np.percentile(w, 90)),
        "max_m": float(np.max(w)),
    }
    if he is not None:
        stats["heading_deg"] = float(np.mean(he[warmup:]))
    return stats


def simulate_ship(
    scenario: str,
    cfg: AGINSConfig = DEFAULT_CONFIG,
    seed: int = 42,
) -> Dict[str, Any]:
    """Run one maritime scenario (clear or storm)."""
    r1 = np.random.default_rng(seed + 10)
    r2 = np.random.default_rng(seed + 20)

    T = generate_ship_truth(scenario, cfg, seed)
    DR = dead_reckon_ship(T, cfg, np.random.default_rng(seed + 99), T[0, :4].copy())
    sky, swell, night, storm_factor = ship_environment(scenario, seed)

    fc = cfg.filter
    x0 = T[0, :4].copy()
    P0 = np.diag([fc.init_pos_var, fc.init_pos_var, fc.init_vel_var * 0.5, fc.init_vel_var * 0.5])

    gh = GHSRIMM(cfg)
    kf = StandardKF(cfg)
    gh.init(x0, P0)
    kf.init(x0, P0)

    eg = np.zeros((N_STEPS, 4))
    ek = np.zeros((N_STEPS, 4))
    eg[0] = ek[0] = x0
    mu = np.zeros((N_STEPS, 3))
    mu[0] = gh.model_probs()
    counts = {"celestial": 0, "mag": 0, "pol": 0}

    cel = cfg.ship.celestial
    mag = cfg.ship.magnav
    pol = cfg.ship.polar

    for k in range(1, N_STEPS):
        gh.predict()
        kf.predict()

        tp = T[k, :2]
        th = np.arctan2(T[k, 3], T[k, 2])
        sf = sky[k]

        zp = Rp = None
        zh2 = Rh2 = None

        if sf > cel.sky_threshold and k % cel.interval_steps == 0:
            zp, Rp = celestial_fix(tp, r1, cel, storm_factor)
            counts["celestial"] += 1
        elif k % mag.interval_steps == 0:
            zm, Rm = magnav_fix(tp, swell[k], r1, mag, storm_factor)
            if zm is not None:
                zp, Rp = zm, Rm
                counts["mag"] += 1

        if sf > pol.sky_threshold:
            zh2, Rh2 = polar_compass_heading(th, sf, r2, pol, storm_factor)
            counts["pol"] += 1

        eg[k] = gh.update(zp, Rp, None, None, zh2, Rh2, fc.heading_gate_deg)
        ek[k] = kf.update(zp, Rp, None, None, zh2, Rh2, fc.heading_gate_deg)
        mu[k] = gh.model_probs()

    pg = _position_error(eg, T)
    pk = _position_error(ek, T)
    pd = _position_error(DR, T)
    hg = _heading_error(eg, T)
    hk = _heading_error(ek, T)

    w = cfg.warmup_steps
    filters = {
        "GH+compass": _error_stats(pg, hg, w),
        "KF+compass": _error_stats(pk, hk, w),
        "DR (FOG IMU)": _error_stats(pd, None, w),
    }

    return {
        "platform": "ship",
        "scenario": scenario,
        "seed": seed,
        "speed_kn": cfg.ship.speed_kn,
        "speed_kmh": ship_speed_kmh(cfg),
        "duration_hr": N_STEPS * DT / 60.0,
        "sensor_counts": counts,
        "storm_factor": storm_factor,
        "filters": filters,
        "trajectory": {
            "truth_north_km": T[:, 0].tolist(),
            "truth_east_km": T[:, 1].tolist(),
            "gh_north_km": eg[:, 0].tolist(),
            "gh_east_km": eg[:, 1].tolist(),
        },
        "time_series": {
            "position_error_gh_m": pg.tolist(),
            "position_error_kf_m": pk.tolist(),
            "position_error_dr_m": pd.tolist(),
            "imm_probs": mu.tolist(),
            "sky_fraction": sky.tolist(),
            "swell_m": swell.tolist(),
        },
    }
