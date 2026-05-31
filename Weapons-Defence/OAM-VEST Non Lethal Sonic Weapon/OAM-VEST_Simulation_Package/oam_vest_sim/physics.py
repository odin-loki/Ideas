"""
OAM-VEST Simulation Package
physics.py — Core acoustic physics, propagation, and biological thresholds

All equations derived from first principles. References:
  - NIOSH Occupational Noise Exposure criteria
  - Kinsler et al., Fundamentals of Acoustics (4th ed.)
  - DoD Non-Lethal Weapons Directorate published thresholds
"""

import numpy as np

# ─── Physical constants ────────────────────────────────────────────────────────
C_SOUND       = 343.0      # m/s, speed of sound in air at 20°C
RHO_AIR       = 1.21       # kg/m³, air density at 20°C
P_REF         = 20e-6      # Pa, acoustic reference pressure (0 dB SPL)
BETA_AIR      = 1.2        # nonlinearity parameter for air
RHO_TISSUE    = 1060.0     # kg/m³, soft tissue
CP_TISSUE     = 3500.0     # J/kg/K, specific heat capacity of tissue

# ─── Atmospheric absorption coefficients (dB/m) ───────────────────────────────
# ISO 9613-1, 20°C, 50% RH
ALPHA_DB_PER_M = {
    63:    0.0004,
    125:   0.0007,
    250:   0.0015,
    500:   0.003,
    1000:  0.006,
    2000:  0.010,
    3000:  0.014,
    4000:  0.020,
    8000:  0.060,
    16000: 0.180,
}

# ─── Biological thresholds (dB SPL) ───────────────────────────────────────────
THRESHOLD = {
    "annoyance":            85,
    "disorientation":      115,   # OAM vestibular onset
    "pain":                130,
    "incapacitation":      147,
    "eardrum_rupture":     160,
    "cardiac_stress":      170,   # sustained >10s
    "lung_rupture":        185,   # lethal
}

# Vestibular system parameters
CUPULA_TIME_CONSTANT   = 10.0   # seconds
NYSTAGMUS_THRESHOLD    = 2.0    # rad/s angular velocity to canal
BONE_COND_ATTENUATION  = 5.0    # dB, earplug residual attenuation via bone conduction
EARPLUG_NRR            = 33.0   # dB, foam earplug noise reduction rating

# ─── Core SPL functions ───────────────────────────────────────────────────────

def spl_to_pa(spl_db: float) -> float:
    """Convert SPL in dB to pressure amplitude in Pascals."""
    return P_REF * 10.0 ** (spl_db / 20.0)

def pa_to_spl(pressure_pa: float) -> float:
    """Convert pressure amplitude in Pascals to SPL in dB."""
    return 20.0 * np.log10(max(abs(pressure_pa), 1e-30) / P_REF)

def intensity(spl_db: float) -> float:
    """Acoustic intensity in W/m² from SPL."""
    p = spl_to_pa(spl_db)
    return p**2 / (2.0 * RHO_AIR * C_SOUND)

def alpha_db_per_m(freq_hz: float) -> float:
    """
    Atmospheric absorption coefficient in dB/m via log-linear interpolation
    from ISO 9613-1 octave-band values.
    """
    freqs = sorted(ALPHA_DB_PER_M.keys())
    alphas = [ALPHA_DB_PER_M[f] for f in freqs]
    if freq_hz <= freqs[0]:
        return alphas[0]
    if freq_hz >= freqs[-1]:
        return alphas[-1]
    for i in range(len(freqs) - 1):
        if freqs[i] <= freq_hz <= freqs[i+1]:
            t = (np.log10(freq_hz) - np.log10(freqs[i])) / \
                (np.log10(freqs[i+1]) - np.log10(freqs[i]))
            return alphas[i] + t * (alphas[i+1] - alphas[i])
    return 0.01  # fallback

def spl_at_range(spl0_db: float, freq_hz: float, range_m: float) -> float:
    """
    SPL at range r from source.
    Accounts for geometric spreading (inverse square) and atmospheric absorption.

    SPL(r) = SPL0 - 20*log10(r) - alpha*r
    """
    r = max(range_m, 0.01)
    alpha = alpha_db_per_m(freq_hz)
    return spl0_db - 20.0 * np.log10(r) - alpha * r

def required_source_spl(target_spl_db: float, freq_hz: float, range_m: float) -> float:
    """
    Required source SPL to achieve a target SPL at a given range.
    Inverse of spl_at_range.
    """
    r = max(range_m, 0.01)
    alpha = alpha_db_per_m(freq_hz)
    return target_spl_db + 20.0 * np.log10(r) + alpha * r

def max_range_for_effect(spl_source: float, freq_hz: float,
                          effect: str = "disorientation") -> float:
    """
    Maximum range at which a given effect threshold is exceeded.
    Uses binary search (no closed form due to alpha*r term).
    """
    from scipy.optimize import brentq
    target = THRESHOLD[effect]
    def residual(r):
        return spl_at_range(spl_source, freq_hz, r) - target
    try:
        return brentq(residual, 0.1, 5000.0)
    except ValueError:
        # Source not strong enough to reach threshold at any range
        return 0.0

# ─── Nonlinear / shock physics ─────────────────────────────────────────────────

def shock_formation_distance(spl0_db: float, freq_hz: float) -> float:
    """
    Plane-wave shock formation distance (Rankine-Hugoniot).

    x_shock = rho * c^3 / (beta * omega * P0)
    """
    P0    = spl_to_pa(spl0_db)
    omega = 2.0 * np.pi * freq_hz
    return (RHO_AIR * C_SOUND**3) / (BETA_AIR * omega * P0)

def radiation_pressure_force(spl_db: float, area_m2: float = 0.6) -> float:
    """
    Acoustic radiation pressure force on an object.
    F = (I/c) * A = P^2 * A / (2 * rho * c^2)
    Returns force in Newtons.
    """
    p  = spl_to_pa(spl_db)
    I  = p**2 / (2.0 * RHO_AIR * C_SOUND)
    Pr = I / C_SOUND
    return Pr * area_m2

# ─── Effect classification ─────────────────────────────────────────────────────

def classify_effect(spl_db: float) -> str:
    """Classify biological effect from SPL."""
    if spl_db > THRESHOLD["lung_rupture"]:   return "LETHAL"
    if spl_db > THRESHOLD["cardiac_stress"]: return "LETHAL_RISK"
    if spl_db > THRESHOLD["eardrum_rupture"]:return "EARDRUM_RUPTURE"
    if spl_db > THRESHOLD["incapacitation"]: return "INCAPACITATION"
    if spl_db > THRESHOLD["pain"]:           return "PAIN"
    if spl_db > THRESHOLD["disorientation"]: return "DISORIENTATION"
    if spl_db > THRESHOLD["annoyance"]:      return "ANNOYANCE"
    return "NEGLIGIBLE"

def effect_with_earplug(spl_db: float, bone_conducted: bool = False) -> str:
    """Classify effect accounting for earplug attenuation."""
    if bone_conducted:
        effective = spl_db - BONE_COND_ATTENUATION
    else:
        effective = spl_db - EARPLUG_NRR
    return classify_effect(effective)
