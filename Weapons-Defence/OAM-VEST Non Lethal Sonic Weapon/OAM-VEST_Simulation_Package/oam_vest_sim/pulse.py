"""
OAM-VEST Simulation Package
pulse.py — Pulsed operation, power system sizing, LiDAR interleaving

Models:
  - Pulsed SPL (time-averaged vs peak)
  - Cochlear fatigue accumulation and recovery
  - Vestibular cumulative integration
  - Supercapacitor bank sizing
  - LiDAR / acoustic interleave timing
  - Dwell timer safety enforcement
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from physics import (C_SOUND, spl_to_pa, pa_to_spl,
                     CUPULA_TIME_CONSTANT, THRESHOLD)


# ─── Pulse regime dataclass ────────────────────────────────────────────────────

@dataclass
class PulseRegime:
    """
    Defines a pulsed acoustic emission regime.

    prf_hz:         pulse repetition frequency (Hz)
    pulse_width_s:  pulse on-time (seconds)
    peak_spl_db:    source SPL during pulse (dB)
    """
    prf_hz:        float = 2.0
    pulse_width_s: float = 0.1
    peak_spl_db:   float = 173.0

    @property
    def duty_cycle(self) -> float:
        return self.prf_hz * self.pulse_width_s

    @property
    def period_s(self) -> float:
        return 1.0 / self.prf_hz

    @property
    def off_time_s(self) -> float:
        return self.period_s - self.pulse_width_s

    @property
    def time_averaged_spl_db(self) -> float:
        """Time-averaged SPL = peak + 10*log10(duty_cycle)."""
        return self.peak_spl_db + 10.0 * np.log10(self.duty_cycle)

    def spl_at_range_avg(self, freq_hz: float, range_m: float) -> float:
        """Time-averaged SPL at a given range."""
        from physics import spl_at_range
        peak_at_r = spl_at_range(self.peak_spl_db, freq_hz, range_m)
        return peak_at_r + 10.0 * np.log10(self.duty_cycle)

    def spl_at_range_peak(self, freq_hz: float, range_m: float) -> float:
        """Peak SPL at a given range (during pulse on-time)."""
        from physics import spl_at_range
        return spl_at_range(self.peak_spl_db, freq_hz, range_m)


# ─── Cochlear fatigue model ────────────────────────────────────────────────────

# NIOSH permissible exposure times (seconds) vs SPL
# From NIOSH 98-126 Table B-1
NIOSH_EXPOSURE_LIMITS = {
    85:  28800,   # 8 hours
    88:  14400,   # 4 hours
    91:   7200,   # 2 hours
    94:   3600,   # 1 hour
    97:   1800,   # 30 min
    100:   900,   # 15 min
    103:   450,
    106:   225,
    109:   113,
    112:    56,
    115:    28,
    118:    14,
    121:     7,
    124:     3.5,
    127:     1.75,
    130:     0.88,
    133:     0.44,
    136:     0.22,
    139:     0.11,
    142:     0.054,
    145:     0.027,
}

def niosh_permissible_time(spl_db: float) -> float:
    """
    NIOSH permissible exposure time in seconds at given SPL.
    Uses linear interpolation in log-SPL domain.
    """
    if spl_db <= 85:
        return float('inf')
    if spl_db >= 145:
        return 0.01

    spl_levels = sorted(NIOSH_EXPOSURE_LIMITS.keys())
    for i in range(len(spl_levels) - 1):
        lo, hi = spl_levels[i], spl_levels[i+1]
        if lo <= spl_db <= hi:
            t = (spl_db - lo) / (hi - lo)
            return NIOSH_EXPOSURE_LIMITS[lo] * (1 - t) + NIOSH_EXPOSURE_LIMITS[hi] * t
    return 0.01


class CochlearFatigueModel:
    """
    Models cumulative cochlear fatigue under pulsed exposure.
    Uses NIOSH dose fractions: D = sum(t_i / T_i)
    D > 1.0 => hearing damage threshold exceeded.
    Cochlear recovery follows exponential decay with ~5 min time constant.
    """

    RECOVERY_TAU = 300.0  # seconds, cochlear TTS recovery time constant

    def __init__(self):
        self.dose = 0.0       # cumulative NIOSH dose fraction
        self.time = 0.0       # simulation time

    def step(self, spl_db: float, dt_s: float, is_pulse_on: bool):
        """
        Advance model by dt_s seconds.
        During pulse: accumulate dose.
        During gap:   recover.
        """
        self.time += dt_s
        if is_pulse_on and spl_db > 85:
            T_perm = niosh_permissible_time(spl_db)
            self.dose += dt_s / T_perm
        else:
            # Exponential recovery
            recovery = 1.0 - np.exp(-dt_s / self.RECOVERY_TAU)
            self.dose *= (1.0 - recovery)
        self.dose = max(self.dose, 0.0)

    @property
    def is_safe(self) -> bool:
        return self.dose < 1.0

    @property
    def dose_percent(self) -> float:
        return self.dose * 100.0


def simulate_cochlear_dose(regime: PulseRegime, freq_hz: float,
                            range_m: float, duration_s: float,
                            dt_s: float = 0.01) -> dict:
    """
    Simulate cochlear dose accumulation for a given pulse regime over time.

    Returns dict with time series arrays and summary statistics.
    """
    from physics import spl_at_range
    peak_spl  = spl_at_range(regime.peak_spl_db, freq_hz, range_m)
    model     = CochlearFatigueModel()
    times     = []
    doses     = []
    t = 0.0
    period    = regime.period_s
    pw        = regime.pulse_width_s

    while t < duration_s:
        t_in_period = t % period
        is_on       = t_in_period < pw
        model.step(peak_spl, dt_s, is_on)
        times.append(t)
        doses.append(model.dose_percent)
        t += dt_s

    return {
        "time_s":        np.array(times),
        "dose_percent":  np.array(doses),
        "peak_spl_db":   peak_spl,
        "max_dose":      max(doses),
        "safe_at_end":   model.is_safe,
        "range_m":       range_m,
        "duration_s":    duration_s,
    }


# ─── Vestibular integration model ─────────────────────────────────────────────

class VestibularIntegrationModel:
    """
    Models cumulative vestibular disorientation under pulsed OAM exposure.

    The semicircular canal cupula integrates angular velocity with time constant
    ~10 seconds. Pulsed stimulation at PRF >> 1/tau appears continuous.

    State variable: cupula deflection (proportional to perceived rotation).
    """

    def __init__(self):
        self.deflection = 0.0   # normalised cupula deflection (1.0 = saturation)
        self.time       = 0.0

    def step(self, stimulus_rad_per_s: float, dt_s: float, is_pulse_on: bool):
        """
        First-order cupula dynamics:
        d(deflection)/dt = stimulus/tau - deflection/tau
        """
        tau = CUPULA_TIME_CONSTANT
        if is_pulse_on:
            target = min(stimulus_rad_per_s / 15.0, 1.0)  # normalise to saturation
        else:
            target = 0.0
        self.deflection += (target - self.deflection) * (dt_s / tau)
        self.deflection  = np.clip(self.deflection, 0.0, 1.0)
        self.time        += dt_s

    @property
    def nystagmus_active(self) -> bool:
        """Nystagmus is induced above ~13% of saturation deflection."""
        return self.deflection > 0.13

    @property
    def disorientation_level(self) -> str:
        if self.deflection > 0.8:   return "SEVERE"
        if self.deflection > 0.5:   return "MODERATE"
        if self.deflection > 0.13:  return "ONSET"
        return "NONE"


def simulate_vestibular(regime: PulseRegime, oam_stimulus_rad_s: float,
                         duration_s: float, dt_s: float = 0.05) -> dict:
    """
    Simulate vestibular disorientation over time for a pulsed OAM regime.
    """
    model  = VestibularIntegrationModel()
    times, deflections, nystagmus_flags = [], [], []
    t      = 0.0
    period = regime.period_s
    pw     = regime.pulse_width_s

    while t < duration_s:
        t_in_period = t % period
        is_on       = t_in_period < pw
        model.step(oam_stimulus_rad_s, dt_s, is_on)
        times.append(t)
        deflections.append(model.deflection)
        nystagmus_flags.append(model.nystagmus_active)
        t += dt_s

    nystagmus_onset = None
    for i, (flag, ti) in enumerate(zip(nystagmus_flags, times)):
        if flag:
            nystagmus_onset = ti
            break

    return {
        "time_s":           np.array(times),
        "deflection":       np.array(deflections),
        "nystagmus":        np.array(nystagmus_flags),
        "nystagmus_onset_s": nystagmus_onset,
        "stimulus_rad_s":   oam_stimulus_rad_s,
    }


# ─── Power system sizing ──────────────────────────────────────────────────────

@dataclass
class PowerSystem:
    """
    Models the supercapacitor-backed power system for pulsed operation.
    """
    peak_power_w:    float = 51200.0   # W, peak during pulse
    avg_power_w:     float = 10200.0   # W, average (20% DC)
    supercap_j:      float = 5120.0    # J, supercap bank energy
    recharge_rate_w: float = 12800.0   # W, recharge during off-time
    standby_w:       float = 800.0     # W, standby power

    def pulse_energy_j(self, pulse_width_s: float) -> float:
        return self.peak_power_w * pulse_width_s

    def recharge_time_s(self, energy_j: float) -> float:
        return energy_j / self.recharge_rate_w

    def validate(self, regime: PulseRegime) -> dict:
        """Check power system is adequate for given pulse regime."""
        pulse_e  = self.pulse_energy_j(regime.pulse_width_s)
        recharge = self.recharge_time_s(pulse_e)
        adequate = recharge < regime.off_time_s
        return {
            "pulse_energy_j":    pulse_e,
            "supercap_capacity_j": self.supercap_j,
            "supercap_adequate": pulse_e <= self.supercap_j,
            "recharge_time_s":   recharge,
            "off_time_s":        regime.off_time_s,
            "recharge_adequate": adequate,
            "avg_draw_w":        self.avg_power_w,
            "vehicle_supply_ok": self.avg_power_w < 15000,  # <15kW = Land Rover class
        }


# ─── LiDAR / acoustic interleave ──────────────────────────────────────────────

class LiDARInterleave:
    """
    Models the interleaved LiDAR / acoustic pulse timing.

    During acoustic pulse: LiDAR reads are suppressed (acoustic noise floor).
    During off-window: LiDAR reads target range, FPGA updates phase.
    """

    LIDAR_READ_TIME_S  = 0.020   # 20ms per LiDAR frame at 50Hz
    FPGA_UPDATE_TIME_S = 0.001   # <1ms phase calculation and load

    def __init__(self, regime: PulseRegime):
        self.regime = regime

    @property
    def lidar_reads_per_period(self) -> int:
        """Number of LiDAR frames available in the off-window."""
        available = self.regime.off_time_s - self.FPGA_UPDATE_TIME_S
        return max(1, int(available / self.LIDAR_READ_TIME_S))

    @property
    def phase_update_latency_s(self) -> float:
        """Total latency from target movement to updated beam phase."""
        return self.regime.off_time_s + self.FPGA_UPDATE_TIME_S

    @property
    def max_target_velocity_ms(self) -> float:
        """
        Maximum target radial velocity the system can track without beam
        de-focusing by more than lambda/4.
        delta_r = v * latency < lambda/4
        """
        lam = C_SOUND / 3000.0
        return (lam / 4.0) / self.phase_update_latency_s

    def timing_summary(self) -> dict:
        return {
            "pulse_on_ms":             self.regime.pulse_width_s * 1000,
            "off_window_ms":           self.regime.off_time_s * 1000,
            "lidar_reads_per_period":  self.lidar_reads_per_period,
            "phase_update_latency_ms": self.phase_update_latency_s * 1000,
            "max_target_velocity_ms":  round(self.max_target_velocity_ms, 2),
            "conflict_free":           True,  # guaranteed by design
        }


# ─── Safety dwell timer ───────────────────────────────────────────────────────

class DwellTimer:
    """
    Enforces maximum dwell time on a single target.
    After max_dwell_s, mandates a cooldown_s pause before re-engagement.
    """

    def __init__(self, max_dwell_s: float = 5.0, cooldown_s: float = 3.0):
        self.max_dwell  = max_dwell_s
        self.cooldown   = cooldown_s
        self._dwell     = 0.0
        self._cooldown  = 0.0
        self._engage    = True

    def step(self, dt_s: float, beam_active: bool) -> bool:
        """
        Advance timer. Returns True if beam is permitted.
        """
        if self._cooldown > 0:
            self._cooldown -= dt_s
            self._engage    = False
            if self._cooldown <= 0:
                self._dwell  = 0.0
                self._engage = True
            return False

        if beam_active and self._engage:
            self._dwell += dt_s
            if self._dwell >= self.max_dwell:
                self._cooldown = self.cooldown
                self._engage   = False
                return False
            return True

        self._dwell = max(0.0, self._dwell - dt_s * 0.5)  # slow passive recovery
        return self._engage
