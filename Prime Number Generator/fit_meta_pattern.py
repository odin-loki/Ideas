#!/usr/bin/env python3
"""
fit_meta_pattern.py
═══════════════════

Empirical study of how the *relative* usefulness of local divisibility
filters and global PNT-style density heuristics changes with scale
``s = log10(n)``.  Three independent measurements are taken across a
dense scale grid and each is fit to three candidate functional forms by
maximum likelihood.

Measurements
------------

  M1.  **Residue-classifier excess AUC.**  At each scale we sample a
       balanced set of primes and composites and train a logistic
       regression on residues modulo a fixed list of small primes plus
       a 6k±1 indicator.  The held-out AUC minus the chance baseline
       0.5 quantifies how much information the residue features carry
       about primality at that scale.

  M2.  **Small-prime filter rejection rate.**  The probability that a
       random composite at this scale is rejected by trial-dividing
       against the same small-prime list.  This is the *useful-work
       rate* of a sieve-style pre-filter.

  M3.  **PNT density relative error.**  ``|observed - 1/ln(n)| / (1/ln(n))``
       on a uniform sample inside a window centred at 10**s.  Decays as
       PNT becomes more accurate.

Each curve is fit to three candidate forms and selected by AIC:

  Form A (power law):    f(s) = A · s^(-γ)
  Form B (exponential):  f(s) = A · exp(-b · s)
  Form C (rational):     f(s) = A / (1 + B · s)

Model selection: AIC = 2k - 2 ln L on the log-target Gaussian error model.
Lower AIC = better fit.  ΔAIC ≥ 2 is conventionally significant; ≥ 10 is
strong; ≥ 100 is overwhelming.

Outputs
-------
    fit_meta_pattern.json  — all measurements and fits
    fit_meta_pattern.md    — human-readable report
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import numpy as np

try:
    from sympy import isprime
except ImportError:  # pragma: no cover
    raise SystemExit("This script requires sympy.  Install with: pip install sympy")

try:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
except ImportError:  # pragma: no cover
    raise SystemExit("This script requires scikit-learn.  Install with: pip install scikit-learn")

try:
    from scipy.optimize import curve_fit
except ImportError:  # pragma: no cover
    raise SystemExit("This script requires scipy.  Install with: pip install scipy")


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

SCALES: List[float] = [
    1.0,  1.20, 1.40, 1.60, 1.80,
    2.0,  2.20, 2.40, 2.60, 2.80,
    3.0,  3.20, 3.40, 3.60, 3.80,
    4.0,  4.20, 4.40, 4.60, 4.80,
    5.0,  5.20, 5.40, 5.60, 5.80,
    6.0,  6.20, 6.40, 6.60, 6.80,
    7.0,  7.25, 7.50, 7.75,
    8.0,  8.25, 8.50, 8.75,
    9.0,  9.50,
]

# Number of (prime, composite) sample pairs per scale.  At each scale we draw
# a balanced sample so the AUC is on a directly comparable footing.
SAMPLES_PER_CLASS = 1000

# Small primes used as residue features and as the trial-division pre-filter.
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

OUT_JSON = Path(__file__).with_name("fit_meta_pattern.json")
OUT_MD   = Path(__file__).with_name("fit_meta_pattern.md")


# ─────────────────────────────────────────────────────────────────────────────
# Sampling: balanced primes / composites near a given scale
# ─────────────────────────────────────────────────────────────────────────────

def _sample_balanced(scale: float, n_each: int, rng: np.random.Generator) -> Tuple[List[int], List[int]]:
    """Return n_each primes and n_each composites drawn from a window near 10**scale."""
    n_center = int(round(10.0 ** scale))
    if n_center < 4:
        n_center = 4
    # Window width:  10 % of the scale, but at least enough to contain
    # comfortably more than 2·n_each primes by PNT.
    needed_window = int(2 * n_each * math.log(max(n_center, 10)))
    width = max(int(0.1 * n_center) + 1, needed_window, 200)
    lo = max(2, n_center - width)
    hi = n_center + width

    primes: List[int] = []
    composites: List[int] = []
    seen_p: set = set()
    seen_c: set = set()

    # Bias the draw to be efficient: at very large scales the prime density is
    # low, so we draw 6k±1 candidates first and let isprime() do the work.
    target_p = n_each
    target_c = n_each
    max_iters = 300 * n_each + 20_000
    iters = 0
    while (len(primes) < target_p or len(composites) < target_c) and iters < max_iters:
        iters += 1
        x = int(rng.integers(lo, hi + 1))
        if x < 2:
            continue
        # Only sample 6k±1 candidates for efficiency at large scale.  We must
        # also include some non-6k±1 composites so the residue-based classifier
        # can learn the 6k±1 rule, otherwise AUC saturates trivially.
        biased_to_6kpm1 = (rng.random() < 0.7)
        if biased_to_6kpm1 and not (x % 6 == 1 or x % 6 == 5):
            continue
        if isprime(x):
            if len(primes) < target_p and x not in seen_p:
                primes.append(x); seen_p.add(x)
        else:
            if len(composites) < target_c and x not in seen_c:
                composites.append(x); seen_c.add(x)

    if len(primes) < n_each // 2 or len(composites) < n_each // 2:
        raise RuntimeError(f"Could not collect a balanced sample at scale s={scale}: "
                           f"got {len(primes)} primes and {len(composites)} composites in {iters} iters.")
    return primes, composites


# ─────────────────────────────────────────────────────────────────────────────
# Measurement M1: residue-classifier excess AUC
# ─────────────────────────────────────────────────────────────────────────────

def _residue_features(numbers: List[int]) -> np.ndarray:
    """Residue features mod each small prime + 6k±1 indicator."""
    rows = []
    for x in numbers:
        feats = [float(x % p) for p in SMALL_PRIMES]
        feats.append(1.0 if (x % 6 == 1 or x % 6 == 5) else 0.0)
        rows.append(feats)
    return np.asarray(rows, dtype=np.float64)


def measure_residue_excess_auc(scale: float, rng: np.random.Generator) -> float:
    """
    M1: Train a logistic regression on residue features at this scale and
    return AUC − 0.5 (excess over chance) on a held-out split.
    """
    primes, composites = _sample_balanced(scale, SAMPLES_PER_CLASS, rng)
    X = _residue_features(primes + composites)
    y = np.array([1] * len(primes) + [0] * len(composites))

    perm = rng.permutation(len(y))
    X = X[perm]; y = y[perm]
    n_train = int(0.7 * len(y))
    X_tr, X_te = X[:n_train], X[n_train:]
    y_tr, y_te = y[:n_train], y[n_train:]

    clf = LogisticRegression(max_iter=4000, C=1.0)
    clf.fit(X_tr, y_tr)
    proba = clf.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_te, proba)
    return float(max(0.0, auc - 0.5))


# ─────────────────────────────────────────────────────────────────────────────
# Measurement M2: small-prime trial-division filter rejection rate
# ─────────────────────────────────────────────────────────────────────────────

def _passes_trial_filter(x: int) -> bool:
    """Return True if x passes the small-prime trial-division pre-filter."""
    for p in SMALL_PRIMES:
        if x == p:
            return True
        if x % p == 0:
            return False
    return True


def measure_filter_rejection_rate(scale: float, rng: np.random.Generator) -> float:
    """
    M2: Probability that a random composite at this scale is *rejected* by the
    small-prime pre-filter.  This is the filter's "useful-work" rate.
    """
    primes, composites = _sample_balanced(scale, SAMPLES_PER_CLASS, rng)
    rejected = sum(1 for x in composites if not _passes_trial_filter(x))
    return rejected / len(composites)


# ─────────────────────────────────────────────────────────────────────────────
# Measurement M3: PNT density accuracy (independent sanity-check curve)
# ─────────────────────────────────────────────────────────────────────────────

def measure_density_accuracy(scale: float, rng: np.random.Generator) -> float:
    """
    M3: |observed_density − expected_density| / expected_density
    Smaller = PNT regime is more accurate.  Should *decrease* with scale.
    """
    n_center = int(round(10.0 ** scale))
    if n_center < 100:
        n_center = 100
    width = max(int(0.05 * n_center) + 1, 5000)
    lo = max(2, n_center - width)
    hi = n_center + width

    sample_size = min(20_000, hi - lo)
    xs = rng.integers(lo, hi, sample_size)
    n_prime = sum(1 for x in xs if isprime(int(x)))
    obs_density = n_prime / sample_size
    exp_density = 1.0 / math.log(n_center)
    return abs(obs_density - exp_density) / exp_density


# ─────────────────────────────────────────────────────────────────────────────
# Functional forms and MLE fitting (Gaussian errors on log-targets)
# ─────────────────────────────────────────────────────────────────────────────

def f_power(s: np.ndarray, A: float, gamma: float) -> np.ndarray:
    return A * np.power(s, -gamma)


def f_exp(s: np.ndarray, A: float, b: float) -> np.ndarray:
    return A * np.exp(-b * s)


def f_rational(s: np.ndarray, A: float, B: float) -> np.ndarray:
    return A / (1.0 + B * s)


def fit_form(form: Callable, s: np.ndarray, y: np.ndarray, p0, name: str) -> Dict:
    """
    Fit *form* to (s, y) with Gaussian errors on log y (i.e. log-residuals
    have constant variance, which is the natural noise model for positive,
    multiplicative quantities).

    Returns dict with parameters, log-likelihood, AIC, BIC, R² (on log y).
    """
    log_y = np.log(np.maximum(y, 1e-12))

    def resid_log(s_, *params):
        return np.log(np.maximum(form(s_, *params), 1e-12))

    try:
        popt, pcov = curve_fit(resid_log, s, log_y, p0=p0, maxfev=20_000)
    except Exception as exc:  # pragma: no cover
        return {"name": name, "ok": False, "error": str(exc)}

    yhat_log = resid_log(s, *popt)
    resid = log_y - yhat_log
    n = len(s)
    k = len(popt)
    rss = float(np.sum(resid ** 2))
    sigma2 = max(rss / n, 1e-12)
    log_like = -0.5 * n * (math.log(2 * math.pi * sigma2) + 1.0)
    aic = 2 * k - 2 * log_like
    bic = k * math.log(n) - 2 * log_like
    ss_tot = float(np.sum((log_y - log_y.mean()) ** 2))
    r2 = 1.0 - rss / ss_tot if ss_tot > 0 else float("nan")

    return {
        "name": name,
        "ok": True,
        "params": [float(p) for p in popt],
        "param_stderr": [float(math.sqrt(max(0.0, pcov[i, i]))) for i in range(k)],
        "rss_log": rss,
        "log_likelihood": float(log_like),
        "aic": float(aic),
        "bic": float(bic),
        "r2_log": float(r2),
        "n": n,
        "k": k,
    }


def best_by_aic(fits: List[Dict]) -> Dict:
    ok = [f for f in fits if f.get("ok")]
    if not ok:
        return {}
    return min(ok, key=lambda f: f["aic"])


# ─────────────────────────────────────────────────────────────────────────────
# Main experiment
# ─────────────────────────────────────────────────────────────────────────────

def run_experiment() -> Dict:
    rng = np.random.default_rng(20260517)
    s_arr = np.array(SCALES, dtype=float)

    print(f"Running fit experiment over {len(SCALES)} scales: "
          f"s = {SCALES[0]} … {SCALES[-1]}")
    print(f"Samples per class per scale: {SAMPLES_PER_CLASS}")

    m1_vals, m2_vals, m3_vals = [], [], []
    timings: List[float] = []
    for i, s in enumerate(SCALES, 1):
        t0 = time.perf_counter()
        try:
            m1 = measure_residue_excess_auc(s, rng)
        except Exception as exc:
            print(f"  [{i:2d}/{len(SCALES)}] s={s}: M1 failed ({exc})")
            m1 = float("nan")
        try:
            m2 = measure_filter_rejection_rate(s, rng)
        except Exception as exc:
            print(f"  [{i:2d}/{len(SCALES)}] s={s}: M2 failed ({exc})")
            m2 = float("nan")
        try:
            m3 = measure_density_accuracy(s, rng)
        except Exception as exc:
            print(f"  [{i:2d}/{len(SCALES)}] s={s}: M3 failed ({exc})")
            m3 = float("nan")
        elapsed = time.perf_counter() - t0
        timings.append(elapsed)
        print(f"  [{i:2d}/{len(SCALES)}] s={s:5.2f}  "
              f"M1(excess AUC)={m1:.4f}  "
              f"M2(filter rej)={m2:.4f}  "
              f"M3(rel-density-err)={m3:.4f}  "
              f"({elapsed:.1f}s)")
        m1_vals.append(m1)
        m2_vals.append(m2)
        m3_vals.append(m3)

    measurements = {
        "scales": SCALES,
        "M1_residue_excess_auc": m1_vals,
        "M2_filter_rejection_rate": m2_vals,
        "M3_pnt_density_error": m3_vals,
        "samples_per_class": SAMPLES_PER_CLASS,
        "small_primes": SMALL_PRIMES,
        "rng_seed": 20260517,
    }

    # ── Fit each measurement to all three forms ──────────────────────────────
    fits_summary: Dict[str, Dict] = {}
    for label, vals in (
        ("M1_residue_excess_auc", m1_vals),
        ("M2_filter_rejection_rate", m2_vals),
        ("M3_pnt_density_error", m3_vals),
    ):
        y = np.array(vals, dtype=float)
        good = np.isfinite(y) & (y > 0)
        if good.sum() < 4:
            fits_summary[label] = {"skipped": "too few finite positive points"}
            continue
        s_fit = s_arr[good]
        y_fit = y[good]

        f_p = fit_form(f_power,    s_fit, y_fit, p0=(1.0, 0.5),  name="power_law      A·s^(-γ)")
        f_e = fit_form(f_exp,      s_fit, y_fit, p0=(1.0, 0.5),  name="exponential   A·exp(-b·s)")
        f_r = fit_form(f_rational, s_fit, y_fit, p0=(1.0, 0.5),  name="rational      A/(1+B·s)")
        winner = best_by_aic([f_p, f_e, f_r])
        fits_summary[label] = {
            "n_points": int(good.sum()),
            "fits": [f_p, f_e, f_r],
            "winner_by_aic": winner.get("name") if winner else None,
            "delta_aic_power_minus_exp": (
                f_p["aic"] - f_e["aic"]
                if (f_p.get("ok") and f_e.get("ok")) else None
            ),
        }

    return {"measurements": measurements, "fits": fits_summary}


# ─────────────────────────────────────────────────────────────────────────────
# Reporting
# ─────────────────────────────────────────────────────────────────────────────

def write_report(result: Dict, md_path: Path) -> None:
    meas = result["measurements"]
    fits = result["fits"]
    lines: List[str] = []
    lines.append("# Prime meta-pattern: empirical scale dependence of local and global generation methods")
    lines.append("")
    lines.append("Maximum-likelihood fit of three independent measurements (residue-classifier")
    lines.append("excess AUC; small-prime filter rejection rate; PNT density relative error) to")
    lines.append("three candidate functional forms (power law, exponential, rational), selected")
    lines.append("by AIC.")
    lines.append("")
    lines.append(f"- Scale samples (`s = log₁₀ n`): `{meas['scales']}`")
    lines.append(f"- Balanced sample size per class per scale: `{meas['samples_per_class']}`")
    lines.append(f"- Small primes used as features and pre-filter: `{meas['small_primes']}`")
    lines.append(f"- RNG seed: `{meas['rng_seed']}`")
    lines.append("")
    lines.append("## Raw measurements")
    lines.append("")
    lines.append("| `s` | M1 residue excess AUC | M2 filter rejection rate | M3 PNT density error |")
    lines.append("|---:|---:|---:|---:|")
    for s, m1, m2, m3 in zip(
        meas["scales"], meas["M1_residue_excess_auc"],
        meas["M2_filter_rejection_rate"], meas["M3_pnt_density_error"]
    ):
        lines.append(f"| {s} | {m1:.4f} | {m2:.4f} | {m3:.4f} |")
    lines.append("")

    lines.append("## Maximum-likelihood fits (Gaussian on log-target)")
    lines.append("")
    for label, summary in fits.items():
        lines.append(f"### {label}")
        if summary.get("skipped"):
            lines.append(f"  - Skipped: {summary['skipped']}")
            lines.append("")
            continue
        lines.append("")
        lines.append("| Form | Params | Param SE | log L | AIC | BIC | R² (log) |")
        lines.append("|---|---|---|---:|---:|---:|---:|")
        for fit in summary["fits"]:
            if not fit.get("ok"):
                lines.append(f"| {fit['name']} | FIT FAILED | | | | | |")
                continue
            params = ", ".join(f"{p:.4f}" for p in fit["params"])
            ses    = ", ".join(f"{e:.4f}" for e in fit["param_stderr"])
            lines.append(
                f"| `{fit['name']}` | {params} | {ses} | "
                f"{fit['log_likelihood']:.2f} | {fit['aic']:.2f} | "
                f"{fit['bic']:.2f} | {fit['r2_log']:.4f} |"
            )
        winner = summary.get("winner_by_aic")
        d_aic  = summary.get("delta_aic_power_minus_exp")
        lines.append("")
        lines.append(f"  - **Winner by AIC:** `{winner}`")
        if d_aic is not None:
            verdict = "power law preferred" if d_aic < -2 else (
                      "exponential preferred" if d_aic > 2 else
                      "indistinguishable (|ΔAIC| < 2)")
            lines.append(f"  - **Δ AIC (power − exp) = {d_aic:+.2f}** → {verdict}")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {md_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t0 = time.perf_counter()
    result = run_experiment()
    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_JSON}  ({OUT_JSON.stat().st_size:,} bytes)")
    write_report(result, OUT_MD)
    print(f"\nTotal runtime: {time.perf_counter() - t0:.1f}s")
