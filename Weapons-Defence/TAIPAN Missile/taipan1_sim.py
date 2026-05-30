#!/usr/bin/env python3
"""
TAIPAN-1 Rocket Simulation Suite
==================================
Complete simulation toolkit for the TAIPAN-1 guided ballistic interceptor.

Modules:
    AtmosphereModel   — US Standard Atmosphere 1976
    EngineModel       — RP-1/LOX electric pump-fed engine
    AeroModel         — Barrowman CP + semi-empirical drag
    MassModel         — CG, stability margin, ballast
    FlightSim         — 3-DOF point-mass trajectory
    BayesOptimiser    — GP surrogate + Expected Improvement
    Analyses          — Ballast sweep, thrust profiles, launch angle sweep,
                        engine sensitivity, full verification

Usage:
    python taipan1_sim.py --help
    python taipan1_sim.py --sim all
    python taipan1_sim.py --sim trajectory
    python taipan1_sim.py --sim ballast
    python taipan1_sim.py --sim engine
    python taipan1_sim.py --sim optimise
    python taipan1_sim.py --sim thrust_profiles
    python taipan1_sim.py --sim verify
    python taipan1_sim.py --sim launch_angle
    python taipan1_sim.py --ballast 50 --angle 70.4
"""

import argparse
import sys
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from dataclasses import dataclass, field
from typing import Tuple, List, Optional, Dict
from scipy.stats import norm, qmc

warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
G0          = 9.80665        # Standard gravity [m/s²]
R_AIR       = 287.05         # Specific gas constant air [J/(kg·K)]
GAMMA_AIR   = 1.4            # Ratio of specific heats, air
R_UNIV      = 8.314          # Universal gas constant [J/(mol·K)]

# RP-1/LOX thermochemical (NASA CEA, O/F=2.56)
GAMMA_GAS   = 1.235
MW_GAS      = 23.3e-3        # [kg/mol]
R_GAS       = R_UNIV / MW_GAS
T_CHAMBER   = 3670.0         # Adiabatic flame temp [K]
C_STAR_IDEAL = 1774.0        # Theoretical c* [m/s]
RHO_RP1     = 810.0          # [kg/m³]
RHO_LOX     = 1141.0         # [kg/m³]


# ══════════════════════════════════════════════════════════════════════════════
# US STANDARD ATMOSPHERE 1976
# ══════════════════════════════════════════════════════════════════════════════
class AtmosphereModel:
    """US Standard Atmosphere 1976. Valid 0–86 km."""

    @staticmethod
    def state(alt_m: float) -> Tuple[float, float, float, float]:
        """
        Returns (pressure Pa, density kg/m³, temperature K, speed_of_sound m/s).
        alt_m: geometric altitude in metres.
        """
        h = max(0.0, float(alt_m))
        if h <= 11_000:
            T = 288.15 - 0.0065 * h
            p = 101325 * (T / 288.15) ** 5.2561
        elif h <= 20_000:
            T = 216.65
            p = 22632.1 * np.exp(-0.0001577 * (h - 11_000))
        elif h <= 32_000:
            T = 216.65 + 0.001 * (h - 20_000)
            p = 5474.89 * (T / 216.65) ** -34.1632
        elif h <= 47_000:
            T = 228.65 + 0.0028 * (h - 32_000)
            p = 868.019 * (T / 228.65) ** -12.2009
        else:
            T = 270.65
            p = max(110.906 * np.exp(-0.0001578 * (h - 47_000)), 0.01)
        rho = p / (R_AIR * T)
        a   = np.sqrt(GAMMA_AIR * R_AIR * T)
        return p, rho, T, a

    @staticmethod
    def pressure(alt_m: float) -> float:
        return AtmosphereModel.state(alt_m)[0]

    @staticmethod
    def density(alt_m: float) -> float:
        return AtmosphereModel.state(alt_m)[1]


# ══════════════════════════════════════════════════════════════════════════════
# ENGINE MODEL
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class EngineConfig:
    """Engine design parameters."""
    thrust_vac_N:      float = 50_000.0
    burn_time_s:       float = 30.0
    of_ratio:          float = 2.56
    p_chamber_pa:      float = 5e6
    expansion_ratio:   float = 10.0
    nozzle_angle_deg:  float = 15.0
    c_star_eff:        float = 0.96
    cf_efficiency:     float = 0.98


@dataclass
class EngineResults:
    """Computed engine performance."""
    c_star:         float = 0.0
    isp_vac:        float = 0.0
    isp_sl:         float = 0.0
    cf_vac:         float = 0.0
    cf_sl:          float = 0.0
    mach_exit:      float = 0.0
    p_exit_pa:      float = 0.0
    v_exit:         float = 0.0
    t_throat:       float = 0.0
    t_exit:         float = 0.0
    a_throat_m2:    float = 0.0
    a_exit_m2:      float = 0.0
    d_throat_mm:    float = 0.0
    d_exit_mm:      float = 0.0
    nozzle_len_mm:  float = 0.0
    mdot_total:     float = 0.0
    mdot_fuel:      float = 0.0
    mdot_ox:        float = 0.0
    m_prop:         float = 0.0
    m_fuel:         float = 0.0
    m_ox:           float = 0.0
    vol_fuel_l:     float = 0.0
    vol_ox_l:       float = 0.0
    m_engine_dry:   float = 0.0


def _mach_from_eps(eps: float, g: float) -> float:
    """Supersonic Mach from area ratio via Newton-Raphson."""
    exp = (g + 1) / (2 * (g - 1))
    def f(M):
        t = 1 + (g - 1) / 2 * M ** 2
        return (1 / M) * (2 / (g + 1) * t) ** exp - eps
    def df(M):
        t = 1 + (g - 1) / 2 * M ** 2
        base = 2 / (g + 1) * t
        return (-1 / M ** 2 * base ** exp
                + 1 / M * exp * base ** (exp - 1) * (2 / (g + 1)) * (g - 1) * M)
    M = 2.5
    for _ in range(150):
        dM = -f(M) / df(M)
        M += dM
        if abs(dM) < 1e-10:
            break
    return M


def _cf(g, pc, pe, pa, eps, eta):
    """Thrust coefficient (ideal × efficiency)."""
    mom = np.sqrt(2 * g ** 2 / (g - 1)
                  * (2 / (g + 1)) ** ((g + 1) / (g - 1))
                  * (1 - (pe / pc) ** ((g - 1) / g)))
    return (mom + (pe - pa) / pc * eps) * eta


class EngineModel:
    """
    RP-1/LOX electric pump-fed engine.

    Computes thermochemical performance from first principles using
    isentropic nozzle flow relations and NASA CEA-derived gas properties.
    """

    def __init__(self, cfg: EngineConfig = None):
        self.cfg = cfg or EngineConfig()
        self._results: Optional[EngineResults] = None
        self._atm = AtmosphereModel()

    def build(self) -> EngineResults:
        """Compute all engine performance parameters."""
        cfg = self.cfg
        g   = GAMMA_GAS
        res = EngineResults()

        res.c_star     = C_STAR_IDEAL * cfg.c_star_eff
        res.mach_exit  = _mach_from_eps(cfg.expansion_ratio, g)
        res.t_throat   = T_CHAMBER * (2 / (g + 1))
        res.t_exit     = T_CHAMBER / (1 + (g - 1) / 2 * res.mach_exit ** 2)
        res.p_exit_pa  = cfg.p_chamber_pa * (
            1 + (g - 1) / 2 * res.mach_exit ** 2) ** (-g / (g - 1))
        res.v_exit     = res.mach_exit * np.sqrt(g * R_GAS * res.t_exit)

        res.cf_vac     = _cf(g, cfg.p_chamber_pa, res.p_exit_pa,
                             0.0, cfg.expansion_ratio, cfg.cf_efficiency)
        res.cf_sl      = _cf(g, cfg.p_chamber_pa, res.p_exit_pa,
                             101325.0, cfg.expansion_ratio, cfg.cf_efficiency)
        res.isp_vac    = res.cf_vac * res.c_star / G0
        res.isp_sl     = res.cf_sl  * res.c_star / G0

        # Geometry
        res.a_throat_m2 = cfg.thrust_vac_N / (res.cf_vac * cfg.p_chamber_pa)
        res.a_exit_m2   = res.a_throat_m2 * cfg.expansion_ratio
        res.d_throat_mm = np.sqrt(4 * res.a_throat_m2 / np.pi) * 1000
        res.d_exit_mm   = np.sqrt(4 * res.a_exit_m2   / np.pi) * 1000
        half_ang         = np.radians(cfg.nozzle_angle_deg)
        res.nozzle_len_mm = (res.d_exit_mm / 2 - res.d_throat_mm / 2) / np.tan(half_ang)

        # Propellant
        res.mdot_total  = cfg.thrust_vac_N / (res.isp_vac * G0)
        res.mdot_fuel   = res.mdot_total / (1 + cfg.of_ratio)
        res.mdot_ox     = res.mdot_total - res.mdot_fuel
        res.m_fuel      = res.mdot_fuel * cfg.burn_time_s
        res.m_ox        = res.mdot_ox   * cfg.burn_time_s
        res.m_prop      = res.m_fuel + res.m_ox
        res.vol_fuel_l  = res.m_fuel / RHO_RP1 * 1000
        res.vol_ox_l    = res.m_ox   / RHO_LOX  * 1000
        res.m_engine_dry = 0.00124 * cfg.thrust_vac_N  # 1.24 kg/kN

        self._results = res
        return res

    def thrust_at_altitude(self, alt_m: float) -> float:
        """Altitude-corrected thrust [N]."""
        if self._results is None:
            self.build()
        pa = self._atm.pressure(alt_m)
        return (self._results.cf_vac * self.cfg.p_chamber_pa
                * self._results.a_throat_m2
                - pa * self._results.a_exit_m2)

    def print_summary(self):
        r = self._results or self.build()
        print(f"\n{'═'*52}")
        print(f"  ENGINE PERFORMANCE SUMMARY")
        print(f"{'═'*52}")
        print(f"  Cycle              : Electric pump-fed, RP-1/LOX")
        print(f"  Thrust (vacuum)    : {self.cfg.thrust_vac_N/1e3:.1f} kN")
        print(f"  Thrust (SL)        : {r.cf_sl*self.cfg.p_chamber_pa*r.a_throat_m2/1e3:.1f} kN")
        print(f"  Isp (vacuum)       : {r.isp_vac:.1f} s")
        print(f"  Isp (sea level)    : {r.isp_sl:.1f} s")
        print(f"  c*                 : {r.c_star:.0f} m/s")
        print(f"  Chamber pressure   : {self.cfg.p_chamber_pa/1e5:.0f} bar")
        print(f"  Expansion ratio    : {self.cfg.expansion_ratio:.0f}")
        print(f"  Exit Mach          : {r.mach_exit:.2f}")
        print(f"  Throat diameter    : {r.d_throat_mm:.1f} mm")
        print(f"  Exit diameter      : {r.d_exit_mm:.1f} mm")
        print(f"  Nozzle length      : {r.nozzle_len_mm:.0f} mm")
        print(f"  Mass flow          : {r.mdot_total:.3f} kg/s")
        print(f"  Burn time          : {self.cfg.burn_time_s:.1f} s")
        print(f"  RP-1 mass          : {r.m_fuel:.1f} kg  ({r.vol_fuel_l:.0f} L)")
        print(f"  LOX mass           : {r.m_ox:.1f} kg  ({r.vol_ox_l:.0f} L)")
        print(f"  Propellant total   : {r.m_prop:.1f} kg")
        print(f"  Engine dry mass    : {r.m_engine_dry:.1f} kg")
        print(f"{'═'*52}")


# ══════════════════════════════════════════════════════════════════════════════
# AERODYNAMICS MODEL
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class VehicleGeometry:
    """
    Parametric rocket geometry.
    All linear dimensions in metres.
    """
    d_body:        float = 0.275
    l_body:        float = 3.85
    nose_length:   float = 0.920
    nose_shape:    float = 1.0    # 0=conical, 1=ogive, 2=Von Karman
    n_fins:        int   = 4
    fin_span:      float = 0.229
    fin_root:      float = 0.283
    fin_tip:       float = 0.164
    fin_sweep:     float = 37.9
    fin_thickness: float = 0.005
    fin_pos:       float = None
    bt_length:     float = 0.10

    def __post_init__(self):
        if self.fin_pos is None:
            self.fin_pos = self.nose_length + self.l_body - self.fin_root

    @property
    def d_ref(self):   return self.d_body
    @property
    def A_ref(self):   return np.pi * (self.d_body / 2) ** 2
    @property
    def l_total(self): return self.nose_length + self.l_body + self.bt_length

    @classmethod
    def from_calibers(cls, d_body, nose_cal, nose_shape,
                      body_cal, fin_span_cal, fin_root_cal,
                      fin_taper, fin_sweep_deg, n_fins=4):
        D = d_body
        return cls(d_body=D, l_body=body_cal * D,
                   nose_length=nose_cal * D, nose_shape=nose_shape,
                   n_fins=n_fins, fin_span=fin_span_cal * D,
                   fin_root=fin_root_cal * D,
                   fin_tip=fin_taper * fin_root_cal * D,
                   fin_sweep=fin_sweep_deg)


class AeroModel:
    """
    Barrowman Centre of Pressure + semi-empirical drag model.

    Drag components:
        CD_nose     — wave + pressure drag (nose cone)
        CD_friction — turbulent flat-plate skin friction (Schlichting)
        CD_base     — base drag
        CD_fins     — fin leading/trailing edge bluntness
    """

    def __init__(self, geo: VehicleGeometry):
        self.g = geo
        self._atm = AtmosphereModel()

    # ── Barrowman CP ──────────────────────────────────────────────────────────
    def _nose_cp(self) -> Tuple[float, float]:
        s = self.g.nose_shape
        frac = (0.666 * (1 - s) + 0.466 * s) if s <= 1 else (0.466 * (2 - s) + 0.437 * (s - 1))
        return 2.0, self.g.nose_length * frac

    def _fin_cp(self) -> Tuple[float, float]:
        g   = self.g
        s, cr, ct = g.fin_span, g.fin_root, g.fin_tip
        r   = g.d_body / 2
        tan_mc = np.tan(np.radians(g.fin_sweep)) - (cr - ct) / (2 * s)
        cna = (4 * g.n_fins * (s / g.d_body) ** 2
               / (1 + np.sqrt(1 + (2 * s / (cr + ct)) ** 2)))
        cna *= 1 + r / (s + r)
        mac  = 2 / 3 * (cr + ct - cr * ct / (cr + ct))
        xcp  = g.fin_pos + (cr - mac) / 2 + mac * tan_mc / 2 + mac / 4
        return cna, xcp

    def cp_location(self) -> float:
        """Centre of pressure location [m from nose tip] — Barrowman."""
        cna_n, xcp_n = self._nose_cp()
        cna_f, xcp_f = self._fin_cp()
        return (cna_n * xcp_n + cna_f * xcp_f) / (cna_n + cna_f)

    # ── Drag model ────────────────────────────────────────────────────────────
    def _cd_nose(self, M: float) -> float:
        FR   = self.g.nose_length / self.g.d_body
        half = np.degrees(np.arctan(self.g.d_body / 2 / self.g.nose_length))
        base = 0.8 * np.sin(np.radians(half)) ** 2
        if M < 0.8:   return base
        elif M < 1.2: return base + (M - 0.8) / 0.4 * (0.083 / FR)
        else:         return 0.083 / FR * (M - 1) ** (-0.25) * 1.1

    def _cd_friction(self, M: float, alt_m: float) -> float:
        _, rho, T, a = self._atm.state(alt_m)
        v  = max(M * a, 1.0)
        mu = 1.716e-5 * (T / 273.15) ** 1.5 * (273.15 + 110.4) / (T + 110.4)
        g  = self.g
        Aw = (np.pi * g.d_body * (g.nose_length * 1.1 + g.l_body)
              + g.n_fins * (g.fin_root + g.fin_tip) / 2 * g.fin_span * 2)
        Re = max(rho * v * g.l_total / mu, 1e4)
        cf = 0.455 / np.log10(Re) ** 2.58
        if M > 0.3:
            cf /= (1 + 0.12 * M ** 2) ** 0.5
        return cf * Aw / g.A_ref

    def _cd_base(self, M: float) -> float:
        return 0.12 + 0.13 * M ** 2 if M < 1.0 else 0.25 / M

    def _cd_fins(self, M: float) -> float:
        g  = self.g
        Af = g.n_fins * g.fin_thickness * g.fin_root
        return (1.0 if M < 1.0 else 0.6 / M) * Af / g.A_ref

    def cd(self, M: float, alt_m: float = 0.0) -> float:
        """Total drag coefficient at given Mach and altitude."""
        M = max(M, 0.01)
        return (self._cd_nose(M) + self._cd_friction(M, alt_m)
                + self._cd_base(M) + self._cd_fins(M))

    def cd_curve(self, mach_range: np.ndarray = None,
                 alt_m: float = 5000.0) -> Tuple[np.ndarray, np.ndarray]:
        """Return (mach_array, cd_array) for plotting."""
        if mach_range is None:
            mach_range = np.linspace(0.1, 15.0, 300)
        cds = np.array([self.cd(m, alt_m) for m in mach_range])
        return mach_range, cds


# ══════════════════════════════════════════════════════════════════════════════
# MASS MODEL
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class MassModel:
    """
    Mass budget and centre-of-gravity model.

    CG locations are expressed as fractions of total vehicle length,
    based on the TAIPAN-1 configuration (engine aft, tanks forward-of-engine).
    """
    m_structure:   float = 30.0    # kg — airframe + tanks
    m_engine:      float = 62.0    # kg — engine dry
    m_avionics:    float = 3.0     # kg — IMU + GPS + FTS
    m_propellant:  float = 521.8   # kg — total RP-1 + LOX
    m_ballast:     float = 14.0    # kg — nose tungsten ballast
    ballast_pos_m: float = 0.05    # m from nose tip

    # CG fractions along vehicle (as fraction of l_total)
    cg_struct_frac: float = 0.42
    cg_eng_frac:    float = 0.92
    cg_avi_frac:    float = 0.48
    cg_prop_frac:   float = 0.40

    @property
    def m_dry(self) -> float:
        return self.m_structure + self.m_engine + self.m_avionics + self.m_ballast

    @property
    def m_wet(self) -> float:
        return self.m_dry + self.m_propellant

    def cg(self, geo: VehicleGeometry, with_prop: bool = True) -> float:
        """Centre of gravity [m from nose tip]."""
        L  = geo.l_total
        mp = self.m_propellant if with_prop else 0.0
        mt = self.m_dry + mp
        mm = (self.m_structure  * L * self.cg_struct_frac
            + self.m_engine     * L * self.cg_eng_frac
            + self.m_avionics   * L * self.cg_avi_frac
            + self.m_ballast    * self.ballast_pos_m
            + mp                * L * self.cg_prop_frac)
        return mm / mt if mt > 0 else L * 0.5

    def stability_margin(self, geo: VehicleGeometry,
                         aero: AeroModel,
                         with_prop: bool = True) -> float:
        """Stability margin [calibers]. Positive = stable."""
        xcp = aero.cp_location()
        xcg = self.cg(geo, with_prop)
        return (xcp - xcg) / geo.d_body

    def stability_vs_propellant(self, geo: VehicleGeometry,
                                aero: AeroModel,
                                n_pts: int = 50) -> Tuple[np.ndarray, np.ndarray]:
        """Stability margin as a function of propellant fraction remaining."""
        fracs = np.linspace(0, 1, n_pts)
        sms   = []
        for f in fracs:
            mm_copy = MassModel(
                m_structure=self.m_structure, m_engine=self.m_engine,
                m_avionics=self.m_avionics,
                m_propellant=self.m_propellant * f,
                m_ballast=self.m_ballast, ballast_pos_m=self.ballast_pos_m)
            sms.append(mm_copy.stability_margin(geo, aero, with_prop=(f > 0)))
        return fracs * 100, np.array(sms)

    def print_summary(self, geo: VehicleGeometry, aero: AeroModel):
        xcp = aero.cp_location()
        xcg_l = self.cg(geo, True)
        xcg_b = self.cg(geo, False)
        mr    = self.m_wet / self.m_dry
        dv    = 293.1 * G0 * np.log(mr)
        print(f"\n{'═'*52}")
        print(f"  MASS AND STABILITY SUMMARY")
        print(f"{'═'*52}")
        print(f"  Structure          : {self.m_structure:.1f} kg")
        print(f"  Engine (dry)       : {self.m_engine:.1f} kg")
        print(f"  Avionics           : {self.m_avionics:.1f} kg")
        print(f"  Ballast            : {self.m_ballast:.1f} kg @ {self.ballast_pos_m*1e3:.0f}mm")
        print(f"  Propellant         : {self.m_propellant:.1f} kg")
        print(f"  Dry mass           : {self.m_dry:.1f} kg")
        print(f"  Wet mass           : {self.m_wet:.1f} kg")
        print(f"  Mass ratio         : {mr:.3f}")
        print(f"  Ideal Δv           : {dv:.0f} m/s")
        print(f"  CP location        : {xcp:.3f} m")
        print(f"  CG launch          : {xcg_l:.3f} m  (SM={self.stability_margin(geo,aero,True):.2f} cal)")
        print(f"  CG burnout         : {xcg_b:.3f} m  (SM={self.stability_margin(geo,aero,False):.2f} cal)")
        print(f"{'═'*52}")

# ══════════════════════════════════════════════════════════════════════════════
# 3-DOF FLIGHT SIMULATION
# ══════════════════════════════════════════════════════════════════════════════
class FlightSim:
    """
    3-DOF point-mass trajectory simulation in a vertical plane.

    State vector: [h (altitude), x (downrange), v (speed), θ (flight path angle)]

    Forces:
        Thrust  — altitude-corrected, engine on for burn_time seconds
        Drag    — ½ρv²CD·Aref, Mach and altitude dependent
        Gravity — constant G0 (adequate below 500 km)

    Integration: explicit Euler (dt=0.05s default, stable for this problem)
    """

    def __init__(self, geo: VehicleGeometry, aero: AeroModel,
                 mass: MassModel, engine_cfg: EngineConfig,
                 engine: EngineResults,
                 launch_angle_deg: float = 70.4,
                 dt: float = 0.05):
        self.geo   = geo
        self.aero  = aero
        self.mass  = mass
        self.ecfg  = engine_cfg
        self.eng   = engine
        self.angle = launch_angle_deg
        self.dt    = dt
        self._atm  = AtmosphereModel()

    def _thrust(self, t: float, alt_m: float) -> float:
        """Altitude-corrected thrust [N], zero after burnout."""
        if t > self.ecfg.burn_time_s:
            return 0.0
        pa = self._atm.pressure(alt_m)
        return (self.eng.cf_vac * self.ecfg.p_chamber_pa * self.eng.a_throat_m2
                - pa * self.eng.a_exit_m2)

    def run(self) -> Dict:
        """
        Integrate trajectory until ground impact or t=800s.
        Returns dict of time-series arrays and scalar performance metrics.
        """
        dt   = self.dt
        mdot = self.eng.mdot_total
        m    = self.mass.m_wet
        m_dry = self.mass.m_dry

        t, h, x, v = 0.0, 0.1, 0.0, 1.0
        theta = np.radians(self.angle)
        mp_left = self.mass.m_propellant

        # Pre-allocate (generous upper bound)
        n_max = int(800 / dt) + 1000
        ts   = np.empty(n_max); hs   = np.empty(n_max)
        xs   = np.empty(n_max); vs   = np.empty(n_max)
        Ms   = np.empty(n_max); cds  = np.empty(n_max)
        thrs = np.empty(n_max); gls  = np.empty(n_max)
        idx  = 0

        max_h = 0.0; max_x = 0.0; max_M = 0.0; peak_g = 0.0; max_q = 0.0

        while idx < n_max:
            pa, rho, _, a_s = self._atm.state(h)
            Mn   = v / max(a_s, 1.0)
            q    = 0.5 * rho * v ** 2
            drag = q * self.aero.cd(Mn, h) * self.geo.A_ref
            F    = self._thrust(t, h)

            if mp_left > 0 and t <= self.ecfg.burn_time_s:
                dm = min(mdot * dt, mp_left)
                mp_left -= dm
                m       -= dm
            else:
                F = 0.0

            a_net = (F - drag) / m
            vx    = v * np.cos(theta); vy = v * np.sin(theta)
            vx   += a_net * np.cos(theta) * dt
            vy   += (a_net * np.sin(theta) - G0) * dt
            v     = np.sqrt(vx ** 2 + vy ** 2)
            if v > 0.1:
                theta = np.arctan2(vy, vx)

            h += vy * dt; x += vx * dt; t += dt
            gl = abs(a_net) / G0 + 1.0

            ts[idx]=t; hs[idx]=h; xs[idx]=x; vs[idx]=v
            Ms[idx]=Mn; cds[idx]=self.aero.cd(Mn,h)
            thrs[idx]=F; gls[idx]=gl; idx+=1

            if h > max_h: max_h = h
            if x > max_x: max_x = x
            if Mn > max_M: max_M = Mn
            if gl > peak_g: peak_g = gl
            if q > max_q: max_q = q

            if h < 0 and t > 5.0:
                break
            if t > 800.0:
                break

        n = idx
        return dict(
            t=ts[:n], h=hs[:n]/1e3, x=xs[:n]/1e3,
            v=vs[:n], mach=Ms[:n], cd=cds[:n],
            thrust=thrs[:n], gload=gls[:n],
            apogee_km  = max_h / 1e3,
            range_km   = max_x / 1e3,
            max_mach   = max_M,
            peak_g     = peak_g,
            max_q_kpa  = max_q / 1e3,
            burnout_v  = vs[min(int(self.ecfg.burn_time_s/dt), n-1)],
            burnout_h  = hs[min(int(self.ecfg.burn_time_s/dt), n-1)] / 1e3,
            t_above_100 = np.sum(hs[:n] > 100e3) * dt,
            flight_time = ts[n-1],
        )

    def print_summary(self, R: Dict):
        print(f"\n{'═'*52}")
        print(f"  TRAJECTORY SUMMARY  (launch {self.angle:.1f}°)")
        print(f"{'═'*52}")
        print(f"  Apogee             : {R['apogee_km']:.1f} km")
        print(f"  Max range          : {R['range_km']:.1f} km")
        print(f"  Max Mach           : {R['max_mach']:.2f}")
        print(f"  Burnout velocity   : {R['burnout_v']:.0f} m/s")
        print(f"  Burnout altitude   : {R['burnout_h']:.1f} km")
        print(f"  Peak dynamic pres  : {R['max_q_kpa']:.1f} kPa")
        print(f"  Peak G-load        : {R['peak_g']:.1f} g")
        print(f"  Time above 100 km  : {R['t_above_100']:.0f} s")
        print(f"  Total flight time  : {R['flight_time']:.0f} s")
        print(f"{'═'*52}")


# ══════════════════════════════════════════════════════════════════════════════
# GAUSSIAN PROCESS BAYESIAN OPTIMISER
# ══════════════════════════════════════════════════════════════════════════════
class GaussianProcess:
    """
    Squared-exponential GP for Bayesian optimisation.
    Input space normalised to [0,1]^D.
    """

    def __init__(self, noise: float = 1e-3, length_scale: float = 0.3):
        self.noise = noise
        self.ls    = length_scale
        self.sf    = 1.0
        self.X     = None
        self.yn    = None
        self.Ki    = None
        self.ym    = 0.0
        self.ys    = 1.0

    def _K(self, X1: np.ndarray, X2: np.ndarray) -> np.ndarray:
        X1n = X1 / self.ls; X2n = X2 / self.ls
        d2  = np.sum((X1n[:, None, :] - X2n[None, :, :]) ** 2, axis=-1)
        return self.sf ** 2 * np.exp(-0.5 * d2)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.X  = X.copy()
        self.ym = y.mean(); self.ys = max(y.std(), 1e-8)
        self.yn = (y - self.ym) / self.ys
        K = self._K(X, X) + np.eye(len(X)) * (self.noise + 1e-6)
        self.Ki = np.linalg.inv(K)

    def predict(self, Xs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        Ks  = self._K(Xs, self.X)
        Kss = self._K(Xs, Xs)
        mu  = Ks @ self.Ki @ self.yn
        var = np.maximum(np.diag(Kss - Ks @ self.Ki @ Ks.T), 1e-10)
        return mu * self.ys + self.ym, np.sqrt(var) * self.ys

    @staticmethod
    def expected_improvement(mu: np.ndarray, std: np.ndarray,
                             y_best: float, xi: float = 0.01) -> np.ndarray:
        Z = (mu - y_best - xi) / (std + 1e-9)
        return (mu - y_best - xi) * norm.cdf(Z) + std * norm.pdf(Z)


# ── Design space for aerodynamic optimisation ─────────────────────────────────
OPT_BOUNDS = np.array([
    [2.0,  5.0],   # nose_cal
    [0.0,  2.0],   # nose_shape
    [0.8,  2.5],   # fin_span_cal
    [1.0,  2.5],   # fin_root_cal
    [0.2,  0.8],   # fin_taper
    [15.,  55.],   # fin_sweep_deg
    [0.0,  0.15],  # ballast_frac
    [0.5,  2.5],   # ballast_pos_cal
    [60.,  88.],   # launch_angle_deg
])
OPT_NAMES = ['nose_cal','nose_shape','fin_span_cal','fin_root_cal',
             'fin_taper','fin_sweep','ballast_frac','ballast_pos_cal',
             'launch_deg']
STAB_MIN  = 1.5


def _norm(X, B):    return (X - B[:,0]) / (B[:,1] - B[:,0])
def _denorm(Xn, B): return Xn * (B[:,1] - B[:,0]) + B[:,0]


def _vec_to_vehicle(x: np.ndarray, eng: EngineResults,
                    m_engine_dry: float) -> Tuple:
    (nc, ns, fsc, frc, ft, fsw, bf, bpc, la) = x
    D   = np.sqrt(4 * eng.a_exit_m2 / np.pi)
    geo = VehicleGeometry.from_calibers(D, nc, ns, 14.0,
                                         fsc, frc, ft, fsw)
    aero = AeroModel(geo)
    ms   = max(4.0 * np.pi * D * (geo.nose_length + geo.l_body), 20.0)
    mm   = MassModel(
        m_structure=ms, m_engine=m_engine_dry,
        m_propellant=eng.m_prop, m_avionics=3.0,
        m_ballast=bf * (ms + m_engine_dry),
        ballast_pos_m=bpc * D)
    return geo, aero, mm, la


def _evaluate(x: np.ndarray, ecfg: EngineConfig,
              eng: EngineResults) -> Dict:
    geo, aero, mm, la = _vec_to_vehicle(x, eng, ecfg.thrust_vac_N * 0.00124)
    sm = mm.stability_margin(geo, aero, True)
    sim = FlightSim(geo, aero, mm, ecfg, eng, launch_angle_deg=la, dt=0.1)
    R   = sim.run()
    penalty  = max(0.0, STAB_MIN - sm) * 80.0
    fitness  = R['apogee_km'] - penalty
    return dict(fitness=fitness, sm=sm, sm_bo=mm.stability_margin(geo,aero,False),
                traj=R, geo=geo, aero=aero, mass=mm, x=x, la=la)


class BayesOptimiser:
    """
    Adaptive Bayesian optimisation over rocket design space.
    Maximises apogee subject to burnout stability margin ≥ 1.5 cal.
    """

    def __init__(self, n_init: int = 20, n_iter: int = 40,
                 n_candidates: int = 2000):
        self.n_init  = n_init
        self.n_iter  = n_iter
        self.n_cand  = n_candidates
        self.history: List[Dict] = []

    def run(self, ecfg: EngineConfig, eng: EngineResults) -> Tuple[Dict, np.ndarray]:
        print(f"\n{'═'*58}")
        print(f"  BAYESIAN OPTIMISER — {self.n_init} LHS + {self.n_iter} adaptive")
        print(f"{'═'*58}")

        # Phase 1 — Latin Hypercube
        sampler = qmc.LatinHypercube(d=len(OPT_BOUNDS), seed=42)
        Xn_all  = sampler.random(self.n_init)
        X_all   = _denorm(Xn_all, OPT_BOUNDS)
        y_all   = []

        print(f"\n[Phase 1] LHS initialisation ({self.n_init} samples)...")
        for i, x in enumerate(X_all):
            r = _evaluate(x, ecfg, eng)
            y_all.append(r['fitness'])
            self.history.append(r)
            if (i + 1) % 5 == 0:
                print(f"  [{i+1:3d}] best={max(y_all):.1f} km")

        y_all = np.array(y_all)
        gp    = GaussianProcess(noise=1e-3)

        # Phase 2 — GP guided
        print(f"\n[Phase 2] GP-guided search ({self.n_iter} iterations)...")
        for i in range(self.n_iter):
            gp.fit(_norm(X_all, OPT_BOUNDS), y_all)
            rng_  = np.random.default_rng(i + 1000)
            Xc_n  = rng_.uniform(0, 1, (self.n_cand, len(OPT_BOUNDS)))
            mu, s = gp.predict(Xc_n)
            ei    = GaussianProcess.expected_improvement(mu, s, y_all.max())
            x_new = _denorm(Xc_n[np.argmax(ei)], OPT_BOUNDS)
            r     = _evaluate(x_new, ecfg, eng)
            y_new = r['fitness']
            X_all = np.vstack([X_all, x_new])
            y_all = np.append(y_all, y_new)
            self.history.append(r)
            if y_new >= y_all[:-1].max():
                print(f"  [{i+1:3d}] ★ {y_new:.1f} km | "
                      f"SM={r['sm']:.2f} | Mach={r['traj']['max_mach']:.2f}")
            elif (i + 1) % 10 == 0:
                print(f"  [{i+1:3d}] best={y_all.max():.1f} km")

        best = self.history[int(np.argmax(y_all))]
        print(f"\n  Best apogee: {best['traj']['apogee_km']:.1f} km | "
              f"Range: {best['traj']['range_km']:.1f} km | "
              f"SM: {best['sm']:.2f} cal")
        print(f"{'═'*58}")
        return best, y_all

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

DARK = '#080808'; A='#00e5ff'; B='#ff6b35'; C='#a0ff60'
D='#ffd060'; E='#e080ff'; W='white'; R='#ff4466'

def _mkfig(rows, cols, figsize):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor(DARK)
    return fig

def _axstyle(ax):
    ax.set_facecolor('#111')
    for sp in ax.spines.values():
        sp.set_edgecolor('#2a2a2a')
    ax.grid(alpha=0.12)
    return ax


def default_vehicle() -> Tuple:
    """Return the default TAIPAN-1 design objects."""
    ecfg = EngineConfig(thrust_vac_N=50_000, burn_time_s=30.0,
                        of_ratio=2.56, p_chamber_pa=5e6,
                        expansion_ratio=10.0, c_star_eff=0.96, cf_efficiency=0.98)
    em   = EngineModel(ecfg); eng = em.build()
    geo  = VehicleGeometry()
    aero = AeroModel(geo)
    mass = MassModel()
    return ecfg, eng, geo, aero, mass


# ── Analysis 1: Engine Performance Sweep ─────────────────────────────────────
def analysis_engine(output_dir: str = '.'):
    """Plot engine performance vs O/F ratio and expansion ratio."""
    print("\n[Engine Analysis]")
    ecfg, eng, geo, aero, mass = default_vehicle()
    em = EngineModel(ecfg); em.build(); em.print_summary()

    fig = _mkfig(1, 1, (16, 5))
    gs  = gridspec.GridSpec(1, 4, figure=fig, wspace=0.4)

    # Nozzle profile
    ax0 = _axstyle(fig.add_subplot(gs[0, 0]))
    rt, re = eng.d_throat_mm/2, eng.d_exit_mm/2
    xn = np.linspace(0, eng.nozzle_len_mm, 200)
    rn = rt + (re - rt) * (xn / eng.nozzle_len_mm)
    ax0.fill_between(xn, rn, -rn, alpha=0.2, color=D)
    ax0.plot(xn, rn, color=D, lw=2); ax0.plot(xn, -rn, color=D, lw=2)
    ax0.set_aspect('equal'); ax0.set_xlabel('mm', fontsize=9)
    ax0.set_title(f'Nozzle Profile\nDt={eng.d_throat_mm:.0f}mm De={eng.d_exit_mm:.0f}mm',
                  fontsize=9, color=D)

    # Isp vs O/F
    ax1 = _axstyle(fig.add_subplot(gs[0, 1]))
    ofs = np.linspace(1.8, 3.8, 100)
    isps = -14 * (ofs - 2.77)**2 + 363
    ax1.plot(ofs, isps, color=A, lw=2)
    ax1.axvline(ecfg.of_ratio, color=B, lw=1.5, linestyle='--',
                label=f'Design {ecfg.of_ratio}')
    ax1.set_xlabel('O/F Ratio', fontsize=9); ax1.set_ylabel('Isp vac [s]', fontsize=9)
    ax1.set_title('Isp vs O/F', fontsize=9, color=A); ax1.legend(fontsize=7)

    # Thrust vs altitude
    ax2 = _axstyle(fig.add_subplot(gs[0, 2]))
    alts = np.linspace(0, 80e3, 200)
    thrs = np.array([em.thrust_at_altitude(h) for h in alts])
    ax2.plot(alts/1e3, thrs/1e3, color=B, lw=2)
    ax2.set_xlabel('Altitude [km]', fontsize=9); ax2.set_ylabel('Thrust [kN]', fontsize=9)
    ax2.set_title('Thrust vs Altitude', fontsize=9, color=B)

    # Isp vs expansion ratio
    ax3 = _axstyle(fig.add_subplot(gs[0, 3]))
    eps_r = np.linspace(4, 40, 150)
    isp_e = []
    for eps in eps_r:
        me = _mach_from_eps(eps, GAMMA_GAS)
        pe = ecfg.p_chamber_pa*(1+(GAMMA_GAS-1)/2*me**2)**(-GAMMA_GAS/(GAMMA_GAS-1))
        cf = _cf(GAMMA_GAS, ecfg.p_chamber_pa, pe, 0, eps, ecfg.cf_efficiency)
        isp_e.append(cf * C_STAR_IDEAL * ecfg.c_star_eff / G0)
    ax3.plot(eps_r, isp_e, color=C, lw=2)
    ax3.axvline(ecfg.expansion_ratio, color=B, lw=1.5, linestyle='--',
                label=f'ε={ecfg.expansion_ratio}')
    ax3.set_xlabel('Expansion Ratio ε', fontsize=9); ax3.set_ylabel('Isp vac [s]', fontsize=9)
    ax3.set_title('Isp vs Expansion Ratio', fontsize=9, color=C); ax3.legend(fontsize=7)

    fig.suptitle('TAIPAN-1 Engine Performance Analysis', fontsize=12,
                 color=W, fontweight='bold')
    path = f'{output_dir}/taipan1_engine.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")


# ── Analysis 2: Single Trajectory ────────────────────────────────────────────
def analysis_trajectory(ballast_kg: float = 14.0,
                        launch_deg: float = 70.4,
                        output_dir: str = '.'):
    """Simulate and plot a single trajectory."""
    print(f"\n[Trajectory  ballast={ballast_kg:.0f}kg  angle={launch_deg:.1f}°]")
    ecfg, eng, geo, aero, mass = default_vehicle()
    mass.m_ballast = ballast_kg
    sim = FlightSim(geo, aero, mass, ecfg, eng, launch_deg, dt=0.05)
    R   = sim.run(); sim.print_summary(R)

    fig = _mkfig(2, 3, (16, 9))
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.36)

    ax1 = _axstyle(fig.add_subplot(gs[0,:2]))
    ax1.plot(R['x'], R['h'], color=C, lw=2.5)
    ax1.fill_between(R['x'], 0, R['h'], alpha=0.06, color=C)
    ax1.axhline(100, color=W, lw=1, linestyle=':', alpha=0.4, label='Kármán 100km')
    ax1.scatter([R['x'][np.argmax(R['h'])]], [R['apogee_km']],
                s=80, color=D, zorder=5, label=f"Apogee {R['apogee_km']:.0f}km")
    ax1.set_xlabel('Downrange [km]', fontsize=9); ax1.set_ylabel('Altitude [km]', fontsize=9)
    ax1.set_title(f"Trajectory  Range={R['range_km']:.0f}km  Apogee={R['apogee_km']:.0f}km",
                  fontsize=10, color=C); ax1.legend(fontsize=8)

    ax2 = _axstyle(fig.add_subplot(gs[0,2]))
    ax2.plot(R['t'], R['mach'], color=D, lw=2)
    ax2.axhline(1, color=W, lw=1, linestyle=':', alpha=0.3)
    ax2.axhline(5, color=B, lw=1, linestyle=':', alpha=0.4)
    ax2.axvline(ecfg.burn_time_s, color=W, lw=1, linestyle='--', alpha=0.3)
    ax2.set_xlabel('Time [s]', fontsize=9); ax2.set_ylabel('Mach', fontsize=9)
    ax2.set_title(f"Mach  Peak={R['max_mach']:.2f}", fontsize=10, color=D)

    ax3 = _axstyle(fig.add_subplot(gs[1,0]))
    ax3.plot(R['t'], R['h'], color=A, lw=2)
    ax3.axvline(ecfg.burn_time_s, color=B, lw=1.5, linestyle='--',
                label=f'Burnout {R["burnout_h"]:.0f}km')
    ax3.set_xlabel('Time [s]', fontsize=9); ax3.set_ylabel('Altitude [km]', fontsize=9)
    ax3.set_title('Altitude vs Time', fontsize=10, color=A); ax3.legend(fontsize=7)

    ax4 = _axstyle(fig.add_subplot(gs[1,1]))
    ax4b = ax4.twinx()
    ax4.plot(R['t'], R['v']/1e3, color=C, lw=2, label='Velocity')
    ax4b.plot(R['t'], R['thrust']/1e3, color=B, lw=1.5, linestyle='--', label='Thrust kN')
    ax4.set_xlabel('Time [s]', fontsize=9)
    ax4.set_ylabel('Velocity [km/s]', fontsize=9, color=C)
    ax4b.set_ylabel('Thrust [kN]', fontsize=9, color=B)
    ax4.set_title(f"Velocity & Thrust  Burnout {R['burnout_v']:.0f}m/s", fontsize=10, color=C)
    l1,lb1=ax4.get_legend_handles_labels(); l2,lb2=ax4b.get_legend_handles_labels()
    ax4.legend(l1+l2, lb1+lb2, fontsize=7)

    ax5 = _axstyle(fig.add_subplot(gs[1,2]))
    ax5.plot(R['t'], R['gload'], color=E, lw=2)
    ax5.axhline(55, color=R_COL, lw=1.5, linestyle='--', alpha=0.7, label='55g design limit')
    ax5.axhline(R['peak_g'], color=B, lw=1, linestyle=':', label=f"Peak {R['peak_g']:.1f}g")
    ax5.set_xlabel('Time [s]', fontsize=9); ax5.set_ylabel('G-load', fontsize=9)
    ax5.set_title('Structural G-Load', fontsize=10, color=E); ax5.legend(fontsize=7)

    fig.suptitle(f'TAIPAN-1 Trajectory  |  Ballast={ballast_kg:.0f}kg  '
                 f'Launch={launch_deg:.1f}°  '
                 f'Range={R["range_km"]:.0f}km  Mach={R["max_mach"]:.1f}',
                 fontsize=11, color=W, fontweight='bold')
    path = f'{output_dir}/taipan1_trajectory.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")
    return R

R_COL = '#ff4466'  # red colour alias


# ── Analysis 3: Ballast Sweep ─────────────────────────────────────────────────
def analysis_ballast(launch_deg: float = 70.4, output_dir: str = '.'):
    """Sweep ballast 10–250 kg and tabulate/plot performance."""
    print(f"\n[Ballast Sweep  launch={launch_deg:.1f}°]")
    ecfg, eng, geo, aero, _ = default_vehicle()
    ballasts = list(range(10, 260, 10))
    rows = []
    for mb in ballasts:
        mass = MassModel(m_ballast=mb)
        sim  = FlightSim(geo, aero, mass, ecfg, eng, launch_deg, dt=0.1)
        R    = sim.run()
        sm   = mass.stability_margin(geo, aero, False)
        rows.append((mb, mass.m_wet, sm,
                     R['apogee_km'], R['range_km'],
                     R['max_mach'], R['peak_g']))

    rows = np.array(rows)
    print(f"\n  {'Ballast':>7} {'Wet kg':>7} {'SM_bo':>6} "
          f"{'Apogee':>8} {'Range':>8} {'Mach':>7} {'PeakG':>7}")
    print('  ' + '─'*58)
    for row in rows:
        flag = ' ← design' if int(row[0])==14 else (' ⚠ marginal' if row[2]<1.5 else '')
        print(f"  {row[0]:>7.0f} {row[1]:>7.0f} {row[2]:>6.2f} "
              f"{row[3]:>8.1f} {row[4]:>8.1f} {row[5]:>7.2f} {row[6]:>7.1f}{flag}")

    fig = _mkfig(1,3,(15,5))
    gs  = gridspec.GridSpec(1,3,figure=fig,wspace=0.38)

    ax1 = _axstyle(fig.add_subplot(gs[0,0]))
    ax1b= ax1.twinx()
    ax1.plot(rows[:,0],rows[:,4],color=B,lw=2,label='Range')
    ax1b.plot(rows[:,0],rows[:,3],color=A,lw=2,linestyle='--',label='Apogee')
    ax1.axvline(14,color=C,lw=2,linestyle=':',label='Design 14kg')
    ax1.set_xlabel('Ballast [kg]',fontsize=9)
    ax1.set_ylabel('Range [km]',fontsize=9,color=B)
    ax1b.set_ylabel('Apogee [km]',fontsize=9,color=A)
    ax1.set_title('Range & Apogee vs Ballast',fontsize=10,color=B)
    l1,lb1=ax1.get_legend_handles_labels(); l2,lb2=ax1b.get_legend_handles_labels()
    ax1.legend(l1+l2,lb1+lb2,fontsize=7)

    ax2 = _axstyle(fig.add_subplot(gs[0,1]))
    ax2b= ax2.twinx()
    ax2.plot(rows[:,0],rows[:,5],color=D,lw=2,label='Mach')
    ax2b.plot(rows[:,0],rows[:,6],color=E,lw=2,linestyle='--',label='Peak G')
    ax2.axvline(14,color=C,lw=2,linestyle=':')
    ax2.set_xlabel('Ballast [kg]',fontsize=9)
    ax2.set_ylabel('Max Mach',fontsize=9,color=D)
    ax2b.set_ylabel('Peak G',fontsize=9,color=E)
    ax2.set_title('Mach & G-load vs Ballast',fontsize=10,color=D)
    l1,lb1=ax2.get_legend_handles_labels(); l2,lb2=ax2b.get_legend_handles_labels()
    ax2.legend(l1+l2,lb1+lb2,fontsize=7)

    ax3 = _axstyle(fig.add_subplot(gs[0,2]))
    ax3.plot(rows[:,0],rows[:,2],color=C,lw=2)
    ax3.axhline(1.5,color=R_COL,lw=1.5,linestyle='--',alpha=0.7,label='Min 1.5 cal')
    ax3.axvline(14,color=C,lw=2,linestyle=':',label='Design 14kg')
    ax3.set_xlabel('Ballast [kg]',fontsize=9)
    ax3.set_ylabel('SM burnout [cal]',fontsize=9)
    ax3.set_title('Burnout Stability vs Ballast',fontsize=10,color=C)
    ax3.legend(fontsize=7)

    fig.suptitle(f'TAIPAN-1 Ballast Sweep  launch={launch_deg:.1f}°',
                 fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_ballast.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")


# ── Analysis 4: Launch Angle Sweep ───────────────────────────────────────────
def analysis_launch_angle(ballast_kg: float = 14.0, output_dir: str = '.'):
    """Sweep launch angle 30–88° to find max range."""
    print(f"\n[Launch Angle Sweep  ballast={ballast_kg:.0f}kg]")
    ecfg, eng, geo, aero, _ = default_vehicle()
    mass  = MassModel(m_ballast=ballast_kg)
    angles = np.linspace(30, 88, 80)
    rngs, aps, machs = [], [], []
    for ang in angles:
        sim = FlightSim(geo, aero, mass, ecfg, eng, ang, dt=0.1)
        R   = sim.run()
        rngs.append(R['range_km']); aps.append(R['apogee_km'])
        machs.append(R['max_mach'])
    rngs=np.array(rngs); aps=np.array(aps); machs=np.array(machs)
    opt_ang = angles[np.argmax(rngs)]
    print(f"  Optimal launch angle: {opt_ang:.1f}°  →  range={rngs.max():.1f} km")

    fig = _mkfig(1,1,(12,5))
    gs  = gridspec.GridSpec(1,2,figure=fig,wspace=0.38)

    ax1 = _axstyle(fig.add_subplot(gs[0,0]))
    ax1b= ax1.twinx()
    ax1.plot(angles,rngs,color=B,lw=2,label='Range')
    ax1b.plot(angles,aps,color=A,lw=2,linestyle='--',label='Apogee')
    ax1.axvline(opt_ang,color=C,lw=2,linestyle=':',label=f'Opt {opt_ang:.1f}°')
    ax1.set_xlabel('Launch angle [°]',fontsize=9)
    ax1.set_ylabel('Range [km]',fontsize=9,color=B)
    ax1b.set_ylabel('Apogee [km]',fontsize=9,color=A)
    ax1.set_title('Range & Apogee vs Launch Angle',fontsize=10,color=B)
    l1,lb1=ax1.get_legend_handles_labels(); l2,lb2=ax1b.get_legend_handles_labels()
    ax1.legend(l1+l2,lb1+lb2,fontsize=7)

    ax2 = _axstyle(fig.add_subplot(gs[0,1]))
    ax2.plot(angles,machs,color=D,lw=2)
    ax2.axvline(opt_ang,color=C,lw=2,linestyle=':')
    ax2.set_xlabel('Launch angle [°]',fontsize=9)
    ax2.set_ylabel('Max Mach',fontsize=9,color=D)
    ax2.set_title('Max Mach vs Launch Angle',fontsize=10,color=D)

    fig.suptitle(f'TAIPAN-1 Launch Angle Sweep  ballast={ballast_kg:.0f}kg',
                 fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_launch_angle.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")
    return opt_ang


# ── Analysis 5: Thrust Profile Comparison ────────────────────────────────────
def analysis_thrust_profiles(output_dir: str = '.'):
    """Compare flat, tapered, and hybrid thrust profiles."""
    print("\n[Thrust Profile Comparison]")
    ecfg, eng, geo, aero, mass = default_vehicle()
    nominal = ecfg.thrust_vac_N
    bt      = ecfg.burn_time_s

    def flat(t):
        return nominal if t <= bt else 0.0

    def tapered(t):
        if t > bt: return 0.0
        return nominal * (1.6 - 1.0 * t / bt)

    def hybrid(t):
        if t > bt: return 0.0
        raw = 1.8 if t<=8 else (0.85 if t<=22 else 1.1)
        norm = bt / (1.8*8 + 0.85*14 + 1.1*8)
        return nominal * raw * norm

    profiles = [('Flat (baseline)', flat, '#888'),
                ('Tapered (accel)', tapered, D),
                ('Hybrid (spike→sustain)', hybrid, A)]
    results  = []

    for name, fn, col in profiles:
        # Override thrust in sim via monkey-patch
        ecfg2 = EngineConfig(**{k: getattr(ecfg, k) for k in
                                ['thrust_vac_N','burn_time_s','of_ratio',
                                 'p_chamber_pa','expansion_ratio',
                                 'nozzle_angle_deg','c_star_eff','cf_efficiency']})
        sim = FlightSim(geo, aero, mass, ecfg2, eng, 70.4, dt=0.05)
        # Patch thrust method
        sim._thrust = lambda t, h, _fn=fn: _fn(t)
        R = sim.run()
        results.append((name, col, R))
        print(f"  {name:35s}  range={R['range_km']:.0f}km  "
              f"mach={R['max_mach']:.2f}  peakG={R['peak_g']:.1f}")

    t_arr = np.linspace(0, 35, 500)
    fig = _mkfig(1,1,(16,8)); gs = gridspec.GridSpec(2,3,figure=fig,hspace=0.42,wspace=0.38)

    ax1 = _axstyle(fig.add_subplot(gs[0,0]))
    for name,col,_ in zip([p[0] for p in profiles],[p[1] for p in profiles],[]):
        pass
    for (name,col,_),(_, fn,_2) in zip(profiles, [(n,f,c) for n,f,c in profiles]):
        ax1.plot(t_arr, [fn(t)/1e3 for t in t_arr], color=col, lw=2, label=name.split('(')[0])
    ax1.set_xlabel('Time [s]',fontsize=9); ax1.set_ylabel('Thrust [kN]',fontsize=9)
    ax1.set_title('Thrust Profiles',fontsize=10,color=W); ax1.legend(fontsize=7)

    for i, (label, ax_idx, key, ylab, col_) in enumerate([
        ('Altitude [km]', (0,1), 'h', 'Altitude [km]', C),
        ('Mach', (0,2), 'mach', 'Mach', D),
        ('Velocity [km/s]', (1,0), 'v', 'Velocity [km/s]', A),
        ('G-load', (1,1), 'gload', 'G-load', E),
    ]):
        ax = _axstyle(fig.add_subplot(gs[ax_idx[0], ax_idx[1]]))
        for name, col, R in results:
            ydata = R[key] / (1e3 if key == 'v' else 1)
            ax.plot(R['t'], ydata, color=col, lw=2,
                    label=name.split('(')[0].strip())
        ax.set_xlabel('Time [s]',fontsize=9); ax.set_ylabel(ylab,fontsize=9)
        ax.set_title(ylab,fontsize=10,color=col_); ax.legend(fontsize=7)

    ax_bar = _axstyle(fig.add_subplot(gs[1,2]))
    cats = ['Range\n[km]','Apogee\n[km]','Max\nMach','Peak G']
    vals = [[R['range_km'],R['apogee_km'],R['max_mach'],R['peak_g']]
            for _,_,R in results]
    x_pos = np.arange(len(cats)); w = 0.25
    for i,((name,col,_),v) in enumerate(zip(profiles,vals)):
        ax_bar.bar(x_pos+i*w, v, w, color=col, alpha=0.8,
                   label=name.split('(')[0].strip())
    ax_bar.set_xticks(x_pos+w); ax_bar.set_xticklabels(cats,fontsize=8)
    ax_bar.set_title('Performance Comparison',fontsize=10,color=W)
    ax_bar.legend(fontsize=7)

    fig.suptitle('TAIPAN-1 Thrust Profile Comparison',fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_thrust_profiles.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")


# ── Analysis 6: Engine Mass Sensitivity ──────────────────────────────────────
def analysis_engine_sensitivity(output_dir: str = '.'):
    """Show effect of engine dry mass on range and required ballast."""
    print("\n[Engine Mass Sensitivity]")
    ecfg, eng, geo, aero, _ = default_vehicle()
    eng_masses = np.linspace(30, 325, 80)
    ranges, ballasts, sms = [], [], []

    for me in eng_masses:
        mass = MassModel(m_engine=me, m_ballast=14.0)
        sm_b = mass.stability_margin(geo, aero, False)
        # Minimum ballast for SM=1.5
        mb = 0.0
        for mb_try in np.linspace(0, 200, 200):
            mm_t = MassModel(m_engine=me, m_ballast=mb_try)
            if mm_t.stability_margin(geo, aero, False) >= 1.5:
                mb = mb_try; break
        mass2 = MassModel(m_engine=me, m_ballast=mb)
        sim   = FlightSim(geo, aero, mass2, ecfg, eng, 70.4, dt=0.1)
        R     = sim.run()
        ranges.append(R['range_km']); ballasts.append(mb)
        sms.append(mass2.stability_margin(geo, aero, False))

    ranges=np.array(ranges); ballasts=np.array(ballasts)
    print(f"  62 kg engine: range≈{ranges[np.argmin(abs(eng_masses-62))]:.0f} km, "
          f"ballast≈{ballasts[np.argmin(abs(eng_masses-62))]:.0f} kg")
    print(f"  325 kg engine: range≈{ranges[-1]:.0f} km, ballast≈{ballasts[-1]:.0f} kg")

    fig = _mkfig(1,2,(12,5)); gs = gridspec.GridSpec(1,2,figure=fig,wspace=0.38)
    ax1 = _axstyle(fig.add_subplot(gs[0,0]))
    ax1b = ax1.twinx()
    ax1.plot(eng_masses, ranges, color=B, lw=2, label='Range')
    ax1b.plot(eng_masses, ballasts, color=A, lw=2, linestyle='--', label='Ballast')
    ax1.axvline(62, color=C, lw=2, linestyle=':', label='TAIPAN-1 62kg')
    ax1.axvline(325, color=R_COL, lw=1.5, linestyle=':', alpha=0.6, label='Legacy 325kg')
    ax1.set_xlabel('Engine dry mass [kg]',fontsize=9)
    ax1.set_ylabel('Range [km]',fontsize=9,color=B)
    ax1b.set_ylabel('Min ballast [kg]',fontsize=9,color=A)
    ax1.set_title('Range & Ballast vs Engine Mass',fontsize=10,color=B)
    l1,lb1=ax1.get_legend_handles_labels(); l2,lb2=ax1b.get_legend_handles_labels()
    ax1.legend(l1+l2,lb1+lb2,fontsize=7)

    ax2 = _axstyle(fig.add_subplot(gs[0,1]))
    mr = np.array([(MassModel(m_engine=me).m_wet/MassModel(m_engine=me).m_dry)
                   for me in eng_masses])
    dv = 293.1 * G0 * np.log(mr)
    ax2.plot(eng_masses, dv/1e3, color=D, lw=2)
    ax2.axvline(62, color=C, lw=2, linestyle=':')
    ax2.set_xlabel('Engine dry mass [kg]',fontsize=9)
    ax2.set_ylabel('Ideal Δv [km/s]',fontsize=9,color=D)
    ax2.set_title('Delta-V vs Engine Mass',fontsize=10,color=D)

    fig.suptitle('TAIPAN-1 Engine Mass Sensitivity',fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_engine_sensitivity.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")


# ── Analysis 7: Aerodynamic Optimisation ──────────────────────────────────────
def analysis_optimise(n_init: int = 20, n_iter: int = 40, output_dir: str = '.'):
    """Run Bayesian optimiser over rocket geometry."""
    print("\n[Bayesian Aerodynamic Optimisation]")
    ecfg, eng, _, _, _ = default_vehicle()
    opt  = BayesOptimiser(n_init=n_init, n_iter=n_iter)
    best, y_all = opt.run(ecfg, eng)
    R = best['traj']

    print(f"\n  Best design parameters:")
    for name, val in zip(OPT_NAMES, best['x']):
        print(f"    {name:20s}: {val:.3f}")

    fig = _mkfig(1,1,(16,6)); gs = gridspec.GridSpec(1,3,figure=fig,wspace=0.38)

    ax1 = _axstyle(fig.add_subplot(gs[0,0]))
    fits = [h['fitness'] for h in opt.history]
    ax1.scatter(range(len(fits)), fits, s=6, alpha=0.4, color=A)
    ax1.plot(range(len(fits)), np.maximum.accumulate(fits), color=B, lw=2)
    ax1.axvline(n_init, color=W, lw=1, linestyle=':', alpha=0.4)
    ax1.set_xlabel('Iteration',fontsize=9); ax1.set_ylabel('Fitness [km]',fontsize=9)
    ax1.set_title('Optimiser Convergence',fontsize=10,color=B)

    ax2 = _axstyle(fig.add_subplot(gs[0,1]))
    aps = [h['traj']['apogee_km'] for h in opt.history]
    sms = [h['sm'] for h in opt.history]
    sc  = ax2.scatter(sms, aps, c=fits, cmap='plasma', s=15, alpha=0.6)
    ax2.scatter([best['sm']], [R['apogee_km']], s=150, color=B, marker='*', zorder=5)
    ax2.axvline(STAB_MIN, color=R_COL, lw=1, linestyle='--', alpha=0.6)
    plt.colorbar(sc, ax=ax2, label='Fitness')
    ax2.set_xlabel('Stability [cal]',fontsize=9); ax2.set_ylabel('Apogee [km]',fontsize=9)
    ax2.set_title('Apogee vs Stability',fontsize=10,color=A)

    ax3 = _axstyle(fig.add_subplot(gs[0,2]))
    ax3.plot(R['x'], R['h'], color=C, lw=2)
    ax3.fill_between(R['x'], 0, R['h'], alpha=0.07, color=C)
    ax3.set_xlabel('Downrange [km]',fontsize=9); ax3.set_ylabel('Altitude [km]',fontsize=9)
    ax3.set_title(f"Best Trajectory  {R['apogee_km']:.0f}km apogee",fontsize=10,color=C)

    fig.suptitle(f'TAIPAN-1 Aero Optimisation  Best={y_all.max():.0f}km',
                 fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_optimise.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")
    return best


# ── Analysis 8: Full Verification ────────────────────────────────────────────
def analysis_verify(output_dir: str = '.'):
    """Run the complete verification simulation and produce full dashboard."""
    print("\n[Full Verification Simulation]")
    ecfg, eng, geo, aero, mass = default_vehicle()
    em = EngineModel(ecfg); em.build(); em.print_summary()
    mass.print_summary(geo, aero)
    sim = FlightSim(geo, aero, mass, ecfg, eng, 70.4, dt=0.05)
    R   = sim.run(); sim.print_summary(R)

    fig = _mkfig(1,1,(20,12))
    gs  = gridspec.GridSpec(2,4,figure=fig,hspace=0.42,wspace=0.36)

    # Row 0 — trajectory (wide)
    ax0 = _axstyle(fig.add_subplot(gs[0,:2]))
    ax0.plot(R['x'],R['h'],color=C,lw=2.5)
    ax0.fill_between(R['x'],0,R['h'],alpha=0.07,color=C)
    ax0.axhline(100,color=W,lw=1,linestyle=':',alpha=0.4,label='Kármán 100km')
    ax0.axhline(R['burnout_h'],color=B,lw=1,linestyle='--',alpha=0.5,
                label=f'Burnout {R["burnout_h"]:.0f}km')
    ax0.scatter([R['x'][np.argmax(R['h'])]],[R['apogee_km']],
                s=80,color=D,zorder=5,label=f'Apogee {R["apogee_km"]:.0f}km')
    ax0.set_xlabel('Downrange [km]',fontsize=9); ax0.set_ylabel('Altitude [km]',fontsize=9)
    ax0.set_title(f'Trajectory  Range={R["range_km"]:.0f}km  Apogee={R["apogee_km"]:.0f}km',
                  fontsize=10,color=C); ax0.legend(fontsize=8)

    ax1 = _axstyle(fig.add_subplot(gs[0,2]))
    ax1.plot(R['t'],R['mach'],color=D,lw=2)
    ax1.axhline(1,color=W,lw=1,linestyle=':',alpha=0.3,label='Mach 1')
    ax1.axhline(5,color=B,lw=1,linestyle=':',alpha=0.4,label='Mach 5')
    ax1.axvline(ecfg.burn_time_s,color=W,lw=1,linestyle='--',alpha=0.3)
    ax1.set_xlabel('Time [s]',fontsize=9); ax1.set_ylabel('Mach',fontsize=9)
    ax1.set_title(f'Mach  Peak={R["max_mach"]:.2f}',fontsize=10,color=D)
    ax1.legend(fontsize=7)

    ax2 = _axstyle(fig.add_subplot(gs[0,3]))
    ax2.plot(R['t'],R['gload'],color=E,lw=2)
    ax2.axhline(55,color=R_COL,lw=1.5,linestyle='--',alpha=0.7,label='55g limit')
    ax2.axhline(R['peak_g'],color=B,lw=1,linestyle=':',
                label=f"Peak {R['peak_g']:.1f}g")
    ax2.set_xlabel('Time [s]',fontsize=9); ax2.set_ylabel('G-load',fontsize=9)
    ax2.set_title('G-Load',fontsize=10,color=E); ax2.legend(fontsize=7)

    ax3 = _axstyle(fig.add_subplot(gs[1,0]))
    ax3.plot(R['t'],R['h'],color=A,lw=2)
    ax3.axvline(ecfg.burn_time_s,color=B,lw=1.5,linestyle='--',alpha=0.7,
                label=f't_burnout={ecfg.burn_time_s}s')
    ax3.set_xlabel('Time [s]',fontsize=9); ax3.set_ylabel('Altitude [km]',fontsize=9)
    ax3.set_title('Altitude vs Time',fontsize=10,color=A); ax3.legend(fontsize=7)

    ax4 = _axstyle(fig.add_subplot(gs[1,1]))
    ax4b= ax4.twinx()
    ax4.plot(R['t'],R['v']/1e3,color=C,lw=2,label='Velocity')
    ax4b.plot(R['t'],R['thrust']/1e3,color=B,lw=1.5,linestyle='--',label='Thrust kN')
    ax4.set_xlabel('Time [s]',fontsize=9)
    ax4.set_ylabel('Velocity [km/s]',fontsize=9,color=C)
    ax4b.set_ylabel('Thrust [kN]',fontsize=9,color=B)
    ax4.set_title('Velocity & Thrust',fontsize=10,color=C)
    l1,lb1=ax4.get_legend_handles_labels(); l2,lb2=ax4b.get_legend_handles_labels()
    ax4.legend(l1+l2,lb1+lb2,fontsize=7)

    ax5 = _axstyle(fig.add_subplot(gs[1,2]))
    mr   = np.linspace(0.1, 15, 300)
    cds  = [aero.cd(m, 5e3) for m in mr]
    ax5.plot(mr, cds, color=A, lw=2)
    ax5.axvline(1.0,color=W,lw=1,linestyle=':',alpha=0.4)
    ax5.axvline(R['max_mach'],color=B,lw=1.5,linestyle='--',
                label=f'Max Mach {R["max_mach"]:.1f}')
    ax5.set_xlabel('Mach',fontsize=9); ax5.set_ylabel('CD',fontsize=9)
    ax5.set_title('Drag Coefficient',fontsize=10,color=A); ax5.legend(fontsize=7)

    ax6 = _axstyle(fig.add_subplot(gs[1,3]))
    fracs, sms = mass.stability_vs_propellant(geo, aero)
    ax6.plot(fracs, sms, color=C, lw=2)
    ax6.axhline(STAB_MIN, color=R_COL, lw=1.5, linestyle='--',
                alpha=0.7, label=f'Min {STAB_MIN} cal')
    ax6.set_xlabel('Propellant remaining [%]',fontsize=9)
    ax6.set_ylabel('Stability [cal]',fontsize=9)
    ax6.set_title('Stability vs Propellant',fontsize=10,color=C)
    ax6.legend(fontsize=7)

    fig.suptitle(
        f'TAIPAN-1 Final Verification  |  RP-1/LOX 50kN  |  '
        f'Range={R["range_km"]:.0f}km  Apogee={R["apogee_km"]:.0f}km  '
        f'Mach={R["max_mach"]:.1f}  Mwet={mass.m_wet:.0f}kg',
        fontsize=12,color=W,fontweight='bold')
    path = f'{output_dir}/taipan1_verification.png'
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=DARK)
    plt.close(); print(f"  → {path}")
    return R

# ══════════════════════════════════════════════════════════════════════════════
# COMMAND-LINE INTERFACE
# ══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='taipan1_sim',
        description='TAIPAN-1 Rocket Simulation Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Simulations
-----------
  engine         Engine performance sweep (Isp, thrust vs altitude, nozzle)
  trajectory     Single trajectory at given ballast and launch angle
  ballast        Ballast mass sweep (10–250 kg)
  launch_angle   Launch angle sweep to find max range
  thrust_profiles Compare flat / tapered / hybrid thrust profiles
  engine_sensitivity  Effect of engine dry mass on range
  optimise       Bayesian aerodynamic design optimisation
  verify         Full verification run (recommended first)
  all            Run all analyses (takes ~5 minutes)

Examples
--------
  python taipan1_sim.py --sim verify
  python taipan1_sim.py --sim trajectory --ballast 80 --angle 65
  python taipan1_sim.py --sim ballast --angle 70.4
  python taipan1_sim.py --sim optimise --n-init 30 --n-iter 60
  python taipan1_sim.py --sim all --output ./results
        """
    )
    p.add_argument('--sim', type=str, default='verify',
                   choices=['engine','trajectory','ballast','launch_angle',
                            'thrust_profiles','engine_sensitivity',
                            'optimise','verify','all'],
                   help='Simulation to run (default: verify)')
    p.add_argument('--ballast', type=float, default=14.0,
                   help='Ballast mass [kg] (default: 14.0)')
    p.add_argument('--angle', type=float, default=70.4,
                   help='Launch angle from vertical [deg] (default: 70.4)')
    p.add_argument('--n-init', type=int, default=20,
                   help='Bayesian optimiser LHS samples (default: 20)')
    p.add_argument('--n-iter', type=int, default=40,
                   help='Bayesian optimiser iterations (default: 40)')
    p.add_argument('--output', type=str, default='.',
                   help='Output directory for plots (default: current dir)')
    return p


def main():
    parser = build_parser()
    args   = parser.parse_args()

    import os
    os.makedirs(args.output, exist_ok=True)

    print("=" * 58)
    print("  TAIPAN-1 SIMULATION SUITE")
    print("  RP-1/LOX Guided Ballistic Interceptor")
    print("=" * 58)
    print(f"  Simulation : {args.sim}")
    print(f"  Output dir : {args.output}")

    sim = args.sim

    if sim in ('engine', 'all'):
        analysis_engine(args.output)

    if sim in ('trajectory', 'all'):
        analysis_trajectory(args.ballast, args.angle, args.output)

    if sim in ('ballast', 'all'):
        analysis_ballast(args.angle, args.output)

    if sim in ('launch_angle', 'all'):
        analysis_launch_angle(args.ballast, args.output)

    if sim in ('thrust_profiles', 'all'):
        analysis_thrust_profiles(args.output)

    if sim in ('engine_sensitivity', 'all'):
        analysis_engine_sensitivity(args.output)

    if sim in ('optimise', 'all'):
        analysis_optimise(args.n_init, args.n_iter, args.output)

    if sim in ('verify', 'all'):
        analysis_verify(args.output)

    print(f"\n  All outputs saved to: {args.output}")
    print("  Done.")


if __name__ == '__main__':
    main()
