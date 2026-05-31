"""
BSG-10 "Goliath" — Central Configuration
All design parameters for the simulation suite.
Edit this file to explore design variants.
"""

from dataclasses import dataclass, field
from typing import Tuple
import numpy as np


# ── Output directory ────────────────────────────────────────────
import os
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════
# CARTRIDGE
# ════════════════════════════════════════════════════════════════

@dataclass
class CartridgeConfig:
    """10-gauge 3.5 inch magnum — canister load."""
    bore_diam:      float = 0.0197      # m   (19.7 mm / 0.775 in)
    shell_len:      float = 0.0889      # m   (3.5 in)
    shot_mass:      float = 0.058       # kg  (58 g canister)
    wad_mass:       float = 0.008       # kg
    powder_mass:    float = 0.0065      # kg  (6.5 g)
    target_vel:     float = 415.0       # m/s muzzle velocity
    saami_limit:    float = 75.8e6      # Pa  (11,000 PSI)

    # Propellant (fixed — progressive powder, γ=1.12)
    gamma:          float = 1.12        # effective adiabatic index
    x_peak:         float = 0.009       # m   peak pressure position
    rise_exp:       float = 0.35        # pressure rise shape exponent
    case_volume:    float = 72e-6       # m³  case gas volume

    @property
    def bore_area(self) -> float:
        return np.pi / 4 * self.bore_diam ** 2

    @property
    def payload_mass(self) -> float:
        return self.shot_mass + self.wad_mass


# ════════════════════════════════════════════════════════════════
# BARREL & GAS SYSTEM
# ════════════════════════════════════════════════════════════════

@dataclass
class BarrelConfig:
    """Barrel, chamber, and gas system geometry."""
    length:         float = 0.510       # m   barrel length
    gas_port:       float = 0.320       # m   gas port from breech
    float_travel:   float = 0.018       # m   short-recoil barrel travel
    float_spring_k: float = 22000.0     # N/m barrel return spring rate
    sleeve_od:      float = 0.0317      # m   barrel sleeve outer diameter
    bushing_len:    float = 0.020       # m   each bushing length

    # Erosion model (Module B)
    k_base:         float = 2.5e-5      # mm/shot erosion at P_ref
    p_ref:          float = 65e6        # Pa  reference pressure
    alpha_erosion:  float = 1.80        # pressure exponent
    f_melonite:     float = 0.65        # Melonite coating factor
    f_chrome:       float = 0.52        # chrome-line coating factor
    f_steel_shot:   float = 1.30        # steel/canister shot abrasion factor
    f_forcing_cone: float = 2.20        # forcing cone wear multiplier
    erosion_fail:   float = 0.50        # mm  throat erosion failure threshold


@dataclass
class GasSystemConfig:
    """Gas piston, cylinder, and regulator."""
    piston_diam:    float = 0.022       # m
    piston_stroke:  float = 0.038       # m
    port_diam:      float = 0.0042      # m  (4.2 mm)
    n_regulator:    int   = 3           # positions

    # Life model
    k_piston:       float = 1.8e-5      # mm/shot erosion
    p_ref_piston:   float = 20e6        # Pa reference
    alpha_piston:   float = 1.50
    f_17_4PH:       float = 0.70        # material factor
    piston_fail:    float = 0.30        # mm clearance failure
    piston_warn:    float = 0.225       # mm clearance warning (75% of fail)

    k_cylinder:     float = 0.8e-5      # mm/shot bore wear
    f_chrome_cyl:   float = 0.50
    alpha_cyl:      float = 1.30
    cylinder_fail:  float = 0.25        # mm bore increase failure

    regulator_wear_per_adj: float = 0.004   # mm per adjustment
    regulator_adj_interval: int   = 500     # rounds between adjustments
    regulator_fail: float = 0.40        # mm seat wear failure


# ════════════════════════════════════════════════════════════════
# OPERATING SYSTEM
# ════════════════════════════════════════════════════════════════

@dataclass
class ActionConfig:
    """Bolt, carrier, counter-mass, buffer."""
    n_lugs:         int   = 6
    lug_width:      float = 0.006       # m
    lug_depth:      float = 0.009       # m

    carrier_mass:   float = 0.420       # kg
    counter_mass:   float = 0.380       # kg
    carrier_stroke: float = 0.080       # m

    # Buffer
    buf_k:          float = 18000.0     # N/m
    buf_c:          float = 850.0       # N·s/m

    # Bolt material (4140 steel, 35 HRC)
    sut_bolt:       float = 1000.0      # MPa tensile
    sys_bolt:       float = 378.0       # MPa shear yield
    se_shear:       float = 300.0       # MPa shear endurance limit

    # Fretting wear (ion nitrided lugs)
    k_fret_nitrided: float = 0.25e-7    # mm³/(MPa·shot·mm)
    k_fret_bare:     float = 2.50e-7
    delta_slip:      float = 0.005      # mm micro-slip per shot
    lug_wear_fail:   float = 0.05       # fraction of contact area

    @property
    def gear_ratio(self) -> float:
        """Gear ratio for momentum balance."""
        return self.carrier_mass / self.counter_mass


# ════════════════════════════════════════════════════════════════
# RECOIL MITIGATION
# ════════════════════════════════════════════════════════════════

@dataclass
class RecoilConfig:
    """All seven recoil mitigation layers."""
    comp_efficiency:  float = 0.30      # 30% gas impulse reduction

    # CBS-10
    cbs_travel:       float = 0.052     # m  max travel
    cbs_l1:           float = 0.022     # m  stage 1 end
    cbs_l2:           float = 0.042     # m  stage 2 end
    cbs_k1:           float = 7000.0    # N/m stage 1 rate
    cbs_k2:           float = 45000.0   # N/m stage 2 rate
    cbs_k3:           float = 140000.0  # N/m stage 3 rate
    cbs_c_comp:       float = 240.0     # N·s/m compression damping
    cbs_c_ext:        float = 80.0      # N·s/m extension damping
    cbs_plate_mass:   float = 0.250     # kg floating plate assembly

    # CBS-10 life models
    # Coil spring (SAE 9254, chrome-silicon)
    cs_inf_coil:      float = 0.055     # asymptotic compression set
    n_set_coil:       float = 95000.0   # characteristic rounds
    fail_cs_coil:     float = 0.040     # failure threshold

    # Belleville (17-7PH SS)
    cs_inf_bell:      float = 0.080
    n_set_bell:       float = 70000.0
    fail_cs_bell:     float = 0.060

    # Hydraulic damper seals (PTFE on chrome rod)
    k_seal:           float = 3.0e-8    # mm³/(N·mm) Archard
    f_seal_contact:   float = 65.0      # N
    l_slide_per_shot: float = 104.0     # mm (2 × 52 mm)
    v_fail_seal:      float = 4.10      # mm³ critical wear volume

    # Sorbothane 50A
    cs_inf_sorb:      float = 0.280
    n_sorb:           float = 9000.0
    fail_sorb:        float = 0.220

    # D3O
    cs_inf_d3o:       float = 0.320
    n_d3o:            float = 11500.0
    fail_d3o:         float = 0.240

    def spring_force(self, x: float) -> float:
        """Progressive spring force at displacement x (m)."""
        x = float(np.clip(x, 0.0, self.cbs_travel))
        if x <= self.cbs_l1:
            return self.cbs_k1 * x
        elif x <= self.cbs_l2:
            return self.cbs_k1 * self.cbs_l1 + self.cbs_k2 * (x - self.cbs_l1)
        else:
            f1 = self.cbs_k1 * self.cbs_l1
            f2 = self.cbs_k2 * (self.cbs_l2 - self.cbs_l1)
            return f1 + f2 + self.cbs_k3 * (x - self.cbs_l2)

    def damper_force(self, v: float) -> float:
        """Asymmetric damper force at velocity v (m/s)."""
        return self.cbs_c_comp * v if v > 0.0 else self.cbs_c_ext * v


# ════════════════════════════════════════════════════════════════
# MAGAZINE
# ════════════════════════════════════════════════════════════════

@dataclass
class MagazineConfig:
    """Tommy-style helical belt drum magazine."""
    drum_od:        float = 0.200       # m
    hub_radius:     float = 0.028       # m
    shell_od:       float = 0.0222      # m  hull + link
    link_gap:       float = 0.003       # m  inter-shell gap
    f_feed_req:     float = 25.0        # N  required feed force (full)
    f_feed_min:     float = 8.0         # N  minimum acceptable feed force

    @property
    def shell_pitch(self) -> float:
        return self.shell_od + self.link_gap

    @property
    def track_width(self) -> float:
        return self.shell_od + 0.003

    @property
    def usable_r(self) -> float:
        return self.drum_od / 2 - self.hub_radius


# ════════════════════════════════════════════════════════════════
# WEAPON SYSTEM (MASS)
# ════════════════════════════════════════════════════════════════

@dataclass
class SystemConfig:
    """Overall weapon system mass and layout."""
    gun_empty:      float = 5.62        # kg
    drum_empty:     float = 0.80        # kg
    round_mass:     float = 0.065       # kg per shell

    # Dimensional layout (mm)
    comp_length:    float = 110.0       # mm  compensator overhang
    barrel_length:  float = 510.0       # mm  barrel chamber to muzzle
    receiver_len:   float = 82.0        # mm  bolt face to rear
    stock_length:   float = 310.0       # mm  CBS-10 total
    bore_height:    float = 152.0       # mm  above stock underside
    grip_from_butt: float = 275.0       # mm
    fg_from_muzzle: float = 330.0       # mm  foregrip from comp tip

    @property
    def oal(self) -> float:
        return (self.comp_length + self.barrel_length +
                self.receiver_len + self.stock_length)

    def loaded_mass(self, n_rounds: int) -> float:
        return self.gun_empty + self.drum_empty + n_rounds * self.round_mass


# ════════════════════════════════════════════════════════════════
# MASTER CONFIG
# ════════════════════════════════════════════════════════════════

@dataclass
class BSG10Config:
    """Master configuration — instantiates all sub-configs."""
    cartridge:  CartridgeConfig  = field(default_factory=CartridgeConfig)
    barrel:     BarrelConfig     = field(default_factory=BarrelConfig)
    gas:        GasSystemConfig  = field(default_factory=GasSystemConfig)
    action:     ActionConfig     = field(default_factory=ActionConfig)
    recoil:     RecoilConfig     = field(default_factory=RecoilConfig)
    magazine:   MagazineConfig   = field(default_factory=MagazineConfig)
    system:     SystemConfig     = field(default_factory=SystemConfig)


# Convenience singleton
DEFAULT_CONFIG = BSG10Config()
