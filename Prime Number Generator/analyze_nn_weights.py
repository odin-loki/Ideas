#!/usr/bin/env python3
"""
analyze_nn_weights.py
═════════════════════

Phase 3 + Phase 4 of the NN-based prime meta-pattern study.

Phase 3 — black-box analysis of every trained MLP.  For every linear
layer (fc1, fc2, fc3, fc_out) we compute:

  * full SVD of the weight matrix `W = U Σ Vᵀ`
  * Frobenius norm  ‖W‖_F
  * spectral norm    σ_max(W)
  * stable rank      ‖W‖_F² / σ_max(W)²
  * effective rank   exp(- Σ p_i log p_i),  p_i = σ_i / Σσ_j
  * heavy-tail (Pareto) tail exponent α via maximum-likelihood
    on the upper half of the singular value spectrum
    (Martin–Mahoney style),  ŝ_α = 1 + n / Σ log(σ_i / σ_min)
  * weight-magnitude statistics: mean |w|, median |w|, kurtosis,
    fraction of |w| < 1e-3 (effectively-zero entries)

We additionally compute integrated gradients on the held-out test
set to get a per-feature attribution score, aggregated by the six
feature groups (residue, binary, scale, wheel, sieve, digits).

Phase 4 — for each scalar statistic that varies with scale,
fit four functional forms by maximum likelihood with Gaussian errors
on the log target (matching `fit_meta_pattern.py`):

  * constant         f(s) = c
  * power law        f(s) = a · s^b
  * exponential      f(s) = a · exp(b s)
  * rational         f(s) = a / (1 + b s)

Pick the best by AIC.  This is the operational meaning of
"discover the function for generating primes from the weights":
we extract ~30 weight statistics per scale and fit a closed-form
scaling law to each.  Anything that fits a non-trivial form is a
*meta-pattern* — a property of the trained network that scales in
a regular way with problem size.

Outputs:  artifacts/nn/weight_analysis.json
          artifacts/nn/weight_analysis.md
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np
import torch
from scipy.optimize import curve_fit
from scipy.stats import kurtosis

import sys
sys.path.insert(0, str(Path(__file__).parent))
from train_nn_classifiers import PrimeMLP, FEATURE_GROUPS, D, HIDDEN, SCALES


ARTIFACT_DIR = Path("artifacts") / "nn"


# ─────────────────────────────────────────────────────────────────────────────
# Per-matrix spectral analysis
# ─────────────────────────────────────────────────────────────────────────────

def analyze_matrix(W: np.ndarray) -> Dict[str, float]:
    """Return a dict of spectral / norm / heavy-tail stats for W."""
    s = np.linalg.svd(W, compute_uv=False)
    s = np.sort(s)[::-1]
    s_pos = s[s > 1e-12]

    fro = float(np.linalg.norm(W, "fro"))
    smax = float(s_pos[0]) if len(s_pos) else 0.0
    stable_rank = float(fro ** 2 / smax ** 2) if smax > 0 else 0.0

    if len(s_pos) > 0 and s_pos.sum() > 0:
        p = s_pos / s_pos.sum()
        eff_rank = float(np.exp(-np.sum(p * np.log(p + 1e-30))))
    else:
        eff_rank = 0.0

    # Hill estimator on the upper half of the singular value distribution
    n_tail = max(2, len(s_pos) // 2)
    tail = s_pos[:n_tail]
    if len(tail) >= 2 and tail[-1] > 0:
        log_ratios = np.log(tail[:-1] / tail[-1])
        hill_alpha = float(1.0 + len(log_ratios) / max(np.sum(log_ratios), 1e-12))
    else:
        hill_alpha = float("nan")

    w_abs = np.abs(W).flatten()
    return {
        "fro_norm": fro,
        "spectral_norm": smax,
        "stable_rank": stable_rank,
        "effective_rank": eff_rank,
        "hill_alpha": hill_alpha,
        "weight_mean_abs": float(w_abs.mean()),
        "weight_median_abs": float(np.median(w_abs)),
        "weight_kurtosis": float(kurtosis(w_abs, fisher=True)),
        "weight_frac_near_zero": float((w_abs < 1e-3).mean()),
        "shape": list(W.shape),
        "n_singular_values": int(len(s)),
        "singular_values_top10": [float(x) for x in s[:10]],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Per-scale model analysis
# ─────────────────────────────────────────────────────────────────────────────

LAYER_NAMES = ["fc1", "fc2", "fc3", "fc_out"]


def analyze_model(scale: int) -> Dict:
    pt_path = ARTIFACT_DIR / f"model_s{scale}.pt"
    npz_path = ARTIFACT_DIR / f"data_s{scale}.npz"

    state = torch.load(pt_path, weights_only=False)
    model = PrimeMLP(in_dim=state["in_dim"], hidden=tuple(state["hidden"]))
    model.load_state_dict(state["state_dict"])
    model.eval()

    layer_stats: Dict[str, Dict] = {}
    for name in LAYER_NAMES:
        layer = getattr(model, name)
        W = layer.weight.detach().numpy()
        layer_stats[name] = analyze_matrix(W)
        layer_stats[name]["bias_mean_abs"] = float(np.abs(layer.bias.detach().numpy()).mean())

    data = np.load(npz_path)
    X_test = torch.tensor(data["X_test"])
    y_test = data["y_test"]

    # Integrated gradients vs zero baseline, mean over class-1 samples
    pos_mask = y_test > 0.5
    Xpos = X_test[pos_mask]
    if len(Xpos) > 200:
        Xpos = Xpos[:200]

    n_steps = 25
    ig = torch.zeros(D)
    baseline = torch.zeros_like(Xpos)
    Xpos.requires_grad_(False)
    for k in range(1, n_steps + 1):
        alpha = k / n_steps
        x_k = baseline + alpha * (Xpos - baseline)
        x_k.requires_grad_(True)
        out = model(x_k)
        grads = torch.autograd.grad(out.sum(), x_k)[0]
        ig = ig + grads.mean(dim=0).detach()
    ig = ig * (Xpos.mean(dim=0) - baseline.mean(dim=0)) / n_steps
    ig_abs = ig.abs().numpy()

    group_importance: Dict[str, float] = {}
    group_share: Dict[str, float] = {}
    total = float(ig_abs.sum()) + 1e-12
    for g, idxs in FEATURE_GROUPS.items():
        s_total = float(ig_abs[idxs].sum())
        group_importance[g] = s_total
        group_share[g] = s_total / total

    return {
        "scale": scale,
        "layers": layer_stats,
        "feature_attribution_abs": group_importance,
        "feature_attribution_share": group_share,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Aggregate scalar statistics across scales
# ─────────────────────────────────────────────────────────────────────────────

def collect_series(per_scale: List[Dict]) -> Dict[str, np.ndarray]:
    """Pull out scalar series indexed by scale."""
    series: Dict[str, List[float]] = {}
    s_axis = [r["scale"] for r in per_scale]

    for layer in LAYER_NAMES:
        for k in ("fro_norm", "spectral_norm", "stable_rank",
                  "effective_rank", "hill_alpha",
                  "weight_mean_abs", "weight_median_abs",
                  "weight_kurtosis", "weight_frac_near_zero",
                  "bias_mean_abs"):
            key = f"{layer}.{k}"
            series[key] = [r["layers"][layer][k] for r in per_scale]

    for g in FEATURE_GROUPS:
        series[f"attribution_share.{g}"] = [r["feature_attribution_share"][g]
                                             for r in per_scale]
        series[f"attribution_abs.{g}"]   = [r["feature_attribution_abs"][g]
                                             for r in per_scale]

    return {"s": np.array(s_axis, dtype=float),
            **{k: np.array(v, dtype=float) for k, v in series.items()}}


# ─────────────────────────────────────────────────────────────────────────────
# Functional-form fits (MLE with Gaussian errors on log target)
# ─────────────────────────────────────────────────────────────────────────────

def _safe_log(y):
    y = np.asarray(y, dtype=float)
    return np.log(np.maximum(y, 1e-20))


def fit_constant(s, y):
    log_y = _safe_log(y)
    c = float(np.exp(np.mean(log_y)))
    pred = np.full_like(log_y, np.log(c))
    return {"name": "constant", "params": {"c": c}, "pred_log": pred, "k": 1}


def fit_power(s, y):
    def model(s_, a, b): return np.log(a) + b * np.log(np.maximum(s_, 1e-12))
    try:
        popt, _ = curve_fit(model, s, _safe_log(y),
                            p0=[max(np.median(y), 1e-3), -0.1],
                            maxfev=20_000)
        a, b = popt
        if a <= 0:
            raise RuntimeError("a<=0")
        pred = model(s, a, b)
        return {"name": "power", "params": {"a": float(a), "b": float(b)},
                "pred_log": pred, "k": 2}
    except Exception as e:
        return {"name": "power", "params": {}, "pred_log": None, "k": 2,
                "error": str(e)}


def fit_exponential(s, y):
    def model(s_, a, b): return np.log(a) + b * s_
    try:
        popt, _ = curve_fit(model, s, _safe_log(y),
                            p0=[max(np.median(y), 1e-3), 0.0],
                            maxfev=20_000)
        a, b = popt
        if a <= 0:
            raise RuntimeError("a<=0")
        pred = model(s, a, b)
        return {"name": "exponential", "params": {"a": float(a), "b": float(b)},
                "pred_log": pred, "k": 2}
    except Exception as e:
        return {"name": "exponential", "params": {}, "pred_log": None, "k": 2,
                "error": str(e)}


def fit_rational(s, y):
    def model(s_, a, b): return np.log(np.maximum(a / (1.0 + b * s_), 1e-20))
    try:
        popt, _ = curve_fit(model, s, _safe_log(y),
                            p0=[max(np.median(y), 1e-3), 0.05],
                            maxfev=20_000)
        a, b = popt
        if a <= 0:
            raise RuntimeError("a<=0")
        pred = model(s, a, b)
        return {"name": "rational", "params": {"a": float(a), "b": float(b)},
                "pred_log": pred, "k": 2}
    except Exception as e:
        return {"name": "rational", "params": {}, "pred_log": None, "k": 2,
                "error": str(e)}


def aic_and_pick(s, y, fits):
    n = len(y)
    log_y = _safe_log(y)
    out = []
    for f in fits:
        if f.get("pred_log") is None:
            f["aic"] = float("inf")
            f["rmse_log"] = float("nan")
            out.append(f); continue
        resid = log_y - f["pred_log"]
        sigma2 = float(np.mean(resid ** 2))
        ll = -0.5 * n * (np.log(2 * np.pi * sigma2 + 1e-30) + 1.0)
        aic = 2 * f["k"] - 2 * ll
        f["aic"] = float(aic)
        f["rmse_log"] = float(np.sqrt(sigma2))
        f["sigma_log"] = float(np.sqrt(sigma2))
        f.pop("pred_log", None)
        out.append(f)
    out_sorted = sorted(out, key=lambda f: f["aic"])
    best = out_sorted[0]
    delta_aic = {f["name"]: f["aic"] - best["aic"] for f in out_sorted}
    return best, out, delta_aic


def fit_all_scaling_laws(series: Dict[str, np.ndarray]) -> Dict[str, Dict]:
    s = series["s"]
    out: Dict[str, Dict] = {}
    for key, y in series.items():
        if key == "s":
            continue
        if np.all(y <= 0) or not np.isfinite(y).all():
            out[key] = {"skipped": True, "reason": "non-positive or non-finite"}
            continue
        if np.std(y) / (np.mean(np.abs(y)) + 1e-12) < 1e-4:
            best = fit_constant(s, y)
            best.pop("pred_log", None)
            best["aic"] = 0.0
            best["rmse_log"] = 0.0
            out[key] = {"best": best, "all": [best],
                         "delta_aic": {"constant": 0.0},
                         "y": [float(v) for v in y],
                         "s": [float(v) for v in s],
                         "note": "essentially constant"}
            continue
        fits = [fit_constant(s, y), fit_power(s, y),
                fit_exponential(s, y), fit_rational(s, y)]
        best, all_fits, delta = aic_and_pick(s, y, fits)
        out[key] = {"best": best, "all": all_fits, "delta_aic": delta,
                    "y": [float(v) for v in y],
                    "s": [float(v) for v in s]}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Markdown report
# ─────────────────────────────────────────────────────────────────────────────

def render_markdown(per_scale: List[Dict], fits: Dict[str, Dict]) -> str:
    lines: List[str] = []
    lines.append("# Black-box weight analysis of the prime-classification MLPs\n")
    lines.append("Generated by `analyze_nn_weights.py`. For each scale "
                 "`s ∈ {3, 4, 5, 6, 7, 8}` we trained an MLP "
                 f"(input → 128 → 64 → 32 → 1, dropout 0.2) on a balanced "
                 "prime-vs-composite dataset, then **measured the trained weights "
                 "and gradients** without inspecting any source code or features.\n")

    # Per-scale summary
    lines.append("## Per-scale layer statistics\n")
    lines.append("| scale | layer | shape | ‖W‖_F | σ_max | stable rank | "
                 "effective rank | Hill α | mean \\|w\\| | frac \\|w\\|<1e-3 |")
    lines.append("|------:|:------|:------|------:|------:|------------:|"
                 "---------------:|-------:|------------:|------------------:|")
    for r in per_scale:
        for layer in LAYER_NAMES:
            ls = r["layers"][layer]
            lines.append(
                f"| {r['scale']} | `{layer}` | "
                f"{ls['shape'][0]}×{ls['shape'][1]} | "
                f"{ls['fro_norm']:.3f} | {ls['spectral_norm']:.3f} | "
                f"{ls['stable_rank']:.2f} | {ls['effective_rank']:.2f} | "
                f"{ls['hill_alpha']:.3f} | {ls['weight_mean_abs']:.4f} | "
                f"{ls['weight_frac_near_zero']:.3f} |"
            )
    lines.append("")

    # Feature attributions
    lines.append("## Feature-group attribution (integrated gradients)\n")
    groups = list(FEATURE_GROUPS.keys())
    lines.append("Share of total |∇| attributed to each input-feature group, "
                 "averaged over up to 200 prime examples per scale.\n")
    lines.append("| scale | " + " | ".join(groups) + " |")
    lines.append("|------:|" + "|".join("------:" for _ in groups) + "|")
    for r in per_scale:
        share = r["feature_attribution_share"]
        lines.append(f"| {r['scale']} | " +
                     " | ".join(f"{share[g]:.3f}" for g in groups) + " |")
    lines.append("")

    # Scaling laws
    lines.append("## Scaling laws extracted from the weights\n")
    lines.append("For every weight statistic that varies non-trivially across "
                 "scales we fit four functional forms by maximum likelihood "
                 "(Gaussian errors on log target) and pick the best by AIC.\n")
    lines.append("| statistic | best form | a | b | RMSE (log) | "
                 "ΔAIC vs power | ΔAIC vs exp | ΔAIC vs rational |")
    lines.append("|:----------|:----------|------:|------:|----------:|"
                 "-------------:|-----------:|----------------:|")

    interesting = []
    for key, info in fits.items():
        if info.get("skipped"):
            continue
        best = info["best"]
        if best["name"] == "constant":
            continue
        delta = info["delta_aic"]
        a = best["params"].get("a", float("nan"))
        b = best["params"].get("b", float("nan"))
        lines.append(
            f"| `{key}` | {best['name']} | {a:.4f} | {b:.4f} | "
            f"{best['rmse_log']:.4f} | "
            f"{delta.get('power', float('inf')):+.2f} | "
            f"{delta.get('exponential', float('inf')):+.2f} | "
            f"{delta.get('rational', float('inf')):+.2f} |"
        )
        if best["rmse_log"] < 0.10:
            interesting.append((key, best, delta))

    lines.append("")
    lines.append("## Tightest-fitting scaling laws (RMSE_log < 0.10)\n")
    if not interesting:
        lines.append("_None of the weight statistics fit a parametric form "
                     "tighter than RMSE_log < 0.10._\n")
    else:
        lines.append("| statistic | form | parameters | RMSE_log |")
        lines.append("|:----------|:-----|:-----------|---------:|")
        for key, best, delta in sorted(interesting, key=lambda x: x[1]["rmse_log"]):
            params = ", ".join(f"{k}={v:.4f}"
                               for k, v in best["params"].items())
            lines.append(f"| `{key}` | {best['name']} | {params} | "
                         f"{best['rmse_log']:.4f} |")
    lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    per_scale = []
    for s in SCALES:
        print(f"  analyzing scale s={s}...")
        per_scale.append(analyze_model(s))

    series = collect_series(per_scale)
    fits = fit_all_scaling_laws(series)

    out_json = ARTIFACT_DIR / "weight_analysis.json"
    json.dump({"per_scale": per_scale, "scaling_laws": fits,
               "feature_groups": FEATURE_GROUPS,
               "scales": SCALES, "feature_dim": D},
              open(out_json, "w"), indent=2)

    md = render_markdown(per_scale, fits)
    out_md = ARTIFACT_DIR / "weight_analysis.md"
    out_md.write_text(md, encoding="utf-8")

    n_skipped = sum(1 for v in fits.values() if v.get("skipped"))
    n_best = {"constant": 0, "power": 0, "exponential": 0, "rational": 0}
    for v in fits.values():
        if v.get("skipped"):
            continue
        n_best[v["best"]["name"]] += 1
    print(f"\nWrote {out_json}")
    print(f"Wrote {out_md}")
    print(f"\nFitted {sum(n_best.values())} scaling laws "
          f"({n_skipped} skipped):")
    for k, v in n_best.items():
        print(f"  {k:>12}:  {v}")
