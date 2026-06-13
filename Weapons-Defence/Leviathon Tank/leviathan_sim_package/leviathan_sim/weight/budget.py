"""Weight budget verification."""

from __future__ import annotations

from typing import Any, Dict

from leviathan_sim.config import LeviathanConfig


def simulate_weight(cfg: LeviathanConfig) -> Dict[str, Any]:
    items = dict(cfg.weight.items)
    total = sum(items.values())
    target = cfg.hull.combat_mass_kg
    delta = total - target
    pct = delta / target * 100

    return {
        "items_kg": items,
        "computed_total_kg": total,
        "spec_combat_mass_kg": target,
        "delta_kg": delta,
        "delta_percent": round(pct, 2),
        "balanced": abs(delta) <= 50,
        "spec_arithmetic_gap_kg": delta,
        "notes": (
            "Part XIX table sums to 31,000 kg while claiming 38,000 kg combat weight — "
            "≈7,000 kg likely embedded in hull/turret structure as AlNiCyN armour mass. "
            "Sim flags this inconsistency; do not treat as balanced until spec is reconciled."
        ),
    }
