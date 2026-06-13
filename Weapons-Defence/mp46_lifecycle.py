"""
MP-4.6 family lifecycle — backward-compatible shim.

All portfolio platforms are now modelled in ``weapon_lifecycle.py``.
This module re-exports the MP-4.6 firearm API used by older imports.
"""

from __future__ import annotations

from typing import Dict, Optional

from weapon_lifecycle import LifecycleConfig, run_all as _run_all_platforms
from weapon_lifecycle_configs import TIER2_RATES, BASELINE_RATES, all_platform_configs

__all__ = [
    "LifecycleConfig",
    "TIER2_RATES",
    "BASELINE_RATES",
    "simulate_platform",
    "run_all",
]

_MP46_KEYS = ("MP-4.6P Guardian LE", "MP-4.6M Pistol", "MP-4.6M Defender PDW")


def _configs():
    return {k: v for k, v in all_platform_configs().items() if k in _MP46_KEYS}


def simulate_platform(cfg, ib_pressure_MPa=None, ib_mv_ms=None):
    from weapon_lifecycle import simulate_platform as _sim  # noqa: PLC0415
    cartridges = None
    if ib_pressure_MPa is not None or ib_mv_ms is not None:
        row: Dict[str, float] = {}
        if ib_pressure_MPa is not None:
            row["chamber_pressure_max_MPa"] = ib_pressure_MPa
        if ib_mv_ms is not None:
            row["muzzle_velocity_ms"] = ib_mv_ms
        cartridges = {cfg.cartridge_key: row}
    return _sim(cfg, cartridges=cartridges)


def run_all(ib_lookup: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
    full = _run_all_platforms(cartridges=ib_lookup)
    return {k: full[k] for k in _MP46_KEYS if k in full}
