#!/usr/bin/env python3
"""MP-4.6P Guardian LE — local verification slice (portfolio + §23 lifecycle)."""

from __future__ import annotations

import sys
from pathlib import Path

_DEFENCE = Path(__file__).resolve().parents[2] / "Weapons-Defence"
sys.path.insert(0, str(_DEFENCE))
import sim_common  # noqa: E402

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Verify MP-4.6P Guardian LE claims")
    p.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = p.parse_args()
    raise SystemExit(sim_common.main("mp46p_guardian_le", json_out=args.json))
