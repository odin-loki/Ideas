"""Markdown and JSON report generation for ORCA simulations."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import numpy as np

from orca_sim.config import DEFAULT_CONFIG, ORCAConfig, OUTPUT_DIR, SPEC_TARGETS


def to_json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return to_json_safe(obj.tolist())
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if hasattr(obj, "__dataclass_fields__"):
        return to_json_safe(obj.__dict__)
    if isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
        return None
    return obj


def _range_row(label: str, block: dict) -> str:
    r = block.get("range_km", 0)
    target = block.get("spec_target_km", 0)
    err = block.get("error_pct", 0)
    ok = "✓" if block.get("within_tolerance") else "✗"
    return f"| {label} | {target:.2f} | {r:.2f} | {err:.3f}% | {ok} |"


def generate_report(results: Dict[str, Any], cfg: ORCAConfig = DEFAULT_CONFIG) -> str:
    md_path = os.path.join(OUTPUT_DIR, "orca_sim_report.md")
    json_path = os.path.join(OUTPUT_DIR, "orca_sim_results.json")

    validation = results.get("validation", {})
    uncal = validation.get("uncalibrated", {})
    cal = validation.get("calibrated", {})

    lines = [
        "# ORCA — Simulation Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Executive summary",
        "",
        _executive_summary(results),
        "",
        "## Detection range validation (Appendix A)",
        "",
        "### Calibrated model",
        "",
        "| Mode | Spec (km) | Simulated (km) | Error | Pass |",
        "|------|-----------|----------------|-------|------|",
    ]

    if cal:
        for key, label in [
            ("submarine_uep", "Type-039 UEP"),
            ("surface_uep", "Surface ISR UEP"),
            ("propeller_demon", "Propeller DEMON"),
        ]:
            if key in cal:
                lines.append(_range_row(label, cal[key]))

    lines.extend([
        "",
        "### Uncalibrated (raw Appendix A parameters)",
        "",
        "| Mode | Spec (km) | Simulated (km) | Error | Pass |",
        "|------|-----------|----------------|-------|------|",
    ])

    if uncal:
        for key, label in [
            ("submarine_uep", "Type-039 UEP"),
            ("surface_uep", "Surface ISR UEP"),
            ("propeller_demon", "Propeller DEMON"),
        ]:
            if key in uncal:
                lines.append(_range_row(label, uncal[key]))

    lines.extend([
        "",
        "## Array coverage",
        "",
        _coverage_section(results.get("coverage", {})),
        "",
        "## Economics",
        "",
        _economics_section(results.get("economics", {})),
        "",
        "## Calibration notes",
        "",
        _calibration_section(results.get("calibration", {})),
        "",
        "## Full JSON",
        "",
        "See `orca_sim_results.json` for machine-readable output.",
        "",
    ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(to_json_safe(results), f, indent=2)

    return md_path


def _executive_summary(results: Dict[str, Any]) -> str:
    bullets = []
    cal = results.get("validation", {}).get("calibrated", {})
    if cal:
        sub = cal.get("submarine_uep", {})
        surf = cal.get("surface_uep", {})
        prop = cal.get("propeller_demon", {})
        bullets.append(
            f"- **Type-039 UEP detection:** {sub.get('range_km', 0):.2f} km "
            f"(spec {SPEC_TARGETS['submarine_uep_range_km']} km)"
        )
        bullets.append(
            f"- **Surface ISR UEP detection:** {surf.get('range_km', 0):.2f} km "
            f"(spec {SPEC_TARGETS['surface_uep_range_km']} km)"
        )
        bullets.append(
            f"- **Propeller DEMON classification:** {prop.get('range_km', 0):.2f} km "
            f"(spec {SPEC_TARGETS['propeller_demon_range_km']} km)"
        )

    cov = results.get("coverage", {})
    if cov:
        bullets.append(
            f"- **Tier 1 array:** {cov.get('node_count', 54)} nodes, "
            f"{cov.get('node_spacing_km', 57):.1f} km spacing, "
            f"{cov.get('coast_length_km', 3000):.0f} km coast"
        )

    eco = results.get("economics", {})
    if eco:
        bullets.append(
            f"- **Tier 1 acquisition:** ${eco.get('tier1_acquisition_usd', 0):,.0f} "
            f"(spec ${SPEC_TARGETS['tier1_acquisition_usd']:,})"
        )

    fa = results.get("false_alarm", {})
    if fa:
        bullets.append(
            f"- **False alarm rate:** {fa.get('per_node_per_week', 0):.3f} events/node/week "
            f"(spec < {SPEC_TARGETS['false_alarm_per_node_per_week']}/week)"
        )

    return "\n".join(bullets) if bullets else "- No simulation results."


def _coverage_section(cov: dict) -> str:
    if not cov:
        return "- No coverage data."
    return "\n".join([
        f"- Nodes: **{cov.get('node_count')}** @ **{cov.get('node_spacing_km', 0):.2f} km** spacing",
        f"- Coast length: **{cov.get('coast_length_km', 0):.0f} km**",
        f"- Detection radius: **{cov.get('detection_radius_km', 0):.2f} km**",
        f"- Full coverage: **{'yes' if cov.get('coverage_fraction', 0) >= 1.0 else 'partial'}**",
        f"- Blind corridor on single-node failure: **{cov.get('blind_corridor_km', 0):.1f} km**",
    ])


def _economics_section(eco: dict) -> str:
    if not eco:
        return "- No economics data."
    return "\n".join([
        f"- Node cost (nominal): **${eco.get('node_cost_nominal_usd', 0):,.2f}**",
        f"- Tier 1 acquisition: **${eco.get('tier1_acquisition_usd', 0):,.0f}**",
        f"- P-8A comparison: ORCA is **{eco.get('orca_pct_of_p8a_cost', 0):.4f}%** of one P-8A",
    ])


def _calibration_section(cal: dict) -> str:
    if not cal:
        return "- No calibration applied."
    gaps = cal.get("gaps", [])
    lines = [
        f"- DC noise bandwidth: **{cal.get('dc_noise_bandwidth_hz', 'n/a')} Hz** "
        f"(default 0.01 Hz)",
        f"- Propeller gain scale: **{cal.get('propeller_gain_scale', 1.0):.4f}**",
    ]
    if gaps:
        lines.append("")
        lines.append("**Known gaps:**")
        for g in gaps:
            lines.append(f"- {g}")
    return "\n".join(lines)


def generate_plots(results: Dict[str, Any], cfg: ORCAConfig = DEFAULT_CONFIG) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from orca_sim.config import VESSEL_TYPES
    from orca_sim.detection.snr import noise_voltage_matched_filter_v, snr_db
    from orca_sim.physics.corrosion_field import corrosion_voltage_v
    from orca_sim.physics.propeller_field import propeller_voltage_processed_v

    path = os.path.join(OUTPUT_DIR, "orca_sim_plots.png")
    sub = VESSEL_TYPES["type_039_ssk"]
    surf = VESSEL_TYPES["surface_isr"]

    r_uep_km = np.linspace(1, 60, 200)
    r_prop_m = np.linspace(100, 2500, 200)

    noise_dc = noise_voltage_matched_filter_v(cfg, dc_band=True)
    noise_prop = noise_voltage_matched_filter_v(cfg, dc_band=False)
    thresh = 10 ** (cfg.node.snr_threshold_db / 20.0)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    for vessel, label, color in [(sub, "Type-039 SSK", "#0D47A1"), (surf, "Surface ISR", "#2E7D32")]:
        sig = [corrosion_voltage_v(r * 1000, vessel, cfg) for r in r_uep_km]
        snr = [20 * np.log10(max(s / noise_dc, 1e-30)) for s in sig]
        ax.plot(r_uep_km, snr, lw=2, color=color, label=label)
    ax.axhline(cfg.node.snr_threshold_db, color="red", ls="--", lw=1, label="10 dB threshold")
    ax.axvline(SPEC_TARGETS["submarine_uep_range_km"], color="#0D47A1", ls=":", alpha=0.6)
    ax.axvline(SPEC_TARGETS["surface_uep_range_km"], color="#2E7D32", ls=":", alpha=0.6)
    ax.set_xlabel("Range (km)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title("UEP Corrosion Field Detection", fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1]
    sig_p = [propeller_voltage_processed_v(r, sub, cfg) for r in r_prop_m]
    snr_p = [snr_db(s, noise_prop) for s in sig_p]
    ax.plot(r_prop_m / 1000, snr_p, lw=2, color="#E65100", label="Type-039 DEMON")
    ax.axhline(cfg.node.snr_threshold_db, color="red", ls="--", lw=1, label="10 dB threshold")
    ax.axvline(SPEC_TARGETS["propeller_demon_range_km"], color="#E65100", ls=":", alpha=0.6)
    ax.set_xlabel("Range (km)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title("Propeller ELFE / DEMON Classification", fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("ORCA Coastal Array — Detection Range Model", fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path
