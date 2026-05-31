#!/usr/bin/env python3
"""BSG-10 run_all — invoke from the repo root: python run_all.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, runpy

# Forward all args to the internal run_all module
import argparse
parser = argparse.ArgumentParser(description="BSG-10 Simulation Suite")
parser.add_argument("--no-plots",  action="store_true")
parser.add_argument("--variant",   default="default", choices=["default","heavy","light"])
parser.add_argument("--module",    default="all",
                    choices=["all","ballistics","action","recoil","dimensions","magazine","life"])
args = parser.parse_args()

from bsg10_sim.config import BSG10Config, DEFAULT_CONFIG
import numpy as np

def load_variant(name):
    if name == "default": return DEFAULT_CONFIG
    elif name == "heavy":
        cfg = BSG10Config()
        cfg.cartridge.bore_diam   = 0.0185
        cfg.cartridge.shot_mass   = 0.049
        cfg.cartridge.wad_mass    = 0.007
        cfg.cartridge.powder_mass = 0.0058
        cfg.cartridge.target_vel  = 420.0
        cfg.cartridge.gamma       = 1.15
        return cfg
    elif name == "light":
        cfg = BSG10Config()
        cfg.cartridge.powder_mass = 0.0058
        cfg.cartridge.target_vel  = 390.0
        return cfg
    return DEFAULT_CONFIG

cfg   = load_variant(args.variant)
plots = not args.no_plots

from bsg10_sim.ballistics.internal      import run as rA
from bsg10_sim.dynamics.balanced_action import run as rB
from bsg10_sim.dynamics.recoil_chain    import run as rC
from bsg10_sim.mechanical.dimensions    import run as rD
from bsg10_sim.mechanical.magazine      import run as rE
from bsg10_sim.lifecycle.parts_life     import run as rF
from bsg10_sim.reports.generate         import generate

import time; t0 = time.perf_counter()
print(f"\n{'='*62}\n  BSG-10 Goliath — Simulation Suite  |  variant: {args.variant}\n{'='*62}")

bal = rA(cfg, plot_results=plots)
act = rB(cfg, plot_results=plots)
rec = rC(cfg, I_total=bal.impulse_total, plot_results=plots)
dim = rD(cfg, carrier_stroke_used_mm=act.carrier_stroke_mm,
             cbs_travel_used_mm=rec.cbs_max_travel_mm, plot_results=plots)
mag = rE(cfg, plot_results=plots)
lif = rF(cfg, P_peak=bal.P_peak, plot_results=plots)

if args.module == "all":
    generate(bal, act, rec, dim, mag, lif, cfg, save=True)

print(f"\n{'='*62}\n  Complete in {time.perf_counter()-t0:.1f}s  |  outputs → bsg10_sim/outputs/\n{'='*62}\n")
