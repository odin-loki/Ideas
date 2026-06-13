#!/usr/bin/env python3
"""TACS Military Noise Cancellation — verification simulation.

Runs the portfolio physics engine (``weapons_simulation.py``) and prints the
subset of results that verify claims in this platform's specification and
research paper. See ``SIM_README.md`` for methodology and table cross-references.
"""
from __future__ import annotations

import sys
from pathlib import Path

_PORTFOLIO = Path(__file__).resolve().parents[1]
if str(_PORTFOLIO) not in sys.path:
    sys.path.insert(0, str(_PORTFOLIO))

from sim_common import main  # noqa: E402

PLATFORM_ID = "military_noise_cancellation"

if __name__ == "__main__":
    import argparse
    _p = argparse.ArgumentParser(description="Verify platform claims against portfolio sim.")
    _p.add_argument("--json", action="store_true", help="Emit JSON summary at end")
    _args = _p.parse_args()
    raise SystemExit(main(PLATFORM_ID, json_out=_args.json))
