"""
Portfolio weapon lifecycle — seven-phase physics for firearms, tailored
lifecycle models for armour / sustainment / systems platforms.

Replaces the MP-4.6-only ``mp46_lifecycle.py`` slice. Each platform has a
unique configuration in ``weapon_lifecycle_configs.py``.

Used by ``weapons_simulation.py`` Tier-3 (§23) and ``sim_common.py`` claim
verification for every ``PLATFORM_HANDLERS`` entry.
"""

from __future__ import annotations

import math
from dataclasses import asdict
from typing import Dict, List, Optional

from weapon_lifecycle_configs import (
    BASELINE_RATES,
    FirearmLifecycleConfig,
    GenericLifecycleConfig,
    PlatformConfig,
    all_platform_configs,
)
from weapon_lifecycle_core import (
    analytic_mrbf,
    archard_bore_life,
    felt_recoil_ftlbf,
    lame_hoop_sf,
    reliability_monte_carlo,
)


def _effective_bore_life(cfg: FirearmLifecycleConfig,
                          tier2_barrel_rounds: Optional[int]) -> int:
    archard = archard_bore_life(
        cfg.barrel_r_i_mm, cfg.peak_pressure_MPa, cfg.barrel_length_mm,
        cfg.archard_K, cfg.archard_H_GPa, cfg.bore_life_target_rounds,
    )
    bore = min(archard, cfg.bore_life_target_rounds)
    if tier2_barrel_rounds is not None:
        bore = min(bore, tier2_barrel_rounds)
    return max(bore, 1)


_MC_CACHE: Dict[tuple, Dict[str, float]] = {}


def _cached_mc(rates: Dict[str, int]) -> Dict[str, float]:
    key = tuple(sorted(rates.items()))
    if key not in _MC_CACHE:
        _MC_CACHE[key] = reliability_monte_carlo(rates, seed=42 + len(_MC_CACHE))
    return _MC_CACHE[key]


def simulate_firearm(
    cfg: FirearmLifecycleConfig,
    ib_pressure_MPa: Optional[float] = None,
    ib_mv_ms: Optional[float] = None,
    tier2_barrel_rounds: Optional[int] = None,
) -> Dict[str, object]:
    if ib_pressure_MPa is not None:
        cfg = FirearmLifecycleConfig(**{**asdict(cfg),
                                        "peak_pressure_MPa": ib_pressure_MPa})
    if ib_mv_ms is not None:
        cfg = FirearmLifecycleConfig(**{**asdict(cfg),
                                        "muzzle_velocity_ms": ib_mv_ms})

    rates = cfg.failure_rates if cfg.tier2_equipped else BASELINE_RATES
    mrbf_a = analytic_mrbf(rates)
    mc = _cached_mc(rates)
    bore = _effective_bore_life(cfg, tier2_barrel_rounds)
    sf_yield = lame_hoop_sf(cfg.peak_pressure_MPa, cfg.barrel_r_i_mm,
                            cfg.barrel_r_o_mm, cfg.barrel_yield_MPa)
    sf_spring = (cfg.spring_S_e_MPa / max(cfg.spring_tau_max_MPa, 1.0)
                 if cfg.spring_tau_max_MPa > 0 else None)
    felt = felt_recoil_ftlbf(
        cfg.projectile_mass_g, cfg.muzzle_velocity_ms, cfg.propellant_mass_g,
        cfg.shooter_effective_mass_kg, cfg.muzzle_brake_efficiency,
    )

    if cfg.bolt_mass_kg > 0 and cfg.spring_rate_N_per_mm > 0:
        omega_n = math.sqrt(cfg.spring_rate_N_per_mm * 1000.0 / cfg.bolt_mass_kg)
        x_max = cfg.bolt_impulse_Ns / math.sqrt(
            cfg.spring_rate_N_per_mm * 1000.0 * cfg.bolt_mass_kg
        ) * 1000.0
    else:
        omega_n = 0.0
        x_max = 0.0

    components: List[Dict[str, object]] = []
    for comp in cfg.components:
        row = dict(comp)
        if "Barrel" in comp["name"] or "barrel" in comp["name"].lower():
            row["fail_rds"] = min(int(comp["fail_rds"]), bore)
        components.append(row)

    structural: Dict[str, object] = {
        "barrel_sf_yield": round(sf_yield, 2),
        "bolt_stroke_mm": round(x_max, 1),
        "bolt_omega_rad_s": round(omega_n, 1),
    }
    if sf_spring is not None:
        structural["spring_fatigue_sf"] = round(sf_spring, 1)

    out: Dict[str, object] = {
        "platform": cfg.platform,
        "category": cfg.category,
        "cartridge_key": cfg.cartridge_key,
        "action": cfg.action,
        "tier2_equipped": cfg.tier2_equipped,
        "structural": structural,
        "parts_life": {
            "bore_life_rounds": bore,
            "tier2_barrel_rounds": tier2_barrel_rounds,
            "components": components,
        },
        "recoil": {
            "felt_recoil_ftlbf": round(felt, 3),
            "muzzle_brake_efficiency": cfg.muzzle_brake_efficiency,
            "free_recoil_impulse_Ns": round(
                cfg.projectile_mass_g / 1000.0 * cfg.muzzle_velocity_ms, 3
            ),
        },
        "reliability": {
            "failure_rates": rates,
            "mrbf_analytic": round(mrbf_a, 0),
            "mrbf_simulated": mc["mrbf_simulated"],
            "mrbf_ci_90_low": mc["mrbf_ci_90_low"],
            "mrbf_ci_90_high": mc["mrbf_ci_90_high"],
            "ftf_rate": rates.get("FTFire", 80_000),
        },
    }
    return out


def simulate_generic(cfg: GenericLifecycleConfig,
                     ration_lookup: Optional[Dict] = None) -> Dict[str, object]:
    headline = dict(cfg.headline)
    if ration_lookup and cfg.platform == "TACT-1 Mark II Ration":
        for key, row in ration_lookup.items():
            temp = key.replace(" °C", "").replace("°C", "")
            headline[f"shelf_life_{temp}C_mo"] = row.get("shelf_life_months")

    components = []
    for comp in cfg.components:
        row = dict(comp)
        row["warn_display"] = f"{comp['warn']:,} {comp['unit']}"
        row["fail_display"] = f"{comp['fail']:,} {comp['unit']}"
        components.append(row)

    out: Dict[str, object] = {
        "platform": cfg.platform,
        "category": cfg.category,
        "primary_metric": cfg.primary_metric,
        "headline": headline,
        "parts_life": {"components": components},
    }
    if cfg.scope_note:
        out["scope_note"] = cfg.scope_note
    if cfg.failure_rates:
        mrbf_a = analytic_mrbf(cfg.failure_rates)
        mc = reliability_monte_carlo(cfg.failure_rates)
        out["reliability"] = {
            "failure_rates": cfg.failure_rates,
            "mrbf_analytic": round(mrbf_a, 0),
            "mrbf_simulated": mc["mrbf_simulated"],
            "mrbf_ci_90_low": mc["mrbf_ci_90_low"],
            "mrbf_ci_90_high": mc["mrbf_ci_90_high"],
        }
    return out


def simulate_platform(
    cfg: PlatformConfig,
    cartridges: Optional[Dict[str, Dict]] = None,
    barrel_tier2: Optional[Dict[str, Dict]] = None,
    ration_lookup: Optional[Dict] = None,
) -> Dict[str, object]:
    if isinstance(cfg, FirearmLifecycleConfig):
        ib_p = ib_mv = None
        tier2_bore = None
        if cartridges and cfg.cartridge_key in cartridges:
            row = cartridges[cfg.cartridge_key]
            ib_p = row.get("chamber_pressure_max_MPa")
            ib_mv = row.get("muzzle_velocity_ms")
        if barrel_tier2 and cfg.platform in barrel_tier2:
            tier2_bore = barrel_tier2[cfg.platform].get("barrel_life_rounds")
        return simulate_firearm(cfg, ib_p, ib_mv, tier2_bore)
    return simulate_generic(cfg, ration_lookup)


def run_platform(
    platform_name: str,
    cartridges: Optional[Dict[str, Dict]] = None,
    barrel_tier2: Optional[Dict[str, Dict]] = None,
    ration_lookup: Optional[Dict] = None,
) -> Dict[str, Dict]:
    """Run lifecycle sim for one platform by display name."""
    cfg = all_platform_configs()[platform_name]
    return {platform_name: simulate_platform(
        cfg, cartridges, barrel_tier2, ration_lookup)}


def run_all(
    cartridges: Optional[Dict[str, Dict]] = None,
    barrel_tier2: Optional[Dict[str, Dict]] = None,
    ration_lookup: Optional[Dict] = None,
) -> Dict[str, Dict]:
    """Run lifecycle sim for every portfolio platform."""
    _MC_CACHE.clear()
    out: Dict[str, Dict] = {}
    for key, cfg in all_platform_configs().items():
        out[key] = simulate_platform(cfg, cartridges, barrel_tier2, ration_lookup)
    return out


# Backward compatibility with mp46_lifecycle imports
LifecycleConfig = FirearmLifecycleConfig


def _legacy_mp46_run(ib_lookup: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
    keys = ("MP-4.6P Guardian LE", "MP-4.6M Pistol", "MP-4.6M Defender PDW")
    full = run_all(cartridges=ib_lookup)
    return {k: full[k] for k in keys if k in full}


if __name__ == "__main__":
    import json
    res = run_all()
    for plat, data in res.items():
        cat = data.get("category", "?")
        print(f"\n=== {plat} ({cat}) ===")
        if cat in ("firearm", "crew_served"):
            rel = data["reliability"]
            print(f"  MRBF analytic: {rel['mrbf_analytic']:,.0f}")
            print(f"  Bore life: {data['parts_life']['bore_life_rounds']:,}")
        elif cat == "scope":
            print(f"  {data.get('scope_note', 'scope-only')}")
        else:
            print(json.dumps(data.get("headline", {}), indent=2))
