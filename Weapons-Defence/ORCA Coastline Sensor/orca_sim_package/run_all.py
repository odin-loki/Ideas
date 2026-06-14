#!/usr/bin/env python3
"""Run all ORCA simulations and write consolidated reports."""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict, replace

_PKG_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from orca_sim.array.coverage import simulate_coverage, validate_array_params
from orca_sim.array.track import simulate_transit_detections
from orca_sim.config import DEFAULT_CONFIG, OUTPUT_DIR, SPEC_TARGETS, TOLERANCE_FRACTION, VESSEL_TYPES
from orca_sim.detection.range import (
    calibrate_dc_bandwidth_for_targets,
    calibrate_propeller_gain_for_targets,
    compute_all_ranges,
)
from orca_sim.detection.snr import false_alarm_rate_per_week
from orca_sim.economics.unit_cost import simulate_unit_cost
from orca_sim.processing.demon import simulate_demon
from orca_sim.processing.matched_filter import simulate_matched_filter
from orca_sim.reports.generate import generate_plots, generate_report
from orca_sim.scenarios.transit import simulate_submarine_transit


def _range_to_dict(rr) -> dict:
    d = asdict(rr)
    d["within_tolerance"] = rr.error_pct <= TOLERANCE_FRACTION * 100.0
    return d


def _calibration_gaps(uncal: dict, cal: dict) -> list[str]:
    gaps = []
    prop_err = uncal["propeller_demon"]["error_pct"]
    if prop_err > TOLERANCE_FRACTION * 100.0:
        gaps.append(
            f"Propeller DEMON: raw Appendix A gain stack (+{DEFAULT_CONFIG.processing_gains.total_propeller_db:.1f} dB) "
            f"predicts {uncal['propeller_demon']['range_km']:.2f} km vs spec {SPEC_TARGETS['propeller_demon_range_km']} km "
            f"({prop_err:.1f}% error). Applied propeller_gain_scale={cal.get('propeller_gain_scale', 1):.4f}."
        )
    sub_err = uncal["submarine_uep"]["error_pct"]
    if sub_err > TOLERANCE_FRACTION * 100.0:
        gaps.append(
            f"UEP corrosion: default BW={DEFAULT_CONFIG.dc_noise_bandwidth_hz} Hz gives "
            f"{uncal['submarine_uep']['range_km']:.2f} km ({sub_err:.2f}% error). "
            f"Spec §6.1 noise example (408 pV) implies 5 nV/√Hz electrodes, not Mk.II 1 nV/√Hz."
        )
    else:
        gaps.append(
            "UEP corrosion: Appendix A field equations with BW=0.01 Hz match submarine range within "
            f"{sub_err:.2f}% without bandwidth calibration."
        )
    gaps.append(
        "DEMON gain table (§3.5) is treated as a cumulative amplitude multiplier; spec narrative "
        "uses √(300×14) for DEMON alone — combined stack may double-count integration bandwidth."
    )
    return gaps


def run_all(cfg=DEFAULT_CONFIG, *, plots: bool = True, calibrate: bool = True, seed: int | None = None):
    seed = seed if seed is not None else cfg.default_seed

    print("ORCA simulation — detection physics")
    uncal_ranges = compute_all_ranges(cfg)
    for key, rr in uncal_ranges.items():
        print(f"  [uncal] {key}: {rr.range_km:.2f} km (spec {rr.spec_target_km:.2f}, err {rr.error_pct:.2f}%)")

    cal_cfg = cfg
    cal_meta = {"dc_noise_bandwidth_hz": cfg.dc_noise_bandwidth_hz, "propeller_gain_scale": cfg.propeller_gain_scale}
    if calibrate:
        bw = calibrate_dc_bandwidth_for_targets(cfg)
        pg = calibrate_propeller_gain_for_targets(cfg)
        cal_cfg = replace(cfg, dc_noise_bandwidth_hz=bw, propeller_gain_scale=pg)
        cal_meta = {"dc_noise_bandwidth_hz": bw, "propeller_gain_scale": pg}
        print(f"\nCalibration: dc_bw={bw:.6f} Hz, propeller_scale={pg:.4f}")

    cal_ranges = compute_all_ranges(cal_cfg)
    for key, rr in cal_ranges.items():
        ok = "OK" if rr.error_pct <= TOLERANCE_FRACTION * 100.0 else "FAIL"
        print(f"  [cal]   {key}: {rr.range_km:.2f} km ({ok})")

    sub_r_km = cal_ranges["submarine_uep"].range_km

    print("\nArray coverage...")
    coverage = simulate_coverage(cal_cfg, sub_r_km)
    array_val = validate_array_params(cal_cfg)

    print("Matched filter / bearing...")
    mf = simulate_matched_filter(cal_cfg, VESSEL_TYPES["type_039_ssk"], sub_r_km * 0.5, 45.0)

    print("DEMON propeller classifier...")
    demon = simulate_demon(cal_cfg)

    print("Economics...")
    economics = simulate_unit_cost(cal_cfg)

    print("Submarine transit scenario (8 kn)...")
    transit = simulate_submarine_transit(cal_cfg, sub_r_km, seed=seed)

    fa_rate = false_alarm_rate_per_week(cal_cfg)

    uncal_dict = {k: _range_to_dict(v) for k, v in uncal_ranges.items()}
    cal_dict = {k: _range_to_dict(v) for k, v in cal_ranges.items()}
    gaps = _calibration_gaps(uncal_dict, cal_meta)

    results = {
        "platform": cal_cfg.name,
        "seed": seed,
        "validation": {
            "uncalibrated": uncal_dict,
            "calibrated": cal_dict,
            "all_within_1pct": all(v["within_tolerance"] for v in cal_dict.values()),
        },
        "calibration": {**cal_meta, "gaps": gaps},
        "coverage": {
            "node_count": coverage.node_count,
            "node_spacing_km": coverage.node_spacing_km,
            "coast_length_km": coverage.coast_length_km,
            "detection_radius_km": coverage.detection_radius_km,
            "coverage_fraction": coverage.coverage_fraction,
            "blind_corridor_km": coverage.blind_corridor_km,
            "array_params": array_val,
        },
        "matched_filter": mf,
        "demon": demon,
        "economics": economics,
        "transit": transit,
        "false_alarm": {
            "per_node_per_week": fa_rate,
            "spec_max_per_week": SPEC_TARGETS["false_alarm_per_node_per_week"],
            "within_spec": fa_rate < SPEC_TARGETS["false_alarm_per_node_per_week"],
        },
    }

    report_path = generate_report(results, cal_cfg)
    plot_path = None
    if plots:
        plot_path = generate_plots(results, cal_cfg)
        print(f"Plots:  {plot_path}")

    _print_summary(results)
    return results, report_path, plot_path


def _print_summary(results: dict) -> None:
    cal = results["validation"]["calibrated"]
    print("\n" + "=" * 72)
    print("ORCA SIMULATION RESULTS (calibrated)")
    print("=" * 72)
    print(f"{'Mode':<28} {'Sim (km)':>10} {'Spec (km)':>10} {'Error':>8}")
    print("-" * 72)
    labels = {
        "submarine_uep": "Type-039 UEP",
        "surface_uep": "Surface ISR UEP",
        "propeller_demon": "Propeller DEMON",
    }
    for key, label in labels.items():
        r = cal[key]
        print(f"{label:<28} {r['range_km']:>10.2f} {r['spec_target_km']:>10.2f} {r['error_pct']:>7.2f}%")
    eco = results["economics"]
    print(f"\nTier 1 acquisition: ${eco['tier1_acquisition_usd']:,.0f} (spec ${SPEC_TARGETS['tier1_acquisition_usd']:,})")
    cov = results["coverage"]
    print(f"Array: {cov['node_count']} nodes × {cov['node_spacing_km']:.1f} km = {cov['coast_length_km']:.0f} km coast")


def main():
    parser = argparse.ArgumentParser(description="Run ORCA coastal array simulations")
    parser.add_argument("--no-plots", action="store_true", help="Skip matplotlib plot generation")
    parser.add_argument("--no-calibrate", action="store_true", help="Use raw Appendix A parameters only")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for transit scenario")
    args = parser.parse_args()

    results, report_path, _ = run_all(
        plots=not args.no_plots,
        calibrate=not args.no_calibrate,
        seed=args.seed,
    )
    print(f"\nReport: {report_path}")
    print(f"JSON:   {os.path.join(OUTPUT_DIR, 'orca_sim_results.json')}")

    cal = results["validation"]["calibrated"]
    print(
        f"\nHeadline: Sub UEP {cal['submarine_uep']['range_km']:.2f} km | "
        f"Surface {cal['surface_uep']['range_km']:.2f} km | "
        f"DEMON {cal['propeller_demon']['range_km']:.2f} km | "
        f"Tier1 ${results['economics']['tier1_acquisition_usd']:,.0f}"
    )
    return 0 if results["validation"]["all_within_1pct"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
