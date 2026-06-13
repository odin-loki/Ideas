"""
Weapons-Defence — per-platform claim verification runner
========================================================

Each platform subfolder with a SIM_README.md also contains
``platform_simulation.py``, which calls ``main(<platform_id>)`` here.

The portfolio physics engine (``weapons_simulation.py``) computes every
ballistic, energetic, acoustic, armour, PK, and sustainment number in
the spec sheets. This module runs that engine once, extracts the slice
relevant to one platform, and prints a human-readable verification
report showing what was simulated and which headline numbers were derived.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

PORTFOLIO_ROOT = Path(__file__).resolve().parent


def _configure_stdio() -> None:
    """Avoid Windows cp1252 crashes on physics-unit Unicode in reports."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Portfolio import
# ---------------------------------------------------------------------------

def _load_results() -> Dict[str, Any]:
    sys.path.insert(0, str(PORTFOLIO_ROOT))
    import weapons_simulation as ws  # noqa: PLC0415

    return ws.run_all()


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _banner(title: str) -> None:
    line = "=" * 72
    print(line)
    print(title)
    print(line)


def _section(title: str) -> None:
    print(f"\n--- {title} ---")


def _kv(rows: List[Tuple[str, Any]]) -> None:
    w = max(len(k) for k, _ in rows) if rows else 0
    for k, v in rows:
        print(f"  {k:<{w}}  {v}")


def _table(headers: List[str], rows: List[List[Any]]) -> None:
    str_rows = [[str(c) for c in r] for r in rows]
    widths = [len(h) for h in headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * w for w in widths]))
    for row in str_rows:
        print(fmt.format(*row))


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------

def _cartridge(results: Dict, key: str) -> Dict:
    return results["cartridges"][key]


def _weapon(results: Dict, key: str) -> Dict:
    return results["weapons"][key]


def _penetration(results: Dict, key: str) -> Optional[List[Dict]]:
    return results.get("armour_interactions", {}).get(key)


def _tier2(results: Dict) -> Dict:
    return results.get("tier2", {})


def _tier3(results: Dict) -> Dict:
    return results.get("tier3", {})


def _lifecycle_data(results: Dict, platform: str) -> Optional[Dict]:
    t3 = _tier3(results)
    return (t3.get("weapon_lifecycle") or t3.get("mp46_lifecycle", {})).get(platform)


def _print_platform_lifecycle(results: Dict, platform: str) -> None:
    lc = _lifecycle_data(results, platform)
    if not lc:
        return
    cat = lc.get("category", "firearm")
    _section(f"Lifecycle / reliability (§23) — {platform}")

    if cat == "scope":
        print(f"  {lc.get('scope_note', 'Scope-only — no physics lifecycle model.')}")
        return

    if cat in ("firearm", "crew_served"):
        rel = lc["reliability"]
        struct = lc["structural"]
        parts = lc["parts_life"]
        rec = lc["recoil"]
        rows = [
            ("Category", cat),
            ("Felt recoil", f"{rec['felt_recoil_ftlbf']} ft·lb"),
            ("Barrel SF_yield", struct["barrel_sf_yield"]),
            ("Bore life", f"{parts['bore_life_rounds']:,} rounds"),
            ("MRBF analytic", f"{rel['mrbf_analytic']:,.0f} rounds"),
            ("MRBF simulated", f"{rel['mrbf_simulated']:,.0f} rounds"),
            ("MRBF 90% CI",
             f"[{rel['mrbf_ci_90_low']:,.0f} – {rel['mrbf_ci_90_high']:,.0f}]"),
            ("FTF rate", f"1:{rel['ftf_rate']:,}"),
        ]
        if struct.get("spring_fatigue_sf") is not None:
            rows.insert(4, ("Spring fatigue SF", struct["spring_fatigue_sf"]))
        if parts.get("tier2_barrel_rounds"):
            rows.insert(4, ("Tier-2 barrel life (§10)",
                            f"{parts['tier2_barrel_rounds']:,} rounds"))
        _kv(rows)
        _section("Component parts-life")
        headers = ["Component", "Warn @ rd", "Replace @ rd", "Action"]
        comp_rows = [[c["name"], f"{c['warn_rds']:,}", f"{c['fail_rds']:,}", c["action"]]
                     for c in parts["components"]]
        _table(headers, comp_rows)
        return

    headline = lc.get("headline", {})
    if headline:
        _kv([(k.replace("_", " ").title(), v) for k, v in headline.items()])
    comps = lc.get("parts_life", {}).get("components", [])
    if comps:
        _section("Component service thresholds")
        headers = ["Component", "Warn", "Replace", "Action"]
        comp_rows = [[c["name"], c.get("warn_display", c["warn"]),
                      c.get("fail_display", c["fail"]), c["action"]]
                     for c in comps]
        _table(headers, comp_rows)
    rel = lc.get("reliability")
    if rel:
        _kv([
            ("MRBF analytic", f"{rel['mrbf_analytic']:,.0f}"),
            ("MRBF simulated", f"{rel['mrbf_simulated']:,.0f}"),
        ])


def _print_mp46_lifecycle(results: Dict, platform: str) -> None:
    """Backward-compatible alias."""
    _print_platform_lifecycle(results, platform)


def _print_cartridge(results: Dict, key: str) -> None:
    c = _cartridge(results, key)
    _section(f"Cartridge internal ballistics — {key}")
    _kv([
        ("Muzzle velocity", f"{c['muzzle_velocity_ms']:.1f} m/s"),
        ("Muzzle energy", f"{c['muzzle_energy_J']:.0f} J"),
        ("Peak chamber pressure", f"{c['chamber_pressure_max_MPa']:.1f} MPa "
         f"({c['chamber_pressure_max_psi']:.0f} psi)"),
        ("Recoil impulse", f"{c['recoil_impulse_Ns']:.2f} N·s"),
    ])


def _print_weapon(results: Dict, key: str) -> None:
    w = _weapon(results, key)
    _section(f"Weapon platform — {key}")
    _kv([
        ("Cartridge", w["cartridge"]),
        ("Empty mass", f"{w['weight_empty_kg']} kg"),
        ("Magazine", w["magazine_capacity"]),
        ("Action", w["action"]),
        ("Free recoil", f"{w['free_recoil_energy_J']} J "
         f"({w['free_recoil_energy_ftlb']} ft·lb)"),
    ])


def _print_penetration_sample(results: Dict, key: str,
                              ranges: Optional[List[int]] = None) -> None:
    rows = _penetration(results, key)
    if not rows:
        _section(f"RHA penetration — {key}")
        print("  n/a — warhead platform (no KE penetrator in portfolio sim)")
        return
    _section(f"RHA penetration — {key}")
    if ranges is None:
        ranges = [0, 500, 1000, 2000]
    for r in rows:
        if r["range_m"] in ranges:
            _kv([(f"@ {r['range_m']} m",
                  f"{r['rha_penetration_mm']} mm RHA "
                  f"(v={r['velocity_ms']} m/s)")])
    obliq = _tier2(results).get("obliquity_penetration", {}).get(key, [])
    if obliq:
        muzzle = next((o for o in obliq if o["range_m"] == 0), None)
        if muzzle:
            _kv([("60° oblique RHA @ 0 m",
                  f"{muzzle['rha_60deg_mm']} mm")])


def _print_suppressor(results: Dict, key: str) -> None:
    s = results.get("suppressors", {}).get(key)
    if not s:
        return
    _section(f"Suppressor — {key}")
    _kv([
        ("Attenuation", f"{s['attenuation_dB']} dB"),
        ("Suppressor volume", f"{s['suppressor_volume_cm3']} cm³"),
        ("Baffles", s["baffle_count"]),
    ])


def _print_weapon_acoustic(results: Dict, weapon_key: str) -> None:
    a = _tier2(results).get("acoustic", {}).get(weapon_key)
    if not a:
        return
    _section(f"Muzzle blast & hearing protection — {weapon_key}")
    _kv([
        ("Muzzle SPL (unsuppressed)", f"{a['muzzle_dB_unsuppressed']} dB"),
        ("Shooter ear (unsuppressed)", f"{a['shooter_ear_dB_unsuppressed']} dB"),
        ("Muzzle SPL (suppressed)", f"{a['muzzle_dB_suppressed']} dB"),
        ("Ear + single plug", f"{a['ear_dB_with_single_plug']} dB"),
        ("Ear + double plug/muff", f"{a['ear_dB_with_double_plug_muff']} dB"),
        ("Ear + double + TACS", f"{a['ear_dB_with_TACS_personal']} dB"),
    ])


def _print_aux_ballistics(results: Dict, cartridge_key: str) -> None:
    aux = _tier2(results).get("aux_ballistics", {}).get(cartridge_key)
    if not aux:
        return
    _section(f"Auxiliary ballistics — {cartridge_key}")
    _kv([
        ("Zero range", f"{aux['zero_range_m']} m"),
        ("Max effective range (80 J KE)", f"{aux['max_effective_range_m_against_personnel']} m"),
        ("Supersonic range", f"{aux['supersonic_range_m']} m"),
    ])
    if aux.get("wind_drift_m_10mph_crosswind"):
        _section("Wind drift (10 mph crosswind)")
        for row in aux["wind_drift_m_10mph_crosswind"][:4]:
            print(f"  @ {row['range_m']} m: {row['drift_m_10mph']} m drift")


def _print_barrel_life(results: Dict, weapon_key: str) -> None:
    b = _tier2(results).get("barrel", {}).get(weapon_key)
    if not b:
        return
    _section(f"Barrel life & sustained fire — {weapon_key}")
    _kv([
        ("Barrel life (rounds)", f"{b['barrel_life_rounds']:,}"),
        ("Thermal sustained RPM", b.get("sustained_rpm_thermal_bound", "N/A")),
    ])


def _print_recoil_detail(results: Dict, weapon_key: str) -> None:
    r = _tier2(results).get("recoil_detail", {}).get(weapon_key)
    if not r:
        return
    _section(f"Peak recoil force — {weapon_key}")
    _kv([
        ("Peak recoil force", f"{r['peak_recoil_force_N']} N"),
        ("Stock travel", f"{r['stock_travel_mm']} mm"),
    ])


def _print_armour_panel(results: Dict, panel_name: str) -> None:
    panel = _tier2(results).get("armour_v50", {}).get(panel_name)
    if not panel:
        return
    _section(f"Body armour V50 — {panel_name}")
    headers = ["Threat", "V50 (m/s)", "Threat v", "Outcome", "BFD (mm)"]
    rows = []
    for threat, row in panel.items():
        bfd = row["back_face_deformation_mm"]
        bfd_s = "PERF" if bfd is None else f"{bfd}"
        rows.append([
            threat[:40], row["V50_ms"], row["threat_velocity_ms"],
            row["outcome"], bfd_s,
        ])
    _table(headers, rows)


def _print_frag(results: Dict, warhead_name: str) -> None:
    f = _tier2(results).get("fragmentation", {}).get(warhead_name)
    if not f:
        return
    _section(f"HE-Frag lethality — {warhead_name}")
    _kv([
        ("Fragment velocity", f"{f['fragment_velocity_ms']} m/s"),
        ("Fragment count (>0.5 g)", f"{f['fragment_count_above_0.5_g']:,}"),
        ("Lethal area", f"{f['lethal_area_m2']} m²"),
        ("Effective radius", f"{f['effective_radius_m']} m"),
    ])


def _print_heat(results: Dict, warhead_name: str) -> None:
    h = _tier2(results).get("shaped_charge", {}).get(warhead_name)
    if not h:
        return
    _section(f"Shaped-charge penetration — {warhead_name}")
    _kv([
        ("Static RHA penetration", f"{h['RHA_penetration_mm_static']} mm"),
        ("Penetration (calibres)", h["RHA_penetration_calibres"]),
    ])


def _print_rocketry(results: Dict) -> None:
    hpr = _tier2(results).get("rocketry", {})
    _section("HPR-X rocket trajectory (portfolio §16)")
    headers = ["Variant", "Apogee (m)", "35-deg range (m)", "TOF (s)"]
    rows = []
    for name, row in hpr.items():
        rows.append([
            name[:35],
            row["high_angle_apogee_m"],
            row["35deg_max_range_m"],
            row["high_angle_TOF_s"],
        ])
    _table(headers, rows)


def _print_energetics(results: Dict, explosives: Optional[List[str]] = None) -> None:
    ener = _tier2(results).get("energetics", {})
    _section("Kamlet–Jacobs detonation chemistry (portfolio §17)")
    headers = ["Explosive", "rho (g/cm3)", "P_CJ (GPa)", "VOD (km/s)", "Brisance"]
    rows = []
    for name, row in ener.items():
        if explosives and name not in explosives:
            continue
        rows.append([
            name, row["density_gcm3"], row["P_CJ_GPa"],
            row["VOD_kms"], row["brisance_TNT_eq"],
        ])
    _table(headers, rows)


def _print_tacs(results: Dict) -> None:
    tacs = _tier2(results).get("tacs_cancellation", {})
    _section("TACS active cancellation depth (portfolio §18)")
    for variant, bands in tacs.items():
        print(f"\n  {variant}")
        freqs = ["125_Hz", "250_Hz", "500_Hz", "1000_Hz", "2000_Hz", "4000_Hz"]
        vals = [str(bands.get(f, "")) for f in freqs]
        _table(["125", "250", "500", "1k", "2k", "4k", "A-wt"], [vals + [bands.get("A-weighted_avg_dB", "")]])


def _print_track_pad(results: Dict) -> None:
    tp = _tier2(results).get("track_pad_noise", {})
    _section("Rubber track-pad noise reduction (portfolio §19)")
    _kv([
        ("Steel transmissibility", f"{tp.get('steel_transmission_dB', 'N/A')} dB"),
        ("HNBR transmissibility", f"{tp.get('rubber_transmission_dB', 'N/A')} dB"),
        ("Net SPL reduction", f"{tp.get('net_reduction_dB', 'N/A')} dB"),
    ])


def _print_pk(results: Dict) -> None:
    pk = _tier2(results).get("pharmacokinetics", [])
    _section("Combat-drug PK (portfolio §20)")
    headers = ["Drug", "Dose", "t_max (h)", "C_max", "t½ (h)", "AUC"]
    rows = []
    for row in pk:
        rows.append([
            row["drug"][:45], row["dose_mg"], row["t_max_hr"],
            row["C_max_ng_mL"], row["t_half_hr"], row["AUC_ng_hr_mL"],
        ])
    _table(headers, rows)


def _print_injectable(results: Dict) -> None:
    inj = _tier2(results).get("injectable_nutrition", {})
    _section("Injectable nutrition osmolality (portfolio §21)")
    headers = ["Formulation", "Osmolality (mOsm/kg)", "Peripheral safe (<600)"]
    rows = [[n, v["osmolality_mOsm_kg"], v["peripheral_safe"]]
            for n, v in inj.items()]
    _table(headers, rows)


def _print_ration(results: Dict) -> None:
    ration = _tier2(results).get("ration_stability", {})
    _section("TACT-1 ration shelf life (portfolio §22)")
    headers = ["Temperature", "Shelf life (months)"]
    rows = [[k, v["shelf_life_months"]] for k, v in ration.items()]
    _table(headers, rows)


def _print_scope_limit(note: str) -> None:
    _section("Scope limit")
    print(f"  {note}")


def _claim_checks(checks: List[Tuple[str, float, float, float]]) -> None:
    """Print PASS/FAIL for (label, actual, expected, abs_tolerance)."""
    _section("Claim verification (vs weapons_sim_results.md)")
    for label, actual, expected, tol in checks:
        ok = abs(actual - expected) <= tol
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {actual} (expected {expected} ±{tol})")


def _lifecycle_claims(
    results: Dict,
    platform: str,
    specs: List[Tuple[str, str, float, float]],
) -> None:
    """Verify §23 headline metrics: (headline_key, label, expected, abs_tolerance)."""
    lc = _lifecycle_data(results, platform) or {}
    hd = lc.get("headline", {})
    checks: List[Tuple[str, float, float, float]] = []
    for key, label, expected, tol in specs:
        if key in hd and hd[key] is not None:
            checks.append((label, float(hd[key]), expected, tol))
    if checks:
        _claim_checks(checks)


def _run_subprocess(script: Path, *args: str) -> int:
    print(f"\n>>> Running standalone sim: {script.name} {' '.join(args)}")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.call(
        [sys.executable, str(script), *args],
        cwd=str(script.parent),
        env=env,
    )


# ---------------------------------------------------------------------------
# Platform handlers
# ---------------------------------------------------------------------------

Handler = Callable[[Dict[str, Any]], Dict[str, Any]]


def _weapon_full(results: Dict, weapon: str, cartridge: str,
                 suppressor: Optional[str] = None,
                 pen_ranges: Optional[List[int]] = None,
                 claim_checks: Optional[List[Tuple[str, float, float, float]]] = None,
                 lifecycle_platform: Optional[str] = None,
                 ) -> Dict[str, Any]:
    _print_cartridge(results, cartridge)
    _print_weapon(results, weapon)
    _print_penetration_sample(results, cartridge, ranges=pen_ranges)
    if suppressor:
        _print_suppressor(results, suppressor)
    _print_weapon_acoustic(results, weapon)
    _print_aux_ballistics(results, cartridge)
    _print_barrel_life(results, weapon)
    _print_recoil_detail(results, weapon)
    if lifecycle_platform:
        _print_platform_lifecycle(results, lifecycle_platform)
    if claim_checks:
        _claim_checks(claim_checks)
    return {"weapon": weapon, "cartridge": cartridge}


def _verify_mp46m_guardian(results: Dict) -> Dict[str, Any]:
    _banner("MP-4.6M Guardian Pistol — claim verification")
    print("Physics: portfolio weapons_simulation.py (Tier-1 + Tier-2 + §23 lifecycle)")
    pen = _penetration(results, "4.6x30mm")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "MP-4.6M Pistol")
    lc = _lifecycle_data(results, "MP-4.6M Pistol") or {}
    rel = lc.get("reliability", {})
    rec = lc.get("recoil", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 501.0, 1.0),
        ("Muzzle energy (J)", w["muzzle_energy_J"], 326.0, 2.0),
        ("RHA @ 0 m (mm)", p0, 3.8, 0.2),
        ("Free recoil (J)", w["free_recoil_energy_J"], 1.5, 0.2),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 20_270.0, 800.0),
        ("Felt recoil (ft·lb)", rec.get("felt_recoil_ftlbf", 0), 0.11, 0.04),
    ]
    return _weapon_full(results, "MP-4.6M Pistol", "4.6x30mm",
                        "MP-4.6M Pistol integral",
                        pen_ranges=[0, 500, 1000],
                        claim_checks=checks,
                        lifecycle_platform="MP-4.6M Pistol")


def _verify_mp46m_defender(results: Dict) -> Dict[str, Any]:
    _banner("MP-4.6M Defender PDW — claim verification")
    print("Physics: portfolio weapons_simulation.py (Tier-1 + Tier-2 + §23 lifecycle)")
    pen = _penetration(results, "4.6x30mm_PDW")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "MP-4.6M Defender PDW")
    lc = _lifecycle_data(results, "MP-4.6M Defender PDW") or {}
    rel = lc.get("reliability", {})
    rec = lc.get("recoil", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 542.0, 1.0),
        ("Muzzle energy (J)", w["muzzle_energy_J"], 382.0, 2.0),
        ("RHA @ 0 m (mm)", p0, 4.2, 0.2),
        ("Free recoil (J)", w["free_recoil_energy_J"], 0.8, 0.2),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 20_000.0, 500.0),
        ("Felt recoil (ft·lb)", rec.get("felt_recoil_ftlbf", 0), 0.125, 0.03),
    ]
    return _weapon_full(results, "MP-4.6M Defender PDW", "4.6x30mm_PDW",
                        "MP-4.6M Defender PDW",
                        pen_ranges=[0, 500, 1000],
                        claim_checks=checks,
                        lifecycle_platform="MP-4.6M Defender PDW")


def _verify_mp46p_guardian_le(results: Dict) -> Dict[str, Any]:
    _banner("MP-4.6P Guardian LE — claim verification")
    print("Physics: portfolio weapons_simulation.py (Tier-1 + Tier-2 + §23 lifecycle)")
    pen = _penetration(results, "4.6x22mm")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "MP-4.6P Guardian LE")
    lc = _lifecycle_data(results, "MP-4.6P Guardian LE") or {}
    rel = lc.get("reliability", {})
    rec = lc.get("recoil", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 396.0, 1.0),
        ("Muzzle energy (J)", w["muzzle_energy_J"], 259.0, 2.0),
        ("Peak pressure (MPa)", w["chamber_pressure_MPa"], 246.0, 2.0),
        ("RHA @ 0 m (mm)", p0, 3.1, 0.3),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 20_548.0, 300.0),
        ("MRBF simulated (rd)", rel.get("mrbf_simulated", 0), 27_778.0, 8000.0),
        ("Felt recoil (ft·lb)", rec.get("felt_recoil_ftlbf", 0), 0.084, 0.015),
        ("FTF rate", float(rel.get("ftf_rate", 0)), 80_000.0, 1.0),
    ]
    return _weapon_full(results, "MP-4.6P Guardian LE", "4.6x22mm",
                        pen_ranges=[0, 100, 300],
                        claim_checks=checks,
                        lifecycle_platform="MP-4.6P Guardian LE")


def _verify_mp68(results: Dict) -> Dict[str, Any]:
    _banner("MP-6.8 Mark II Rifle — claim verification")
    pen = _penetration(results, "6.8x51mm")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "MP-6.8 Mark II Rifle")
    lc = _lifecycle_data(results, "MP-6.8 Mark II Rifle") or {}
    rel = lc.get("reliability", {})
    rec = lc.get("recoil", {})
    parts = lc.get("parts_life", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 731.0, 1.0),
        ("Muzzle energy (J)", w["muzzle_energy_J"], 2324.0, 3.0),
        ("RHA @ 0 m (mm)", p0, 11.1, 0.2),
        ("Free recoil (J)", w["free_recoil_energy_J"], 11.3, 0.3),
        ("Bore life (rd)", parts.get("bore_life_rounds", 0), 25_000.0, 1.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 15_656.0, 1000.0),
        ("Felt recoil (ft·lb)", rec.get("felt_recoil_ftlbf", 0), 1.631, 0.2),
    ]
    return _weapon_full(results, "MP-6.8 Mark II Rifle", "6.8x51mm",
                        "MP-6.8 Mark II Rifle",
                        pen_ranges=[0, 500, 1000],
                        claim_checks=checks,
                        lifecycle_platform="MP-6.8 Mark II Rifle")


def _verify_mas152e(results: Dict) -> Dict[str, Any]:
    _banner("MAS-15.2E Anti-Materiel Sniper — claim verification")
    pen = _penetration(results, "15.2x115mm")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "MAS-15.2E Sniper")
    lc = _lifecycle_data(results, "MAS-15.2E Sniper") or {}
    rel = lc.get("reliability", {})
    parts = lc.get("parts_life", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 781.0, 1.0),
        ("Muzzle energy (J)", w["muzzle_energy_J"], 19505.0, 10.0),
        ("RHA @ 0 m (mm)", p0, 42.0, 0.5),
        ("Free recoil (J)", w["free_recoil_energy_J"], 255.2, 1.0),
        ("Bore life service (rd)", parts.get("bore_life_rounds", 0), 1_500.0, 1.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 35_613.0, 8000.0),
    ]
    return _weapon_full(results, "MAS-15.2E Sniper", "15.2x115mm",
                        "MAS-15.2E Sniper",
                        pen_ranges=[0, 500, 1000, 2000],
                        claim_checks=checks,
                        lifecycle_platform="MAS-15.2E Sniper")


def _verify_57mm_autocannon(results: Dict) -> Dict[str, Any]:
    _banner("57 mm Autocannon — claim verification")
    pen = _penetration(results, "57x347mm")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    w = _weapon(results, "57 mm Autocannon")
    lc = _lifecycle_data(results, "57 mm Autocannon") or {}
    parts = lc.get("parts_life", {})
    rel = lc.get("reliability", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 948.0, 1.0),
        ("RHA @ 0 m (mm)", p0, 139.7, 0.5),
        ("Bore life (rd)", parts.get("bore_life_rounds", 0), 1_166.0, 50.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 8_375.0, 200.0),
    ]
    out = _weapon_full(results, "57 mm Autocannon", "57x347mm",
                       pen_ranges=[0, 500, 1000, 2000],
                       claim_checks=checks,
                       lifecycle_platform="57 mm Autocannon")
    _print_frag(results, "57 mm Autocannon HE-Frag")
    _print_heat(results, "57 mm Autocannon HEDP")
    return out


def _verify_57mm_ubgl(results: Dict) -> Dict[str, Any]:
    _banner("57 mm Underbarrel Grenade — claim verification")
    w = _weapon(results, "57 mm Underbarrel GL")
    c = _cartridge(results, "57mm_LV_grenade")
    lc = _lifecycle_data(results, "57 mm Underbarrel GL") or {}
    parts = lc.get("parts_life", {})
    rel = lc.get("reliability", {})
    checks = [
        ("Muzzle velocity (m/s)", c["muzzle_velocity_ms"], 149.0, 1.0),
        ("Muzzle energy (J)", c["muzzle_energy_J"], 3872.0, 5.0),
        ("Free recoil (J)", w["free_recoil_energy_J"], 578.8, 2.0),
        ("Bore life (rd)", parts.get("bore_life_rounds", 0), 5_000.0, 1.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 13_857.0, 500.0),
    ]
    out = _weapon_full(results, "57 mm Underbarrel GL", "57mm_LV_grenade",
                       claim_checks=checks,
                       lifecycle_platform="57 mm Underbarrel GL")
    _print_frag(results, "57 mm Underbarrel HE-Frag")
    _print_heat(results, "57 mm Underbarrel HEAT")
    frag = _tier2(results).get("fragmentation", {}).get("57 mm Underbarrel HE-Frag", {})
    if frag:
        _claim_checks([("HE-Frag effective radius (m)", frag["effective_radius_m"], 1.9, 0.2)])
    return out


def _verify_57mm_mortar(results: Dict) -> Dict[str, Any]:
    _banner("57 mm Mortar / RPG — claim verification")
    w = _weapon(results, "57 mm Mortar/RPG")
    c = _cartridge(results, "57mm_mortar")
    lc = _lifecycle_data(results, "57 mm Mortar/RPG") or {}
    parts = lc.get("parts_life", {})
    rel = lc.get("reliability", {})
    checks = [
        ("Muzzle velocity (m/s)", c["muzzle_velocity_ms"], 187.0, 1.0),
        ("Muzzle energy (J)", c["muzzle_energy_J"], 24427.0, 10.0),
        ("Free recoil (J)", w["free_recoil_energy_J"], 4965.9, 5.0),
        ("Bore life (rd)", parts.get("bore_life_rounds", 0), 8_000.0, 1.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 11_041.0, 500.0),
    ]
    out = _weapon_full(results, "57 mm Mortar/RPG", "57mm_mortar",
                       claim_checks=checks,
                       lifecycle_platform="57 mm Mortar/RPG")
    _print_frag(results, "57 mm Mortar HE")
    _print_heat(results, "57 mm Mortar/RPG HEAT")
    return out


def _verify_140mm_ke(results: Dict) -> Dict[str, Any]:
    _banner("140 mm Tank KE Round — claim verification")
    pen = _penetration(results, "140mm_KE")
    p0 = pen[0]["rha_penetration_mm"] if pen else 0.0
    p500 = next((r["rha_penetration_mm"] for r in (pen or []) if r["range_m"] == 500), 0.0)
    w = _weapon(results, "140 mm Tank Gun")
    lc = _lifecycle_data(results, "140 mm Tank Gun") or {}
    parts = lc.get("parts_life", {})
    rel = lc.get("reliability", {})
    checks = [
        ("Muzzle velocity (m/s)", w["muzzle_velocity_ms"], 1698.0, 2.0),
        ("RHA @ 0 m (mm)", p0, 867.1, 1.0),
        ("RHA @ 500 m (mm)", p500, 698.1, 1.0),
        ("Bore life (rd)", parts.get("bore_life_rounds", 0), 618.0, 5.0),
        ("MRBF analytic (rd)", rel.get("mrbf_analytic", 0), 3_502.0, 100.0),
    ]
    out = _weapon_full(results, "140 mm Tank Gun", "140mm_KE",
                       pen_ranges=[0, 500, 1000, 2000, 3000],
                       claim_checks=checks,
                       lifecycle_platform="140 mm Tank Gun")
    _print_frag(results, "140 mm Multi-Effect HE-Frag")
    _print_heat(results, "140 mm Multi-Effect HEAT")
    return out


def _verify_apes(results: Dict) -> Dict[str, Any]:
    _banner("APES Body Armour — claim verification")
    print("Physics: portfolio weapons_simulation.py section 13 (V50 + BFD)")
    mil_panel = "APES military (16-layer + 12 mm B4C tile, 35 kg/m²)"
    _print_armour_panel(results, mil_panel)
    _print_armour_panel(results, "APES-L police (10-layer + 8 mm B4C, 22 kg/m²)")
    panel = _tier2(results).get("armour_v50", {}).get(mil_panel, {})
    m855 = panel.get("5.56 × 45 NATO M855 (940 m/s, 4.0 g)")
    if m855:
        _claim_checks([
            ("APES military vs 5.56 M855 — outcome STOPPED",
             1.0 if m855["outcome"] == "STOPPED" else 0.0, 1.0, 0.0),
        ])
    _print_platform_lifecycle(results, "APES Body Armour")
    _lifecycle_claims(results, "APES Body Armour", [
        ("panel_service_life_yr", "Panel service life (yr)", 12.0, 0.5),
    ])
    return {"panels": ["APES military", "APES-L police"]}


def _verify_nacs(results: Dict) -> Dict[str, Any]:
    _banner("NACS CBRN — claim verification")
    _print_scope_limit(
        "NACS chemical / thermal / signature claims are prose-only. "
        "Adjacent ballistic protection is validated via APES panels (§13)."
    )
    _print_armour_panel(results, "APES military (16-layer + 12 mm B4C tile, 35 kg/m²)")
    _print_platform_lifecycle(results, "NACS CBRN")
    _lifecycle_claims(results, "NACS CBRN", [
        ("filter_cartridge_life_mo", "Filter cartridge life (mo)", 6.0, 0.5),
    ])
    return {"adjacent": "APES §13"}


def _verify_alnicyn(results: Dict) -> Dict[str, Any]:
    _banner("AlNiCyN Armour — claim verification")
    _print_scope_limit(
        "AlNiCyN areal-density and alloy-tier claims are not individually "
        "modelled. Portfolio §3 RHA penetration tables anchor heavy-threat "
        "ballistic context."
    )
    _print_penetration_sample(results, "6.8x51mm", [0, 500, 1000])
    _print_penetration_sample(results, "57x347mm", [0, 1000, 3000])
    _print_platform_lifecycle(results, "AlNiCyN Armour")
    _lifecycle_claims(results, "AlNiCyN Armour", [
        ("plate_service_life_yr", "Plate service life (yr)", 15.0, 0.5),
    ])
    return {"baseline_cartridges": ["6.8x51mm", "57x347mm"]}


def _verify_adf_fk(results: Dict) -> Dict[str, Any]:
    _banner("ADF Tactical Field Kit — claim verification")
    _print_scope_limit(
        "Load-carriage mass budget and ergonomics are prose targets in the "
        "spec. Portfolio §22 validates TACT-1 ration thermal stability; "
        "PODS energy chemistry is validated by pods_simulation.py."
    )
    _print_ration(results)
    pods = PORTFOLIO_ROOT / "TACT-1 Tactical Ration" / "PODS- Edible High Energy Protein" / "pods_simulation.py"
    if pods.exists():
        _run_subprocess(pods, "--module", "verify")
    _print_platform_lifecycle(results, "ADF Tactical Field Kit")
    _lifecycle_claims(results, "ADF Tactical Field Kit", [
        ("load_carriage_fabric_yr", "Load carriage fabric (yr)", 8.0, 0.5),
    ])
    return {"ration": True, "pods": pods.exists()}


def _verify_caseless(results: Dict) -> Dict[str, Any]:
    _banner("Caseless Bullets (BPC) — claim verification")
    _print_scope_limit(
        "Protein-casing chemistry and cook-off are NOT modelled. "
        "Conventional 5.56 × 45 mm NATO baseline from §1 anchors "
        "ballistic envelope targets."
    )
    _print_cartridge(results, "5.56x45mm")
    c = _cartridge(results, "5.56x45mm")
    _section("BPC design-target comparison")
    _kv([
        ("Sim MV (5.56 baseline)", f"{c['muzzle_velocity_ms']:.1f} m/s"),
        ("BPC target MV", "900–960 m/s"),
        ("Sim ME", f"{c['muzzle_energy_J']:.0f} J"),
        ("BPC target ME", "~1 700–1 800 J"),
    ])
    _claim_checks([
        ("5.56 baseline MV (m/s)", c["muzzle_velocity_ms"], 939.0, 1.0),
        ("5.56 baseline ME (J)", c["muzzle_energy_J"], 1764.0, 3.0),
    ])
    _print_platform_lifecycle(results, "Caseless Bullets (BPC)")
    _lifecycle_claims(results, "Caseless Bullets (BPC)", [
        ("protein_case_shelf_mo", "Protein case shelf (mo)", 24.0, 0.5),
    ])
    return {"baseline": "5.56x45mm"}


def _verify_combat_drug(results: Dict) -> Dict[str, Any]:
    _banner("Combat Drug — claim verification")
    _print_scope_limit(
        "HSX7 six-novel-compound depot PK is NOT simulated. "
        "§20 models FDA-approved oral stimulant reference stack only."
    )
    _print_pk(results)
    pk = _tier2(results).get("pharmacokinetics", [])
    if pk:
        caf = pk[0]
        _claim_checks([
            ("Caffeine C_max (ng/mL)", caf["C_max_ng_mL"], 4069.5, 5.0),
        ])
    _print_platform_lifecycle(results, "Combat Drug")
    _lifecycle_claims(results, "Combat Drug", [
        ("depot_shelf_cold_chain_mo", "Depot shelf cold chain (mo)", 36.0, 0.5),
    ])
    return {"section": "tier2.pharmacokinetics"}


def _verify_hel_cms(results: Dict) -> Dict[str, Any]:
    _banner("HEL-CMS/DB — claim verification")
    _print_scope_limit(
        "No laser engagement simulator in repo. Dwell-time, irradiance, and "
        "TCO numbers are first-principles derivations in the spec and paper. "
        "This script documents scope only — see HEL_CMS_DB_Full_Spec.md."
    )
    print("\n  To verify: read spec Part I (beam physics) and Part X (TCO).")
    _print_platform_lifecycle(results, "HEL-CMS/DB")
    _lifecycle_claims(results, "HEL-CMS/DB", [
        ("diode_array_life_hr", "Diode array life (hr)", 10_000.0, 100.0),
    ])
    return {"runnable": False}


def _verify_hprx(results: Dict) -> Dict[str, Any]:
    _banner("HPR-X Rocketry — claim verification")
    _print_rocketry(results)
    hpr = _tier2(results).get("rocketry", {})
    v3 = hpr.get("HPR-X V3 (152 mm SOF spotter)", {})
    if v3:
        _claim_checks([
            ("V3 35° max range (m)", v3["35deg_max_range_m"], 6502.0, 50.0),
        ])
    _print_platform_lifecycle(results, "HPR-X Rocketry")
    _lifecycle_claims(results, "HPR-X Rocketry", [
        ("motor_case_life_flights", "Motor case life (flights)", 50.0, 1.0),
    ])
    return {"section": "tier2.rocketry"}


def _verify_hearing(results: Dict) -> Dict[str, Any]:
    _banner("Hearing Protection — claim verification")
    _print_scope_limit(
        "APE-1 / HANC-1 product NRR claims are spec-internal acoustic models. "
        "Portfolio §6 validates threat-side muzzle SPL and layered protection "
        "stack for each weapon."
    )
    acoustic = _tier2(results).get("acoustic", {})
    headers = ["Weapon", "Ear unsup", "Ear sup", "Ear+double", "Ear+TACS"]
    rows = []
    for wk, a in acoustic.items():
        rows.append([
            wk[:28], a["shooter_ear_dB_unsuppressed"],
            a["shooter_ear_dB_suppressed"],
            a["ear_dB_with_double_plug_muff"],
            a["ear_dB_with_TACS_personal"],
        ])
    _section("Per-weapon ear SPL (portfolio §6)")
    _table(headers, rows)
    _print_platform_lifecycle(results, "Hearing Protection")
    _lifecycle_claims(results, "Hearing Protection", [
        ("foam_plug_life_mo", "Foam plug life (mo)", 6.0, 0.5),
    ])
    return {"weapons": list(acoustic.keys())}


def _verify_injectable(results: Dict) -> Dict[str, Any]:
    _banner("Injectable Nutrition — claim verification")
    _print_injectable(results)
    _print_platform_lifecycle(results, "Injectable Nutrition")
    _lifecycle_claims(results, "Injectable Nutrition", [
        ("formulation_shelf_25C_mo", "Formulation shelf @25°C (mo)", 18.0, 0.5),
    ])
    return {"section": "tier2.injectable_nutrition"}


def _verify_doctrine(results: Dict) -> Dict[str, Any]:
    _banner("Military Command Doctrine — claim verification")
    _print_scope_limit(
        "Doctrinal tier sizes, training durations, and force-structure "
        "economics are prose targets — not physics-sim outputs."
    )
    _print_platform_lifecycle(results, "Military Command Doctrine")
    return {"runnable": False}


def _verify_tacs(results: Dict) -> Dict[str, Any]:
    _banner("TACS — claim verification")
    _print_tacs(results)
    tacs = _tier2(results).get("tacs_cancellation", {})
    personal = tacs.get("Personal (3-5 m zone, 16-element wearable)", {})
    if personal:
        _claim_checks([
            ("Personal A-weighted avg (dB)", personal["A-weighted_avg_dB"], 36.3, 0.2),
        ])
    _print_platform_lifecycle(results, "TACS Military Noise Cancellation")
    _lifecycle_claims(results, "TACS Military Noise Cancellation", [
        ("wearable_array_service_yr", "Wearable array service (yr)", 8.0, 0.5),
    ])
    return {"section": "tier2.tacs_cancellation"}


def _verify_obsidian(results: Dict) -> Dict[str, Any]:
    _banner("OBSIDIAN Body Armour — claim verification")
    _print_scope_limit(
        "Hypothetical carbyne / STF suit — no ballistic simulator. "
        "For validated armour numbers see APES Body Armour (§13)."
    )
    _print_platform_lifecycle(results, "OBSIDIAN Body Armour")
    return {"runnable": False, "see_also": "APES Body Armour"}


def _verify_obsidian_x(results: Dict) -> Dict[str, Any]:
    _banner("OBSIDIAN-X Body Armour — claim verification")
    _print_scope_limit(
        "Full-body hypothetical armour — no runnable simulator. "
        "See APES §13 for portfolio-validated V50/BFD methodology."
    )
    _print_platform_lifecycle(results, "OBSIDIAN-X Body Armour")
    return {"runnable": False}


def _verify_rubber_tracks(results: Dict) -> Dict[str, Any]:
    _banner("Rubber Tank Tracks — claim verification")
    _print_track_pad(results)
    tp = _tier2(results).get("track_pad_noise", {})
    if tp:
        _claim_checks([
            ("Net SPL reduction (dB)", tp["net_reduction_dB"], 20.8, 0.5),
        ])
    _print_platform_lifecycle(results, "Rubber Tank Tracks")
    _lifecycle_claims(results, "Rubber Tank Tracks", [
        ("rubber_pad_life_km", "Rubber pad life (km)", 8000.0, 50.0),
        ("net_noise_reduction_dB", "Net noise reduction (dB)", 20.8, 0.5),
    ])
    return {"section": "tier2.track_pad_noise"}


def _verify_tact1(results: Dict) -> Dict[str, Any]:
    _banner("TACT-1 Tactical Ration — claim verification")
    _print_ration(results)
    ration = _tier2(results).get("ration_stability", {})
    at25 = ration.get("25 °C", {})
    if at25:
        _claim_checks([
            ("Shelf life @ 25 °C (months)", at25["shelf_life_months"], 36.0, 0.5),
        ])
    _print_platform_lifecycle(results, "TACT-1 Mark II Ration")
    _lifecycle_claims(results, "TACT-1 Mark II Ration", [
        ("shelf_life_25C_mo", "Shelf life @25°C (mo)", 36.0, 0.5),
    ])
    return {"section": "tier2.ration_stability"}


def _verify_asnp(results: Dict) -> Dict[str, Any]:
    _banner("ASNP Sports Nutrition — claim verification")
    _print_scope_limit(
        "ASNP caloric / electrolyte claims are formulation targets in the "
        "spec. Portfolio §22 ration shelf-life model is the nearest "
        "thermal-stability anchor."
    )
    _print_ration(results)
    _print_platform_lifecycle(results, "ASNP Sports Nutrition")
    return {"adjacent": "tier2.ration_stability"}


def _verify_taipan(results: Dict) -> Dict[str, Any]:
    _banner("TAIPAN-1 Missile — claim verification")
    script = PORTFOLIO_ROOT / "TAIPAN Missile" / "taipan1_sim.py"
    if script.exists():
        _run_subprocess(script, "--sim", "verify")
    else:
        _print_scope_limit("taipan1_sim.py not found.")
    _print_platform_lifecycle(results, "TAIPAN-1 Missile")
    return {"standalone": "taipan1_sim.py"}


def _verify_cl20(results: Dict) -> Dict[str, Any]:
    _banner("CL-20 High Explosive — claim verification")
    _print_energetics(results, ["CL-20", "HMX", "RDX", "TNT"])
    ener = _tier2(results).get("energetics", {}).get("CL-20", {})
    if ener:
        _claim_checks([
            ("CL-20 P_CJ (GPa)", ener["P_CJ_GPa"], 45.3, 0.5),
            ("CL-20 VOD (km/s)", ener["VOD_kms"], 9.75, 0.1),
        ])
    script = PORTFOLIO_ROOT / "CL-20 High Explosive" / "cl20_simulation.py"
    if script.exists():
        _run_subprocess(script)
    _print_platform_lifecycle(results, "CL-20 High Explosive")
    _lifecycle_claims(results, "CL-20 High Explosive", [
        ("cold_storage_shelf_mo", "Cold storage shelf (mo)", 240.0, 1.0),
    ])
    return {"portfolio": "tier2.energetics", "standalone": "cl20_simulation.py"}


# Platforms that do not need the portfolio engine (saves ~30 s per run).
PORTFOLIO_SKIP_IDS = frozenset({
    "hel_cms_db",
    "military_command_doctrine",
    "obsidian_body_armour",
    "obsidian_x_body_armour",
    "taipan_missile",
})


def _verify_apes_l(results: Dict) -> Dict[str, Any]:
    _banner("APES-L Mark I — claim verification")
    print("Physics: portfolio weapons_simulation.py (§13 V50/BFD + spec prose sims)")
    _print_armour_panel(results, "APES-L police (10-layer + 8 mm B4C, 22 kg/m²)")
    _print_scope_limit(
        "23 formulation simulations documented in APES-L_Specification.md "
        "(Sims 1–23) are prose-anchored; portfolio §13 cross-checks soft-panel V50."
    )
    _print_platform_lifecycle(results, "APES-L Mark I Body Armour")
    _lifecycle_claims(results, "APES-L Mark I Body Armour", [
        ("panel_service_life_yr", "Panel service life (yr)", 10.0, 0.5),
    ])
    return {"panels": ["APES-L police"]}


PLATFORM_HANDLERS: Dict[str, Handler] = {
    "mp46m_guardian_pistol": _verify_mp46m_guardian,
    "mp46m_defender_pdw": _verify_mp46m_defender,
    "mp46p_guardian_le": _verify_mp46p_guardian_le,
    "mp68_mark_ii_rifle": _verify_mp68,
    "mas152e_sniper": _verify_mas152e,
    "57mm_autocannon": _verify_57mm_autocannon,
    "57mm_underbarrel_grenade": _verify_57mm_ubgl,
    "57mm_mortar_rpg": _verify_57mm_mortar,
    "140mm_tank_ke": _verify_140mm_ke,
    "apes_body_armour": _verify_apes,
    "apes_l_body_armour": _verify_apes_l,
    "nacs_cbrn": _verify_nacs,
    "alnicyn_armour": _verify_alnicyn,
    "adf_tactical_field_kit": _verify_adf_fk,
    "caseless_bullets": _verify_caseless,
    "combat_drug": _verify_combat_drug,
    "hel_cms_db": _verify_hel_cms,
    "hprx_rocketry": _verify_hprx,
    "hearing_protection": _verify_hearing,
    "injectable_nutrition": _verify_injectable,
    "military_command_doctrine": _verify_doctrine,
    "military_noise_cancellation": _verify_tacs,
    "obsidian_body_armour": _verify_obsidian,
    "obsidian_x_body_armour": _verify_obsidian_x,
    "rubber_tank_tracks": _verify_rubber_tracks,
    "tact1_ration": _verify_tact1,
    "asnp_sports_nutrition": _verify_asnp,
    "taipan_missile": _verify_taipan,
    "cl20_high_explosive": _verify_cl20,
}


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def main(platform_id: str, json_out: bool = False) -> int:
    _configure_stdio()
    if platform_id not in PLATFORM_HANDLERS:
        print(f"Unknown platform: {platform_id}", file=sys.stderr)
        print(f"Known: {', '.join(sorted(PLATFORM_HANDLERS))}", file=sys.stderr)
        return 1

    print("Running portfolio physics engine (weapons_simulation.py)…")
    if platform_id in PORTFOLIO_SKIP_IDS:
        sys.path.insert(0, str(PORTFOLIO_ROOT))
        import weapon_lifecycle as wl  # noqa: PLC0415
        from weapon_lifecycle_configs import PLATFORM_ID_TO_LIFECYCLE  # noqa: PLC0415
        lc_name = PLATFORM_ID_TO_LIFECYCLE.get(platform_id, platform_id)
        try:
            wl_slice = wl.run_platform(lc_name)
        except KeyError:
            wl_slice = {}
        results = {"tier3": {"weapon_lifecycle": wl_slice}}
        print("Skipped portfolio — single-platform lifecycle slice.\n")
    else:
        results = _load_results()
        print("OK — extracting platform-specific verification slice.\n")

    summary = PLATFORM_HANDLERS[platform_id](results)

    _banner("Verification complete")
    print(f"  Platform ID : {platform_id}")
    print(f"  Engine      : {PORTFOLIO_ROOT / 'weapons_simulation.py'}")
    print(f"  Full results: {PORTFOLIO_ROOT / 'weapons_sim_results.md'}")
    print("\n  This run verifies portfolio claims against the shared physics")
    print("  engine. Update spec/paper numbers to match sim output.")

    if json_out:
        payload = {
            "platform_id": platform_id,
            "summary": summary,
            "portfolio_root": str(PORTFOLIO_ROOT),
        }
        print(json.dumps(payload, indent=2))

    return 0


def cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Weapons-Defence per-platform claim verification runner."
    )
    parser.add_argument(
        "platform_id",
        help="Platform identifier (see PLATFORM_HANDLERS in sim_common.py)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args(argv)
    return main(args.platform_id, json_out=args.json)


if __name__ == "__main__":
    raise SystemExit(cli())
