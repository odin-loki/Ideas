#!/usr/bin/env python3
"""APES-L Mark I — local verification slice (portfolio §13 + spec sims)."""

from __future__ import annotations

import sys
from pathlib import Path

_DEFENCE = Path(__file__).resolve().parents[2] / "Weapons-Defence"
sys.path.insert(0, str(_DEFENCE))
import sim_common  # noqa: E402

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Verify APES-L Mark I claims")
    p.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = p.parse_args()
    raise SystemExit(sim_common.main("apes_l_body_armour", json_out=args.json))
