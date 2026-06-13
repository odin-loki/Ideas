"""Shared lifecycle physics — firearm + crew-served reliability models."""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional


def lame_hoop_sf(pressure_MPa: float, r_i_mm: float, r_o_mm: float,
                 yield_MPa: float) -> float:
    r_i = r_i_mm / 1000.0
    r_o = r_o_mm / 1000.0
    sigma = pressure_MPa * 1e6 * (r_i ** 2) * (r_o ** 2 + r_i ** 2) / (
        (r_i ** 2) * (r_o ** 2 - r_i ** 2)
    ) / 1e6
    return yield_MPa / max(sigma, 1.0)


def archard_bore_life(r_i_mm: float, peak_pressure_MPa: float,
                      barrel_length_mm: float, archard_K: float,
                      archard_H_GPa: float, cap_rounds: int) -> int:
    bore_area = math.pi * (r_i_mm / 1000.0) ** 2
    p_avg = peak_pressure_MPa * 0.55 * 1e6
    f_n = p_avg * bore_area
    l_per_round = barrel_length_mm / 1000.0
    wear_per_round = archard_K * f_n * l_per_round / (archard_H_GPa * 1e9)
    max_wear = 0.05e-3
    if wear_per_round <= 0:
        return cap_rounds
    calc = int(max_wear / wear_per_round)
    return min(cap_rounds, max(calc, 1_000))


def felt_recoil_ftlbf(projectile_mass_g: float, mv_ms: float,
                      propellant_g: float, shooter_mass_kg: float,
                      brake_eff: float = 0.0) -> float:
    m_b = projectile_mass_g / 1000.0
    m_prop = propellant_g / 1000.0
    j_free = m_b * mv_ms + m_prop * 600.0
    e_j = j_free ** 2 / (2.0 * shooter_mass_kg)
    return e_j * 0.737562 * (1.0 - brake_eff)


def analytic_mrbf(rates: Dict[str, int]) -> float:
    total = sum(1.0 / n for n in rates.values())
    return 1.0 / total if total > 0 else float("inf")


def reliability_monte_carlo(rates: Dict[str, int],
                            n_rounds: int = 30_000,
                            n_bootstrap: int = 200,
                            seed: int = 42) -> Dict[str, float]:
    rng = random.Random(seed)
    probs = [1.0 / rates[m] for m in rates]
    stoppages = 0
    for _ in range(n_rounds):
        for p in probs:
            if rng.random() < p:
                stoppages += 1
                break
    mean_mrbf = n_rounds / max(stoppages, 1)
    boots: List[float] = []
    for _ in range(n_bootstrap):
        s = sum(1 for _ in range(n_rounds)
                if any(rng.random() < p for p in probs))
        boots.append(n_rounds / max(s, 1))
    boots.sort()
    lo = boots[int(0.05 * len(boots))]
    hi = boots[int(0.95 * len(boots)) - 1]
    return {
        "mrbf_simulated": round(mean_mrbf, 0),
        "mrbf_ci_90_low": round(lo, 0),
        "mrbf_ci_90_high": round(hi, 0),
    }
