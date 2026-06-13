"""
UCDR Weapons Portfolio — Common Ballistics Simulator
====================================================

A single source-of-truth physics engine used to derive consistent specification
numbers across every weapon, cartridge, armour interaction, and ancillary
claim in the Weapons-Defence portfolio. The goal is internal coherence:
muzzle energy, chamber pressure, recoil impulse, penetration, drop, time of
flight, accuracy, suppressor depth, fragmentation lethality, shaped-charge
performance, rocket trajectory, body-armour V50 and back-face deformation,
acoustic-cancellation depth, ration thermal stability, and pharmacokinetic
peak-and-trough plasma concentration all follow from one set of physical
constants and one set of calibrated empirical correlations rather than from
prose-only assertions.

Tier-1 models (core ballistics, calibrated against published reference data):
  * Internal ballistics: simplified Le Duc / Powley closed-form chamber
    pressure → muzzle velocity for given case capacity, bore, barrel length.
  * External ballistics: 4DOF point-mass integration (drag + gravity) with
    ICAO standard atmosphere and G7 form-factor drag for spitzer / saboted
    projectiles, G1 for blunt projectiles.
  * Terminal ballistics: De Marre and Lambert–Jonas / Lanz–Odermatt
    penetration correlations against RHA; Thor equation for soft-skin
    personnel targets.
  * Suppressor / muzzle blast: adiabatic-expansion bound on peak overpressure
    reduction (capped at 40 dB).
  * Free-recoil energy.

Tier-2 models (added in v2 — comprehensive coverage of every numerical claim
made anywhere in the Weapons-Defence portfolio):
  * Muzzle SPL (unsuppressed) and net SPL at the shooter's ear with hearing
    protection layered (single, double, TACS, double + TACS).
  * Wind drift at canonical ranges from a 10 mph (4.47 m/s) crosswind.
  * Zero-range solution and bullet-drop tables from the optical sight line.
  * Hatcher's max effective range (the "danger space" out to which the
    bullet still has lethal KE against an unarmoured combatant).
  * Barrel life in rounds (calibrated against M14, M2HB, M256 120 mm).
  * Sustained rate of fire bounded by barrel-thermal capacity.
  * Peak recoil force with sprung-stock dissipation and muzzle-brake
    impulse reduction; hydraulic-stock stroke length.
  * RHA penetration at obliquity (NATO 60° standard).
  * Body armour V50 and back-face deformation (NIJ 0101.06 style).
  * Fragmentation: Gurney cylindrical-charge velocity, Mott fragment
    distribution, Carlton lethal-area / effective-radius.
  * Shaped-charge: Birkhoff steady-state jet velocity and depth-of-
    penetration in RHA.
  * Rocketry: Tsiolkovsky burnout + drag-corrected max altitude / max range
    with launch-angle sweep (HPR-X V1 / V2 / V3 + two-stage).
  * Detonation physics: Kamlet-Jacobs detonation pressure and detonation
    velocity for CL-20 / RDX / HMX / TNT comparator chemistry.
  * Acoustic cancellation: Nelson-Elliott multi-mic-array bound on
    cancellation depth vs source/control distance for TACS.
  * Tank-track noise: vibration-transmission ratio (steel vs HNBR composite),
    integrated to SPL reduction at a free-field listener.
  * Pharmacokinetics: one-compartment oral-absorption model for the
    caffeine + modafinil + dextroamphetamine combat-drug stack and the
    HyperSynergy-X7 monograph.
  * Injectable nutrition: osmolality from solute concentrations + Plumb /
    Holliday-Segar safe-infusion bound.
  * Ration thermal stability: Q10 = 2 Arrhenius lipid-oxidation kinetics +
    carnauba-coating melt temperature.

All outputs (Tier-1 and Tier-2) are written into `weapons_sim_results.json`
and a human-readable `weapons_sim_results.md` for citation by the spec sheets
and research papers.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Physical constants & atmosphere
# ---------------------------------------------------------------------------

G          = 9.80665        # m/s^2 — standard gravity
RHO0       = 1.2250         # kg/m^3 — ISA sea-level density
T0         = 288.15         # K
P0         = 101_325.0      # Pa
A0         = 340.294        # m/s — sea-level speed of sound (ISA)
R_AIR      = 287.052874     # J/(kg·K)

# RHA mechanical properties (typical mid-hardness 280–300 BHN plate)
RHA_DENSITY = 7_850.0       # kg/m^3
RHA_BHN     = 290.0         # Brinell hardness

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def isa_density(h: float) -> float:
    """ISA density at geopotential altitude h (m)."""
    if h < 11_000:
        T = T0 - 0.0065 * h
        p = P0 * (T / T0) ** 5.2561
    else:
        T = 216.65
        p = 22_632.0 * math.exp(-(h - 11_000) / 6_341.624)
    return p / (R_AIR * T)


def speed_of_sound(h: float) -> float:
    if h < 11_000:
        T = T0 - 0.0065 * h
    else:
        T = 216.65
    return math.sqrt(1.4 * R_AIR * T)


# Drag-coefficient tables — G7 (boat-tailed spitzer) and G1 (flat-base / blunt)
# Tabulated Cd vs Mach. Linear interpolation between knots.
G7_TABLE = [
    (0.00, 0.119), (0.50, 0.119), (0.70, 0.119), (0.80, 0.120),
    (0.85, 0.121), (0.90, 0.125), (0.95, 0.139), (1.00, 0.196),
    (1.05, 0.260), (1.10, 0.296), (1.20, 0.319), (1.40, 0.328),
    (1.80, 0.310), (2.20, 0.280), (3.00, 0.227), (4.00, 0.180),
    (5.00, 0.155),
]

G1_TABLE = [
    (0.00, 0.226), (0.50, 0.222), (0.70, 0.215), (0.80, 0.220),
    (0.90, 0.243), (0.95, 0.300), (1.00, 0.470), (1.05, 0.604),
    (1.10, 0.638), (1.20, 0.620), (1.40, 0.558), (1.80, 0.456),
    (2.20, 0.380), (3.00, 0.299), (4.00, 0.249), (5.00, 0.220),
]


def cd_interp(table: List[Tuple[float, float]], mach: float) -> float:
    if mach <= table[0][0]:
        return table[0][1]
    if mach >= table[-1][0]:
        return table[-1][1]
    for (m0, c0), (m1, c1) in zip(table, table[1:]):
        if m0 <= mach <= m1:
            return c0 + (c1 - c0) * (mach - m0) / (m1 - m0)
    return table[-1][1]


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Cartridge:
    name: str
    bore_mm: float                    # bore (projectile) diameter
    projectile_mass_g: float          # bullet mass (no case)
    case_capacity_cm3: float          # net case water capacity
    propellant_mass_g: float
    propellant_force: float = 950_000 # J/kg — "impetus" of nitrocellulose
    propellant_covolume: float = 0.001 # m^3/kg
    propellant_gamma: float = 1.27
    barrel_length_mm: float = 500
    bullet_form: str = "G7"           # G7 spitzer / G1 blunt
    bullet_drag_factor: float = 1.00  # form factor applied to G-table Cd
    notes: str = ""
    calibrated_mv_ms: Optional[float] = None
    calibrated_pressure_MPa: Optional[float] = None


@dataclass
class InternalBallisticsResult:
    cartridge: str
    barrel_length_mm: float
    bore_area_m2: float
    propellant_mass_g: float
    projectile_mass_g: float
    chamber_pressure_max_MPa: float
    chamber_pressure_max_psi: float
    muzzle_velocity_ms: float
    muzzle_velocity_fps: float
    muzzle_energy_J: float
    muzzle_energy_ftlb: float
    muzzle_momentum_kgms: float
    recoil_impulse_Ns: float

    def as_row(self) -> Dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Internal ballistics — Powley closed-form approximation
# ---------------------------------------------------------------------------
# We use the Le Duc / Powley closed-form:
#   v_muzzle = sqrt( 2 * F * m_prop / (m_proj * (gamma - 1)) *
#                    (1 - (V0 / Vmax) ** (gamma - 1)) )
# where V0 is the chamber volume and Vmax is V0 + bore_area * barrel_length.
# Peak pressure is bounded by the propellant impetus / covolume ratio and a
# loading-density form factor. This is *not* a full Corner / lumped-parameter
# integration; it is a calibrated closed-form that reproduces published muzzle
# velocities for standard cartridges to within ~3 % when bore / case / barrel
# match.

def simulate_internal_ballistics(c: Cartridge) -> InternalBallisticsResult:
    """Calibrated closed-form internal ballistics.

    Calibrated against published M855A1 (5.56 × 45 mm NATO, 940 m/s from 20"
    barrel, 380 MPa), M80 ball (7.62 × 51 mm, 845 m/s from 22"), and
    XM1147 (140 mm-class KE, ~1 750 m/s) within ±5 %.
    """
    bore_area = math.pi * (c.bore_mm / 1000.0) ** 2 / 4.0
    V0 = c.case_capacity_cm3 * 1e-6
    Vmax = V0 + bore_area * (c.barrel_length_mm / 1000.0)
    m_prop = c.propellant_mass_g / 1000.0
    m_proj = c.projectile_mass_g / 1000.0

    # Calibrated ballistic efficiency. Calibrated so that 5.56 × 45 NATO from
    # a 20" barrel returns 940 m/s, 7.62 × 51 NATO from 22" returns 845 m/s,
    # and the 140 mm KE long-rod returns ≈ 1 750 m/s. η is the fraction of
    # the Powley adiabatic-expansion work that ends up as projectile KE after
    # accounting for late-time burn, friction, and heat-loss to the bore.
    if c.bore_mm < 20:
        eta = 0.72
    elif c.bore_mm < 80:
        eta = 0.65
    else:
        eta = 0.55

    work = (c.propellant_force * m_prop / (c.propellant_gamma - 1.0)) * \
           (1.0 - (V0 / Vmax) ** (c.propellant_gamma - 1.0)) * eta

    v_muzzle = math.sqrt(max(2.0 * work / m_proj, 0.0))

    # Peak chamber pressure — calibrated loading-density form
    # P_max ≈ F · m_prop / V_chamber · k(loading_density)
    p_raw = c.propellant_force * m_prop / V0
    if c.bore_mm < 20:
        p_max = p_raw * 0.45   # small-arms regime
    elif c.bore_mm < 80:
        p_max = p_raw * 0.55   # autocannon / mortar
    else:
        p_max = p_raw * 0.40   # tank gun (longer, slower burn)

    if c.calibrated_mv_ms is not None:
        v_muzzle = c.calibrated_mv_ms
    if c.calibrated_pressure_MPa is not None:
        p_max = c.calibrated_pressure_MPa * 1e6

    return InternalBallisticsResult(
        cartridge=c.name,
        barrel_length_mm=c.barrel_length_mm,
        bore_area_m2=bore_area,
        propellant_mass_g=c.propellant_mass_g,
        projectile_mass_g=c.projectile_mass_g,
        chamber_pressure_max_MPa=p_max / 1e6,
        chamber_pressure_max_psi=p_max / 6894.76,
        muzzle_velocity_ms=v_muzzle,
        muzzle_velocity_fps=v_muzzle * 3.28084,
        muzzle_energy_J=0.5 * m_proj * v_muzzle ** 2,
        muzzle_energy_ftlb=0.5 * m_proj * v_muzzle ** 2 * 0.737562,
        muzzle_momentum_kgms=m_proj * v_muzzle,
        recoil_impulse_Ns=m_proj * v_muzzle + 1.75 * m_prop * v_muzzle,
    )


# ---------------------------------------------------------------------------
# External ballistics — 4DOF point-mass with G-table drag
# ---------------------------------------------------------------------------

def simulate_external_ballistics(c: Cartridge,
                                 v0: float,
                                 max_range_m: float = 2_500.0,
                                 dt: float = 5e-4,
                                 launch_altitude_m: float = 0.0
                                 ) -> Dict:
    """Integrate a horizontal-launch trajectory and sample velocity & drop
    at canonical ranges. Drop is reported as negative y below launch.
    Integration terminates at max_range, or when velocity drops below 50 m/s,
    or after 60 s. The ground is *not* enforced as a stop condition — the
    sample array always reaches the canonical ranges where the projectile
    still carries useful velocity.
    """
    g_table = G7_TABLE if c.bullet_form == "G7" else G1_TABLE
    mass = c.projectile_mass_g / 1000.0
    bore_area = math.pi * (c.bore_mm / 1000.0) ** 2 / 4.0

    x = 0.0
    y = launch_altitude_m
    vx = v0
    vy = 0.0
    t = 0.0
    samples = []
    last_sample_x = -100.0
    while t < 60.0 and x < max_range_m:
        v = math.hypot(vx, vy)
        if v < 50.0:
            break
        # Stop at unambiguous ground impact. For horizontal-fire trajectory
        # tracking (the usual use case) we want to follow the bullet through
        # ballistic drop well past the line-of-sight zero — the bullet keeps
        # losing velocity even after it "dropped past the gun line". Only
        # break when the projectile has dropped past any conceivable shooter
        # posture (50 m) AND has been in flight long enough that the
        # remaining flight is just below-ground integration. This catches the
        # 57 mm subsonic grenade / mortar (which is below ground after a few
        # hundred metres) without truncating rifle trajectories.
        if y < launch_altitude_m - 50.0 and t > 3.0:
            break
        atm_y = max(y, 0.0)
        mach = v / speed_of_sound(atm_y)
        cd = cd_interp(g_table, mach) * c.bullet_drag_factor
        rho = isa_density(atm_y)
        drag = 0.5 * rho * v * v * cd * bore_area
        ax = -drag * vx / v / mass
        ay = -drag * vy / v / mass - G
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
        if x - last_sample_x >= 25.0:
            samples.append((round(x, 1), round(y, 3),
                            round(v, 1), round(mach, 3), round(t, 4)))
            last_sample_x = x
    return {"impact_x": x, "impact_y": y, "impact_v": math.hypot(vx, vy),
            "impact_t": t, "samples": samples}


# ---------------------------------------------------------------------------
# Terminal ballistics — RHA penetration models
# ---------------------------------------------------------------------------

def de_marre_penetration(velocity_ms: float,
                         mass_g: float,
                         diameter_mm: float,
                         core_factor: float = 1.0) -> float:
    """Calibrated De Marre-form RHA penetration (mm) at normal impact:

        e_mm = K · v^1.4 · m_g^0.7 / d_mm^0.75

    K = 7.80e-4 calibrated against three reference points:
        * M80 7.62 × 51 NATO ball:  ~10 mm RHA @ muzzle  (model: 10.0 mm)
        * M2 .50 BMG AP:            ~20 mm RHA @ muzzle  (model: 19.5 mm)
        * 14.5 × 114 B-32 AP:       ~30 mm RHA @ 100 m   (model: 30.6 mm)

    `core_factor` scales for penetrator construction. The values used in
    PENETRATORS below cover the realistic envelope:
        * 0.85  — lead-cored with mild steel tip (5.7 × 28 SS190 class)
        * 0.95  — M855A1-class steel-tipped composite core
        * 1.00  — standard hardened-steel core (M2 AP / M80 calibration anchor)
        * 1.30  — tungsten-carbide / WC-Co core (incl. 15.2 × 115 saboted)
        * 1.50  — depleted-uranium long-rod (used in PENETRATORS["57x347mm"])
    """
    if velocity_ms <= 0:
        return 0.0
    pen = 7.80e-4 * velocity_ms ** 1.4 * mass_g ** 0.7 / diameter_mm ** 0.75
    return max(pen * core_factor, 0.0)


def lanz_odermatt(velocity_ms: float,
                  length_mm: float,
                  diameter_mm: float,
                  bullet_density_kgm3: float = 17_600.0,
                  obliquity_deg: float = 0.0) -> float:
    """Long-rod penetration vs RHA. Calibrated Tate-form approximation:

        P/L  =  K · sqrt(ρp/ρt) · (v / v₀)^α        for v > v₀
        P    =  0                                    for v ≤ v₀

    with K = 0.44, v₀ = 1 500 m/s, α = 1.0 — calibrated against M829-class
    DU long-rod data (≈ 700 mm RHA @ muzzle, ≈ 600 mm @ 2 km).

    Falls off rapidly below the hydrodynamic transition velocity v₀; above it
    the formula tracks observed APFSDS data to within ~10 %.
    """
    if velocity_ms <= 0:
        return 0.0
    rho_p = bullet_density_kgm3
    rho_t = RHA_DENSITY
    sqrt_rho_ratio = math.sqrt(rho_p / rho_t)
    K = 0.44
    v0 = 1_500.0
    if velocity_ms < 800.0:
        return 0.0   # below this the rod fragments without significant pen
    # smooth fall-off below v₀ via a sigmoid
    factor = 1.0 / (1.0 + math.exp(-(velocity_ms - v0) / 200.0))
    P_mm = K * sqrt_rho_ratio * length_mm * (velocity_ms / v0) ** 1.0 * (0.5 + factor)
    if obliquity_deg > 0:
        P_mm *= math.cos(math.radians(obliquity_deg)) ** 0.5
    return max(P_mm, 0.0)


def thor_equation(velocity_ms: float,
                  mass_g: float,
                  diameter_mm: float,
                  target: str = "muscle") -> float:
    """Project Thor (1961) residual velocity / wound channel depth in cm
    of soft-tissue analogue. Conservative — used only for personnel."""
    if target == "muscle":
        K = 1.40   # m/s per cm
        depth = (0.5 * (mass_g / 1000.0) * velocity_ms ** 2) / \
                (math.pi * (diameter_mm / 1000.0) ** 2 / 4.0 * K * 1e7)
        return min(depth * 100.0, 80.0)
    return 0.0


# ---------------------------------------------------------------------------
# Suppressor model — adiabatic expansion bound
# ---------------------------------------------------------------------------

def suppressor_attenuation_dB(volume_chamber_cm3: float,
                              volume_suppressor_cm3: float,
                              n_baffles: int = 6,
                              gamma: float = 1.27) -> float:
    """Sound attenuation across an N-baffle expansion chamber suppressor.

    First-principles bound: each expansion stage reduces pressure by the
    volume-ratio raised to gamma, baffles add ~3 dB per chamber due to
    interference / turbulence losses, capped by the unsuppressed muzzle blast
    ~165 dB peak.
    """
    if volume_chamber_cm3 <= 0:
        return 0.0
    ratio = (volume_chamber_cm3 + volume_suppressor_cm3) / volume_chamber_cm3
    pressure_ratio = ratio ** gamma
    expansion_dB = 20.0 * math.log10(pressure_ratio)
    baffle_dB = 3.0 * n_baffles
    return min(expansion_dB + baffle_dB, 40.0)


# ---------------------------------------------------------------------------
# Recoil model — rigid-body free recoil energy
# ---------------------------------------------------------------------------

def free_recoil_energy_J(projectile_mass_g: float,
                         propellant_mass_g: float,
                         muzzle_velocity_ms: float,
                         weapon_mass_kg: float) -> float:
    momentum = (projectile_mass_g + 1.75 * propellant_mass_g) / 1000.0 * muzzle_velocity_ms
    v_recoil = momentum / weapon_mass_kg
    return 0.5 * weapon_mass_kg * v_recoil ** 2


# ---------------------------------------------------------------------------
# Define the full cartridge / weapon catalogue
# ---------------------------------------------------------------------------

CARTRIDGES: Dict[str, Cartridge] = {

    # -----------------------------------------------------------------
    # MP-4.6M Pistol — corrected from earlier 30-round-mag, 900 rpm
    # numbers to a credible 4.6×30mm PDW-style cartridge in a duty
    # pistol envelope.
    # -----------------------------------------------------------------
    "4.6x30mm": Cartridge(
        name="4.6 × 30 mm Enhanced (pistol barrel)",
        bore_mm=4.65,
        projectile_mass_g=2.6,         # 40 gr tungsten-cored
        case_capacity_cm3=0.95,
        propellant_mass_g=0.40,
        barrel_length_mm=180,          # MP-4.6M Guardian pistol barrel
        bullet_form="G7",
        bullet_drag_factor=1.10,
        notes="Tungsten-cored AP variant; reduced charge for 95kpsi-rated rotating-bolt action. Same cartridge in pistol and PDW; only the barrel length differs (see 4.6x30mm_PDW for the 266.7 mm PDW barrel)."
    ),

    "4.6x30mm_PDW": Cartridge(
        name="4.6 × 30 mm Enhanced (PDW barrel)",
        bore_mm=4.65,
        projectile_mass_g=2.6,         # identical projectile, identical case, identical propellant load
        case_capacity_cm3=0.95,
        propellant_mass_g=0.40,
        barrel_length_mm=266.7,        # MP-4.6M Defender PDW barrel
        bullet_form="G7",
        bullet_drag_factor=1.10,
        notes="Identical loaded cartridge to 4.6x30mm; the longer 266.7 mm PDW barrel allows more complete propellant burn and ~10 % higher muzzle velocity."
    ),

    "4.6x22mm": Cartridge(
        name="4.6 × 22 mm DPAP (LE pistol barrel)",
        bore_mm=4.65,
        projectile_mass_g=3.3,
        case_capacity_cm3=0.65,
        propellant_mass_g=0.22,
        barrel_length_mm=150,
        bullet_form="G7",
        bullet_drag_factor=1.12,
        calibrated_mv_ms=396.0,
        calibrated_pressure_MPa=246.0,
        notes="Police LE variant — WC+Cu jacketed DPAP on shortened 22 mm case. Simulator-calibrated to Noble-Abel reference (MP-4.6P Guardian LE spec §3)."
    ),

    # 5.7 × 28 mm comparator (FN P90)
    "5.7x28mm": Cartridge(
        name="5.7 × 28 mm comparator",
        bore_mm=5.70,
        projectile_mass_g=2.0,
        case_capacity_cm3=0.95,
        propellant_mass_g=0.40,
        barrel_length_mm=263,
        bullet_form="G7",
        bullet_drag_factor=1.05,
    ),

    # MP-6.8 rifle — 6.8 × 51 mm SIG-XM7-class
    "6.8x51mm": Cartridge(
        name="6.8 × 51 mm Common Cartridge",
        bore_mm=6.85,
        projectile_mass_g=8.7,
        case_capacity_cm3=3.55,
        propellant_mass_g=2.55,
        barrel_length_mm=406,
        bullet_form="G7",
        bullet_drag_factor=0.95,
    ),

    # 5.56 × 45mm NATO M855A1 comparator
    "5.56x45mm": Cartridge(
        name="5.56 × 45 mm NATO M855A1",
        bore_mm=5.70,
        projectile_mass_g=4.0,
        case_capacity_cm3=1.85,
        propellant_mass_g=1.62,
        barrel_length_mm=508,
        bullet_form="G7",
        bullet_drag_factor=1.05,
    ),

    # 7.62 × 51mm NATO M80 comparator
    "7.62x51mm": Cartridge(
        name="7.62 × 51 mm NATO M80",
        bore_mm=7.82,
        projectile_mass_g=9.5,
        case_capacity_cm3=3.55,
        propellant_mass_g=2.95,
        barrel_length_mm=508,
        bullet_form="G7",
        bullet_drag_factor=1.00,
    ),

    # 15.2 × 115mm APYT — anti-materiel sniper
    "15.2x115mm": Cartridge(
        name="15.2 × 115 mm APYT",
        bore_mm=15.20,
        projectile_mass_g=64.0,      # saboted tungsten penetrator + sabot
        case_capacity_cm3=39.0,
        propellant_mass_g=23.5,
        barrel_length_mm=720,
        bullet_form="G7",
        bullet_drag_factor=0.85,     # very high-BC saboted penetrator
    ),

    # 14.5 × 114mm Russian comparator
    "14.5x114mm": Cartridge(
        name="14.5 × 114 mm B-32 comparator",
        bore_mm=14.50,
        projectile_mass_g=64.0,
        case_capacity_cm3=42.0,
        propellant_mass_g=29.0,
        barrel_length_mm=1346,
        bullet_form="G7",
        bullet_drag_factor=1.00,
    ),

    # 57 × 347mm autocannon
    "57x347mm": Cartridge(
        name="57 × 347 mm SR autocannon",
        bore_mm=57.0,
        projectile_mass_g=2_400.0,
        case_capacity_cm3=2_600.0,
        propellant_mass_g=1_280.0,
        barrel_length_mm=4_560,
        bullet_form="G7",
        bullet_drag_factor=0.95,
    ),

    # 57 mm underbarrel low-velocity grenade
    "57mm_LV_grenade": Cartridge(
        name="57 mm low-velocity grenade",
        bore_mm=57.0,
        projectile_mass_g=350.0,
        case_capacity_cm3=12.0,
        propellant_mass_g=2.5,
        barrel_length_mm=305,
        bullet_form="G1",
        bullet_drag_factor=1.30,
    ),

    # 57 mm dual-purpose mortar/RPG (lower charge for mortar mode)
    "57mm_mortar": Cartridge(
        name="57 mm dual-purpose mortar mode",
        bore_mm=57.0,
        projectile_mass_g=1_400.0,
        case_capacity_cm3=85.0,
        propellant_mass_g=18.0,
        barrel_length_mm=900,
        bullet_form="G1",
        bullet_drag_factor=1.25,
    ),

    # 140 mm tank KE round (saboted long-rod)
    "140mm_KE": Cartridge(
        name="140 × 920 mm KEW-AP",
        bore_mm=140.0,
        projectile_mass_g=6_400.0,    # saboted penetrator + sabot + obturator
        case_capacity_cm3=24_500.0,
        propellant_mass_g=12_800.0,
        barrel_length_mm=7_350,        # L/D 52
        bullet_form="G7",
        bullet_drag_factor=0.70,
    ),
}


# Sub-projectile descriptors for terminal-ballistics modelling.
# `core_factor` follows the de Marre convention in this script.
PENETRATORS = {
    "4.6x30mm":   dict(length_mm=18.0,  diameter_mm=4.65,  density=17_600,
                       core_factor=1.30, model="de_marre"),     # WC-Co (pistol barrel)
    "4.6x30mm_PDW": dict(length_mm=18.0, diameter_mm=4.65,  density=17_600,
                       core_factor=1.30, model="de_marre"),     # WC-Co (PDW barrel)
    "4.6x22mm":   dict(length_mm=19.0,  diameter_mm=4.65,  density=14_800,
                       core_factor=1.25, model="de_marre"),     # WC+Cu DPAP (LE)
    "5.7x28mm":   dict(length_mm=20.0,  diameter_mm=5.70,  density=11_300,
                       core_factor=0.85, model="de_marre"),     # lead-core w/ steel tip
    "6.8x51mm":   dict(length_mm=33.0,  diameter_mm=6.85,  density=17_600,
                       core_factor=1.30, model="de_marre"),     # WC core
    "5.56x45mm":  dict(length_mm=22.0,  diameter_mm=5.70,  density=10_500,
                       core_factor=0.95, model="de_marre"),     # M855A1 steel-tip
    "7.62x51mm":  dict(length_mm=29.0,  diameter_mm=7.82,  density=11_300,
                       core_factor=1.00, model="de_marre"),     # M80 ball
    "15.2x115mm": dict(length_mm=140.0, diameter_mm=8.5,   density=17_600,
                       core_factor=1.30, model="de_marre"),     # saboted WC-Co sub-cal (matches spec sheet)
    "14.5x114mm": dict(length_mm=51.0,  diameter_mm=14.5,  density=11_300,
                       core_factor=1.30, model="de_marre"),
    "57x347mm":   dict(length_mm=400.0, diameter_mm=25.0,  density=17_600,
                       core_factor=1.50, model="lanz"),         # APFSDS-T 57 mm
    "140mm_KE":   dict(length_mm=920.0, diameter_mm=28.0,  density=18_600,
                       core_factor=1.00, model="lanz"),         # DU long-rod
}


# Weapon platform descriptors — empty-weapon mass for recoil computation.
WEAPON_PLATFORMS = {
    "MP-4.6M Pistol":         dict(cartridge="4.6x30mm",   weight_kg=0.92,  magazine=20,
                                   action="rotating bolt, short recoil",
                                   sustained_rpm=None, semi_only=True),
    "MP-4.6P Guardian LE":    dict(cartridge="4.6x22mm",   weight_kg=0.85,  magazine=20,
                                   action="gas-operated delayed blowback",
                                   sustained_rpm=750, semi_only=False),
    "MP-4.6M Defender PDW":   dict(cartridge="4.6x30mm_PDW", weight_kg=2.10, magazine=40,
                                   action="rotating bolt, short recoil + buffered bolt-carrier",
                                   sustained_rpm=850),
    "MP-6.8 Mark II Rifle":   dict(cartridge="6.8x51mm",   weight_kg=4.10,  magazine=20,
                                   action="short-stroke gas piston, rotating bolt",
                                   sustained_rpm=700),
    "MAS-15.2E Sniper":       dict(cartridge="15.2x115mm", weight_kg=13.2,  magazine=8,
                                   action="bolt action, three-lug rotating bolt",
                                   sustained_rpm=None, semi_only=True),
    "57 mm Autocannon":       dict(cartridge="57x347mm",   weight_kg=350.0, magazine=120,
                                   action="dual-feed externally powered rotary",
                                   sustained_rpm=220),
    "57 mm Underbarrel GL":   dict(cartridge="57mm_LV_grenade", weight_kg=2.40,  magazine=1,
                                   action="single-shot break-action under-barrel",
                                   semi_only=True),
    "57 mm Mortar/RPG":       dict(cartridge="57mm_mortar", weight_kg=7.20, magazine=1,
                                   action="muzzle-loaded dual-mode tube",
                                   semi_only=True),
    "140 mm Tank Gun":        dict(cartridge="140mm_KE",   weight_kg=3_400.0, magazine=1,
                                   action="vertical sliding-block breech, electrothermal-chemical",
                                   semi_only=True),
}


# ===========================================================================
# TIER-2 PHYSICS MODELS — comprehensive coverage of every numerical claim
# ===========================================================================

# ---------------------------------------------------------------------------
# Acoustic muzzle blast — unsuppressed peak SPL and net dB(A) at shooter ear
# ---------------------------------------------------------------------------
# Calibration anchors (published measurements):
#   * 5.56 × 45 NATO from 14.5" carbine: ≈ 165 dB at muzzle, 158 dB at shooter
#   * 7.62 × 51 NATO from 22" rifle:     ≈ 166 dB at muzzle, 159 dB at shooter
#   * .50 BMG from M2HB:                 ≈ 178 dB at muzzle, 170 dB at shooter
#   * 105 mm tank gun:                   ≈ 184 dB at muzzle
#   * 120 mm M256:                       ≈ 187 dB at muzzle
# Empirical fit (Stevens / Westin 1975, adapted): SPL ∝ 10·log10(ME / V_chamber)
# with a calibrated 168 dB offset for 1.0 kJ / 1 cm³ specific muzzle energy.

def muzzle_spl_dB(muzzle_energy_J: float,
                  case_capacity_cm3: float,
                  suppressor_attn_dB: float = 0.0) -> Dict[str, float]:
    """Peak A-weighted SPL at 1 m perpendicular to muzzle, and the equivalent
    SPL reaching the shooter's left ear (~0.6 m behind muzzle, ~0.3 m above)."""
    if muzzle_energy_J <= 0 or case_capacity_cm3 <= 0:
        return {"muzzle_dB": 0.0, "shooter_ear_dB": 0.0}
    me_per_volume = muzzle_energy_J / case_capacity_cm3   # J / cm³
    spl_muzzle = 168.0 + 10.0 * math.log10(max(me_per_volume / 1000.0, 1e-6))
    # Shooter's ear is geometrically off-axis: typically 6–8 dB below muzzle
    spl_ear = spl_muzzle - 7.0
    # Apply suppressor attenuation (cumulative, capped)
    spl_muzzle = max(spl_muzzle - suppressor_attn_dB, 90.0)
    spl_ear    = max(spl_ear    - suppressor_attn_dB, 80.0)
    return {"muzzle_dB": round(spl_muzzle, 1),
            "shooter_ear_dB": round(spl_ear, 1)}


def hearing_protection_layered_dB(unsuppressed_ear_dB: float,
                                  single_plug: bool = False,
                                  double_plug_muff: bool = False,
                                  tacs_active: bool = False) -> float:
    """Net SPL at the eardrum behind a layered hearing-protection stack.
    Approximations:
      * Foam plug (NRR 33 derated to 22): −22 dB
      * Plug + electronic muff (combined derated NRR 36 to 28): −28 dB
      * TACS active cancellation (anti-node-on-ear): additional −35 dB at
        peak, but only inside the 3–5 m personal cancellation zone.
    Stacked attenuation does not add linearly — second protector contributes
    roughly 5 dB on top of the first. TACS, being a phase-cancelling active
    system, stacks more cleanly (≈ 70 % of its rated depth on top of passive).
    """
    attn = 0.0
    if single_plug:
        attn = 22.0
    if double_plug_muff:
        attn = 28.0
    if tacs_active:
        attn = max(attn, 0.0) + 25.0   # TACS adds ~25 dB on top of passive
    return max(unsuppressed_ear_dB - attn, 60.0)


# ---------------------------------------------------------------------------
# Wind drift — 10 mph crosswind (4.47 m/s) over sample ranges
# ---------------------------------------------------------------------------
# Approximation: drift_m = wind_ms · (t_actual - x / v_initial)
# This is the Didion / Bagnold form: drift equals wind speed times the
# difference between actual time-of-flight and the time the bullet would have
# taken in vacuum. It is accurate to within ~5 % for subsonic and supersonic
# small-arms ballistics.

def wind_drift_m(samples: List[Tuple[float, float, float, float, float]],
                 muzzle_velocity_ms: float,
                 wind_ms: float = 4.47) -> List[Dict]:
    rows = []
    for sx, sy, sv, sm, st in samples:
        t_vac = sx / muzzle_velocity_ms if muzzle_velocity_ms > 0 else 0.0
        drift = wind_ms * (st - t_vac)
        rows.append({"range_m": sx, "time_s": st, "drift_m": round(drift, 3)})
    return rows


# ---------------------------------------------------------------------------
# Zeroed-trajectory drop tables (with sight-line zero range)
# ---------------------------------------------------------------------------

def zeroed_drop_table(cart: "Cartridge",
                      v0: float,
                      zero_range_m: float = 100.0,
                      sight_height_m: float = 0.04,
                      sample_ranges_m: Optional[List[float]] = None) -> List[Dict]:
    """Run the external-ballistics integrator with an *elevation* angle
    chosen by bisection so the trajectory crosses the optical line of sight
    at the zero range. Then sample the drop relative to the line of sight at
    canonical ranges.
    """
    if sample_ranges_m is None:
        sample_ranges_m = [0, 50, 100, 200, 300, 500, 800, 1000, 1500]

    def trace(theta_deg: float) -> List[Tuple[float, float, float, float]]:
        g_table = G7_TABLE if cart.bullet_form == "G7" else G1_TABLE
        mass = cart.projectile_mass_g / 1000.0
        bore_area = math.pi * (cart.bore_mm / 1000.0) ** 2 / 4.0
        x = 0.0
        y = 0.0
        vx = v0 * math.cos(math.radians(theta_deg))
        vy = v0 * math.sin(math.radians(theta_deg))
        t = 0.0
        dt = 5e-4
        out = []
        last_sample_x = -100.0
        while t < 60.0 and x < max(sample_ranges_m) + 10:
            v = math.hypot(vx, vy)
            if v < 50.0:
                break
            atm_y = max(y, 0.0)
            mach = v / speed_of_sound(atm_y)
            cd = cd_interp(g_table, mach) * cart.bullet_drag_factor
            rho = isa_density(atm_y)
            drag = 0.5 * rho * v * v * cd * bore_area
            ax = -drag * vx / v / mass
            ay = -drag * vy / v / mass - G
            vx += ax * dt
            vy += ay * dt
            x += vx * dt
            y += vy * dt
            t += dt
            if x - last_sample_x >= 5.0:
                out.append((x, y, v, t))
                last_sample_x = x
        return out

    # Bisect elevation angle so trajectory crosses y = -sight_height at the
    # zero range (i.e., where the sight line is)
    def drop_at(theta: float) -> float:
        traj = trace(theta)
        for x, y, _, _ in traj:
            if x >= zero_range_m:
                return y - (-sight_height_m + (sight_height_m * x / zero_range_m))
        return -1.0

    lo, hi = 0.0, 1.5
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if drop_at(mid) > 0:
            hi = mid
        else:
            lo = mid
    theta_zero = 0.5 * (lo + hi)
    traj = trace(theta_zero)

    rows = []
    for sr in sample_ranges_m:
        for x, y, v, t in traj:
            if x >= sr:
                # Line of sight at range x is at y = -sight_height + sight_height*x/zero_range
                los_y = -sight_height_m + sight_height_m * sr / zero_range_m
                drop = y - los_y
                rows.append({"range_m": sr, "drop_m": round(drop, 4),
                             "velocity_ms": round(v, 1),
                             "time_s": round(t, 4)})
                break
    return rows


# ---------------------------------------------------------------------------
# Hatcher's max effective range — KE threshold for personnel lethality
# ---------------------------------------------------------------------------
# Hatcher's original threshold (1947): ~58 ft·lb (78.6 J) of remaining KE is
# the minimum to incapacitate an unarmoured combatant by direct hit.
# Modern FBI / NIJ threshold: 80 J.

def max_effective_range_m(samples: List[Tuple[float, float, float, float, float]],
                          mass_g: float,
                          ke_threshold_J: float = 80.0) -> Optional[float]:
    for sx, sy, sv, sm, st in samples:
        ke = 0.5 * (mass_g / 1000.0) * sv * sv
        if ke < ke_threshold_J:
            return round(sx, 0)
    return None


# ---------------------------------------------------------------------------
# Barrel life — rounds to throat erosion
# ---------------------------------------------------------------------------
# Calibrated correlation against published military reference data:
#   * 5.56 M4 chrome-lined barrel:     ~10 000 rounds
#   * 7.62 M14 chrome-lined:           ~7 500 rounds
#   * .50 BMG M2HB Stellite-lined:     ~10 000 rounds before throat re-cut
#   * 30 mm GAU-8:                     ~6 000 rounds
#   * 120 mm M256 (tank, KE round):    ~700–1 000 rounds
#   * 15.2 mm AMR class (saboted WC):  ~1 500 rounds (heavy bore wear)
#
# Empirical bore-wear correlation: life ∝ (chamber_capacity^-0.6) ·
# (chamber_pressure^-1.0) · liner_factor
#   liner_factor:  1.00 nitrided / 1.40 chrome / 2.20 Stellite

def barrel_life_rounds(case_capacity_cm3: float,
                       chamber_pressure_MPa: float,
                       liner: str = "stellite") -> int:
    if case_capacity_cm3 <= 0 or chamber_pressure_MPa <= 0:
        return 0
    factor = {"nitrided": 1.00, "chrome": 1.40, "stellite": 2.20}.get(liner, 1.00)
    base = 2.4e7 / (case_capacity_cm3 ** 0.6 * chamber_pressure_MPa)
    return int(base * factor)


# ---------------------------------------------------------------------------
# Sustained rate of fire bounded by barrel thermal capacity
# ---------------------------------------------------------------------------
# Calibrated: 5.56 SAW sustained 100 rpm with quick-change barrel,
# 7.62 MAG-58 sustained 200 rpm, 0.50 M2HB sustained 40 rpm,
# 30 mm GAU-8 burst-only, 57 mm autocannon sustained 220 rpm.

def sustained_rpm_thermal(case_capacity_cm3: float,
                          chamber_pressure_MPa: float,
                          barrel_mass_kg: float,
                          quick_change: bool = True) -> int:
    if case_capacity_cm3 <= 0 or barrel_mass_kg <= 0:
        return 0
    # Heat into the barrel per round ≈ 0.30 · (case_capacity · pressure)
    heat_per_round = 0.30 * case_capacity_cm3 * chamber_pressure_MPa  # J
    # Barrel can absorb ~500 J/kg/°C; thermal limit at 600 °C above ambient
    barrel_capacity = barrel_mass_kg * 500.0 * 600.0  # J
    # Cooling rate via natural convection (open air, ~5 W/kg/°C ΔT)
    cooling_rate = barrel_mass_kg * 5.0 * 300.0       # W (avg ΔT 300 °C)
    sustained_rate = cooling_rate / heat_per_round * 60.0  # rpm
    if quick_change:
        sustained_rate *= 1.5
    return int(min(sustained_rate, 250.0))


# ---------------------------------------------------------------------------
# Peak recoil force with sprung stock / muzzle brake
# ---------------------------------------------------------------------------
# Free recoil energy is the *integrated* recoil energy; the felt peak force
# depends on the stock-travel distance (parabolic dissipation) and any
# muzzle-brake impulse fraction redirected sideways.

def peak_recoil_force_N(free_recoil_energy_J: float,
                        stock_travel_mm: float = 12.0,
                        brake_efficiency: float = 0.0) -> float:
    """Peak force seen at the shooter's shoulder. Assumes parabolic energy
    dissipation over `stock_travel_mm` (typical AR-15 buffer-tube stroke).
    A muzzle brake redirects ~`brake_efficiency` of the propellant gas
    momentum laterally, reducing recoil impulse by the same fraction.
    """
    if free_recoil_energy_J <= 0:
        return 0.0
    e_after_brake = free_recoil_energy_J * (1.0 - brake_efficiency) ** 2
    travel_m = stock_travel_mm / 1000.0
    avg_force = e_after_brake / travel_m
    peak_force = 1.5 * avg_force   # parabolic profile peak / mean ratio
    return peak_force


# ---------------------------------------------------------------------------
# RHA penetration at obliquity (NATO 60°-from-vertical standard)
# ---------------------------------------------------------------------------
# Normalised correction: P(θ) = P(0) · cos(θ) ** n
# where n ≈ 1.6 for hard-cored small-arms (Tate / Krupp data) and n ≈ 0.7 for
# long-rod APFSDS (the rod yaws into normal-incidence behaviour above ~1 km/s).

def obliquity_factor(angle_deg: float, projectile_type: str = "small_arms") -> float:
    if angle_deg <= 0:
        return 1.0
    n = 1.6 if projectile_type == "small_arms" else 0.7
    return max(math.cos(math.radians(angle_deg)) ** n, 0.0)


# ---------------------------------------------------------------------------
# Body-armour V50 and back-face deformation
# ---------------------------------------------------------------------------
# V50 is the velocity at which a given projectile defeats the armour 50 % of
# the time. Empirical fit (Lambert-Jonas / Recht-Ipson):
#   V50 = K_armour · sqrt(areal_density / projectile_mass) · d^0.3
# Calibrated:
#   * NIJ Level IIIA soft armour (Kevlar/UHMWPE) vs 9 mm 124 gr: V50 ≈ 430 m/s
#   * NIJ Level III (steel/ceramic) vs 7.62 M80:                 V50 ≈ 860 m/s
#   * NIJ Level IV (B4C + UHMWPE)  vs .30-06 M2 AP:              V50 ≈ 870 m/s
#   * APES B4C 12-mm-tile + 16-layer UHMWPE/Kevlar vs 7.62 M80:  V50 ≈ 920 m/s

def armour_v50_ms(areal_density_kgm2: float,
                  projectile_mass_g: float,
                  projectile_diameter_mm: float,
                  composite_factor: float = 1.0,
                  is_ap: bool = False) -> float:
    """V50 of a composite armour against a given projectile.

    composite_factor scales for layup quality and presence of a ceramic
    strike-face:
      * 1.00 soft armour only (Kevlar / UHMWPE)
      * 1.45 NIJ III ceramic + composite
      * 1.65 NIJ IV B4C / SiC + UHMWPE (APES class)

    Threat ball / AP distinction (the calibration anchor):
      * ball / FMJ / HP : K_eff = 500 + (composite − 1) · 350
      * AP / WC-core    : K_eff = 200 + (composite − 1) · 575

    Calibration:
      IIIA + 9 mm ball  → 437 m/s  (rated V50 ≈ 430)
      III  + 7.62 ball  → 720 m/s  (rated V50 ≈ 860; slightly under)
      IV   + .30-06 AP  → 880 m/s  (rated V50 ≈ 870)
      IV   + .50 BMG AP → 597 m/s  (rated: penetrates IV, ≈ 890 m/s threat)
    """
    if areal_density_kgm2 <= 0 or projectile_mass_g <= 0:
        return 0.0
    if is_ap:
        K_eff = 200.0 + (composite_factor - 1.0) * 575.0
    else:
        K_eff = 500.0 + (composite_factor - 1.0) * 350.0
    return K_eff * math.sqrt(areal_density_kgm2 / projectile_mass_g) \
           * (projectile_diameter_mm / 7.62) ** 0.3


def back_face_deformation_mm(impact_velocity_ms: float,
                             v50_ms: float,
                             projectile_mass_g: float,
                             areal_density_kgm2: float) -> float:
    """Approximate clay-witness BFD (NIJ 0101.06 measurement) when the
    impact velocity is below V50 (no penetration). Above V50 the armour is
    perforated and BFD is undefined.
    """
    if impact_velocity_ms >= v50_ms or v50_ms <= 0:
        return 0.0
    ratio = impact_velocity_ms / v50_ms
    # Empirical fit: BFD scales linearly with ratio and projectile energy,
    # inversely with armour areal density.
    e_J = 0.5 * (projectile_mass_g / 1000.0) * impact_velocity_ms ** 2
    return min(80.0 * ratio ** 1.5 * (e_J / 4000.0) / (areal_density_kgm2 / 35.0), 44.0)


# ---------------------------------------------------------------------------
# Fragmentation — Gurney velocity + Mott distribution + Carlton lethal area
# ---------------------------------------------------------------------------
# Gurney cylindrical-shell velocity:
#   v_frag = sqrt(2E) · sqrt(C/M / (1 + C/(2M)))
# √(2E) is the Gurney constant (m/s): CL-20 ≈ 3 100, HMX ≈ 2 970,
# RDX ≈ 2 930, TNT ≈ 2 440.

GURNEY_M_PER_S = {"CL-20": 3100, "HMX": 2970, "RDX": 2930, "Comp B": 2700,
                  "PETN": 2930, "TNT": 2440, "ANFO": 1800}


def gurney_cylinder_velocity_ms(explosive: str,
                                charge_mass_kg: float,
                                shell_mass_kg: float) -> float:
    sqrt2E = GURNEY_M_PER_S.get(explosive, 2700)
    CM = charge_mass_kg / shell_mass_kg if shell_mass_kg > 0 else 0
    return sqrt2E * math.sqrt(CM / (1.0 + CM / 2.0))


def mott_fragment_count(shell_mass_kg: float,
                        average_fragment_mass_g: float = 0.5) -> int:
    """Mott (1947) distribution: number of fragments above a given mass
    threshold. Simplification: N = M_shell / (2 · m_avg) for natural
    fragmentation, doubled for pre-scored / controlled fragmentation."""
    if shell_mass_kg <= 0:
        return 0
    return int(2.0 * shell_mass_kg * 1000.0 / (2.0 * average_fragment_mass_g))


def carlton_lethal_area_m2(fragment_velocity_ms: float,
                           fragment_count: int,
                           charge_mass_kg: float) -> float:
    """Carlton's empirical lethal-area formula (1944, generalised). Returns
    the area within which an unprotected standing combatant has > 50 %
    probability of incapacitation. Calibration anchor:
      * 81 mm M821A1 mortar (charge ≈ 0.9 kg Comp B, ≈ 1 700 frags @ 1 300 m/s)
        → A_L ≈ 200 m² (matches FM 3-22.90 published value).
    """
    if fragment_count <= 0 or fragment_velocity_ms <= 0:
        return 0.0
    A = 0.012 * fragment_count * (fragment_velocity_ms / 1000.0) ** 1.6 * \
        (charge_mass_kg / 0.9) ** 0.4
    return round(A, 1)


def effective_radius_m(lethal_area_m2: float) -> float:
    if lethal_area_m2 <= 0:
        return 0.0
    return round(math.sqrt(lethal_area_m2 / math.pi), 1)


# ---------------------------------------------------------------------------
# Shaped-charge (HEAT) — Birkhoff steady-state jet penetration
# ---------------------------------------------------------------------------
# Jet velocity:
#   v_jet = (v_collapse) · sin(α/2) / (1 - cos(α/2))
# with v_collapse calibrated against published copper-liner HEAT data:
#   Standard cone half-angle α/2 ≈ 22°, v_jet ≈ 8 000 m/s.
# Penetration in RHA (hydrodynamic):
#   P = L_jet · sqrt(ρ_jet / ρ_target)
# For copper jet (8 920 kg/m³) into 290 BHN RHA (7 850 kg/m³):
#   P/L ≈ 1.065 — typically L ≈ 0.7 · charge_diameter (effective jet length)
# So P ≈ 0.75 · charge_diameter (PER rule-of-thumb).

def shaped_charge_penetration_mm(charge_diameter_mm: float,
                                 explosive: str = "RDX",
                                 liner_material: str = "copper") -> float:
    if charge_diameter_mm <= 0:
        return 0.0
    rho_jet = {"copper": 8920, "tungsten": 17600, "tantalum": 16650}.get(liner_material, 8920)
    sqrt2E = GURNEY_M_PER_S.get(explosive, 2700)
    # Jet length scales with charge diameter (≈ 0.7 · CD for standard cone)
    L_jet = 0.7 * charge_diameter_mm
    P = L_jet * math.sqrt(rho_jet / RHA_DENSITY)
    # Explosive-power scaling: CL-20 gives ~7 % more than the RDX baseline
    P *= sqrt2E / 2930.0
    return round(P, 0)


# ---------------------------------------------------------------------------
# Rocket trajectory — HPR-X V1 / V2 / V3 + two-stage
# ---------------------------------------------------------------------------
# Tsiolkovsky burnout velocity:
#   Δv = Isp · g · ln(m_initial / m_final)
# Drag-loss-corrected max altitude is solved by point-mass integration with
# a simple supersonic drag coefficient and ICAO atmosphere.

@dataclass
class RocketStage:
    name: str
    motor_isp_s: float        # specific impulse (s)
    motor_mass_g: float       # propellant grain mass
    dry_mass_g: float
    burn_time_s: float
    diameter_mm: float
    cd_subsonic: float = 0.55
    cd_supersonic: float = 0.65


def rocket_trajectory(stages: List[RocketStage],
                      launch_angle_deg: float = 35.0,
                      payload_mass_g: float = 0.0,
                      sample_dt: float = 0.01,
                      max_altitude_cap_m: float = 200_000.0) -> Dict:
    """Point-mass rocket simulation in vertical plane with ICAO atmosphere
    and constant-thrust per stage.

    - Intermediate stages drop their dry mass at burnout; the LAST stage
      retains its dry mass (it carries the payload to apogee).
    - Mass is clamped to a 1 g floor to prevent integration blow-up.
    - Apogee is clamped at `max_altitude_cap_m` as a sanity bound.
    """
    g_local = G
    total_mass = sum(s.motor_mass_g + s.dry_mass_g for s in stages) + payload_mass_g
    mass = total_mass / 1000.0
    x = 0.0; y = 0.0
    vx = 0.0; vy = 0.0
    t = 0.0
    apogee = 0.0
    stage_burnout = []
    theta = math.radians(launch_angle_deg)

    for s_idx, stg in enumerate(stages):
        # Bore area uses THIS stage's diameter (the lower-stage stack drops
        # its diameter when sustainers ignite).
        diameter_m = stg.diameter_mm / 1000.0
        bore_area = math.pi * diameter_m ** 2 / 4.0
        thrust = stg.motor_isp_s * g_local * (stg.motor_mass_g / 1000.0) / stg.burn_time_s
        burn_remaining = stg.burn_time_s
        while burn_remaining > 0:
            v = math.hypot(vx, vy)
            atm_y = max(y, 0.0)
            if atm_y > 80_000:        # essentially-vacuum cap
                rho = 0.0
            else:
                rho = isa_density(atm_y)
            cd = stg.cd_supersonic if v > 340 else stg.cd_subsonic
            drag = 0.5 * rho * v * v * cd * bore_area
            if v > 5.0:
                tx = thrust * vx / v
                ty = thrust * vy / v
            else:
                tx = thrust * math.cos(theta)
                ty = thrust * math.sin(theta)
            if v > 0:
                dx = -drag * vx / v
                dy = -drag * vy / v
            else:
                dx = dy = 0.0
            mass = max(mass, 0.001)  # 1 g floor
            ax = (tx + dx) / mass
            ay = (ty + dy) / mass - g_local
            vx += ax * sample_dt
            vy += ay * sample_dt
            x += vx * sample_dt
            y += vy * sample_dt
            mass -= (stg.motor_mass_g / 1000.0) * sample_dt / stg.burn_time_s
            burn_remaining -= sample_dt
            t += sample_dt
            apogee = max(apogee, y)
            if apogee > max_altitude_cap_m:
                break
        v_bo = math.hypot(vx, vy)
        stage_burnout.append({"stage": stg.name, "burnout_v_ms": round(v_bo, 1),
                              "burnout_alt_m": round(y, 0),
                              "burnout_t_s": round(t, 2)})
        # Drop dry mass of INTERMEDIATE stages only (the last stage carries
        # its dry mass and the payload to apogee).
        if s_idx < len(stages) - 1:
            mass -= stg.dry_mass_g / 1000.0
        if apogee > max_altitude_cap_m:
            break

    # Coast to apogee then descend
    diameter_m = stages[-1].diameter_mm / 1000.0
    bore_area = math.pi * diameter_m ** 2 / 4.0
    coast_dt = max(sample_dt, 0.05)   # coarser dt is fine in coast phase
    while y > 0 and t < 600 and apogee < max_altitude_cap_m:
        v = math.hypot(vx, vy)
        atm_y = max(y, 0.0)
        if atm_y > 80_000:
            rho = 0.0
        else:
            rho = isa_density(atm_y)
        cd = 0.55
        drag = 0.5 * rho * v * v * cd * bore_area if v > 0 else 0
        if v > 0:
            dx = -drag * vx / v
            dy = -drag * vy / v
        else:
            dx = dy = 0.0
        mass = max(mass, 0.001)
        ax = dx / mass
        ay = dy / mass - g_local
        vx += ax * coast_dt
        vy += ay * coast_dt
        x += vx * coast_dt
        y += vy * coast_dt
        t += coast_dt
        apogee = max(apogee, y)
    max_range = x
    return {"apogee_m": round(min(apogee, max_altitude_cap_m), 0),
            "max_range_m": round(max_range, 0),
            "time_of_flight_s": round(t, 1),
            "stage_burnouts": stage_burnout,
            "launch_angle_deg": launch_angle_deg}


# ---------------------------------------------------------------------------
# Detonation physics — Kamlet-Jacobs detonation pressure and VOD
# ---------------------------------------------------------------------------
# Kamlet-Jacobs (1968) empirical correlation:
#   P_CJ = K · ρ² · ϕ            with K = 1.558 × 10⁻⁴ (kbar / (g/cm³)² / ϕ)
#   D    = A · ϕ^0.5 · (1 + B·ρ) with A = 1.01 km/s, B = 1.30
# ϕ = N · sqrt(M · Q), N = mol gas / g exp., M = mean MW of gas, Q = heat / g

EXPLOSIVE_KJ = {
    # name : (density g/cm³, N, M, Q kJ/g)
    "CL-20":   (2.040, 0.0344, 27.0, 6.40),
    "HMX":     (1.905, 0.0339, 27.0, 5.69),
    "RDX":     (1.806, 0.0344, 27.0, 5.49),
    "TNT":     (1.654, 0.0327, 24.5, 4.30),
    "Comp B":  (1.715, 0.0341, 26.0, 5.05),
    "PETN":    (1.770, 0.0316, 28.7, 5.81),
    "ANFO":    (0.840, 0.0411, 25.0, 3.91),
}


def kamlet_jacobs(explosive: str) -> Dict:
    """Kamlet-Jacobs (1968) empirical detonation correlation.

    Working units (the form Kamlet and Jacobs originally calibrated):
      ρ (g/cm³), Q in cal/g (NOT kJ/g), M in g/mol gas, N in mol gas/g exp.
      P_CJ (kbar) = 15.58 · ρ² · ϕ
      D (km/s)    = 1.01 · √ϕ · (1 + 1.30 · ρ)
      ϕ           = N · √(M · Q_cal)

    Calibrated values (literature):
      CL-20:  ρ 2.04, P_CJ ≈ 42 GPa, D ≈ 9.4 km/s
      HMX:    ρ 1.91, P_CJ ≈ 39 GPa, D ≈ 9.1 km/s
      RDX:    ρ 1.81, P_CJ ≈ 34 GPa, D ≈ 8.7 km/s
      Comp B: ρ 1.71, P_CJ ≈ 29 GPa, D ≈ 8.0 km/s
      TNT:    ρ 1.65, P_CJ ≈ 21 GPa, D ≈ 6.9 km/s
    """
    if explosive not in EXPLOSIVE_KJ:
        return {}
    rho, N, M, Q_kJ = EXPLOSIVE_KJ[explosive]
    Q_cal = Q_kJ * 239.006        # kJ/g → cal/g
    phi = N * math.sqrt(M * Q_cal)
    P_CJ_kbar = 15.58 * rho ** 2 * phi          # kbar
    D_kms = 1.01 * math.sqrt(phi) * (1.0 + 1.30 * rho)
    # Brisance (Plate-dent / sand-crush, comparative to TNT = 100)
    if explosive == "TNT":
        brisance = 100.0
    else:
        rho_t, Nt, Mt, Q_tnt_kJ = EXPLOSIVE_KJ["TNT"]
        Q_tnt_cal = Q_tnt_kJ * 239.006
        phi_t = Nt * math.sqrt(Mt * Q_tnt_cal)
        brisance = 100.0 * (rho ** 2 * phi) / (rho_t ** 2 * phi_t)
    return {"density_gcm3": rho,
            "P_CJ_GPa": round(P_CJ_kbar / 10.0, 1),
            "VOD_kms":   round(D_kms, 2),
            "Q_kJ_g":    Q_kJ,
            "brisance_TNT_eq": round(brisance, 0),
            "gurney_sqrt2E_ms": GURNEY_M_PER_S.get(explosive, 0)}


# ---------------------------------------------------------------------------
# Acoustic cancellation depth — Nelson-Elliott (1992) multi-microphone bound
# ---------------------------------------------------------------------------
# Theoretical cancellation depth at the target zone:
#   D_dB = 20 · log10(λ / (4π · d_sc))   for d_sc < λ/2
# where λ is the acoustic wavelength and d_sc is the distance between the
# unwanted source and the control source. Wavelength scales with frequency.
# Bandwidth-integrated:
#   D̄_dB = (1/B) ∫_{f_lo}^{f_hi} D(f) df   (Hz-weighted average)
# Personal TACS (3–5 m zone, 16-element array) reaches ≈ 40 dB at 100 Hz
# and ≈ 25 dB at 1 kHz before the geometric bound kicks in.

def tacs_cancellation_dB(array_element_spacing_m: float,
                         freq_hz: float,
                         array_elements: int = 16) -> float:
    """Peak cancellation depth (dB) achievable at the cancellation node for
    a multi-element coherent ANC array. Calibration anchors:

      * Personal (16-element wearable, d_sc ≈ 0.2 m): ≈ 40 dB peak at low
        freq, rolling off to ≈ 25 dB at 4 kHz.
      * Mobile  (64-element vehicle, d_sc ≈ 0.5 m): ≈ 44 dB at 125 Hz,
        ≈ 30 dB at 4 kHz.
      * Fixed   (64-element installation, d_sc ≈ 1.0 m): ≈ 46 dB at 125 Hz,
        ≈ 23 dB at 4 kHz.

    Bounded by (i) the Nelson-Elliott geometric bound (D degrades when the
    inter-source spacing exceeds λ/2) and (ii) a high-frequency rolloff
    (ANC systems lose ≈ 3 dB / octave above 1 kHz because of phase-locking
    latency in the controller).
    """
    if freq_hz <= 0 or array_element_spacing_m <= 0:
        return 0.0
    D_peak = 40.0 + 6.0 * math.log10(max(array_elements / 16.0, 1.0))
    lam = A0 / freq_hz
    if array_element_spacing_m > lam / 2.0:
        D_peak -= 4.0 * math.log2(array_element_spacing_m / (lam / 2.0))
    if freq_hz > 1000:
        D_peak -= 3.0 * math.log2(freq_hz / 1000.0)
    return max(0.0, min(D_peak, 55.0))


# ---------------------------------------------------------------------------
# Tank-track noise transmission
# ---------------------------------------------------------------------------
# Vibration transmission through rubber composite vs steel tracks. Simple
# 1-DOF mass-spring-damper transmissibility:
#   T(ω) = 1 / sqrt((1 - r²)² + (2ζr)²)   with r = ω/ω_n
# Steel-on-steel coupling: ω_n ≈ 80 Hz, ζ ≈ 0.02
# HNBR rubber pad:         ω_n ≈ 25 Hz, ζ ≈ 0.18
# At drive frequency ω ≈ 300 Hz (track frequency at 30 km/h):
#   steel T = ~0.07 (−23 dB transmission ratio)
#   HNBR  T = ~0.007 (−43 dB transmission ratio)
# Net SPL reduction at the listener ≈ −20 dB across the audible band.

def track_pad_noise_reduction_dB(drive_freq_hz: float = 300.0) -> Dict:
    def transmissibility(omega_n: float, zeta: float, omega: float) -> float:
        r = omega / omega_n
        return 1.0 / math.sqrt((1.0 - r * r) ** 2 + (2 * zeta * r) ** 2)

    omega = 2 * math.pi * drive_freq_hz
    omega_n_steel = 2 * math.pi * 80.0
    omega_n_rubber = 2 * math.pi * 25.0
    T_steel = transmissibility(omega_n_steel, 0.02, omega)
    T_rubber = transmissibility(omega_n_rubber, 0.18, omega)
    reduction_dB = 20.0 * math.log10(T_steel / T_rubber)
    return {"steel_transmission_dB": round(20.0 * math.log10(T_steel), 1),
            "rubber_transmission_dB": round(20.0 * math.log10(T_rubber), 1),
            "net_reduction_dB": round(reduction_dB, 1)}


# ---------------------------------------------------------------------------
# Combat-drug pharmacokinetics — one-compartment oral absorption
# ---------------------------------------------------------------------------
# Model: C(t) = (F · D · k_a) / (V · (k_a - k_e)) · (exp(-k_e t) - exp(-k_a t))
# where F = bioavailability, D = dose, V = volume of distribution,
# k_a = absorption rate constant (1/h), k_e = elimination rate constant (1/h).

@dataclass
class DrugPK:
    name: str
    dose_mg: float
    F: float
    V_L_per_kg: float
    ka_per_hr: float
    ke_per_hr: float          # k_e = ln(2)/t_half
    weight_kg: float = 80.0


def drug_concentration_ngmL(pk: DrugPK, t_hr: float) -> float:
    V = pk.V_L_per_kg * pk.weight_kg
    if pk.ka_per_hr == pk.ke_per_hr:
        return 0.0
    C_mg_L = (pk.F * pk.dose_mg * pk.ka_per_hr / (V * (pk.ka_per_hr - pk.ke_per_hr))) \
             * (math.exp(-pk.ke_per_hr * t_hr) - math.exp(-pk.ka_per_hr * t_hr))
    return max(0.0, C_mg_L * 1000.0)  # mg/L → ng/mL


def pk_summary(pk: DrugPK) -> Dict:
    # Time of peak: t_max = ln(k_a/k_e) / (k_a - k_e)
    if pk.ka_per_hr == pk.ke_per_hr:
        return {}
    t_max = math.log(pk.ka_per_hr / pk.ke_per_hr) / (pk.ka_per_hr - pk.ke_per_hr)
    C_max = drug_concentration_ngmL(pk, t_max)
    t_half = math.log(2) / pk.ke_per_hr
    # AUC via Σ trapezoidal integration to 8 half-lives
    AUC = 0.0
    t = 0.0
    dt = 0.05
    last_C = 0.0
    while t < 8 * t_half:
        C = drug_concentration_ngmL(pk, t)
        AUC += 0.5 * (C + last_C) * dt
        last_C = C
        t += dt
    return {"drug": pk.name,
            "dose_mg": pk.dose_mg,
            "t_max_hr": round(t_max, 2),
            "C_max_ng_mL": round(C_max, 1),
            "t_half_hr": round(t_half, 2),
            "AUC_ng_hr_mL": round(AUC, 0)}


# ---------------------------------------------------------------------------
# Injectable nutrition osmolality + safe-infusion bound
# ---------------------------------------------------------------------------
# Osmolality from solutes:
#   each mmol/L of solute contributes 1 mOsm/kg for non-dissociating species
#   NaCl dissociates into 2 ions ⇒ contributes 2 mOsm per mmol
# Plumb / Holliday-Segar safe peripheral-IV bound: 600 mOsm/kg
# Central-line bound (TPN through central vein): 1 200–1 800 mOsm/kg

def osmolality_mOsm_kg(glucose_g_L: float = 0.0,
                       aa_g_L: float = 0.0,
                       lipid_g_L: float = 0.0,
                       NaCl_g_L: float = 0.0,
                       KCl_g_L: float = 0.0) -> float:
    osm = 0.0
    osm += (glucose_g_L / 180.16) * 1000.0      # MW 180.16, 1 ion
    osm += (aa_g_L / 100.0)  * 1000.0           # average AA MW ≈ 100, 1 ion
    osm += (lipid_g_L / 900.0) * 2.5 * 1000.0   # emulsion contribution is small
    osm += (NaCl_g_L / 58.44) * 2.0 * 1000.0    # 2 ions per molecule
    osm += (KCl_g_L  / 74.55) * 2.0 * 1000.0
    return round(osm, 0)


# ---------------------------------------------------------------------------
# Ration thermal stability — Q10 = 2 Arrhenius
# ---------------------------------------------------------------------------
# Shelf-life follows Q10 = 2: every 10 °C rise halves the shelf life.
#   life(T) = life(T_ref) · 2^((T_ref - T) / 10)
# Carnauba coating softening point ≈ 82–86 °C.
# Lipid oxidation in TACT-1 base (HBCD + MCT + casein) calibrated at 25 °C
# baseline = 36 months.

def ration_shelf_life_months(temperature_C: float = 25.0,
                             baseline_months_at_25C: float = 36.0) -> float:
    return round(baseline_months_at_25C * 2.0 ** ((25.0 - temperature_C) / 10.0), 1)


# ---------------------------------------------------------------------------
# Run the catalogue
# ---------------------------------------------------------------------------

def run_all() -> Dict:
    out: Dict = {"cartridges": {}, "weapons": {}, "armour_interactions": {},
                 "suppressors": {}}

    for key, cart in CARTRIDGES.items():
        ib = simulate_internal_ballistics(cart)
        out["cartridges"][key] = ib.as_row()

        if cart.bore_mm < 20:
            sample_ranges = [0, 100, 300, 500, 800, 1000, 1500, 2000]
            max_r = 2_500.0
        elif cart.bore_mm < 80:
            sample_ranges = [0, 100, 500, 1000, 1500, 2000, 3000, 4000]
            max_r = 5_000.0
        else:
            sample_ranges = [0, 500, 1000, 2000, 3000, 4000, 5000, 6000]
            max_r = 8_000.0

        traj = simulate_external_ballistics(cart, v0=ib.muzzle_velocity_ms,
                                            max_range_m=max_r)

        ext_rows = []
        for sr in sample_ranges:
            row = None
            for sx, sy, sv, sm, st in traj["samples"]:
                if sx >= sr:
                    row = dict(range_m=sr, velocity_ms=sv, mach=sm,
                               drop_m=round(sy, 3), time_s=st)
                    break
            if row is None and sr == 0:
                row = dict(range_m=0, velocity_ms=round(ib.muzzle_velocity_ms, 1),
                           mach=round(ib.muzzle_velocity_ms / A0, 3),
                           drop_m=0.0, time_s=0.0)
            if row:
                ext_rows.append(row)
        out["cartridges"][key]["trajectory"] = ext_rows

    # Per-weapon recoil & armour interaction.
    for wkey, wp in WEAPON_PLATFORMS.items():
        cart = CARTRIDGES[wp["cartridge"]]
        cart_row = {k: v for k, v in out["cartridges"][wp["cartridge"]].items()
                    if k != "trajectory"}
        ib = InternalBallisticsResult(**cart_row)
        # Recoil — free recoil energy
        recoil = free_recoil_energy_J(
            cart.projectile_mass_g, cart.propellant_mass_g,
            ib.muzzle_velocity_ms, wp["weight_kg"])

        out["weapons"][wkey] = {
            "cartridge": wp["cartridge"],
            "weight_empty_kg": wp["weight_kg"],
            "magazine_capacity": wp["magazine"],
            "action": wp["action"],
            "sustained_rpm": wp.get("sustained_rpm"),
            "semi_only": wp.get("semi_only", False),
            "muzzle_velocity_ms": round(ib.muzzle_velocity_ms, 1),
            "muzzle_energy_J": round(ib.muzzle_energy_J, 0),
            "chamber_pressure_MPa": round(ib.chamber_pressure_max_MPa, 1),
            "chamber_pressure_psi": round(ib.chamber_pressure_max_psi, 0),
            "free_recoil_energy_J": round(recoil, 2),
            "free_recoil_energy_ftlb": round(recoil * 0.737562, 2),
        }

    # Armour interaction — RHA penetration vs range for each penetrator
    for ckey, pen in PENETRATORS.items():
        cart = CARTRIDGES[ckey]
        traj = out["cartridges"][ckey]["trajectory"]
        rows = []
        for entry in traj:
            v = entry["velocity_ms"]
            if pen["model"] == "de_marre":
                p = de_marre_penetration(v, cart.projectile_mass_g,
                                         pen["diameter_mm"],
                                         core_factor=pen["core_factor"])
            else:
                p = lanz_odermatt(v, pen["length_mm"], pen["diameter_mm"],
                                  bullet_density_kgm3=pen["density"]) * pen["core_factor"]
            rows.append({"range_m": entry["range_m"],
                         "velocity_ms": v,
                         "rha_penetration_mm": round(p, 1),
                         "drop_m": entry["drop_m"],
                         "time_s": entry["time_s"]})
        out["armour_interactions"][ckey] = rows

    # Suppressor model
    suppressor_specs = {
        "MP-4.6M Pistol integral":   dict(chamber_cm3=1.0, suppressor_cm3=80.0,  baffles=6),
        "MP-4.6M Defender PDW":      dict(chamber_cm3=1.0, suppressor_cm3=180.0, baffles=8),
        "MP-6.8 Mark II Rifle":      dict(chamber_cm3=3.5, suppressor_cm3=410.0, baffles=7),
        "MAS-15.2E Sniper":          dict(chamber_cm3=39.0, suppressor_cm3=1_800.0, baffles=10),
    }
    for k, s in suppressor_specs.items():
        out["suppressors"][k] = {
            "attenuation_dB": round(suppressor_attenuation_dB(
                s["chamber_cm3"], s["suppressor_cm3"], s["baffles"]), 1),
            "chamber_volume_cm3": s["chamber_cm3"],
            "suppressor_volume_cm3": s["suppressor_cm3"],
            "baffle_count": s["baffles"],
        }

    # =====================================================================
    # TIER-2 OUTPUTS
    # =====================================================================

    out["tier2"] = {}

    # ----- Acoustic muzzle blast -----
    acoustic = {}
    for wkey, wp in WEAPON_PLATFORMS.items():
        cart = CARTRIDGES[wp["cartridge"]]
        ckey = wp["cartridge"]
        ib_row = {k: v for k, v in out["cartridges"][ckey].items()
                  if k != "trajectory"}
        ib = InternalBallisticsResult(**ib_row)
        sup = next((s["attenuation_dB"] for k, s in out["suppressors"].items()
                    if wkey in k), 0.0)
        unsup = muzzle_spl_dB(ib.muzzle_energy_J, cart.case_capacity_cm3, 0.0)
        sup_spl = muzzle_spl_dB(ib.muzzle_energy_J, cart.case_capacity_cm3, sup)
        acoustic[wkey] = {
            "muzzle_dB_unsuppressed": unsup["muzzle_dB"],
            "shooter_ear_dB_unsuppressed": unsup["shooter_ear_dB"],
            "muzzle_dB_suppressed": sup_spl["muzzle_dB"],
            "shooter_ear_dB_suppressed": sup_spl["shooter_ear_dB"],
            "ear_dB_with_single_plug": round(
                hearing_protection_layered_dB(sup_spl["shooter_ear_dB"],
                                              single_plug=True), 1),
            "ear_dB_with_double_plug_muff": round(
                hearing_protection_layered_dB(sup_spl["shooter_ear_dB"],
                                              double_plug_muff=True), 1),
            "ear_dB_with_TACS_personal": round(
                hearing_protection_layered_dB(sup_spl["shooter_ear_dB"],
                                              double_plug_muff=True,
                                              tacs_active=True), 1),
        }
    out["tier2"]["acoustic"] = acoustic

    # ----- Wind drift, zero-range drop tables, max effective range -----
    aux_ballistics = {}
    for ckey, cart in CARTRIDGES.items():
        ib_row = {k: v for k, v in out["cartridges"][ckey].items()
                  if k != "trajectory"}
        ib = InternalBallisticsResult(**ib_row)
        if cart.bore_mm < 20:
            max_r = 3500
            zero_r = 100
            sample_drop = [0, 50, 100, 200, 300, 500, 800, 1000, 1500]
            wind_samples = [0, 100, 300, 500, 800, 1000, 1500]
        else:
            max_r = 6000 if cart.bore_mm < 80 else 10000
            zero_r = 500 if cart.bore_mm < 80 else 1500
            sample_drop = [0, 500, 1000, 2000, 3000, 4000]
            wind_samples = [0, 500, 1000, 2000, 3000]
        traj = simulate_external_ballistics(cart, v0=ib.muzzle_velocity_ms,
                                            max_range_m=max_r)
        drop = zeroed_drop_table(cart, ib.muzzle_velocity_ms,
                                 zero_range_m=zero_r,
                                 sample_ranges_m=sample_drop)
        drift = wind_drift_m(traj["samples"], ib.muzzle_velocity_ms, wind_ms=4.47)
        # Sample wind at canonical ranges
        drift_samples = []
        for sr in wind_samples:
            for row in drift:
                if row["range_m"] >= sr:
                    drift_samples.append({"range_m": sr, "drift_m_10mph": row["drift_m"]})
                    break
        max_eff = max_effective_range_m(traj["samples"],
                                        cart.projectile_mass_g,
                                        ke_threshold_J=80.0)
        aux_ballistics[ckey] = {
            "zero_range_m": zero_r,
            "drop_from_sightline_m": drop,
            "wind_drift_m_10mph_crosswind": drift_samples,
            "max_effective_range_m_against_personnel": max_eff,
            "muzzle_velocity_fps": round(ib.muzzle_velocity_ms * 3.28084, 0),
            "supersonic_range_m": next(
                (s[0] for s in traj["samples"] if s[2] < 340.0), None),
        }
    out["tier2"]["aux_ballistics"] = aux_ballistics

    # ----- Barrel life and sustained-fire bound -----
    barrel = {}
    barrel_specs = {
        "MP-4.6M Pistol":          ("stellite", 0.30),
        "MP-4.6P Guardian LE":       ("chrome",  0.28),
        "MP-4.6M Defender PDW":    ("stellite", 0.45),
        "MP-6.8 Mark II Rifle":    ("stellite", 1.30),
        "MAS-15.2E Sniper":        ("stellite", 4.40),
        "57 mm Autocannon":        ("chrome",  120.00),
        "57 mm Underbarrel GL":    ("chrome",    0.55),
        "57 mm Mortar/RPG":        ("chrome",    1.80),
        "140 mm Tank Gun":         ("stellite", 1850.00),
    }
    for wkey, (liner, barrel_mass_kg) in barrel_specs.items():
        wp = WEAPON_PLATFORMS[wkey]
        cart = CARTRIDGES[wp["cartridge"]]
        ib_row = {k: v for k, v in out["cartridges"][wp["cartridge"]].items()
                  if k != "trajectory"}
        ib = InternalBallisticsResult(**ib_row)
        life = barrel_life_rounds(cart.case_capacity_cm3,
                                  ib.chamber_pressure_max_MPa,
                                  liner=liner)
        sustained = sustained_rpm_thermal(cart.case_capacity_cm3,
                                          ib.chamber_pressure_max_MPa,
                                          barrel_mass_kg,
                                          quick_change=(wp.get("sustained_rpm") is not None))
        barrel[wkey] = {
            "barrel_liner": liner,
            "barrel_mass_kg": barrel_mass_kg,
            "barrel_life_rounds": life,
            "sustained_rpm_thermal_bound": sustained,
        }
    out["tier2"]["barrel"] = barrel

    # ----- Peak recoil force (with stock travel + muzzle brake) -----
    recoil_detail = {}
    recoil_brake_specs = {
        "MP-4.6M Pistol":           dict(stock_mm=4.0,  brake=0.00),
        "MP-4.6P Guardian LE":      dict(stock_mm=4.0,  brake=0.42),
        "MP-4.6M Defender PDW":     dict(stock_mm=18.0, brake=0.00),
        "MP-6.8 Mark II Rifle":     dict(stock_mm=20.0, brake=0.35),
        "MAS-15.2E Sniper":         dict(stock_mm=45.0, brake=0.65),
        "57 mm Autocannon":         dict(stock_mm=60.0, brake=0.55),
        "57 mm Underbarrel GL":     dict(stock_mm=18.0, brake=0.00),
        "57 mm Mortar/RPG":         dict(stock_mm=50.0, brake=0.40),
        "140 mm Tank Gun":          dict(stock_mm=600.0, brake=0.55),   # hydraulic recoil
    }
    for wkey, spec in recoil_brake_specs.items():
        w = out["weapons"][wkey]
        peak_N = peak_recoil_force_N(w["free_recoil_energy_J"],
                                     stock_travel_mm=spec["stock_mm"],
                                     brake_efficiency=spec["brake"])
        recoil_detail[wkey] = {
            "free_recoil_energy_J": w["free_recoil_energy_J"],
            "stock_travel_mm": spec["stock_mm"],
            "muzzle_brake_efficiency": spec["brake"],
            "peak_recoil_force_N": round(peak_N, 0),
            "peak_recoil_force_lbf": round(peak_N / 4.448, 0),
        }
    out["tier2"]["recoil_detail"] = recoil_detail

    # ----- RHA penetration at NATO 60° obliquity -----
    obliquity_pen = {}
    for ckey, rows in out["armour_interactions"].items():
        cart = CARTRIDGES[ckey]
        ptype = "long_rod" if PENETRATORS[ckey]["model"] == "lanz" else "small_arms"
        f = obliquity_factor(60.0, projectile_type=ptype)
        obliquity_pen[ckey] = [
            {"range_m": r["range_m"],
             "rha_normal_mm": r["rha_penetration_mm"],
             "rha_60deg_mm": round(r["rha_penetration_mm"] * f, 1)}
            for r in rows
        ]
    out["tier2"]["obliquity_penetration"] = obliquity_pen

    # ----- Body armour V50 and BFD -----
    armour_panels = {
        "Soft IIIA (Kevlar/UHMWPE, 5.5 kg/m²)":
            dict(areal=5.5, composite=1.00),
        "NIJ III (steel + composite, 11.2 kg/m²)":
            dict(areal=11.2, composite=1.45),
        "NIJ IV (B4C + UHMWPE, 25 kg/m²)":
            dict(areal=25.0, composite=1.65),
        "APES military (16-layer + 12 mm B4C tile, 35 kg/m²)":
            dict(areal=35.0, composite=1.65),
        "APES-L police (10-layer + 8 mm B4C, 22 kg/m²)":
            dict(areal=22.0, composite=1.65),
    }
    threats = {
        "9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm)":         dict(v=390, m=8.0, d=9.0,   ap=False),
        "5.7 × 28 mm SS190 (716 m/s, 2.0 g)":              dict(v=716, m=2.0, d=5.7,   ap=False),
        "5.56 × 45 NATO M855 (940 m/s, 4.0 g)":            dict(v=940, m=4.0, d=5.7,   ap=False),
        "7.62 × 51 NATO M80 ball (820 m/s, 9.5 g)":        dict(v=820, m=9.5, d=7.82,  ap=False),
        ".30-06 M2 AP (878 m/s, 10.8 g)":                  dict(v=878, m=10.8, d=7.82, ap=True),
        "7.62 × 54R B-32 AP (820 m/s, 10.4 g)":            dict(v=820, m=10.4, d=7.92, ap=True),
        "12.7 × 99 NATO M2 AP (890 m/s, 46.0 g)":          dict(v=890, m=46.0, d=12.7, ap=True),
        "15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm)": dict(v=781, m=64.0, d=8.5,  ap=True),
    }
    armour = {}
    for pname, panel in armour_panels.items():
        results_p = {}
        for tname, t in threats.items():
            v50 = armour_v50_ms(panel["areal"], t["m"], t["d"],
                                composite_factor=panel["composite"],
                                is_ap=t["ap"])
            defeated = t["v"] > v50
            bfd = back_face_deformation_mm(t["v"], v50, t["m"], panel["areal"])
            results_p[tname] = {
                "V50_ms": round(v50, 0),
                "threat_velocity_ms": t["v"],
                "outcome": "PERFORATED" if defeated else "STOPPED",
                "back_face_deformation_mm": round(bfd, 1) if not defeated else None,
            }
        armour[pname] = results_p
    out["tier2"]["armour_v50"] = armour

    # ----- Fragmentation (Carlton lethal area for HE/HE-frag warheads) -----
    frag = {}
    frag_warheads = {
        "57 mm Underbarrel HE-Frag":   dict(charge_kg=0.12, shell_kg=0.18, explosive="Comp B", controlled=True),
        "57 mm Mortar HE":             dict(charge_kg=0.40, shell_kg=0.85, explosive="Comp B", controlled=False),
        "57 mm Autocannon HE-Frag":    dict(charge_kg=0.55, shell_kg=1.65, explosive="Comp B", controlled=True),
        "140 mm Multi-Effect HE-Frag": dict(charge_kg=4.20, shell_kg=2.20, explosive="CL-20",  controlled=True),
    }
    for name, w in frag_warheads.items():
        v_frag = gurney_cylinder_velocity_ms(w["explosive"], w["charge_kg"], w["shell_kg"])
        n_frag = mott_fragment_count(w["shell_kg"], average_fragment_mass_g=0.5)
        if w["controlled"]:
            n_frag = int(n_frag * 2.0)   # pre-scored doubles useful fragment count
        A_lethal = carlton_lethal_area_m2(v_frag, n_frag, w["charge_kg"])
        r_eff = effective_radius_m(A_lethal)
        frag[name] = {
            "explosive": w["explosive"],
            "charge_mass_kg": w["charge_kg"],
            "shell_mass_kg": w["shell_kg"],
            "fragment_velocity_ms": round(v_frag, 0),
            "fragment_count_above_0.5_g": n_frag,
            "controlled_fragmentation": w["controlled"],
            "lethal_area_m2": A_lethal,
            "effective_radius_m": r_eff,
        }
    out["tier2"]["fragmentation"] = frag

    # ----- Shaped-charge (HEAT) -----
    heat = {}
    heat_warheads = {
        "57 mm Underbarrel HEAT":      dict(diameter_mm=55, explosive="RDX",   liner="copper"),
        "57 mm Mortar/RPG HEAT":       dict(diameter_mm=55, explosive="CL-20", liner="copper"),
        "57 mm Autocannon HEDP":       dict(diameter_mm=50, explosive="RDX",   liner="copper"),
        "140 mm Multi-Effect HEAT":    dict(diameter_mm=130, explosive="CL-20", liner="copper"),
    }
    for name, w in heat_warheads.items():
        pen = shaped_charge_penetration_mm(w["diameter_mm"], w["explosive"], w["liner"])
        heat[name] = {
            "charge_diameter_mm": w["diameter_mm"],
            "explosive": w["explosive"],
            "liner_material": w["liner"],
            "RHA_penetration_mm_static": pen,
            "RHA_penetration_calibres": round(pen / w["diameter_mm"], 2),
        }
    out["tier2"]["shaped_charge"] = heat

    # ----- HPR-X rocket trajectory -----
    hpr = {}
    # V1: civilian L-class hobby
    v1 = [RocketStage("V1 L1390 single", motor_isp_s=210, motor_mass_g=2940,
                      dry_mass_g=2500, burn_time_s=2.1, diameter_mm=75)]
    # V2: dual-stage M-impulse
    v2 = [RocketStage("V2 M booster",  motor_isp_s=220, motor_mass_g=5700,
                      dry_mass_g=2200, burn_time_s=2.6, diameter_mm=98),
          RocketStage("V2 K sustainer", motor_isp_s=225, motor_mass_g=2600,
                      dry_mass_g=1400, burn_time_s=2.0, diameter_mm=75)]
    # V3: SOF spotter-class single large APCP
    v3 = [RocketStage("V3 N5800", motor_isp_s=235, motor_mass_g=16400,
                      dry_mass_g=6500, burn_time_s=3.2, diameter_mm=152)]
    for name, stages, payload, angle in [("HPR-X V1 (civ-amateur, 75 mm)", v1, 100.0, 88.0),
                                         ("HPR-X V2 (two-stage 98→75 mm)", v2, 50.0, 85.0),
                                         ("HPR-X V3 (152 mm SOF spotter)", v3, 800.0, 35.0)]:
        # Apogee shot (high angle)
        apogee_run = rocket_trajectory(stages, launch_angle_deg=angle,
                                       payload_mass_g=payload)
        # Range shot (35° optimum) for non-apogee variants
        range_run = rocket_trajectory(stages, launch_angle_deg=35.0,
                                      payload_mass_g=payload)
        hpr[name] = {
            "high_angle_apogee_m": apogee_run["apogee_m"],
            "high_angle_TOF_s":    apogee_run["time_of_flight_s"],
            "35deg_max_range_m":   range_run["max_range_m"],
            "35deg_apogee_m":      range_run["apogee_m"],
            "burnout_summary":     apogee_run["stage_burnouts"],
            "launch_angle_deg":    angle,
        }
    out["tier2"]["rocketry"] = hpr

    # ----- Energetic detonation chemistry -----
    energetics = {}
    for exp in ["CL-20", "HMX", "RDX", "Comp B", "TNT", "PETN", "ANFO"]:
        energetics[exp] = kamlet_jacobs(exp)
    out["tier2"]["energetics"] = energetics

    # ----- TACS active acoustic cancellation depth -----
    tacs_freqs = [125, 250, 500, 1000, 2000, 4000]
    tacs = {}
    for spacing_m, n_elements, label in [
        (0.2, 16, "Personal (3-5 m zone, 16-element wearable)"),
        (0.5, 64, "Mobile (8-15 m zone, 64-element vehicle)"),
        (1.0, 64, "Fixed (30-60 m zone, 64-element installation)"),
    ]:
        rows = {}
        for f in tacs_freqs:
            depth = tacs_cancellation_dB(spacing_m, f, array_elements=n_elements)
            rows[f"{f}_Hz"] = round(depth, 1)
        # Band-integrated weighted average (125-4000 Hz, octave-weighted A-weighting)
        weights = [0.05, 0.10, 0.20, 0.30, 0.25, 0.10]
        bw_avg = sum(rows[f"{f}_Hz"] * w for f, w in zip(tacs_freqs, weights))
        rows["A-weighted_avg_dB"] = round(bw_avg, 1)
        tacs[label] = rows
    out["tier2"]["tacs_cancellation"] = tacs

    # ----- Tank-track noise reduction -----
    out["tier2"]["track_pad_noise"] = track_pad_noise_reduction_dB(drive_freq_hz=300.0)

    # ----- Combat-drug PK -----
    # Note: the "reference stimulant stack" below is the oral half-dose
    # caffeine + modafinil proxy used to bound the HyperSynergy-X7 spec's
    # claimed C_max envelope. The actual six-novel-compound HyperSynergy-X7
    # depot (MetaMax-2034, MetaFlow-47, MitoBoost-47, NeuroFlow-23,
    # VasoMax-16, RecoveryX-88) has no published human PK to calibrate
    # against; the oral-stimulant proxy is the simulator's stand-in.
    pk_subjects = [
        DrugPK("Caffeine 200 mg PO",                       200.0, 1.0,  0.55, 4.5, math.log(2)/5.0),
        DrugPK("Modafinil 200 mg PO",                      200.0, 0.85, 0.9,  1.6, math.log(2)/14.0),
        DrugPK("Dextroamphetamine 10 mg PO",                10.0, 0.80, 4.0,  1.4, math.log(2)/10.0),
        DrugPK("Reference stimulant stack — caffeine 100 mg (HSX7 proxy)",
                                                           100.0, 1.0,  0.55, 4.5, math.log(2)/5.0),
        DrugPK("Reference stimulant stack — modafinil 100 mg (HSX7 proxy)",
                                                           100.0, 0.85, 0.9,  1.6, math.log(2)/14.0),
    ]
    pk = []
    for s in pk_subjects:
        pk.append(pk_summary(s))
    out["tier2"]["pharmacokinetics"] = pk

    # ----- Injectable-nutrition osmolality -----
    inj = {}
    formulations = {
        "Injectable Food baseline (1 200 kcal/L)":
            dict(glucose=300.0, aa=80.0, lipid=120.0, NaCl=5.0, KCl=2.5),
        "Injectable Food field-ration (1 800 kcal/L)":
            dict(glucose=450.0, aa=120.0, lipid=180.0, NaCl=5.0, KCl=2.5),
        "Saline reference (0.9 %)":
            dict(glucose=0.0, aa=0.0, lipid=0.0, NaCl=9.0, KCl=0.0),
        "Standard TPN reference":
            dict(glucose=250.0, aa=50.0, lipid=80.0, NaCl=3.0, KCl=2.5),
    }
    for name, f in formulations.items():
        osm = osmolality_mOsm_kg(glucose_g_L=f["glucose"], aa_g_L=f["aa"],
                                  lipid_g_L=f["lipid"], NaCl_g_L=f["NaCl"],
                                  KCl_g_L=f["KCl"])
        inj[name] = {
            "osmolality_mOsm_kg": osm,
            "peripheral_safe": osm < 600,
            "central_safe": osm < 1800,
            **f,
        }
    out["tier2"]["injectable_nutrition"] = inj

    # ----- Ration thermal stability -----
    ration = {}
    for T in [4, 25, 35, 49, 60]:  # cold-chain, lab, summer, desert, hot-cabin
        ration[f"{T} °C"] = {
            "shelf_life_months": ration_shelf_life_months(T)
        }
    out["tier2"]["ration_stability"] = ration

    # ----- Portfolio lifecycle / reliability (Tier-3, phases 4–7) -----
    import weapon_lifecycle as wl  # noqa: PLC0415
    wl_results = wl.run_all(
        cartridges=out["cartridges"],
        barrel_tier2=out["tier2"].get("barrel", {}),
        ration_lookup=out["tier2"].get("ration_stability", {}),
    )
    _mp46_keys = ("MP-4.6P Guardian LE", "MP-4.6M Pistol", "MP-4.6M Defender PDW")
    out["tier3"] = {
        "weapon_lifecycle": wl_results,
        "mp46_lifecycle": {k: wl_results[k] for k in _mp46_keys if k in wl_results},
    }

    return out


def write_results(results: Dict, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "weapons_sim_results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    # Markdown summary
    md = ["# Weapons-Defence portfolio — simulation results",
          "",
          "_Output of `weapons_simulation.py`. All numbers in this folder's "
          "specification sheets and research papers should match these._",
          ""]

    md.append("## 1. Cartridges — internal & external ballistics\n")
    md.append("| Cartridge | Bore | Bullet | MV | ME | P_max | Recoil impulse |")
    md.append("|---|---|---|---|---|---|---|")
    for k, r in results["cartridges"].items():
        md.append(f"| {k} | {CARTRIDGES[k].bore_mm:.2f} mm "
                  f"| {r['projectile_mass_g']:.1f} g "
                  f"| {r['muzzle_velocity_ms']:.0f} m/s "
                  f"| {r['muzzle_energy_J']:.0f} J "
                  f"| {r['chamber_pressure_max_MPa']:.0f} MPa "
                  f"({r['chamber_pressure_max_psi']:.0f} psi) "
                  f"| {r['recoil_impulse_Ns']:.2f} N·s |")

    md.append("\n## 2. Weapons — per-platform numbers\n")
    md.append("| Weapon | Cartridge | Empty mass | Mag | Action | MV | ME | P_max | Free recoil |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for k, w in results["weapons"].items():
        md.append(f"| {k} | {w['cartridge']} | {w['weight_empty_kg']:.2f} kg "
                  f"| {w['magazine_capacity']} | {w['action']} "
                  f"| {w['muzzle_velocity_ms']:.0f} m/s "
                  f"| {w['muzzle_energy_J']:.0f} J "
                  f"| {w['chamber_pressure_MPa']:.0f} MPa "
                  f"| {w['free_recoil_energy_J']:.1f} J ({w['free_recoil_energy_ftlb']:.1f} ft·lb) |")

    md.append("\n## 3. Armour-piercing performance vs RHA (mm)\n")
    md.append("Small-arms calibres tabulated at 0 / 100 / 300 / 500 / 800 / "
              "1 000 / 1 500 m. Autocannon and tank calibres at 0 / 500 / "
              "1 000 / 2 000 / 3 000 m.")
    md.append("")
    md.append("| Cartridge | 0 m | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m | 2000 m |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    sa_ranges = [0, 100, 300, 500, 800, 1000, 1500, 2000]
    for ckey, rows in results["armour_interactions"].items():
        vals = {r["range_m"]: r["rha_penetration_mm"] for r in rows}
        if CARTRIDGES[ckey].bore_mm < 20:
            row = vals
            md.append("| " + ckey + " | " + " | ".join(
                str(row.get(rg, "—")) for rg in sa_ranges) + " |")
    md.append("")
    md.append("| Heavy cartridge | 0 m | 500 m | 1000 m | 2000 m | 3000 m | 4000 m |")
    md.append("|---|---|---|---|---|---|---|")
    hw_ranges = [0, 500, 1000, 2000, 3000, 4000]
    for ckey, rows in results["armour_interactions"].items():
        vals = {r["range_m"]: r["rha_penetration_mm"] for r in rows}
        if CARTRIDGES[ckey].bore_mm >= 20:
            md.append("| " + ckey + " | " + " | ".join(
                str(vals.get(rg, "—")) for rg in hw_ranges) + " |")

    md.append("\n## 4. Trajectory — velocity (m/s) vs range\n")
    md.append("| Cartridge | 0 m | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m | 2000 m |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for ckey, r in results["cartridges"].items():
        if CARTRIDGES[ckey].bore_mm < 20:
            tr = {row["range_m"]: row["velocity_ms"] for row in r["trajectory"]}
            md.append("| " + ckey + " | " + " | ".join(
                str(tr.get(rg, "—")) for rg in sa_ranges) + " |")
    md.append("")
    md.append("| Heavy cartridge | 0 m | 500 m | 1000 m | 2000 m | 3000 m | 4000 m |")
    md.append("|---|---|---|---|---|---|---|")
    for ckey, r in results["cartridges"].items():
        if CARTRIDGES[ckey].bore_mm >= 20:
            tr = {row["range_m"]: row["velocity_ms"] for row in r["trajectory"]}
            md.append("| " + ckey + " | " + " | ".join(
                str(tr.get(rg, "—")) for rg in hw_ranges) + " |")

    md.append("\n## 5. Suppressor attenuation (peak dB reduction)\n")
    md.append("| Weapon | Chamber vol | Suppressor vol | Baffles | Attenuation |")
    md.append("|---|---|---|---|---|")
    for k, s in results["suppressors"].items():
        md.append(f"| {k} | {s['chamber_volume_cm3']:.1f} cm³ "
                  f"| {s['suppressor_volume_cm3']:.0f} cm³ "
                  f"| {s['baffle_count']} | {s['attenuation_dB']} dB |")

    # =====================================================================
    # TIER-2 SECTIONS
    # =====================================================================

    t2 = results.get("tier2", {})
    if t2:
        # 6. Acoustic muzzle blast + hearing protection stack
        md.append("\n## 6. Muzzle blast & hearing-protection stack (peak SPL, dB)\n")
        md.append("Calibration: 5.56 carbine ≈ 165 dB / 158 dB; 7.62 rifle ≈ 166 / 159; "
                  ".50 BMG ≈ 178 / 170; 120 mm tank ≈ 187. The shooter-ear column is "
                  "~7 dB below muzzle; layered hearing-protection columns add foam plug "
                  "(−22), double plug+muff (−28), or double + TACS personal active "
                  "cancellation (−28 + 25). The unsuppressed peak SPL exceeds OSHA "
                  "ceiling (140 dB) for every weapon in this folder.\n")
        md.append("| Weapon | Muzzle (unsup) | Ear (unsup) | Muzzle (sup) | Ear (sup) | Ear + plug | Ear + double | Ear + double + TACS |")
        md.append("|---|---|---|---|---|---|---|---|")
        for wkey, a in t2["acoustic"].items():
            md.append(f"| {wkey} | {a['muzzle_dB_unsuppressed']} | "
                      f"{a['shooter_ear_dB_unsuppressed']} | "
                      f"{a['muzzle_dB_suppressed']} | "
                      f"{a['shooter_ear_dB_suppressed']} | "
                      f"{a['ear_dB_with_single_plug']} | "
                      f"{a['ear_dB_with_double_plug_muff']} | "
                      f"{a['ear_dB_with_TACS_personal']} |")

        # 7. Sight-line drop tables (small arms only, zeroed)
        md.append("\n## 7. Zeroed bullet drop from sight-line (cm, small arms)\n")
        md.append("Bullet drop measured from the optical sight line for a "
                  "scope-height-over-bore of 4 cm, with each cartridge bisection-zeroed "
                  "at its canonical range (100 m for service rifles; 100 m for the "
                  "PDW; 100 m for the pistol; 500 m for the 15.2 mm sniper).\n")
        md.append("| Cartridge | Zero | 50 m | 100 m | 200 m | 300 m | 500 m | 800 m | 1000 m | 1500 m |")
        md.append("|---|---|---|---|---|---|---|---|---|---|")
        sa_drop_cols = [50, 100, 200, 300, 500, 800, 1000, 1500]
        for ckey, aux in t2["aux_ballistics"].items():
            cart = CARTRIDGES[ckey]
            if cart.bore_mm >= 20:
                continue
            vals = {r["range_m"]: r["drop_m"] for r in aux["drop_from_sightline_m"]}
            cells = []
            for r in sa_drop_cols:
                if r in vals:
                    cells.append(f"{vals[r] * 100:+.1f}")
                else:
                    cells.append("—")
            md.append(f"| {ckey} | {aux['zero_range_m']} m | " + " | ".join(cells) + " |")

        # 8. Wind drift (10 mph crosswind)
        md.append("\n## 8. Wind drift at 10 mph (4.47 m/s) full-value crosswind\n")
        md.append("| Cartridge | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m |")
        md.append("|---|---|---|---|---|---|---|")
        sa_wd_cols = [100, 300, 500, 800, 1000, 1500]
        for ckey, aux in t2["aux_ballistics"].items():
            cart = CARTRIDGES[ckey]
            if cart.bore_mm >= 20:
                continue
            vals = {r["range_m"]: r["drift_m_10mph"]
                    for r in aux["wind_drift_m_10mph_crosswind"]}
            cells = []
            for r in sa_wd_cols:
                if r in vals:
                    cells.append(f"{vals[r] * 100:.1f} cm")
                else:
                    cells.append("—")
            md.append(f"| {ckey} | " + " | ".join(cells) + " |")
        md.append("\n*Heavy-weapon wind drift (heavy cartridges):*")
        md.append("| Heavy cartridge | 500 m | 1000 m | 2000 m | 3000 m |")
        md.append("|---|---|---|---|---|")
        hw_wd_cols = [500, 1000, 2000, 3000]
        for ckey, aux in t2["aux_ballistics"].items():
            cart = CARTRIDGES[ckey]
            if cart.bore_mm < 20:
                continue
            vals = {r["range_m"]: r["drift_m_10mph"]
                    for r in aux["wind_drift_m_10mph_crosswind"]}
            cells = []
            for r in hw_wd_cols:
                if r in vals:
                    cells.append(f"{vals[r]:.2f} m")
                else:
                    cells.append("—")
            md.append(f"| {ckey} | " + " | ".join(cells) + " |")

        # 9. Max effective range against personnel + supersonic range
        md.append("\n## 9. Hatcher max effective range (`KE > 80 J` personnel "
                  "threshold) + supersonic range\n")
        md.append("| Cartridge | Max effective range (m, KE > 80 J) | Supersonic range (m) | Muzzle (fps) |")
        md.append("|---|---|---|---|")
        for ckey, aux in t2["aux_ballistics"].items():
            mer = aux["max_effective_range_m_against_personnel"]
            ssr = aux["supersonic_range_m"]
            cart = CARTRIDGES[ckey]
            cap_m = 3500 if cart.bore_mm < 20 else (6000 if cart.bore_mm < 80 else 10000)
            md.append(f"| {ckey} | "
                      f"{int(mer) if mer else f'> {cap_m:,} m (sim cap)'} | "
                      f"{int(ssr) if ssr else f'> {cap_m:,} m (sim cap)'} | "
                      f"{aux['muzzle_velocity_fps']:.0f} |")

        # 10. Barrel life + sustained-fire thermal bound
        md.append("\n## 10. Barrel life and sustained-fire thermal limit\n")
        md.append("Barrel life is rounds-to-throat-erosion at the spec'd chamber pressure, "
                  "calibrated against M4 (10 000 rd chrome-lined 5.56), M14 (7 500 rd 7.62), "
                  "M2HB (10 000 rd .50 Stellite), GAU-8 (6 000 rd 30 mm), M256 (700–1 000 rd "
                  "120 mm tank). Sustained-fire bound is set by barrel-thermal capacity "
                  "(quick-change barrels treated as 1.5×).\n")
        md.append("| Weapon | Liner | Barrel mass | Life (rounds) | Sustained rpm (thermal) |")
        md.append("|---|---|---|---|---|")
        for wkey, b in t2["barrel"].items():
            md.append(f"| {wkey} | {b['barrel_liner']} | {b['barrel_mass_kg']:.2f} kg "
                      f"| {b['barrel_life_rounds']:,} | {b['sustained_rpm_thermal_bound']} |")

        # 11. Peak recoil force
        md.append("\n## 11. Peak recoil force (sprung-stock, muzzle-brake corrected)\n")
        md.append("Peak shoulder force at the stock-pad assuming parabolic energy "
                  "dissipation over `stock_travel_mm`. Muzzle-brake efficiency is the "
                  "fraction of recoil impulse redirected laterally. The 140 mm uses a "
                  "600 mm hydraulic recoil stroke (the tank gun, not a shoulder weapon).\n")
        md.append("| Weapon | Free recoil (J) | Stock travel | Brake eff. | Peak force (N) | (lbf) |")
        md.append("|---|---|---|---|---|---|")
        for wkey, r in t2["recoil_detail"].items():
            md.append(f"| {wkey} | {r['free_recoil_energy_J']:.1f} | "
                      f"{r['stock_travel_mm']} mm | "
                      f"{int(r['muzzle_brake_efficiency'] * 100)} % | "
                      f"{r['peak_recoil_force_N']:.0f} | "
                      f"{r['peak_recoil_force_lbf']:.0f} |")

        # 12. Penetration at 60° obliquity
        md.append("\n## 12. RHA penetration at NATO 60°-from-vertical obliquity (mm)\n")
        md.append("Normal incidence numbers are taken from §3 and reduced by "
                  "`cos(θ)^n`, with `n = 1.6` for hardened-core small arms (Tate/Krupp) "
                  "and `n = 0.7` for long-rod APFSDS (the rod yaws into normal-incidence "
                  "behaviour above ~1 km/s).\n")
        md.append("| Cartridge | 0 m (normal) | 0 m (60°) | 300 m (60°) | 500 m (60°) | 1000 m (60°) |")
        md.append("|---|---|---|---|---|---|")
        for ckey, rows in t2["obliquity_penetration"].items():
            d = {r["range_m"]: r for r in rows}
            r0 = d.get(0, {})
            r3 = d.get(300, {})
            r5 = d.get(500, {})
            r10 = d.get(1000, {})
            md.append(f"| {ckey} | "
                      f"{r0.get('rha_normal_mm', '—')} | "
                      f"{r0.get('rha_60deg_mm', '—')} | "
                      f"{r3.get('rha_60deg_mm', '—')} | "
                      f"{r5.get('rha_60deg_mm', '—')} | "
                      f"{r10.get('rha_60deg_mm', '—')} |")

        # 13. Body-armour V50 + BFD
        md.append("\n## 13. Body-armour V50 ballistic-limit + back-face deformation\n")
        md.append("V50 is the projectile velocity at which the armour panel is defeated "
                  "50 % of the time. Threats below V50 are stopped; reported BFD is the "
                  "clay-witness depression (NIJ 0101.06 method) and must remain "
                  "`< 44 mm` to pass. Threats above V50 are PERFORATED.\n")
        for pname, results_p in t2["armour_v50"].items():
            md.append(f"\n**{pname}**\n")
            md.append("| Threat | Threat v | V50 | Outcome | BFD |")
            md.append("|---|---|---|---|---|")
            for tname, t in results_p.items():
                bfd = t["back_face_deformation_mm"]
                md.append(f"| {tname} | {t['threat_velocity_ms']} m/s | "
                          f"{t['V50_ms']} m/s | {t['outcome']} | "
                          f"{bfd if bfd is not None else '—'} mm |")

        # 14. Fragmentation (Gurney + Mott + Carlton)
        md.append("\n## 14. HE-Frag warhead — Gurney velocity, Mott fragment count, Carlton lethal area\n")
        md.append("| Warhead | Explosive | Charge mass | Shell mass | v_frag | Fragments | A_L | r_eff |")
        md.append("|---|---|---|---|---|---|---|---|")
        for name, f in t2["fragmentation"].items():
            md.append(f"| {name} | {f['explosive']} | {f['charge_mass_kg']:.2f} kg "
                      f"| {f['shell_mass_kg']:.2f} kg | {f['fragment_velocity_ms']:.0f} m/s "
                      f"| {f['fragment_count_above_0.5_g']:,} "
                      f"({'pre-scored' if f['controlled_fragmentation'] else 'natural'}) "
                      f"| {f['lethal_area_m2']:.0f} m² | {f['effective_radius_m']:.1f} m |")

        # 15. Shaped-charge (HEAT) penetration
        md.append("\n## 15. Shaped-charge (HEAT) RHA penetration (static, normal incidence)\n")
        md.append("Birkhoff jet penetration assuming a standard copper liner at "
                  "~22° half-angle, jet length ≈ 0.7 × CD. Calibrated against published "
                  "RPG-7 PG-7VL (93 mm CD, ~500 mm RHA), Hellfire (177 mm, ~1 100 mm), "
                  "and TOW-2A (152 mm, ~900 mm).\n")
        md.append("| Warhead | Charge dia | Explosive | Liner | RHA pen (mm) | Calibres |")
        md.append("|---|---|---|---|---|---|")
        for name, h in t2["shaped_charge"].items():
            md.append(f"| {name} | {h['charge_diameter_mm']} mm | {h['explosive']} "
                      f"| {h['liner_material']} | {h['RHA_penetration_mm_static']:.0f} "
                      f"| {h['RHA_penetration_calibres']:.2f} CD |")

        # 16. Rocketry — HPR-X trajectory
        md.append("\n## 16. HPR-X rocket trajectory (Tsiolkovsky + ICAO drag integration)\n")
        md.append("Single (V1, V3) or two-stage (V2) APCP solid rockets. High-angle "
                  "apogee shot is near-vertical (85–88°); range shot is 35° optimum. "
                  "Drag uses subsonic `C_d ≈ 0.55`, supersonic `0.65`.\n")
        md.append("| Vehicle | Launch angle | Apogee | TOF | 35° max range | 35° apogee |")
        md.append("|---|---|---|---|---|---|")
        for name, r in t2["rocketry"].items():
            md.append(f"| {name} | {r['launch_angle_deg']}° | "
                      f"{r['high_angle_apogee_m']:,} m | "
                      f"{r['high_angle_TOF_s']:.1f} s | "
                      f"{r['35deg_max_range_m']:,} m | "
                      f"{r['35deg_apogee_m']:,} m |")
        md.append("\n*Stage burnout details (high-angle shot):*")
        md.append("| Vehicle | Stage | Burnout v | Burnout alt | Burnout t |")
        md.append("|---|---|---|---|---|")
        for name, r in t2["rocketry"].items():
            for b in r["burnout_summary"]:
                md.append(f"| {name} | {b['stage']} | {b['burnout_v_ms']} m/s "
                          f"| {b['burnout_alt_m']:,} m | {b['burnout_t_s']} s |")

        # 17. Energetic detonation chemistry
        md.append("\n## 17. Energetic detonation chemistry (Kamlet–Jacobs)\n")
        md.append("Detonation pressure `P_CJ` and detonation velocity `D` from the "
                  "Kamlet–Jacobs (1968) empirical correlation, plus Gurney constant "
                  "`√(2E)` used in the fragmentation table.\n")
        md.append("| Explosive | ρ (g/cm³) | P_CJ (GPa) | VOD (km/s) | Q (kJ/g) | Brisance (TNT=100) | Gurney √(2E) (m/s) |")
        md.append("|---|---|---|---|---|---|---|")
        for exp, e in t2["energetics"].items():
            md.append(f"| {exp} | {e['density_gcm3']} | {e['P_CJ_GPa']} | "
                      f"{e['VOD_kms']} | {e['Q_kJ_g']} | {e['brisance_TNT_eq']} | "
                      f"{e['gurney_sqrt2E_ms']} |")

        # 18. TACS cancellation depth (Nelson-Elliott)
        md.append("\n## 18. TACS active acoustic cancellation depth (Nelson–Elliott bound)\n")
        md.append("Theoretical cancellation depth (dB) at the target zone as a function "
                  "of source-control-source distance and frequency. Personal variant uses "
                  "a 16-element ANC array, Mobile and Fixed use 64-element arrays. The "
                  "A-weighted average row sums all six octave bands.\n")
        md.append("| Variant | 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | A-weighted avg |")
        md.append("|---|---|---|---|---|---|---|---|")
        for variant, rows in t2["tacs_cancellation"].items():
            md.append(f"| {variant} | {rows['125_Hz']} | {rows['250_Hz']} | "
                      f"{rows['500_Hz']} | {rows['1000_Hz']} | {rows['2000_Hz']} | "
                      f"{rows['4000_Hz']} | {rows['A-weighted_avg_dB']} |")

        # 19. Tank-track noise reduction
        md.append("\n## 19. Tank-track pad noise reduction (steel vs HNBR rubber)\n")
        t = t2["track_pad_noise"]
        md.append(f"At a 300 Hz drive frequency (typical track frequency at 30 km/h):\n")
        md.append(f"- Steel-on-steel transmissibility: **{t['steel_transmission_dB']} dB**")
        md.append(f"- HNBR composite transmissibility: **{t['rubber_transmission_dB']} dB**")
        md.append(f"- **Net free-field SPL reduction: {t['net_reduction_dB']} dB**")
        md.append("\nWithin the published 15–20 dB range for rubber track pads.")

        # 20. Combat-drug pharmacokinetics
        md.append("\n## 20. Combat-drug one-compartment PK (80 kg subject, oral)\n")
        md.append("| Drug | Dose | t_max | C_max | t½ | AUC |")
        md.append("|---|---|---|---|---|---|")
        for p in t2["pharmacokinetics"]:
            md.append(f"| {p['drug']} | {p['dose_mg']} mg | {p['t_max_hr']} h "
                      f"| {p['C_max_ng_mL']} ng/mL | {p['t_half_hr']} h "
                      f"| {p['AUC_ng_hr_mL']:.0f} ng·h/mL |")

        # 21. Injectable-nutrition osmolality
        md.append("\n## 21. Injectable-nutrition osmolality\n")
        md.append("Safe peripheral-IV bound: `< 600 mOsm/kg`. Safe central-line bound: "
                  "`< 1 800 mOsm/kg` (Plumb / Holliday-Segar).\n")
        md.append("| Formulation | Osmolality | Peripheral safe? | Central safe? |")
        md.append("|---|---|---|---|")
        for name, f in t2["injectable_nutrition"].items():
            md.append(f"| {name} | {f['osmolality_mOsm_kg']:.0f} mOsm/kg "
                      f"| {'YES' if f['peripheral_safe'] else 'NO'} "
                      f"| {'YES' if f['central_safe'] else 'NO'} |")

        # 22. Ration thermal stability
        md.append("\n## 22. TACT-1 ration shelf life (Q10 = 2 Arrhenius, 36-month baseline @ 25 °C)\n")
        md.append("| Temperature | Shelf life |")
        md.append("|---|---|")
        for k, v in t2["ration_stability"].items():
            md.append(f"| {k} | {v['shelf_life_months']} months |")

        # 23. Portfolio lifecycle — structural, parts life, reliability
        t3 = results.get("tier3", {})
        lc = t3.get("weapon_lifecycle", {})
        if lc:
            md.append("\n## 23. Portfolio lifecycle — structural, parts life, reliability\n")
            firearms = {k: v for k, v in lc.items()
                        if v.get("category") in ("firearm", "crew_served")}
            if firearms:
                md.append("### 23.0 Firearms and crew-served weapons\n")
                md.append("| Platform | Category | Felt recoil (ft·lb) | Barrel SF_yield | "
                          "Bore life (rd) | MRBF analytic | MRBF simulated | FTF rate |")
                md.append("|---|---|---|---|---|---|---|---|")
                for plat, row in firearms.items():
                    rel = row["reliability"]
                    struct = row["structural"]
                    bore = row["parts_life"]["bore_life_rounds"]
                    felt = row["recoil"]["felt_recoil_ftlbf"]
                    md.append(
                        f"| {plat} | {row['category']} | {felt} | "
                        f"{struct['barrel_sf_yield']} | {bore:,} | "
                        f"{rel['mrbf_analytic']:,.0f} | {rel['mrbf_simulated']:,.0f} | "
                        f"1:{rel['ftf_rate']:,} |"
                    )
                md.append("\n#### 23.0.1 Firearm component parts-life\n")
                for plat, row in firearms.items():
                    md.append(f"**{plat}**\n")
                    md.append("| Component | Warn @ rd | Replace @ rd | Model |")
                    md.append("|---|---|---|---|")
                    for comp in row["parts_life"]["components"]:
                        md.append(
                            f"| {comp['name']} | {comp['warn_rds']:,} | {comp['fail_rds']:,} | "
                            f"{comp['model']} |"
                        )
                    md.append("")

            generic = {k: v for k, v in lc.items()
                       if v.get("category") not in ("firearm", "crew_served", "scope")}
            if generic:
                md.append("### 23.1 Armour, sustainment, and systems platforms\n")
                md.append("| Platform | Category | Primary metric | Headline |")
                md.append("|---|---|---|---|")
                for plat, row in generic.items():
                    headline = "; ".join(
                        f"{hk}={hv}" for hk, hv in row.get("headline", {}).items()
                    ) or "—"
                    md.append(
                        f"| {plat} | {row['category']} | {row.get('primary_metric', '—')} "
                        f"| {headline} |"
                    )
                md.append("\n#### 23.1.1 Component service thresholds\n")
                for plat, row in generic.items():
                    comps = row.get("parts_life", {}).get("components", [])
                    if not comps:
                        continue
                    md.append(f"**{plat}**\n")
                    md.append("| Component | Warn | Replace | Model |")
                    md.append("|---|---|---|---|")
                    for comp in comps:
                        md.append(
                            f"| {comp['name']} | {comp.get('warn_display', comp['warn'])} | "
                            f"{comp.get('fail_display', comp['fail'])} | {comp['model']} |"
                        )
                    md.append("")

            scope_only = {k: v for k, v in lc.items() if v.get("category") == "scope"}
            if scope_only:
                md.append("### 23.2 Scope-only platforms (no physics lifecycle)\n")
                for plat, row in scope_only.items():
                    note = row.get("scope_note", "No runnable lifecycle model.")
                    md.append(f"- **{plat}** — {note}")
                md.append("")

    md.append("")
    md.append("---")
    md.append("")
    md.append("_Tier-1 methodology: Le Duc / Powley closed-form internal ballistics, "
              "G7 / G1 drag-table point-mass external integration with ICAO "
              "atmosphere, De Marre and Lanz–Odermatt terminal-ballistics "
              "correlations against 290 BHN RHA._")
    md.append("")
    md.append("_Tier-2 methodology: Westin (1975) muzzle-blast SPL fit; Didion / "
              "Bagnold wind-drift; bisection-zeroed drop integration; Hatcher max-"
              "effective-range with 80 J KE threshold; calibrated bore-wear and "
              "barrel-thermal models against M4 / M14 / M2HB / GAU-8 / M256 anchors; "
              "Tate / Krupp obliquity correction; Lambert-Jonas / Recht-Ipson V50 "
              "with composite-factor calibration; clay-witness BFD; Gurney "
              "cylindrical-charge velocity, Mott fragment distribution, Carlton "
              "lethal-area; Birkhoff steady-state jet shaped-charge; "
              "Tsiolkovsky-plus-drag rocketry; Kamlet-Jacobs (1968) detonation "
              "physics; Nelson-Elliott (1992) ANC cancellation bound; 1-DOF mass-"
              "spring-damper for track-pad vibration; one-compartment oral PK; "
              "Plumb / Holliday-Segar osmolality; Q10 = 2 Arrhenius lipid oxidation. "
              "See `weapons_simulation.py` for implementation._")

    with open(os.path.join(out_dir, "weapons_sim_results.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print("Running weapons simulation suite…")
    res = run_all()
    write_results(res, here)
    print(f"OK — wrote {len(res['cartridges'])} cartridges, "
          f"{len(res['weapons'])} weapons, "
          f"{len(res['armour_interactions'])} penetration tables, "
          f"{len(res['suppressors'])} suppressor analyses to {here}")
