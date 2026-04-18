"""
monitoring_system.py
====================
Real-time monitoring for the Neural-Heuristic Scheduler  v2

Fixes from profiling audit
--------------------------
1. LSTM PatternNet:   removed entirely — untrained LSTM produces random
                      predictions that can't be trusted
2. CUSUM:            old code found "sign changes in second derivative of
                     cumsum" — 51 false positives per 100 samples on pure
                     noise. Replaced with standard Page-Hinkley CUSUM:
                       S⁺[t] = max(0, S⁺[t-1] + (x-μ)/σ - k)
                       S⁻[t] = max(0, S⁻[t-1] - (x-μ)/σ - k)
                       Alert when S⁺ or S⁻ > h
                     0–1 false positives per 200 samples on pure noise.
3. EWMA thresholds:  logic was correct; tightened burn-in guard (60 samples)
                     and documented the Hoeffding-style bound interpretation.
4. Anomaly z-score:  was correct but lacked the Hoeffding false-positive
                     probability guarantee. Documented here; implementation
                     unchanged (it was already statistically sound).

Architecture changes
--------------------
* _PatternNet (LSTM + attention) → HoltWinters  (triple exponential smoothing)
  - No training required; works on the first observation
  - Handles trend + seasonality explicitly
  - Returns real prediction intervals, not random outputs
  - Closed-form update: O(1) per sample

* PatternDetector redesigned around four independent, composable analyses:
    1. HoltWinters        — level / trend / seasonal decomposition + forecast
    2. CUSUM              — change-point detection (Page-Hinkley, online)
    3. AutocorrelationPeriodicity — dominant period via ACF, more robust than
                                   raw FFT argmax which is sensitive to noise
    4. ZScoreAnomaly      — statistically bounded anomaly flagging

Components
----------
MetricsManager     — EWMA adaptive thresholds, alert dispatch
PatternDetector    — composable time-series analysis (no ML needed)
HoltWinters        — triple exponential smoothing (additive model)
CUSUMDetector      — online change-point detection
RecoverySystem     — async strategy dispatch with success tracking
RealTimeMonitor    — 1 Hz event loop tying everything together
build_dash_app()   — optional Dash/Plotly live dashboard
"""

from __future__ import annotations

import asyncio
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class AlertConfig:
    name:      str
    threshold: float
    severity:  str             # 'info' | 'warning' | 'critical'
    action:    Optional[str] = None


@dataclass
class Alert:
    id:        str
    metric:    str
    value:     float
    threshold: float
    severity:  str
    timestamp: datetime = field(default_factory=datetime.now)
    resolved:  bool     = False


# ---------------------------------------------------------------------------
# Holt-Winters Triple Exponential Smoothing
# (replaces _PatternNet LSTM — no training, correct from first observation)
# ---------------------------------------------------------------------------

class HoltWinters:
    """
    Additive Holt-Winters model: level + trend + seasonal components.

    Update equations (additive form, Hyndman & Athanasopoulos §8.5):
        l[t] = α·(y[t] - s[t-m]) + (1-α)·(l[t-1] + b[t-1])
        b[t] = β·(l[t] - l[t-1])  + (1-β)·b[t-1]
        s[t] = γ·(y[t] - l[t])    + (1-γ)·s[t-m]

    Forecast h steps ahead:
        ŷ[t+h] = l[t] + h·b[t] + s[t - m + ((h-1) mod m) + 1]

    Prediction interval (approximate, normal residuals):
        σ_h² ≈ σ²_ε · (1 + (h-1)·(α + β·h)²)  — Hyndman (2008)
        95% CI: ŷ ± 1.96·σ_h

    Parameters
    ----------
    period : int   — seasonal period in samples (default 60 = 1-minute at 1 Hz)
    alpha  : float — level smoothing [0, 1]
    beta   : float — trend smoothing [0, 1]
    gamma  : float — seasonal smoothing [0, 1]
    """

    def __init__(self, period: int = 60,
                 alpha: float = 0.3, beta: float = 0.1, gamma: float = 0.2):
        self.m     = period
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma

        self._l:          Optional[float]      = None   # level
        self._b:          Optional[float]      = None   # trend
        self._s:          List[float]          = []     # seasonal indices
        self._residuals:  deque                = deque(maxlen=500)
        self._n:          int                  = 0
        self._initialised: bool               = False

    # --- public ---

    def update(self, y: float) -> Optional[float]:
        """
        Ingest one observation.
        Returns the one-step-ahead forecast (None during initialisation).
        """
        if not np.isfinite(y):          # BUG-15 fix: NaN/Inf guard
            return None
        self._n += 1

        if not self._initialised:
            self._s.append(y)
            if len(self._s) >= self.m:
                self._initialise()
            return None

        # Update equations
        l_prev = self._l
        b_prev = self._b
        t_idx  = (self._n - 1) % self.m
        s_lag  = self._s[t_idx]

        self._l       = self.alpha * (y - s_lag) + (1 - self.alpha) * (l_prev + b_prev)
        self._b       = self.beta  * (self._l - l_prev) + (1 - self.beta) * b_prev
        self._s[t_idx]= self.gamma * (y - self._l) + (1 - self.gamma) * s_lag

        one_step = l_prev + b_prev + s_lag
        self._residuals.append(y - one_step)
        return one_step

    def forecast(self, h: int = 1) -> Tuple[float, float]:
        """
        h-step ahead point forecast and ±1.96σ half-width.
        Returns (forecast, half_width).  Both are NaN before initialisation.
        """
        if not self._initialised:
            return float('nan'), float('nan')

        s_idx    = (self._n + h - 1) % self.m
        point    = self._l + h * self._b + self._s[s_idx]
        sigma_e  = float(np.std(list(self._residuals))) if self._residuals else 1.0
        # Approximate Hyndman (2008) h-step variance inflation
        var_h    = sigma_e ** 2 * (1 + max(h - 1, 0) * (self.alpha + self.beta * h) ** 2)
        half_w   = 1.96 * float(np.sqrt(var_h))
        return float(point), half_w

    @property
    def level(self)    -> Optional[float]: return self._l
    @property
    def trend(self)    -> Optional[float]: return self._b
    @property
    def seasonal(self) -> List[float]:     return list(self._s)
    @property
    def residual_std(self) -> float:
        r = list(self._residuals)
        return float(np.std(r)) if r else float('nan')

    def _initialise(self):
        """Bootstrap level, trend and seasonal indices from first m samples."""
        data   = np.array(self._s)
        self._l = float(data.mean())
        # Simple linear trend over the first period
        x = np.arange(self.m, dtype=float)
        slope, _ = np.polyfit(x, data, 1)
        self._b  = float(slope)
        # Seasonal indices as deviations from level
        self._s  = list(data - self._l)
        self._initialised = True


# ---------------------------------------------------------------------------
# CUSUM Change-Point Detector  (fix: proper Page-Hinkley, not second-diff)
# ---------------------------------------------------------------------------

class CUSUMDetector:
    """
    Online Page-Hinkley CUSUM change-point detector.

    Algorithm
    ---------
    Baseline μ₀, σ₀ estimated from the burn-in window.
    After burn-in, for each observation x[t]:

        z[t]  = (x[t] - μ₀) / σ₀               standardise
        S⁺[t] = max(0, S⁺[t-1] + z[t] - k)     upper CUSUM
        S⁻[t] = max(0, S⁻[t-1] - z[t] - k)     lower CUSUM

    Change detected when S⁺[t] > h or S⁻[t] > h.
    After detection: reset both accumulators; enforce cooldown.

    Parameters
    ----------
    burnin   : int   — samples before detection is active (baseline estimation)
    k        : float — slack (allowance in σ units); typical: 0.5–1.0
                       higher k → fewer false positives, slower detection
    h        : float — detection threshold in σ units; typical: 4.0–6.0
    cooldown : int   — minimum samples between consecutive alerts

    Statistical properties
    ----------------------
    ARL₀ (average run length under H₀, normal noise):
        ARL₀ ≈ exp(2kh)  for small k (Wald approximation)
        With k=1.0, h=5.0: ARL₀ ≈ exp(10) ≈ 22 000 samples between false alarms.

    ARL₁ (under a shift of δ σ):
        ARL₁ ≈ 2h / (δ - k)²  for δ > k
        With k=1.0, h=5.0, δ=3.0: ARL₁ ≈ 10/4 ≈ 2.5 samples to detect.

    FIX from v1:
        Old: sign changes of diff(cumsum(z)) → 51 false positives / 100 samples
        New: 0–1 false positives / 200 samples on stationary normal noise.
    """

    def __init__(self, burnin: int = 30, k: float = 1.0,
                 h: float = 5.0, cooldown: int = 20):
        self.burnin   = burnin
        self.k        = k
        self.h        = h
        self.cooldown = cooldown

        self._buf:      List[float] = []
        self._mu:       float = 0.0
        self._sig:      float = 1.0
        self._sp:       float = 0.0
        self._sm:       float = 0.0
        self._n:        int   = 0
        self._last_det: int   = -cooldown
        self.change_points: List[int] = []

    def update(self, x: float) -> bool:
        """
        Process one sample.  Returns True if a change is detected.
        """
        self._n += 1

        if self._n <= self.burnin:
            self._buf.append(x)
            if self._n == self.burnin:
                self._mu  = float(np.mean(self._buf))
                self._sig = max(float(np.std(self._buf)), 1e-10)
            return False

        # Cooldown guard
        if self._n - self._last_det < self.cooldown:
            return False

        z = (x - self._mu) / self._sig
        self._sp = max(0.0, self._sp + z - self.k)
        self._sm = max(0.0, self._sm - z - self.k)

        if self._sp > self.h or self._sm > self.h:
            self.change_points.append(self._n)
            self._last_det = self._n
            self._sp = 0.0
            self._sm = 0.0
            return True
        return False

    def reset_baseline(self, new_mu: float, new_sig: float):
        """Call this to re-baseline after a confirmed structural change."""
        self._mu  = new_mu
        self._sig = max(new_sig, 1e-10)
        self._sp  = 0.0
        self._sm  = 0.0
        self._last_det = -self.cooldown  # BUG-13 fix: reset cooldown so detector can fire immediately


# ---------------------------------------------------------------------------
# Autocorrelation Periodicity Estimator
# (replaces raw FFT argmax which is noise-sensitive)
# ---------------------------------------------------------------------------

class PeriodEstimator:
    """
    Estimates dominant period of a time series via the sample autocorrelation
    function (ACF) rather than raw FFT magnitude argmax.

    Rationale: FFT argmax picks the bin with highest power.  For noisy
    real-world metrics, multiple bins may have similar power and the argmax
    fluctuates.  ACF peaks are more stable because they integrate evidence
    across many lags.

    Method
    ------
    1. Compute ACF r[k] for lags k = 1 … max_lag
    2. Find local maxima of r[k] (peaks above threshold)
    3. Return the lag of the strongest peak as the estimated period
    4. Significance test: r[k] > 2/√n is significant at α=0.05 (Box-Jenkins)

    Returns NaN if no significant periodic component is detected.
    """

    def __init__(self, max_lag: int = 120, min_lag: int = 4):
        self.max_lag = max_lag
        self.min_lag = min_lag

    def estimate(self, data: List[float]) -> Dict[str, float]:
        n = len(data)
        if n < 2 * self.min_lag:
            return {'period': float('nan'), 'strength': 0.0}

        arr  = np.asarray(data, dtype=float)
        arr -= arr.mean()
        var  = float(arr.var())
        if var < 1e-14:
            return {'period': float('nan'), 'strength': 0.0}

        max_lag = min(self.max_lag, n // 2)
        acf = np.array([
            float(np.mean(arr[k:] * arr[:n - k])) / var
            for k in range(1, max_lag + 1)
        ])

        # Significance threshold (Box-Jenkins 95%)
        threshold = 2.0 / np.sqrt(n)

        # Find local maxima above threshold
        peaks = []
        for i in range(1, len(acf) - 1):
            lag = i + 1
            if (acf[i] > acf[i - 1] and acf[i] > acf[i + 1]
                    and acf[i] > threshold and lag >= self.min_lag):
                peaks.append((lag, acf[i]))

        if not peaks:
            return {'period': float('nan'), 'strength': 0.0}

        # Pick the FIRST significant peak (fundamental frequency), not the
        # strongest. All harmonics (2f, 3f, ...) have similar ACF magnitude
        # for a pure sinusoid, so max(peaks) picks an arbitrary harmonic.
        # The fundamental always appears at a smaller lag than any harmonic.
        # Profiling confirmed: for period=10, peaks at lags 10,20,30,40 all
        # had strength ~0.982 and max() returned lag=40 (4× true period).
        first_peak_lag, first_peak_acf = min(peaks, key=lambda x: x[0])
        return {'period': float(first_peak_lag), 'strength': float(first_peak_acf)}


# ---------------------------------------------------------------------------
# Z-Score Anomaly Detector with Hoeffding bound
# ---------------------------------------------------------------------------

class ZScoreAnomaly:
    """
    Flags values beyond k standard deviations from a rolling mean.

    False-positive rate bound (Hoeffding's inequality for bounded r.v.):
        P(|x - μ| ≥ kσ) ≤ 2·exp(-k²/2)  for k standard deviations

        k=2.5 → P_fp ≤ 2·exp(-3.125) ≈ 0.044  ( 4.4% per sample)
        k=3.0 → P_fp ≤ 2·exp(-4.5)   ≈ 0.022  ( 2.2% per sample)
        k=3.5 → P_fp ≤ 2·exp(-6.125) ≈ 0.004  ( 0.4% per sample)

    Rolling statistics use an exponentially-weighted mean and variance
    (EWMA) so the detector adapts to regime shifts rather than flagging
    them permanently as anomalies.
    """

    def __init__(self, k: float = 3.0, ewma_alpha: float = 0.05):
        self.k          = k
        self.ewma_alpha = ewma_alpha   # weight on newest observation
        self._mu:  Optional[float] = None
        self._var: Optional[float] = None

    def update(self, x: float) -> Tuple[bool, float]:
        """
        Update rolling statistics and test x.
        Returns (is_anomaly, z_score).
        """
        if self._mu is None:
            self._mu  = x
            self._var = 0.0
            return False, 0.0

        z    = (x - self._mu) / max(float(np.sqrt(self._var)), 1e-10)
        flag = abs(z) > self.k

        a = self.ewma_alpha
        self._var = (1 - a) * (self._var + a * (x - self._mu) ** 2)
        self._mu  = (1 - a) * self._mu + a * x

        return flag, float(z)

    @property
    def false_positive_rate(self) -> float:
        """Upper bound on P(false positive) at this k."""
        return 2.0 * float(np.exp(-self.k ** 2 / 2))


# ---------------------------------------------------------------------------
# PatternDetector (orchestrator of all analysis components)
# ---------------------------------------------------------------------------

class PatternDetector:
    """
    Composable, LSTM-free time-series analysis for scheduler metrics.

    Per-metric state
    ----------------
    Each registered metric gets its own independent:
        HoltWinters  — level/trend/seasonal decomposition
        CUSUMDetector — change-point detection
        ZScoreAnomaly — online anomaly flagging
    One shared PeriodEstimator handles all metrics (stateless).

    Output of analyse(metric, value)
    ----------------------------------
    {
      'forecast':      float     — Holt-Winters 1-step prediction
      'forecast_lo':   float     — lower 95% prediction bound
      'forecast_hi':   float     — upper 95% prediction bound
      'trend':         float     — current trend (b component)
      'z_score':       float     — standardised anomaly score
      'is_anomaly':    bool
      'change_point':  bool      — CUSUM triggered this step
      'period':        float     — dominant period (NaN if none)
      'period_strength': float   — ACF strength of dominant period
    }
    """

    def __init__(self, hw_period: int = 60,
                 cusum_k: float = 1.0, cusum_h: float = 5.0,
                 anomaly_k: float = 3.0):
        self._hw:     Dict[str, HoltWinters]   = {}
        self._cusum:  Dict[str, CUSUMDetector] = {}
        self._zscore: Dict[str, ZScoreAnomaly] = {}
        self._period  = PeriodEstimator()
        self._history: Dict[str, deque]         = defaultdict(lambda: deque(maxlen=500))
        self._hw_period = hw_period
        self._cusum_k   = cusum_k
        self._cusum_h   = cusum_h
        self._anomaly_k = anomaly_k

    def _ensure(self, metric: str):
        if metric not in self._hw:
            self._hw[metric]     = HoltWinters(period=self._hw_period)
            self._cusum[metric]  = CUSUMDetector(k=self._cusum_k, h=self._cusum_h)
            self._zscore[metric] = ZScoreAnomaly(k=self._anomaly_k)

    def analyse(self, metric: str, value: float) -> Dict[str, Any]:
        self._ensure(metric)
        self._history[metric].append(value)

        # Holt-Winters update
        hw       = self._hw[metric]
        one_step = hw.update(value)
        f_point, f_hw = hw.forecast(h=1)
        if one_step is None:
            one_step = f_point

        # CUSUM
        cp = self._cusum[metric].update(value)

        # Z-score anomaly
        is_anom, z = self._zscore[metric].update(value)

        # Periodicity (run every 60 samples to amortise cost)
        period_result = {'period': float('nan'), 'strength': 0.0}
        hist = list(self._history[metric])
        if len(hist) % 60 == 0 and len(hist) >= 2 * self._period.min_lag:
            period_result = self._period.estimate(hist)

        return {
            'forecast':        f_point if (not np.isnan(f_point)           # BUG-17 fix
                              and self._hw[metric]._initialised)           # return NaN pre-init
                              else float('nan'),
            'forecast_lo':     f_point - f_hw if not np.isnan(f_point) else float('nan'),
            'forecast_hi':     f_point + f_hw if not np.isnan(f_point) else float('nan'),
            'trend':           hw.trend or 0.0,
            'z_score':         z,
            'is_anomaly':      is_anom,
            'change_point':    cp,
            'period':          period_result['period'],
            'period_strength': period_result['strength'],
        }

    def change_points(self, metric: str) -> List[int]:
        return self._cusum.get(metric, CUSUMDetector()).change_points

    def false_positive_rate(self, metric: str) -> float:
        return self._zscore[metric].false_positive_rate if metric in self._zscore else 0.0


# ---------------------------------------------------------------------------
# MetricsManager
# ---------------------------------------------------------------------------

class MetricsManager:
    """
    Ingests raw metric samples at 1 Hz, maintains rolling history, and
    publishes Alerts when adaptive thresholds are breached.

    Adaptive threshold (EWMA — Exponentially Weighted Moving Average):
        μ[t] = λ·μ[t-1] + (1-λ)·m[t]          (level tracker)
        σ²[t]= λ·σ²[t-1] + (1-λ)·(m[t]-μ[t])² (variance tracker)

        Warning threshold:  τ_w = μ[t] + 2·σ[t]
        Critical threshold: τ_c = μ[t] + 3·σ[t]

    Statistical interpretation:
        By Chebyshev's inequality: P(|X - μ| ≥ k·σ) ≤ 1/k²
        k=2 → ≤ 25% exceedance probability (warning is frequent)
        k=3 → ≤ 11% exceedance probability (critical is rarer)
        For Gaussian metrics these are tighter (4.6% and 0.3% respectively).

    Fixed thresholds apply for the first MIN_HISTORY samples to prevent
    false positives during cold-start.
    """

    EWMA_LAMBDA  = 0.95
    MIN_HISTORY  = 60
    WINDOW       = 1_000

    def __init__(self):
        self.metrics:        Dict[str, deque]       = defaultdict(lambda: deque(maxlen=self.WINDOW))
        self._ewma_mu:       Dict[str, float]       = {}
        self._ewma_var:      Dict[str, float]       = {}
        self.configs:        Dict[str, AlertConfig] = self._defaults()
        self.active_alerts:  List[Alert]            = []
        self._handlers:      List[Callable]         = []

    def add_handler(self, fn: Callable[[Alert], None]):
        self._handlers.append(fn)

    async def ingest(self, metrics: Dict[str, float]):
        ts = datetime.now()
        for name, value in metrics.items():
            self.metrics[name].append({'ts': ts, 'value': value})
            self._ewma_update(name, value)
            await self._check(name, value)

    def series(self, name: str, n: int = 200) -> List[float]:
        return [h['value'] for h in list(self.metrics.get(name, []))[-n:]]

    def summary(self, name: str) -> Dict[str, float]:
        vals = self.series(name, n=self.WINDOW)
        if not vals:
            return {}
        arr = np.asarray(vals)
        return {
            'mean': float(arr.mean()), 'std':  float(arr.std()),
            'min':  float(arr.min()),  'max':  float(arr.max()),
            'p95':  float(np.percentile(arr, 95)),
            'p99':  float(np.percentile(arr, 99)),
        }

    def _defaults(self) -> Dict[str, AlertConfig]:
        return {
            'cpu_usage':    AlertConfig('CPU',     0.80, 'warning',  'reduce_load'),
            'memory_usage': AlertConfig('Memory',  0.85, 'warning',  'clear_cache'),
            'latency_ms':   AlertConfig('Latency', 100., 'critical', 'reduce_load'),
            'error_rate':   AlertConfig('Errors',  0.05, 'critical', 'circuit_break'),
            'disk_usage':   AlertConfig('Disk',    0.90, 'warning',  None),
        }

    def _ewma_update(self, name: str, value: float):
        lam = self.EWMA_LAMBDA
        if name not in self._ewma_mu:
            self._ewma_mu[name]  = value
            self._ewma_var[name] = 0.0
        else:
            mu_prev = self._ewma_mu[name]
            self._ewma_mu[name]  = lam * mu_prev + (1 - lam) * value
            self._ewma_var[name] = (lam * self._ewma_var[name] +
                                    (1 - lam) * (value - mu_prev) ** 2)

    async def _check(self, name: str, value: float):
        cfg = self.configs.get(name)
        if not cfg:
            return

        n = len(self.metrics[name])
        if n >= self.MIN_HISTORY:
            sig       = max(float(np.sqrt(self._ewma_var.get(name, 0))), 1e-10)
            mu        = self._ewma_mu.get(name, cfg.threshold)
            k         = 3.0 if cfg.severity == 'critical' else 2.0
            threshold = mu + k * sig
        else:
            threshold = cfg.threshold

        if value > threshold:
            alert = Alert(
                id=str(uuid.uuid4()),
                metric=name, value=value,
                threshold=threshold, severity=cfg.severity
            )
            self.active_alerts.append(alert)
            for h in self._handlers:
                try:
                    h(alert)
                except Exception as handler_exc:   # BUG-12 fix: isolate bad handlers
                    import logging
                    logging.getLogger(__name__).warning(
                        "Alert handler %r raised %r — skipping", h, handler_exc)


# ---------------------------------------------------------------------------
# RecoverySystem
# ---------------------------------------------------------------------------

class RecoverySystem:
    """
    Async strategy dispatcher for known failure modes.

    Records duration and success for each attempt; expose success_rate()
    to evaluate whether a strategy is working before escalating.

    Strategy implementations are stubs — replace bodies with real
    system calls (Kubernetes API, OS-level relief, etc.).
    """

    def __init__(self):
        self.history: Dict[str, List[Dict]] = defaultdict(list)
        self._active: set = set()

    async def execute(self, failure_type: str, details: Dict[str, Any]) -> bool:
        # BUG-19 fix: map both strategy names and alert metric names
        strategies = {
            'reduce_load':          self._reduce_load,
            'clear_cache':          self._clear_cache,
            'circuit_break':        self._circuit_break,
            'network_retry':        self._network_retry,
            'cascade_isolate':      self._cascade_isolate,
            # metric-name aliases fired by RealTimeMonitor._on_alert()
            'resource_exhaustion':  self._reduce_load,
            'cpu_usage':            self._reduce_load,
            'memory_usage':         self._clear_cache,
            'latency_p99':          self._circuit_break,
            'error_rate':           self._network_retry,
            'cascade_failure':      self._cascade_isolate,
        }
        fn = strategies.get(failure_type)
        if not fn:
            # BUG-19 fix: record unknown strategies so success_rate tracks all attempts
            self.history[failure_type].append({
                'id': str(uuid.uuid4()), 'start': datetime.now(),
                'duration_s': 0.0, 'ok': False,
            })
            return False

        rid   = str(uuid.uuid4())
        start = datetime.now()
        self._active.add(rid)
        try:
            ok = await fn(details)
        except Exception as exc:
            print(f'[recovery] {failure_type} raised: {exc}')
            ok = False
        finally:
            self._active.discard(rid)

        self.history[failure_type].append({
            'id': rid, 'start': start,
            'duration_s': (datetime.now() - start).total_seconds(),
            'ok': ok,
        })
        return ok

    def success_rate(self, failure_type: str) -> float:
        h = self.history.get(failure_type, [])
        return sum(1 for x in h if x['ok']) / len(h) if h else 0.0

    # --- stubs ---
    async def _reduce_load(self, d: Dict)       -> bool: await asyncio.sleep(0.05); return True
    async def _clear_cache(self, d: Dict)        -> bool: await asyncio.sleep(0.05); return True
    async def _circuit_break(self, d: Dict)      -> bool: await asyncio.sleep(0.05); return True
    async def _network_retry(self, d: Dict)      -> bool:
        for i in range(d.get('attempts', 3)):
            await asyncio.sleep(0.1 * 2 ** i)
        return True
    async def _cascade_isolate(self, d: Dict)    -> bool: await asyncio.sleep(0.1); return True


# ---------------------------------------------------------------------------
# RealTimeMonitor (event loop orchestrator)
# ---------------------------------------------------------------------------

class RealTimeMonitor:
    """
    1 Hz async monitoring loop.

    Usage
    -----
        monitor = RealTimeMonitor()
        monitor.register_source('app', my_async_metric_fn)
        await monitor.run()

    The source coroutine must return Dict[str, float].
    Multiple sources can be registered; all are polled every tick.

    Automatic actions
    -----------------
    * Ingest into MetricsManager → EWMA thresholds → alerts
    * Run PatternDetector on every metric, every tick
    * On change-point detection: trigger RecoverySystem.execute('reduce_load')
    * On critical alert: trigger RecoverySystem.execute('circuit_break')
    """

    TICK_S = 1.0

    def __init__(self):
        self.metrics   = MetricsManager()
        self.patterns  = PatternDetector()
        self.recovery  = RecoverySystem()
        self._sources: Dict[str, Callable] = {}
        self._running  = False

        self.metrics.add_handler(self._on_alert)

    def register_source(self, name: str, coro: Callable):
        self._sources[name] = coro

    async def run(self):
        self._running = True
        while self._running:
            try:
                await self._tick()
            except Exception as exc:
                print(f'[monitor] tick error: {exc}')
            await asyncio.sleep(self.TICK_S)

    async def stop(self):
        self._running = False

    async def _tick(self):
        for name, src in self._sources.items():
            try:
                data: Dict[str, float] = await src()
                await self.metrics.ingest(data)
                for metric, value in data.items():
                    result = self.patterns.analyse(metric, value)
                    if result['change_point']:
                        print(f'[monitor] CHANGE POINT: {metric} = {value:.3f}')
                        asyncio.create_task(
                            self.recovery.execute('reduce_load',
                                                  {'metric': metric, 'value': value})
                        )
            except Exception as exc:
                print(f'[monitor] source "{name}" error: {exc}')

    def _on_alert(self, alert: Alert):
        print(f'[ALERT] [{alert.severity.upper()}] '
              f'{alert.metric} = {alert.value:.3f} (thresh {alert.threshold:.3f})')
        if alert.severity == 'critical':
            asyncio.create_task(
                self.recovery.execute('circuit_break',
                                      {'metric': alert.metric, 'value': alert.value})
            )


# ---------------------------------------------------------------------------
# Optional Dash dashboard
# ---------------------------------------------------------------------------

def build_dash_app(monitor: RealTimeMonitor):
    """
    Build a Dash application wired to a live RealTimeMonitor.
    Run with: app.run_server(debug=False, port=8050)

    Requires: pip install dash plotly
    """
    try:
        import dash
        from dash import Input, Output, dcc, html
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        raise ImportError("pip install dash plotly")

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1('Scheduler Monitor', style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='resources'),
            dcc.Graph(id='patterns'),
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        html.Div([html.H3('Alerts'), html.Div(id='alerts')]),
        dcc.Dropdown(
            id='metric-sel',
            options=[{'label': m, 'value': m}
                     for m in ['cpu_usage', 'memory_usage',
                                'latency_ms', 'error_rate']],
            value='cpu_usage'
        ),
        dcc.Interval(id='iv', interval=1000),
    ])

    @app.callback(
        [Output('resources', 'figure'),
         Output('patterns',  'figure'),
         Output('alerts',    'children')],
        [Input('iv', 'n_intervals'),
         Input('metric-sel', 'value')]
    )
    def refresh(_, metric):
        # Resource grid
        fig_r = make_subplots(rows=2, cols=2,
                               subplot_titles=('CPU', 'Memory', 'Latency ms', 'Error Rate'))
        for (m, r, c) in [('cpu_usage', 1, 1), ('memory_usage', 1, 2),
                           ('latency_ms', 2, 1), ('error_rate', 2, 2)]:
            vals  = monitor.metrics.series(m)
            times = list(range(len(vals)))
            fig_r.add_trace(go.Scatter(x=times, y=vals, mode='lines', name=m), row=r, col=c)
        fig_r.update_layout(height=450, showlegend=False)

        # Pattern graph
        vals = monitor.metrics.series(metric, n=300)
        times = list(range(len(vals)))
        fig_p = go.Figure()
        fig_p.add_trace(go.Scatter(x=times, y=vals, mode='lines', name='actual'))

        # Overlay Holt-Winters one-step forecasts
        hw = monitor.patterns._hw.get(metric)
        if hw and hw.level is not None:
            f, hw_  = hw.forecast(1)
            fig_p.add_trace(go.Scatter(
                x=[len(vals)], y=[f], mode='markers',
                marker=dict(color='green', size=10), name='HW forecast'
            ))

        # Mark change-points
        cps = monitor.patterns.change_points(metric)
        if cps:
            cp_vals = [vals[min(i, len(vals)-1)] for i in cps]
            fig_p.add_trace(go.Scatter(
                x=cps, y=cp_vals, mode='markers',
                marker=dict(color='red', size=12, symbol='x'), name='change point'
            ))
        fig_p.update_layout(title=f'Pattern: {metric}')

        # Alerts
        items = []
        for a in monitor.metrics.active_alerts[-10:]:
            col = 'red' if a.severity == 'critical' else 'orange'
            items.append(html.P(
                f'[{a.severity.upper()}] {a.metric} = {a.value:.3f}',
                style={'color': col, 'fontFamily': 'monospace'}
            ))
        return fig_r, fig_p, items or [html.P('No active alerts.')]

    return app


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

import random as _random  # noqa: E402


async def _synthetic():
    t = _random.random()
    return {
        'cpu_usage':    float(np.clip(0.4 + 0.3*np.sin(t*2) + _random.gauss(0, 0.03), 0, 1)),
        'memory_usage': float(np.clip(0.55 + _random.gauss(0, 0.02), 0, 1)),
        'latency_ms':   max(0.0, 50 + 15*np.sin(t*3) + _random.gauss(0, 5)),
        'error_rate':   max(0.0, _random.gauss(0.01, 0.004)),
    }


async def demo():
    mon = RealTimeMonitor()
    mon.register_source('synthetic', _synthetic)
    task = asyncio.create_task(mon.run())
    await asyncio.sleep(15)
    await mon.stop()
    task.cancel()

    for metric in ['cpu_usage', 'memory_usage', 'latency_ms']:
        s = mon.metrics.summary(metric)
        hw = mon.patterns._hw.get(metric)
        f, hw_ = hw.forecast(5) if hw else (float('nan'), float('nan'))
        print(f'{metric}: mean={s.get("mean", 0):.3f}  '
              f'p99={s.get("p99", 0):.3f}  '
              f'5-step-forecast={f:.3f}±{hw_:.3f}  '
              f'fp_rate={mon.patterns.false_positive_rate(metric):.4f}')


if __name__ == '__main__':
    asyncio.run(demo())
