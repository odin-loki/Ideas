"""Soldier-portable MEMS navigation simulation."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT, N_STEPS
from agins_sim.filter.gh_sr_imm import GHSRIMM
from agins_sim.filter.standard_kf import StandardKF
from agins_sim.scenarios.environments import soldier_environment
from agins_sim.sensors.celestial import celestial_fix
from agins_sim.sensors.imu import dead_reckon_pdr, dead_reckon_raw, simulate_imu
from agins_sim.sensors.magnav import magnav_fix
from agins_sim.sensors.pdr import pdr_speed_measurement
from agins_sim.sensors.polar_compass import polar_compass_heading


def generate_truth(scenario: str, cfg: AGINSConfig = DEFAULT_CONFIG, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    N = N_STEPS
    spd = cfg.soldier.speed_kmh
    turn_rate = np.radians(cfg.soldier.turn_rate_deg_s)
    T = np.zeros((N, 4))
    h = tgt = np.radians(cfg.soldier.initial_heading_deg)
    n = e = 0.0

    for k in range(N):
        T[k] = [n, e, spd * np.cos(h), spd * np.sin(h)]
        if scenario in ("open_night", "open_day"):
            if k == 40:
                tgt = h + np.radians(50)
            if k == 80:
                tgt = h - np.radians(30)
        elif scenario == "urban":
            for turn_k in (20, 40, 60, 80):
                if k == turn_k:
                    tgt = h + np.radians(90)
        elif scenario == "mixed":
            if k == 40:
                tgt = h + np.radians(60)
            if k == 80:
                tgt = h - np.radians(60)
        d = (tgt - h + np.pi) % (2 * np.pi) - np.pi
        h += np.clip(d, -turn_rate * DT, turn_rate * DT)
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


def simulate_soldier(
    scenario: str,
    cfg: AGINSConfig = DEFAULT_CONFIG,
    seed: int = 42,
) -> Dict[str, Any]:
    """Run one soldier scenario; returns trajectories, errors, and sensor counts."""
    r1 = np.random.default_rng(seed + 10)
    r2 = np.random.default_rng(seed + 20)
    r3 = np.random.default_rng(seed + 30)
    r4 = np.random.default_rng(seed + 99)

    T = generate_truth(scenario, cfg, seed)
    zh, zs = simulate_imu(T, cfg.soldier.imu, cfg.soldier.pdr.steps_per_min, np.random.default_rng(seed + 1))
    DR_raw = dead_reckon_raw(zh, zs, T[0, :4].copy())
    DR_pdr = dead_reckon_pdr(zh, cfg, r4, T[0, :4].copy())
    sky, urb, night = soldier_environment(scenario, seed)

    fc = cfg.filter
    x0 = T[0, :4].copy()
    P0 = np.diag([fc.init_pos_var, fc.init_pos_var, fc.init_vel_var, fc.init_vel_var])

    gh = GHSRIMM(cfg)
    gh0 = GHSRIMM(cfg)
    kf = StandardKF(cfg)
    gh.init(x0, P0)
    gh0.init(x0, P0)
    kf.init(x0, P0)

    eg = np.zeros((N_STEPS, 4))
    eg0 = np.zeros((N_STEPS, 4))
    ek = np.zeros((N_STEPS, 4))
    eg[0] = eg0[0] = ek[0] = x0
    mu = np.zeros((N_STEPS, 3))
    mu[0] = gh.model_probs()
    counts = {"star": 0, "mag": 0, "pol": 0, "pdr": 0}

    cel = cfg.soldier.celestial
    mag = cfg.soldier.magnav
    pol = cfg.soldier.polar

    for k in range(1, N_STEPS):
        gh.predict()
        gh0.predict()
        kf.predict()

        tp = T[k, :2]
        th = np.arctan2(T[k, 3], T[k, 2])
        sf = sky[k]
        un = urb[k]
        ni = night[k]

        zp = Rp = None
        zspd = rspd = None
        zh2 = Rh2 = None

        if ni and sf > cel.sky_threshold and k % cel.interval_steps == 0:
            zp, Rp = celestial_fix(tp, r1, cel)
            counts["star"] += 1
        if zp is None and k % mag.interval_steps == 0:
            zm, Rm = magnav_fix(tp, un, r1, mag)
            if zm is not None:
                zp, Rp = zm, Rm
                counts["mag"] += 1

        zspd, rspd = pdr_speed_measurement(cfg, r3)
        counts["pdr"] += 1

        if sf > pol.sky_threshold:
            zh2, Rh2 = polar_compass_heading(th, sf, r2, pol)
            counts["pol"] += 1

        eg[k] = gh.update(zp, Rp, zspd, rspd, zh2, Rh2, fc.heading_gate_deg)
        eg0[k] = gh0.update(zp, Rp, None, None, zh2, Rh2, fc.heading_gate_deg)
        ek[k] = kf.update(zp, Rp, zspd, rspd, zh2, Rh2, fc.heading_gate_deg)
        mu[k] = gh.model_probs()

    pg = _position_error(eg, T)
    pg0 = _position_error(eg0, T)
    pk = _position_error(ek, T)
    pd = _position_error(DR_raw, T)
    pd2 = _position_error(DR_pdr, T)
    hg = _heading_error(eg, T)
    hg0 = _heading_error(eg0, T)
    hk = _heading_error(ek, T)

    w = cfg.warmup_steps
    filters = {
        "GH+PDR+compass": _error_stats(pg, hg, w),
        "GH compass only": _error_stats(pg0, hg0, w),
        "KF+PDR+compass": _error_stats(pk, hk, w),
        "DR (PDR)": _error_stats(pd2, None, w),
        "DR (raw MEMS)": _error_stats(pd, None, w),
    }

    return {
        "platform": "soldier",
        "scenario": scenario,
        "seed": seed,
        "sensor_counts": counts,
        "filters": filters,
        "pdr_gain_pct": (
            (filters["GH compass only"]["mean_m"] - filters["GH+PDR+compass"]["mean_m"])
            / max(filters["GH compass only"]["mean_m"], 1e-6)
            * 100
        ),
        "trajectory": {
            "truth_north_km": T[:, 0].tolist(),
            "truth_east_km": T[:, 1].tolist(),
            "gh_north_km": eg[:, 0].tolist(),
            "gh_east_km": eg[:, 1].tolist(),
        },
        "time_series": {
            "position_error_gh_m": pg.tolist(),
            "position_error_gh0_m": pg0.tolist(),
            "position_error_kf_m": pk.tolist(),
            "position_error_dr_pdr_m": pd2.tolist(),
            "position_error_dr_raw_m": pd.tolist(),
            "imm_probs": mu.tolist(),
            "sky_fraction": sky.tolist(),
            "urban_disturbance_nt": urb.tolist(),
        },
    }
