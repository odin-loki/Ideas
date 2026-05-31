"""
OAM-VEST Simulation Package
safety.py — Safety analysis, engagement envelope, and interlock simulation

Covers:
  - Full lethality margin table across all ranges
  - Minimum safe engagement range calculations
  - Multi-mode effect mapping (plain air / earplugged)
  - LiDAR interlock and dwell timer integration
  - Thermal analysis (tissue heating verification)
  - Pulsed cochlear dose at all range bands
"""

import numpy as np
from typing import Dict, List, Tuple
from physics import (spl_at_range, spl_to_pa, pa_to_spl, intensity,
                     shock_formation_distance, radiation_pressure_force,
                     classify_effect, effect_with_earplug,
                     THRESHOLD, C_SOUND, RHO_AIR, RHO_TISSUE, CP_TISSUE,
                     alpha_db_per_m)
from pulse import (PulseRegime, PowerSystem, LiDARInterleave, DwellTimer,
                   simulate_cochlear_dose, simulate_vestibular)
from acoustic_array import oam_canal_stimulus, oam_nystagmus_margin


# ─── Design parameters ─────────────────────────────────────────────────────────

DESIGN = {
    "source_spl_db":      173.0,
    "freq_hz":            3000.0,
    "min_engage_range_m":  15.0,
    "lidar_cutoff_m":      10.0,
    "max_dwell_s":          5.0,
    "pulse_prf_hz":         2.0,
    "pulse_width_s":        0.1,
    "oam_charge":           1,
    "oam_mod_hz":           2.0,
    "am_carrier_hz":       2500.0,
    "am_mod_hz":            2.0,
}


# ─── Lethality margin analysis ────────────────────────────────────────────────

def lethality_margins(source_spl: float = 173.0,
                      freq_hz: float = 3000.0) -> List[dict]:
    """
    Compute safety margins against all biological thresholds at key ranges.
    """
    from scipy.optimize import brentq

    def crossover_range(threshold_db):
        def eq(r): return spl_at_range(source_spl, freq_hz, r) - threshold_db
        try:
            return brentq(eq, 0.001, 5000.0)
        except ValueError:
            return 0.0

    ranges_to_check = [1, 5, 10, 15, 20, 50, 100, 200, 465]
    results = []

    for label, thr in THRESHOLD.items():
        r_cross = crossover_range(thr)
        row = {
            "threshold":      label,
            "threshold_db":   thr,
            "crossover_range_m": round(r_cross, 2),
        }
        for r in ranges_to_check:
            spl = spl_at_range(source_spl, freq_hz, r)
            row[f"margin_{r}m"] = round(thr - spl, 1)
        results.append(row)

    return results


def engagement_envelope(source_spl: float = 173.0,
                         freq_hz: float = 3000.0) -> dict:
    """
    Maximum range for each effect level. Also computes area denial footprint.
    """
    from physics import max_range_for_effect
    beam_half_angle_deg = 15.0
    envelope = {}
    for effect in THRESHOLD.keys():
        r = max_range_for_effect(source_spl, freq_hz, effect)
        if r > 0:
            beam_width = 2.0 * r * np.tan(np.radians(beam_half_angle_deg))
            area       = np.pi * (beam_width / 2.0) ** 2
            envelope[effect] = {
                "max_range_m":     round(r, 1),
                "beam_width_m":    round(beam_width, 1),
                "cone_area_m2":    round(area, 0),
            }
    return envelope


# ─── Multi-mode effect matrix ─────────────────────────────────────────────────

def effect_matrix(source_spl: float = 173.0,
                   ranges: List[float] = None,
                   freqs: List[float] = None) -> List[dict]:
    """
    Matrix of effects at various ranges and frequencies,
    for both unprotected and ear-plugged personnel.
    """
    if ranges is None:
        ranges = [5, 10, 15, 20, 30, 50, 100, 200, 300, 465]
    if freqs is None:
        freqs = [500, 2000, 3000]

    results = []
    for r in ranges:
        for f in freqs:
            spl = spl_at_range(source_spl, f, r)
            results.append({
                "range_m":         r,
                "freq_hz":         f,
                "spl_db":          round(spl, 1),
                "effect_bare":     classify_effect(spl),
                "effect_earplug":  effect_with_earplug(spl, bone_conducted=False),
                "effect_mode_b":   effect_with_earplug(spl, bone_conducted=True),
            })
    return results


# ─── Thermal analysis ────────────────────────────────────────────────────────

def tissue_heating(spl_db: float, freq_hz: float, duration_s: float,
                    alpha_tissue_np_m: float = 0.0115) -> float:
    """
    Temperature rise in superficial tissue from acoustic absorption.
    dT = (2 * alpha * I * t) / (rho_tissue * Cp)

    alpha_tissue_np_m: tissue absorption coefficient (Np/m)
      ~0.0115 Np/m for audible freqs in soft tissue
      ~2.65 Np/m for 40 kHz ultrasound in tissue
    """
    p = spl_to_pa(spl_db)
    I = p**2 / (2.0 * RHO_AIR * C_SOUND)
    P_dep = 2.0 * alpha_tissue_np_m * I
    return P_dep * duration_s / (RHO_TISSUE * CP_TISSUE)


def thermal_analysis_table() -> List[dict]:
    """Verify thermal effects are negligible at non-lethal SPLs."""
    results = []
    for spl in [130, 140, 150, 160]:
        for dur in [1, 5, 10]:
            dT_audio   = tissue_heating(spl, 3000, dur, 0.0115)
            dT_ultrasound = tissue_heating(spl, 40000, dur, 2.65)
            results.append({
                "spl_db":          spl,
                "duration_s":      dur,
                "dT_3kHz_degC":    round(dT_audio, 5),
                "dT_40kHz_degC":   round(dT_ultrasound, 4),
                "thermal_hazard":  dT_audio > 1.0 or dT_ultrasound > 1.0,
            })
    return results


# ─── Shock formation analysis ─────────────────────────────────────────────────

def shock_analysis_table() -> List[dict]:
    """Shock formation distances for various SPL/frequency combinations."""
    results = []
    for spl in [140, 150, 155, 160, 165, 173]:
        for freq in [500, 2000, 3000, 8000]:
            x_s = shock_formation_distance(spl, freq)
            results.append({
                "spl_db":            spl,
                "freq_hz":           freq,
                "shock_distance_m":  round(x_s, 3),
                "nonlinear_at_1m":   x_s < 1.0,
            })
    return results


# ─── Multi-target SPL budget ──────────────────────────────────────────────────

def multi_target_budget(source_spl: float = 173.0, freq_hz: float = 3000.0,
                          range_m: float = 20.0) -> List[dict]:
    """
    SPL per beam when splitting aperture across N simultaneous targets.
    Power splits N ways: penalty = 10*log10(N) dB.
    """
    results = []
    for N in range(1, 9):
        spl_beam  = source_spl - 10.0 * np.log10(N)
        spl_at_r  = spl_at_range(spl_beam, freq_hz, range_m)
        results.append({
            "n_targets":       N,
            "spl_per_beam_db": round(spl_beam, 1),
            "spl_at_range_db": round(spl_at_r, 1),
            "effect":          classify_effect(spl_at_r),
        })
    return results


# ─── Interlock simulation ─────────────────────────────────────────────────────

def simulate_interlock_scenario(n_seconds: float = 30.0,
                                  target_profile: str = "advancing") -> dict:
    """
    Simulate a complete engagement including LiDAR interlock and dwell timer.

    target_profile options:
      "advancing"  — target walks from 200m to 5m at 1.5 m/s
      "stationary" — target at fixed 30m
      "retreating" — target moves from 20m to 100m
    """
    dt      = 0.05
    regime  = PulseRegime(prf_hz=2.0, pulse_width_s=0.1, peak_spl_db=173.0)
    dwell   = DwellTimer(max_dwell_s=5.0, cooldown_s=3.0)
    times, ranges_m, spls, beam_permit = [], [], [], []

    t = 0.0
    while t < n_seconds:
        # Target position
        if target_profile == "advancing":
            r = max(200.0 - 1.5 * t, 4.0)
        elif target_profile == "stationary":
            r = 30.0
        elif target_profile == "retreating":
            r = min(20.0 + 2.0 * t, 200.0)
        else:
            r = 30.0

        t_in_period = t % regime.period_s
        is_on       = t_in_period < regime.pulse_width_s
        lidar_ok    = r >= DESIGN["lidar_cutoff_m"]
        range_ok    = r >= DESIGN["min_engage_range_m"]
        permitted   = dwell.step(dt, is_on and lidar_ok and range_ok)
        active      = is_on and permitted and lidar_ok and range_ok

        if active:
            spl = spl_at_range(regime.peak_spl_db, 3000.0, r)
        else:
            spl = 0.0

        times.append(t)
        ranges_m.append(r)
        spls.append(spl)
        beam_permit.append(float(active))
        t += dt

    import numpy as np
    return {
        "time_s":      np.array(times),
        "range_m":     np.array(ranges_m),
        "spl_db":      np.array(spls),
        "beam_active": np.array(beam_permit),
        "profile":     target_profile,
    }


# ─── Full safety report ───────────────────────────────────────────────────────

def full_safety_report() -> dict:
    """
    Run all safety analyses and return consolidated report dict.
    """
    regime = PulseRegime(prf_hz=2.0, pulse_width_s=0.1, peak_spl_db=173.0)
    power  = PowerSystem()
    lidar  = LiDARInterleave(regime)
    oam_stimulus = oam_canal_stimulus(2.0, 1)

    cochlear_20m = simulate_cochlear_dose(regime, 3000.0, 20.0, 60.0)
    cochlear_50m = simulate_cochlear_dose(regime, 3000.0, 50.0, 60.0)
    vest_sim     = simulate_vestibular(regime, oam_stimulus, 30.0)

    return {
        "lethality_margins":   lethality_margins(),
        "engagement_envelope": engagement_envelope(),
        "effect_matrix":       effect_matrix(),
        "thermal_analysis":    thermal_analysis_table(),
        "shock_analysis":      shock_analysis_table(),
        "multi_target":        multi_target_budget(),
        "power_validation":    power.validate(regime),
        "lidar_timing":        lidar.timing_summary(),
        "oam_nystagmus_margin": oam_nystagmus_margin(2.0, 1),
        "cochlear_20m":        cochlear_20m,
        "cochlear_50m":        cochlear_50m,
        "vestibular_sim":      vest_sim,
        "interlock_advancing": simulate_interlock_scenario(30.0, "advancing"),
    }
