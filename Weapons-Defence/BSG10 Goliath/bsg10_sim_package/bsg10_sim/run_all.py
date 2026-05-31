#!/usr/bin/env python3
"""
BSG-10 "Goliath" — Full Simulation Suite
=========================================
Master entry point. Runs all six simulation modules in sequence,
passing results between modules, and generates a consolidated report.

Usage
-----
    python run_all.py                    # run with default config, all plots
    python run_all.py --no-plots         # suppress figure generation
    python run_all.py --variant heavy    # load a config variant (see below)

Config variants
---------------
  default  — baseline BSG-10 as specified
  heavy    — 12-gauge conversion (bore 18.5 mm, 56g payload)
  light    — reduced powder charge (−10% velocity, lower pressure)
  choked   — tighter choke, same load (pattern analysis)
"""

import argparse
import sys
import os
import time

# ── ensure package is importable from project root ─────────────
sys.path.insert(0, os.path.dirname(__file__))

from bsg10_sim.config import BSG10Config, DEFAULT_CONFIG, CartridgeConfig
from bsg10_sim.ballistics.internal      import run as run_ballistics
from bsg10_sim.dynamics.balanced_action import run as run_action
from bsg10_sim.dynamics.recoil_chain    import run as run_recoil
from bsg10_sim.mechanical.dimensions    import run as run_dimensions
from bsg10_sim.mechanical.magazine      import run as run_magazine
from bsg10_sim.lifecycle.parts_life     import run as run_life
from bsg10_sim.reports.generate         import generate


# ════════════════════════════════════════════════════════════════
# CONFIG VARIANTS
# ════════════════════════════════════════════════════════════════

def _load_variant(name: str) -> BSG10Config:
    """Return a named config variant."""
    if name == "default":
        return DEFAULT_CONFIG

    elif name == "heavy":
        # 12-gauge conversion for comparison
        cfg = BSG10Config()
        cfg.cartridge.bore_diam  = 0.0185
        cfg.cartridge.shot_mass  = 0.049
        cfg.cartridge.wad_mass   = 0.007
        cfg.cartridge.powder_mass= 0.0058
        cfg.cartridge.target_vel = 420.0
        cfg.cartridge.gamma      = 1.15
        return cfg

    elif name == "light":
        # −10% powder charge, lower pressure variant
        cfg = BSG10Config()
        cfg.cartridge.powder_mass= 0.0058
        cfg.cartridge.target_vel = 390.0
        return cfg

    else:
        print(f"Unknown variant '{name}'. Using default.")
        return DEFAULT_CONFIG


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="BSG-10 Goliath — Full Simulation Suite"
    )
    parser.add_argument("--no-plots",  action="store_true",
                        help="Suppress matplotlib figure generation")
    parser.add_argument("--variant",   default="default",
                        choices=["default", "heavy", "light"],
                        help="Config variant to run")
    parser.add_argument("--module",    default="all",
                        choices=["all", "ballistics", "action", "recoil",
                                 "dimensions", "magazine", "life"],
                        help="Run a single module only")
    args = parser.parse_args()

    cfg   = _load_variant(args.variant)
    plots = not args.no_plots

    print(f"\n{'='*62}")
    print(f"  BSG-10 Goliath — Simulation Suite")
    print(f"  Variant : {args.variant}")
    print(f"  Plots   : {'enabled' if plots else 'disabled'}")
    print(f"{'='*62}")

    t0 = time.perf_counter()

    # ── Module A — Internal Ballistics ─────────────────────────
    if args.module in ("all", "ballistics"):
        bal = run_ballistics(cfg, plot_results=plots)
    else:
        from bsg10_sim.ballistics.internal import calibrate
        bal = calibrate(cfg)

    # ── Module B — Balanced Action ──────────────────────────────
    if args.module in ("all", "action"):
        act = run_action(cfg, plot_results=plots)
    else:
        from bsg10_sim.dynamics.balanced_action import simulate
        act = simulate(cfg)

    # ── Module C — Recoil Chain ─────────────────────────────────
    if args.module in ("all", "recoil"):
        rec = run_recoil(cfg, I_total=bal.impulse_total, plot_results=plots)
    else:
        from bsg10_sim.dynamics.recoil_chain import simulate as sim_rec
        rec = sim_rec(cfg, bal.impulse_total)

    # ── Module D — Dimensions ───────────────────────────────────
    if args.module in ("all", "dimensions"):
        dim = run_dimensions(cfg,
                             carrier_stroke_used_mm=act.carrier_stroke_mm,
                             cbs_travel_used_mm=rec.cbs_max_travel_mm,
                             plot_results=plots)
    else:
        from bsg10_sim.mechanical.dimensions import check
        dim = check(cfg, act.carrier_stroke_mm, rec.cbs_max_travel_mm)

    # ── Module E — Magazine ─────────────────────────────────────
    if args.module in ("all", "magazine"):
        mag = run_magazine(cfg, plot_results=plots)
    else:
        from bsg10_sim.mechanical.magazine import compute
        mag = compute(cfg)

    # ── Module F — Parts Life ───────────────────────────────────
    if args.module in ("all", "life"):
        lif = run_life(cfg, P_peak=bal.P_peak, plot_results=plots)
    else:
        from bsg10_sim.lifecycle.parts_life import simulate as sim_life
        lif = sim_life(cfg, bal.P_peak)

    # ── Report ──────────────────────────────────────────────────
    if args.module == "all":
        report = generate(bal, act, rec, dim, mag, lif, cfg, save=True)

    elapsed = time.perf_counter() - t0
    print(f"\n{'='*62}")
    print(f"  All modules complete in {elapsed:.1f} s")
    print(f"  Outputs written to: bsg10_sim/outputs/")
    print(f"{'='*62}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
