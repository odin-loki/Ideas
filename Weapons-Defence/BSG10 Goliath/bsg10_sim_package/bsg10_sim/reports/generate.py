"""
BSG-10 Simulation Suite — Report Generator
===========================================
Aggregates all module results into a single text report.
"""

from __future__ import annotations
from datetime import datetime
from ..config import BSG10Config, DEFAULT_CONFIG, OUTPUT_DIR


def generate(
    bal,       # BallisticsResult
    act,       # ActionResult
    rec,       # RecoilResult
    dim,       # DimResult
    mag,       # MagazineResult
    lif,       # LifeResult
    cfg: BSG10Config = DEFAULT_CONFIG,
    save: bool = True,
) -> str:

    c  = cfg.cartridge
    s  = cfg.system
    a  = cfg.action

    now = datetime.now().strftime("%Y-%m-%d  %H:%M")
    loaded_mass = s.loaded_mass(mag.capacity)

    report = f"""
================================================================================
BSG-10 "GOLIATH" — 10-GAUGE SEMI-AUTO BULLPUP COMBAT SHOTGUN
FULL SIMULATION SUITE RESULTS
Generated: {now}
================================================================================

MODULE A — INTERNAL BALLISTICS
  Peak pressure             : {bal.P_peak/1e6:.2f} MPa  ({bal.P_peak/6894.76:.0f} PSI)
  SAAMI 10-ga limit         : {c.saami_limit/1e6:.1f} MPa  (11,000 PSI)
  SAAMI margin              : {(c.saami_limit - bal.P_peak)/c.saami_limit*100:.1f}%  {'PASS' if bal.saami_pass else '*** FAIL ***'}
  Muzzle velocity           : {bal.muzzle_vel:.1f} m/s  ({bal.muzzle_vel*3.2808:.0f} fps)
  Barrel transit time       : {bal.transit_time*1e3:.2f} ms
  Gas port @ {cfg.barrel.gas_port*1e3:.0f} mm          : {bal.port_pressure/1e6:.1f} MPa  /  {bal.port_velocity:.0f} m/s
  Muzzle pressure           : {bal.muzzle_pressure/1e6:.2f} MPa
  Total recoil impulse      : {bal.impulse_total:.2f} N·s
    Shot:                     {bal.impulse_shot:.2f} N·s
    Gas:                      {bal.impulse_gas:.2f} N·s

MODULE B — BALANCED ACTION
  Gear ratio                : {a.gear_ratio:.3f}  (momentum balance)
  Carrier stroke used       : {act.carrier_stroke_mm:.1f} mm  (limit {a.carrier_stroke*1e3:.0f} mm)  {'PASS' if act.stroke_pass else 'FAIL'}
  Max carrier velocity      : {act.carrier_vel_max:.2f} m/s
  Max counter-mass velocity : {act.counter_vel_max:.2f} m/s
  Cycling impulse (raw)     : {act.impulse_raw:.3f} N·s
  Cycling impulse (balanced): {act.impulse_balanced:.3f} N·s
  Cycling reduction         : {act.reduction_pct:.1f}%

MODULE C — INTEGRATED RECOIL
  Raw impulse               : {rec.I_raw:.2f} N·s
  After compensator (−{cfg.recoil.comp_efficiency*100:.0f}%) : {rec.I_after_comp:.2f} N·s
  Gun free-recoil velocity  : {rec.v0_gun:.3f} m/s
  CBS-10 max compression    : {rec.cbs_max_travel_mm:.1f} mm  (limit {cfg.recoil.cbs_travel*1e3:.0f} mm)  {'PASS' if rec.travel_pass else 'FAIL'}
  Peak force (analytical)   : {rec.peak_force_bound:.0f} N  (conservative)
  Peak force (time-domain)  : {rec.peak_force_td:.0f} N  (integrated)
  12-ga field gun reference : {rec.ref_12ga_N:.0f} N
  Raw 10-ga estimate        : {rec.raw_10ga_est_N:.0f} N
  Reduction vs raw 10-ga    : {rec.reduction_pct:.1f}%

MODULE D — DIMENSIONAL GEOMETRY
  Overall Length (OAL)      : {dim.oal_mm:.0f} mm  ({dim.oal_mm/25.4:.1f} in)
  Bore height               : {dim.bore_height_mm:.0f} mm  (target < 160 mm)
  Foregrip from butt        : {dim.fg_from_butt_mm:.0f} mm  (zone 450–720 mm)
  CBS-10 damper gap         : {dim.cbs_damper_gap_mm:.0f} mm  (need > 22 mm)
  Barrel radial clearance   : {dim.barrel_radial_cl_mm:.2f} mm  (sliding fit)
  Carrier stroke clearance  : {dim.carrier_stroke_mm:.1f} mm  used of {a.carrier_stroke*1e3:.0f} mm
  All dimensional checks    : {'ALL PASS' if dim.all_pass else '*** CHECKS FAILED ***'}

MODULE E — MAGAZINE GEOMETRY
  Drum outer diameter       : {cfg.magazine.drum_od*1e3:.0f} mm
  Drum depth                : {mag.drum_depth_mm:.1f} mm
  Coil turns                : {mag.n_coils:.2f}
  Belt length               : {mag.track_length_mm:.0f} mm
  Shell capacity            : {mag.capacity} rounds
  Feed force (full)         : {mag.feed_force_full:.1f} N
  Feed force (last round)   : {mag.feed_force_last:.1f} N  ({'PASS' if mag.feed_pass else 'FAIL — upsize spring'})

MODULE F — PARTS LIFE
  {'Component':<40s} {'Life (rounds)':>14s}  Action
  {'─'*68}"""

    from ..lifecycle.parts_life import ComponentLife
    sorted_comp = sorted(lif.components, key=lambda c: c.fail_rds)
    for comp in sorted_comp:
        report += f"\n  {comp.name:<40s} {comp.fail_rds:>14,}  {comp.action}"

    report += f"""

  Bolt lug fatigue SF       : {lif.lug_SF_fatigue:.1f}×  ({'INFINITE life' if lif.lug_SF_fatigue >= 1.0 else 'FINITE life'})
  Life-limiting component   : {sorted_comp[0].name} @ {sorted_comp[0].fail_rds:,} rounds

WEIGHT SUMMARY
  Gun empty                 : {s.gun_empty:.2f} kg
  Drum magazine (empty)     : {s.drum_empty:.2f} kg
  {mag.capacity} × 10-ga shells         : {mag.capacity * s.round_mass:.2f} kg
  Total loaded              : {loaded_mass:.2f} kg  ({loaded_mass*2.205:.1f} lb)

MAINTENANCE SCHEDULE
  Every   500 rounds : Clean gas, lube action rails, inspect bolt face
  Every 2,000 rounds : Replace extractor spring, check bushing play
  Every 5,000 rounds : Replace gas piston, inspect Belleville stack
  Every {lif.pad_life:,} rounds : Replace CBS-10 viscoelastic pads (D3O + Sorbothane)
  Every {lif.barrel_life:,} rounds : Replace barrel, rebuild CBS-10 dampers
  Every {lif.bell_warn:,} rounds : Replace Belleville washers
  Every 40,000 rounds: Full depot overhaul

OVERALL STATUS
  All SAAMI pressure checks : {'PASS' if bal.saami_pass else 'FAIL'}
  All dimensional checks    : {'PASS' if dim.all_pass else 'FAIL'}
  Bolt lug fatigue          : {'PASS (infinite life)' if lif.lug_SF_fatigue >= 1.0 else 'FAIL'}
  Magazine feed reliability : {'PASS' if mag.feed_pass else 'FAIL'}
  CBS-10 travel             : {'PASS' if rec.travel_pass else 'FAIL'}
  Carrier stroke            : {'PASS' if act.stroke_pass else 'FAIL'}
  Felt recoil vs 12-ga      : {'SOFTER' if rec.peak_force_td < rec.ref_12ga_N else 'COMPARABLE'}

================================================================================
"""

    if save:
        path = f"{OUTPUT_DIR}/simulation_report.txt"
        with open(path, "w") as f:
            f.write(report)
        print(f"\n  → Report saved: simulation_report.txt")

    return report
