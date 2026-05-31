"""
BSG-10 "Goliath" Simulation Suite
==================================
Quick start:
    from bsg10_sim import BSG10Config, run_all
    results = run_all()
    print(results.ballistics.muzzle_vel)
"""
from .config import (BSG10Config, DEFAULT_CONFIG, CartridgeConfig,
                     BarrelConfig, GasSystemConfig, ActionConfig,
                     RecoilConfig, MagazineConfig, SystemConfig)
from dataclasses import dataclass
from typing import Optional

@dataclass
class AllResults:
    ballistics: object
    action:     object
    recoil:     object
    dimensions: object
    magazine:   object
    life:       object
    report:     Optional[str] = None

def run_all(cfg=None, plots=True, save_report=True):
    from .ballistics.internal      import calibrate, plot as pb
    from .dynamics.balanced_action import simulate as sa, plot as pa
    from .dynamics.recoil_chain    import simulate as sr, plot as pr
    from .mechanical.dimensions    import check, plot as pd
    from .mechanical.magazine      import compute, plot as pm
    from .lifecycle.parts_life     import simulate as sl, plot_all
    from .reports.generate         import generate
    if cfg is None: cfg = DEFAULT_CONFIG
    bal = calibrate(cfg);  plots and pb(bal, cfg)
    act = sa(cfg);         plots and pa(act, cfg)
    rec = sr(cfg, bal.impulse_total); plots and pr(rec, cfg)
    dim = check(cfg, act.carrier_stroke_mm, rec.cbs_max_travel_mm); plots and pd(dim, cfg)
    mag = compute(cfg);    plots and pm(mag, cfg)
    lif = sl(cfg, bal.P_peak); plots and plot_all(lif, cfg)
    rpt = generate(bal, act, rec, dim, mag, lif, cfg, save=save_report) if save_report else None
    return AllResults(bal, act, rec, dim, mag, lif, rpt)

__version__ = "1.0.0"
