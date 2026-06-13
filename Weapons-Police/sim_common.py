"""
Weapons-Police — per-platform claim verification runner
========================================================

Delegates to the shared portfolio engine in ``../Weapons-Defence/sim_common.py``.
Police platforms use the same ``weapons_simulation.py`` single source of truth.
"""

from __future__ import annotations

import sys
from pathlib import Path

_DEFENCE = Path(__file__).resolve().parent.parent / "Weapons-Defence"
sys.path.insert(0, str(_DEFENCE))

import sim_common as _defence_sim  # noqa: E402

main = _defence_sim.main
PLATFORM_HANDLERS = _defence_sim.PLATFORM_HANDLERS
