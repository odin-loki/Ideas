"""
HARCF Benchmark Implementation
================================
Generalised Hyperbolic Interacting Multiple Model Filter
with Square-Root Cubature Kalman Filter Propagation (GH-SR-IMM)
and Multi-Sensor Joint Probabilistic Data Association (GH-JPDA)

Reference implementation for:
"Robust Multi-Target Tracking under Non-Gaussian Noise via
 Generalised Hyperbolic IMM Filtering and GH-JPDA Data Association"

Benchmark includes:
  - GH-SR-IMM        : proposed single-target filter
  - GH-JPDA          : proposed multi-target/multi-sensor extension
  - Huang 2017        : Student-t Kalman Filter (IEEE T-SP baseline)
  - Agamennoni 2012   : Variational Bayes Kalman Filter (IEEE T-SP baseline)

Eight single-target test scenarios:
  Gaussian, Heavy-Tail, Levy, Maneuver, Correlated-Q,
  Mixed-Regime, Bimodal, Jerk

Four multi-target test scenarios (2 targets, 2 sensors):
  Crossing, Parallel, Crossing+HeavyTail, Diverging

Score metric (single-target):
  S = RMSE + 0.4*|mean(NIS)-1| + 0.2*std(NIS)   [lower = better]

Score metric (multi-target):
  GOSPA (Generalised Optimal SubPattern Assignment, c=5, p=2)

Usage:
  python harcf_benchmark.py
"""

import numpy as np
from collections import deque
from scipy.special import kv as besselk, gammaln
from scipy.linalg import qr
from scipy.optimize import linear_sum_assignment

# ── CONSTANTS ─────────────────────────────────────────────────
DT = 1.0
F2 = np.array([[1., DT], [0., 1.]])          # CV transition
H2 = np.array([[1., 0.]])                     # position measurement
H3 = np.array([[1., 0., 0.]])                 # position measurement (3D state)
R0 = 1.0                                      # baseline measurement noise
Q0 = np.array([[DT**3/3, DT**2/2],           # baseline process noise
               [DT**2/2, DT + 0.001]]) * 0.01
SD3 = float(np.sqrt(0.3))
N = 500                                       # steps per scenario
SEEDS = [42, 43, 44, 45, 46]                 # evaluation seeds
Tr3 = np.array([[0.95, 0.04, 0.01],          # IMM transition matrix
                [0.04, 0.95, 0.01],
                [0.20, 0.20, 0.60]])

# Multi-target constants
H_pos = np.array([[1., 0.]])
H_vel = np.array([[0., 1.]])
R0_pos = 1.0
R0_vel = 2.0
LAMBDA_C = 0.05
GATE_THRESH = 16.0

# ── SCENARIO GENERATORS ───────────────────────────────────────

def gen_single(kind, seed=42, n=N):
    """Generate single-target tracking scenario."""
    rng = np.random.default_rng(seed)
    x = np.array([0., 0.5])
    L = np.linalg.cholesky(Q0)
    truth, meas = [], []
    ar = 0.
    for k in range(n):
        w = L @ rng.standard_normal(2)
        if kind == 'maneuver' and k == n // 2:
            x[1] += 3.0
        if kind == 'jerk' and n // 3 <= k < n // 3 + n // 6:
            x[1] += 0.04
        x = F2 @ x + w
        truth.append(x.copy())
        if kind == 'gaussian':
            v = rng.standard_normal()
        elif kind == 'heavy_tail':
            v = rng.standard_t(2) * 0.8 if rng.random() < 0.12 else rng.standard_normal()
        elif kind == 'levy':
            U = rng.uniform(-np.pi / 2, np.pi / 2)
            W = rng.exponential(1.)
            a = 1.6
            v = float(np.clip(
                (np.sin(a * U) / np.cos(U) ** (1 / a)) *
                (np.cos(U * (1 - a)) / W) ** ((1 - a) / a) * 0.6, -15, 15))
        elif kind == 'maneuver':
            v = rng.standard_normal()
        elif kind == 'correlated':
            ar = 0.7 * ar + rng.standard_normal() * np.sqrt(1 - 0.49)
            v = ar
        elif kind == 'mixed':
            if k < 150:
                v = rng.standard_normal()
            elif k < 250:
                v = rng.standard_t(2) * 0.8 if rng.random() < 0.12 else rng.standard_normal()
            else:
                ar = 0.7 * ar + rng.standard_normal() * np.sqrt(1 - 0.49)
                v = ar
        elif kind == 'bimodal':
            v = rng.standard_normal() * (3.0 if rng.random() < 0.20 else 1.0)
        elif kind == 'jerk':
            v = rng.standard_normal()
        else:
            v = rng.standard_normal()
        meas.append(float(x[0]) + v)
    return np.array(truth), np.array(meas)


def gen_multi(kind, seed=42, n=300, n_targets=2):
    """Generate multi-target, multi-sensor tracking scenario."""
    rng = np.random.default_rng(seed)
    L = np.linalg.cholesky(Q0)
    if kind == 'crossing':
        xs = [np.array([-15., 0.4]), np.array([15., -0.4])]
    elif kind == 'parallel':
        xs = [np.array([-15., 0.4]), np.array([-12., 0.4])]
    elif kind == 'diverging':
        xs = [np.array([0., 0.3]), np.array([0., -0.3])]
    elif kind == 'heavy_tail':
        xs = [np.array([-15., 0.4]), np.array([15., -0.4])]
    else:
        xs = [np.array([-15., 0.4]), np.array([15., -0.4])]

    truths = [[] for _ in range(n_targets)]
    meas1_list, meas2_list = [], []

    for k in range(n):
        for i in range(n_targets):
            w = L @ rng.standard_normal(2)
            xs[i] = F2 @ xs[i] + w
            truths[i].append(xs[i].copy())

        step1, step2 = [], []
        for i in range(n_targets):
            v1 = rng.standard_t(2) * 0.8 if (kind == 'heavy_tail' and rng.random() < 0.15) \
                else rng.standard_normal()
            step1.append(float(xs[i][0]) + v1 * np.sqrt(R0_pos))
            step2.append(float(xs[i][1]) + rng.standard_normal() * np.sqrt(R0_vel))

        for _ in range(rng.poisson(LAMBDA_C * 2)):
            step1.append(rng.uniform(-25, 25))
        for _ in range(rng.poisson(LAMBDA_C * 2)):
            step2.append(rng.uniform(-3, 3))

        rng.shuffle(step1)
        rng.shuffle(step2)
        meas1_list.append(np.array(step1))
        meas2_list.append(np.array(step2))

    return [np.array(t) for t in truths], meas1_list, meas2_list


# ── SPD UTILITIES ─────────────────────────────────────────────

def spd_ensure(P, eps=1e-8):
    P = (P + P.T) / 2
    try:
        np.linalg.cholesky(P)
        return P
    except np.linalg.LinAlgError:
        w, v = np.linalg.eigh(P)
        return v @ np.diag(np.maximum(w, eps)) @ v.T


# ── GIG / NIG ─────────────────────────────────────────────────

def gig_moments(lam, chi, psi):
    """Moments of Generalised Inverse Gaussian distribution."""
    chi = max(chi, 1e-10)
    psi = max(psi, 1e-10)
    z = float(np.clip(np.sqrt(chi * psi), 1e-10, 500.))
    try:
        Kl = besselk(abs(lam), z)
        Kl1 = besselk(abs(lam + 1), z)
        Klm1 = besselk(abs(lam - 1), z)
        if not (np.isfinite(Kl) and Kl > 1e-300):
            return 1.0, 1.0
        ev = float(np.clip(np.sqrt(chi / psi) * Kl1 / Kl, 1e-6, 1e5))
        einv = float(np.clip(np.sqrt(psi / chi) * Klm1 / Kl, 1e-6, 1e5))
        return ev, einv
    except Exception:
        return 1.0, 1.0


def nig_log_likelihood(nu, chi, psi, R_base):
    """NIG marginal log-likelihood for scalar innovation nu."""
    chi = max(chi, 1e-10)
    psi = max(psi, 1e-10)
    R_base = max(R_base, 1e-6)
    delta = np.sqrt(chi)
    alpha = np.sqrt(psi / R_base)
    arg = chi + nu ** 2 / R_base
    sqrt_arg = np.sqrt(max(arg, 1e-10))
    ad = float(np.clip(alpha * sqrt_arg, 1e-10, 500.))
    try:
        K1 = besselk(1, ad)
        if not np.isfinite(K1) or K1 < 1e-300:
            return float(np.exp(-0.5 * nu ** 2 / R_base) / np.sqrt(2 * np.pi * R_base))
        log_p = (np.log(alpha) + np.log(delta) - np.log(np.pi)
                 - 0.5 * np.log(arg) + alpha * delta + np.log(K1))
        return float(np.exp(np.clip(log_p, -700, 0)))
    except Exception:
        return float(np.exp(-0.5 * nu ** 2 / R_base) / np.sqrt(2 * np.pi * R_base))


def gauss_likelihood(nu, S):
    S = max(float(S), 1e-9)
    return float(np.exp(-0.5 * nu ** 2 / S) / np.sqrt(2 * np.pi * S))


# ── SQUARE ROOT CKF ───────────────────────────────────────────

def sr_predict(x, S, Q, F=F2):
    """Square-root CKF predict step via QR decomposition."""
    n = len(x)
    sq = np.sqrt(n)
    pts = np.hstack([x[:, None] + sq * S, x[:, None] - sq * S]).T
    pp = (F @ pts.T).T
    xp = pp.mean(0)
    dp = pp - xp
    try:
        Lq = np.linalg.cholesky(Q)
    except np.linalg.LinAlgError:
        Lq = np.eye(n) * 1e-5
    A = np.vstack([dp / np.sqrt(2 * n), Lq.T])
    _, R = qr(A, mode='economic')
    Sp = R[:n, :n]
    sg = np.sign(np.diag(Sp))
    sg[sg == 0] = 1
    Sp = Sp * sg[:, None]
    Pp = Sp.T @ Sp
    try:
        return xp, np.linalg.cholesky(Pp + 1e-12 * np.eye(n)).T
    except np.linalg.LinAlgError:
        return xp, np.linalg.cholesky(Pp + 1e-8 * np.eye(n)).T


def gh_sr_update(xp, Sp, z, R_base, chi, psi, H=H2, hinf=False, gamma=2.5):
    """GH measurement model with SR-CKF update.

    Uses GIG posterior E[1/V|nu] to compute effective R,
    then performs SR-CKF update on the 2x2 covariance factor.

    Returns: xf, Sf, nu, Szz, K, NIS, likelihood, chi_new, psi_new
    """
    n = len(xp)
    sq = np.sqrt(n)
    pts = np.hstack([xp[:, None] + sq * Sp, xp[:, None] - sq * Sp]).T
    zi = (H @ pts.T).T
    zp = zi.mean(0)
    nu0 = float(np.ravel(z - zp)[0])

    # GIG posterior for scale mixture
    chi_p = chi + nu0 ** 2 / max(R_base, 1e-6)
    ev_p, einv_p = gig_moments(-1., chi_p, psi)
    R_eff = max(R_base / max(einv_p, 0.01), 0.02)

    dz = zi - zp
    dp = pts - xp

    if not hinf:
        # SR-CKF update
        try:
            sr_R = np.array([[np.sqrt(max(R_eff, 1e-6))]])
        except Exception:
            sr_R = np.array([[1e-3]])
        A_inn = np.vstack([dz / np.sqrt(2 * n), sr_R])
        _, R_inn = qr(A_inn, mode='economic')
        s_R = R_inn[0, 0]
        Szz = float(s_R ** 2)
        if Szz < 1e-9:
            Szz = 1e-9
        Pxz = (dp.T @ dz / (2 * n)).flatten()
        K = Pxz / Szz
        NIS = nu0 ** 2 / Szz
    else:
        # H-infinity robust update
        Sn = float(np.ravel(dz.T @ dz)[0] / (2 * n)) + R_eff
        Sh = Sn + gamma ** (-2)
        K = (dp.T @ dz / (2 * n)).flatten() / Sh
        Szz = Sh
        NIS = nu0 ** 2 / max(Sn, 1e-9)

    xf = xp + K * nu0

    # SR covariance update
    try:
        Pf = spd_ensure(Sp.T @ Sp - K[:, None] * Szz * K[None, :])
        Sf = np.linalg.cholesky(Pf + 1e-10 * np.eye(n)).T
    except np.linalg.LinAlgError:
        Sf = Sp

    like = nig_log_likelihood(nu0, chi, psi, R_base)
    chi_new = float(np.clip(0.98 * chi + 0.02 * ev_p, 0.05, 50.))
    psi_new = float(np.clip(0.98 * psi + 0.02 * einv_p, 0.01, 100.))

    return xf, Sf, nu0, Szz, K, NIS, like, chi_new, psi_new


# ── IMM UTILITIES ─────────────────────────────────────────────

def imm_mix_sr(states, chol_Ss, mu, Tr):
    """IMM interaction step in square-root form."""
    nm = len(states)
    mu_p = Tr.T @ mu
    mx, mS = [], []
    for j in range(nm):
        w = Tr[:, j] * mu / (mu_p[j] + 1e-14)
        d = states[j].shape[0]
        xs = [s[:d] if len(s) >= d else np.pad(s, (0, d - len(s))) for s in states]
        Ps = [S[:d, :d].T @ S[:d, :d] if S.shape[0] >= d
              else np.eye(d) * 0.5 for S in chol_Ss]
        xm = sum(w[i] * xs[i] for i in range(nm))
        Pm = sum(w[i] * (Ps[i] + np.outer(xs[i] - xm, xs[i] - xm)) for i in range(nm))
        Pm = spd_ensure(Pm)
        try:
            Sm = np.linalg.cholesky(Pm).T
        except np.linalg.LinAlgError:
            Sm = np.eye(d) * 0.1
        mx.append(xm)
        mS.append(Sm)
    return mx, mS, mu_p


def update_probs(mu_p, likes):
    """Update IMM mode probabilities from likelihoods."""
    mu_p = np.asarray(mu_p, dtype=float)
    ll = np.array([float(l) for l in likes])
    log_l = np.where(ll > 0, np.log(np.maximum(ll, 1e-300)), -700.)
    log_r = np.log(np.maximum(mu_p, 1e-14)) + log_l
    log_r -= log_r.max()
    r = np.exp(log_r)
    return r / r.sum()


# ── GH-SR-IMM FILTER (proposed) ───────────────────────────────

def run_gh_sr_imm(truth, meas):
    """
    GH-SR-IMM: proposed single-target filter.

    Three IMM models:
      M1: Constant Velocity (CV), GH measurement
      M2: Constant Acceleration with correlated noise (CA), GH measurement
      M3: H-infinity robust (HI), GH measurement

    Per-model NIG parameters (chi, psi) adapted online.
    Square-root CKF propagation throughout.
    Online Q adaptation via Inverse Wishart conjugate prior.
    Online R adaptation via Inverse Wishart conjugate prior.
    Online rho (AR correlation) estimation for M2.
    ACF-based mode probability correction.
    """
    # Initialise SR factors
    S1 = np.linalg.cholesky(np.diag([10., 1.])).T
    S2 = np.linalg.cholesky(np.diag([10., 1., 1.])).T
    S3 = np.linalg.cholesky(np.diag([10., 1.])).T
    s1 = np.array([0., 0.])
    s2 = np.array([0., 0., 0.])
    s3 = np.array([0., 0.])

    mu = np.array([0.475, 0.475, 0.05])
    R_base = R0
    Q1 = Q0.copy()

    # AR correlation estimator
    rho = 0.5
    rho_lag = deque(maxlen=2)

    # VB degree-of-freedom tracker
    vb_a = 6.
    vb_b = 0.2

    # IW-Q process noise adapter
    iw_nu_Q = 5.
    iw_S_Q = Q0 * (iw_nu_Q - 3.)

    # IW-R measurement noise adapter
    iw_nu_R = 5.
    iw_S_R = R0 * (iw_nu_R - 2.)

    # H-infinity adaptive gamma
    gamma = 2.5
    nis3_buf = deque(maxlen=20)

    # Innovation buffers
    buf = deque(maxlen=60)
    nb = deque(maxlen=30)
    acfb = deque(maxlen=40)

    # Per-model NIG params
    chi1, psi1 = 1., 1.
    chi2, psi2 = 1., 1.
    chi3, psi3 = 1., 1.

    errs, nis = [], []

    for k, z in enumerate(meas):

        # ── AR correlation update ──────────────────────────────
        if len(rho_lag) == 2 and len(buf) > 10:
            arr = np.array(buf)
            mad = max(float(np.median(np.abs(arr - np.median(arr)))), 0.01) * 1.4826
            n0 = rho_lag[-1]
            n1_ = rho_lag[-2]
            if abs(n0) < 4. * mad and abs(n1_) < 4. * mad:
                rho = float(np.clip(
                    0.99 * rho + 0.01 * float(
                        np.clip(n0 * n1_ / max(mad ** 2, 1e-8), -0.95, 0.95)),
                    -0.80, 0.80))

        F3l = np.array([[1., DT, DT], [0., 1., 1.], [0., 0., rho]])
        Q3l = np.zeros((3, 3))
        Q3l[:2, :2] = Q1
        Q3l[2, 2] = max(1e-5, SD3 ** 2 * (1 - rho ** 2))

        # ── IMM interaction ────────────────────────────────────
        (xm1, xm2, xm3), (Sm1, Sm2, Sm3), mu_p = imm_mix_sr(
            [s1, s2, s3], [S1, S2, S3], mu, Tr3)

        # ── SR predict ─────────────────────────────────────────
        xp1, Sp1 = sr_predict(xm1, Sm1, Q1, F=F2)
        xp2, Sp2 = sr_predict(xm2, Sm2, Q3l, F=F3l)
        xp3, Sp3 = sr_predict(xm3, Sm3, Q1, F=F2)

        # ── Fading memory (NIS-adaptive) ───────────────────────
        mn = np.mean(nb) if nb else 1.
        lp = min(2., max(1., 1 + 0.1 * (mn - 1))) if mn > 2 else 1.
        lv = min(1.4, max(1., 1 + 0.04 * (mn - 1))) if mn > 3 else 1.
        fade = np.array([[lp * lp, lp * lv], [lv * lp, lv * lv]])
        Sp1 = np.linalg.cholesky(spd_ensure(Sp1.T @ Sp1 * fade) + 1e-10 * np.eye(2)).T
        Sp3 = np.linalg.cholesky(spd_ensure(Sp3.T @ Sp3 * fade) + 1e-10 * np.eye(2)).T

        # ── GH-SR update per model ─────────────────────────────
        xf1, Sf1, nu1, Sz1, K1, NIS1, like1, chi1, psi1 = gh_sr_update(
            xp1, Sp1, z, R_base, chi1, psi1, H=H2)
        xf2, Sf2, nu2, Sz2, K2, NIS2, like2, chi2, psi2 = gh_sr_update(
            xp2, Sp2, z, R_base, chi2, psi2, H=H3)
        xf3, Sf3, nu3, Sz3, K3, NIS3, like3, chi3, psi3 = gh_sr_update(
            xp3, Sp3, z, R_base, chi3, psi3, H=H2, hinf=True, gamma=gamma)

        rho_lag.append(nu1)
        nis3_buf.append(NIS3)
        if len(nis3_buf) >= 5:
            gamma = float(np.clip(gamma + 0.005 * (float(np.mean(nis3_buf)) - 1.0), 0.5, 8.0))

        # ACF monitor
        acfb.append(nu1)
        thresh = 2. / np.sqrt(max(len(acfb), 4))
        acf1 = float(np.mean(
            (np.array(acfb)[1:] - np.array(acfb).mean()) *
            (np.array(acfb)[:-1] - np.array(acfb).mean())
        ) / max(np.array(acfb).var(), 1e-8)) if len(acfb) >= 4 else 0.
        acf_sig = acf1 if abs(acf1) > thresh else 0.

        # VB-DOF update
        nu_dof = vb_a / vb_b
        if len(buf) > 5:
            log_t = np.log(1. + nu1 ** 2 / max(nu_dof, 0.1))
            vb_a = 0.99 * vb_a + 0.015
            vb_b = 0.99 * vb_b + 0.01 * (0.5 * log_t + 0.02)

        # ── IW-Q update (inliers only) ─────────────────────────
        nu1c = float(np.clip(nu1, -3., 3.))
        if len(buf) > 5:
            arr_ = np.array(buf)
            mad_ = max(float(np.median(np.abs(arr_ - np.median(arr_)))), 0.01) * 1.4826
            if abs(nu1) < 2.5 * mad_:
                pe = K1.flatten() * nu1c
                iw_nu_Q += 0.005
                iw_S_Q = 0.995 * iw_S_Q + 0.005 * np.outer(pe, pe)
                iw_S_Q = np.maximum(iw_S_Q, Q0 * 0.01)
        Q_iw = iw_S_Q / max(iw_nu_Q - 3., 0.1)
        Q1 = 0.98 * Q1 + 0.02 * np.clip(Q_iw, Q0 * 0.01, Q0 * 20)

        # ── IW-R update ────────────────────────────────────────
        iw_nu_R += 0.01
        iw_S_R = 0.99 * iw_S_R + 0.01 * nu1c ** 2
        iw_S_R = max(iw_S_R, 0.05)
        R_base = float(np.clip(
            0.98 * R_base + 0.02 * np.clip(iw_S_R / max(iw_nu_R - 2., 0.1), 0.1, 5.),
            0.1, 5.))

        # ── Mode probability update ────────────────────────────
        mu = update_probs(mu_p, [like1, like2, like3])
        buf.append(nu1)

        # ACF boost for M2
        ab = min(0.25, abs(acf_sig)) if abs(acf_sig) > 0 else 0.
        mu1e = max(0., mu[0] - ab / 2)
        mu2e = min(1., mu[1] + ab)
        mu3e = max(0., 1. - mu1e - mu2e)
        tot = mu1e + mu2e + mu3e + 1e-14
        mu1e /= tot; mu2e /= tot; mu3e /= tot

        # ── Arithmetic IMM fusion ──────────────────────────────
        Pf1 = spd_ensure(Sf1.T @ Sf1)
        Pf2 = spd_ensure(Sf2.T @ Sf2)[:2, :2]
        Pf3 = spd_ensure(Sf3.T @ Sf3)
        xs_out = [xf1, xf2[:2], xf3]
        xfuse = sum(m * x for m, x in zip([mu1e, mu2e, mu3e], xs_out))
        Pfuse = spd_ensure(sum(
            m * (P + np.outer(x - xfuse, x - xfuse))
            for m, P, x in zip([mu1e, mu2e, mu3e], [Pf1, Pf2, Pf3], xs_out)))
        try:
            Sfuse = np.linalg.cholesky(Pfuse + 1e-10 * np.eye(2)).T
        except np.linalg.LinAlgError:
            Sfuse = np.eye(2) * 0.1

        s1 = xfuse; S1 = Sfuse
        s2 = xf2;   S2 = Sf2
        s3 = xf3;   S3 = Sf3

        NIS = mu[0] * NIS1 + mu[1] * NIS2 + mu[2] * NIS3
        nb.append(NIS)
        errs.append(abs(xfuse[0] - truth[k, 0]))
        nis.append(NIS)

    return np.array(errs), np.array(nis)


# ── HUANG 2017: Student-t KF ──────────────────────────────────

def run_huang2017(truth, meas):
    """
    Student-t Kalman Filter — Huang, Zhang, Chambers (2017).
    Measurement model: z ~ t(Hx, R, nu).
    Nu (degrees of freedom) adapted online via gradient ascent
    on the Student-t log-likelihood.
    """
    x = np.array([0., 0.])
    P = np.diag([10., 1.])
    Q = Q0.copy()
    R = R0
    nu = 10.0
    errs, nis = [], []

    for k in range(len(meas)):
        z = float(meas[k])
        x = F2 @ x
        P = F2 @ P @ F2.T + Q

        Hx = float(np.ravel(H2 @ x)[0])
        S_base = float(np.ravel(H2 @ P @ H2.T)[0]) + R
        nu_innov = z - Hx

        # E[1/V | z] under Student-t scale mixture
        e_inv_v = (nu + 1.) / (nu + nu_innov ** 2 / max(R, 1e-6))
        R_eff = R / max(e_inv_v, 0.01)
        S_eff = float(np.ravel(H2 @ P @ H2.T)[0]) + R_eff

        K = (P @ H2.T).flatten() / max(S_eff, 1e-9)
        x = x + K * nu_innov
        P = P - K[:, None] * S_eff * K[None, :]
        P = (P + P.T) / 2 + 1e-9 * np.eye(2)

        NIS = nu_innov ** 2 / max(S_base, 1e-9)

        # Online nu update via gradient ascent on log-likelihood
        def nll(n):
            if n < 2.01:
                return -1e10
            return (gammaln((n + 1) / 2) - gammaln(n / 2)
                    - 0.5 * np.log(max(n, 1e-9))
                    - ((n + 1) / 2) * np.log(
                        max(1 + nu_innov ** 2 / (n * max(R, 1e-6)), 1e-10)))

        g = nll(nu + 0.5) - nll(nu - 0.5)
        nu = float(np.clip(nu + 0.1 * np.sign(g), 2.1, 200.))

        Q = np.clip(0.99 * Q + 0.01 * np.outer(K * nu_innov, K * nu_innov),
                    Q0 * 0.01, Q0 * 20)

        errs.append(abs(x[0] - truth[k, 0]))
        nis.append(NIS)

    return np.array(errs), np.array(nis)


# ── AGAMENNONI 2012: VB-KF ────────────────────────────────────

def run_agamennoni2012(truth, meas):
    """
    Variational Bayes Kalman Filter — Agamennoni, Nieto, Nebot (2012).
    Gamma prior on noise precision u = 1/V.
    VB posterior: q(u) = Gamma(a0+0.5, b0 + 0.5*nu^2/S).
    Iterates 3 times per step.
    Prior a0=b0=1e-4 (near-non-informative, maximally robust).
    """
    x = np.array([0., 0.])
    P = np.diag([10., 1.])
    Q = Q0.copy()
    R = R0
    a0 = 1e-4
    b0 = 1e-4
    n_iter = 3
    errs, nis = [], []

    for k in range(len(meas)):
        z = float(meas[k])
        x = F2 @ x
        P = F2 @ P @ F2.T + Q

        xp = x.copy()
        Pp = P.copy()
        Hxp = float(np.ravel(H2 @ xp)[0])
        nu_innov = z - Hxp
        S_base = float(np.ravel(H2 @ Pp @ H2.T)[0])
        NIS = nu_innov ** 2 / max(S_base + R, 1e-9)

        # VB iterations
        u = a0 / max(b0, 1e-10)
        for _ in range(n_iter):
            S_iter = S_base + R / max(u, 1e-6)
            a_n = a0 + 0.5
            b_n = b0 + 0.5 * nu_innov ** 2 / max(S_iter, 1e-9)
            u = a_n / max(b_n, 1e-10)

        R_eff = R / max(u, 0.01)
        S_eff = S_base + R_eff
        K = (Pp @ H2.T).flatten() / max(S_eff, 1e-9)
        x = xp + K * nu_innov
        P = Pp - K[:, None] * S_eff * K[None, :]
        P = (P + P.T) / 2 + 1e-9 * np.eye(2)

        Q = np.clip(0.99 * Q + 0.01 * np.outer(K * nu_innov, K * nu_innov),
                    Q0 * 0.01, Q0 * 20)

        errs.append(abs(x[0] - truth[k, 0]))
        nis.append(NIS)

    return np.array(errs), np.array(nis)


# ── METRICS ───────────────────────────────────────────────────

def score(errs, nis):
    """Composite score: RMSE + 0.4*|mean(NIS)-1| + 0.2*std(NIS)."""
    return float(np.sqrt(np.mean(errs ** 2))
                 + 0.4 * abs(float(np.mean(nis)) - 1.)
                 + 0.2 * float(np.std(nis)))


def gospa(truth_list, est_list, c=5.0, p=2):
    """GOSPA metric for multi-target evaluation."""
    n_t = len(truth_list)
    n_e = len(est_list)
    if n_t == 0 and n_e == 0:
        return 0.
    if n_t == 0:
        return float(n_e) * (c ** p / 2) ** (1. / p)
    if n_e == 0:
        return float(n_t) * (c ** p / 2) ** (1. / p)
    C = np.zeros((n_t, n_e))
    for i, t in enumerate(truth_list):
        for j, e in enumerate(est_list):
            d = np.linalg.norm(np.array(t[:2]) - np.array(e[:2]))
            C[i, j] = min(d, c) ** p
    row, col = linear_sum_assignment(C)
    assignment_cost = C[row, col].sum()
    n_assign = len(row)
    penalty = (n_t - n_assign + n_e - n_assign) * (c ** p / 2)
    return float((assignment_cost + penalty) ** (1. / p))


# ── GH-JPDA MULTI-TARGET TRACKER ─────────────────────────────

class SingleTargetTracker:
    """GH-SR-IMM tracker instance for one target."""

    def __init__(self, x0, P0):
        self.S = np.linalg.cholesky(P0).T
        self.x = x0.copy()
        self.R_base = R0_pos
        self.chi_s1, self.psi_s1 = 1., 1.
        self.chi_s2, self.psi_s2 = 1., 1.
        self.iw_nu_R = 5.
        self.iw_S_R = R0_pos * (5. - 2.)

    def predict(self):
        self.x, self.S = sr_predict(self.x, self.S, Q0, F=F2)

    @property
    def P(self):
        return spd_ensure(self.S.T @ self.S)


def jpda_association(pred_xs, pred_Ss, measurements, R_bases, chis, psis, H,
                     use_gh=True, lambda_c=LAMBDA_C):
    """
    JPDA association weights.

    use_gh=True:  Gaussian(nu, R_eff) where R_eff from GH posterior.
                  Outliers cause R_eff to inflate, reducing their weight.
    use_gh=False: Gaussian(nu, Szz) standard baseline.

    Returns: beta[n_targets x n_meas], gated[n_targets x n_meas]
    """
    n_t = len(pred_xs)
    n_m = len(measurements)
    if n_m == 0:
        return np.zeros((n_t, 0)), np.zeros((n_t, 0), dtype=bool)

    L = np.zeros((n_t, n_m))
    gated = np.zeros((n_t, n_m), dtype=bool)

    for i, (xp, Sp) in enumerate(zip(pred_xs, pred_Ss)):
        n = len(xp)
        sq = np.sqrt(n)
        pts = np.hstack([xp[:, None] + sq * Sp, xp[:, None] - sq * Sp]).T
        zi = (H @ pts.T).T
        zp = float(np.ravel(zi.mean(0))[0])
        dz = zi - zi.mean(0)
        Szz_base = float(np.ravel(dz.T @ dz)[0] / (2 * n))

        for j, z in enumerate(measurements):
            nu = float(z) - zp
            if use_gh:
                chi_p = chis[i] + nu ** 2 / max(R_bases[i], 1e-6)
                _, einv_p = gig_moments(-1., chi_p, psis[i])
                R_eff = max(R_bases[i] / max(einv_p, 0.01), 0.02)
                Szz = Szz_base + R_eff
            else:
                Szz = Szz_base + R_bases[i]

            mahal = nu ** 2 / max(Szz, 1e-9)
            if mahal < GATE_THRESH:
                gated[i, j] = True
                L[i, j] = gauss_likelihood(nu, Szz)

    beta = np.zeros((n_t, n_m))
    for j in range(n_m):
        denom = lambda_c
        for i in range(n_t):
            if gated[i, j]:
                denom += L[i, j]
        if denom < 1e-300:
            continue
        for i in range(n_t):
            if gated[i, j]:
                beta[i, j] = L[i, j] / denom

    return beta, gated


def jpda_update_tracker(xp, Sp, betas_row, measurements, R_base, chi, psi, H,
                        use_gh=True):
    """JPDA state update for one target."""
    if len(measurements) == 0 or betas_row.sum() < 1e-10:
        return xp, Sp, chi, psi

    n = len(xp)
    sq = np.sqrt(n)
    pts = np.hstack([xp[:, None] + sq * Sp, xp[:, None] - sq * Sp]).T
    zi = (H @ pts.T).T
    zp = float(np.ravel(zi.mean(0))[0])
    dz = zi - zi.mean(0)
    dp = pts - xp

    nu_combined = sum(betas_row[j] * (float(measurements[j]) - zp)
                      for j in range(len(measurements)))
    beta0 = max(0., 1. - betas_row.sum())
    Pp = spd_ensure(Sp.T @ Sp)

    if use_gh:
        chi_p = chi + nu_combined ** 2 / max(R_base, 1e-6)
        _, einv_p = gig_moments(-1., chi_p, psi)
        R_eff = max(R_base / max(einv_p, 0.01), 0.02)
    else:
        R_eff = R_base

    Szz = float(np.ravel(dz.T @ dz)[0] / (2 * n)) + R_eff
    Pxz = (dp.T @ dz / (2 * n)).flatten()
    K = Pxz / max(Szz, 1e-9)
    xf = xp + K * nu_combined

    P_ck = Pp
    P_upd = spd_ensure(Pp - K[:, None] * Szz * K[None, :])
    spread = np.zeros((n, n))
    for j in range(len(measurements)):
        if betas_row[j] > 1e-10:
            nu_j = float(measurements[j]) - zp
            spread += betas_row[j] * np.outer(K * nu_j, K * nu_j)
    spread -= np.outer(K * nu_combined, K * nu_combined)

    Pf = spd_ensure(beta0 * P_ck + (1. - beta0) * P_upd + spread)
    try:
        Sf = np.linalg.cholesky(Pf + 1e-10 * np.eye(n)).T
    except np.linalg.LinAlgError:
        Sf = np.linalg.cholesky(Pf + 1e-8 * np.eye(n)).T

    if use_gh:
        ev_p, einv_p = gig_moments(-1., chi + nu_combined ** 2 / max(R_base, 1e-6), psi)
        chi_n = float(np.clip(0.98 * chi + 0.02 * ev_p, 0.05, 50.))
        psi_n = float(np.clip(0.98 * psi + 0.02 * einv_p, 0.01, 100.))
    else:
        chi_n, psi_n = chi, psi

    return xf, Sf, chi_n, psi_n


def run_multi_tracker(truths, meas1_list, meas2_list, seed=42, use_gh=True):
    """
    Multi-target, multi-sensor tracker.

    use_gh=True:  GH-JPDA (proposed) — robust association via GH posterior R_eff
    use_gh=False: Gaussian-JPDA (baseline)

    Two sensors fused sequentially per timestep.
    Returns per-target errors and per-step GOSPA scores.
    """
    rng = np.random.default_rng(seed)
    n_targets = len(truths)
    n_steps = len(meas1_list)

    trackers = [SingleTargetTracker(
        np.array([truths[i][0, 0] + rng.standard_normal() * 0.3,
                  truths[i][0, 1] + rng.standard_normal() * 0.05]),
        np.diag([1.0, 0.25])) for i in range(n_targets)]

    all_errors = [[] for _ in range(n_targets)]
    gospa_scores = []

    for k in range(n_steps):
        for tr in trackers:
            tr.predict()

        # Sensor 1 (position)
        meas1 = meas1_list[k]
        pred_xs = [tr.x for tr in trackers]
        pred_Ss = [tr.S for tr in trackers]

        beta1, _ = jpda_association(
            pred_xs, pred_Ss, meas1,
            [tr.R_base for tr in trackers],
            [tr.chi_s1 for tr in trackers],
            [tr.psi_s1 for tr in trackers],
            H_pos, use_gh=use_gh)

        for i, tr in enumerate(trackers):
            if len(meas1) > 0 and beta1[i].sum() > 1e-10:
                xf, Sf, chi_n, psi_n = jpda_update_tracker(
                    tr.x, tr.S, beta1[i], meas1,
                    tr.R_base, tr.chi_s1, tr.psi_s1, H_pos, use_gh=use_gh)
                tr.x = xf
                tr.S = Sf
                if use_gh:
                    tr.chi_s1 = chi_n
                    tr.psi_s1 = psi_n
                nu1c = float(np.clip(
                    sum(beta1[i, j] * (float(meas1[j]) - float((H_pos @ tr.x)[0]))
                        for j in range(len(meas1)) if j < len(beta1[i])),
                    -3., 3.))
                tr.iw_nu_R += 0.01
                tr.iw_S_R = 0.99 * tr.iw_S_R + 0.01 * nu1c ** 2
                tr.iw_S_R = max(tr.iw_S_R, 0.05)
                tr.R_base = float(np.clip(
                    0.98 * tr.R_base + 0.02 * np.clip(
                        tr.iw_S_R / max(tr.iw_nu_R - 2., 0.1), 0.1, 5.),
                    0.1, 5.))

        # Sensor 2 (velocity)
        meas2 = meas2_list[k]
        pred_xs = [tr.x for tr in trackers]
        pred_Ss = [tr.S for tr in trackers]

        beta2, _ = jpda_association(
            pred_xs, pred_Ss, meas2,
            [R0_vel] * n_targets,
            [tr.chi_s2 for tr in trackers],
            [tr.psi_s2 for tr in trackers],
            H_vel, use_gh=use_gh)

        for i, tr in enumerate(trackers):
            if len(meas2) > 0 and beta2[i].sum() > 1e-10:
                xf, Sf, chi_n, psi_n = jpda_update_tracker(
                    tr.x, tr.S, beta2[i], meas2,
                    R0_vel, tr.chi_s2, tr.psi_s2, H_vel, use_gh=use_gh)
                tr.x = xf
                tr.S = Sf
                if use_gh:
                    tr.chi_s2 = chi_n
                    tr.psi_s2 = psi_n

        est = [tr.x[:2].tolist() for tr in trackers]
        true = [truths[i][k, :2].tolist() for i in range(n_targets)]
        gospa_scores.append(gospa(true, est))
        for i in range(n_targets):
            all_errors[i].append(abs(trackers[i].x[0] - truths[i][k, 0]))

    return all_errors, gospa_scores


# ── MAIN BENCHMARK ────────────────────────────────────────────

def main():
    single_scenarios = [
        ('gaussian',   'Gaussian'),
        ('heavy_tail', 'Heavy-Tail'),
        ('levy',       'Lévy α=1.6'),
        ('maneuver',   'Maneuver'),
        ('correlated', 'Correlated Q'),
        ('mixed',      'Mixed Regime'),
        ('bimodal',    'Bimodal'),
        ('jerk',       'Jerk'),
    ]
    single_methods = [
        ('Huang-2017',     run_huang2017),
        ('Agam-2012',      run_agamennoni2012),
        ('GH-SR-IMM',      run_gh_sr_imm),
    ]
    multi_scenarios = [
        ('crossing',   'Crossing paths'),
        ('parallel',   'Parallel tracks'),
        ('heavy_tail', 'Crossing + Heavy-tail'),
        ('diverging',  'Diverging tracks'),
    ]

    print("=" * 80)
    print("  HARCF Benchmark")
    print("  GH-SR-IMM vs Huang 2017 vs Agamennoni 2012")
    print("  Score = RMSE + 0.4|NIS-1| + 0.2·σ(NIS)   [lower = better]")
    print("=" * 80)

    # ── Single-target multi-seed ───────────────────────────────
    print(f"\n  SINGLE-TARGET  (multi-seed, seeds 42–46)")
    hdr = f"  {'scenario':>16}"
    for n, _ in single_methods:
        hdr += f"  {n:>16}"
    print(hdr)
    print("  " + "-" * (18 + 18 * len(single_methods)))

    totals = {n: [] for n, _ in single_methods}
    for sc_id, sc_label in single_scenarios:
        row = {}
        for n, fn in single_methods:
            ss = [score(*fn(*gen_single(sc_id, seed=s))) for s in SEEDS]
            row[n] = (np.mean(ss), np.std(ss))
            totals[n].append(np.mean(ss))
        best = min(v[0] for v in row.values())
        line = f"  {sc_label:>16}"
        for n, _ in single_methods:
            mu_, sd_ = row[n]
            w = '◀' if abs(mu_ - best) < 1e-4 else ''
            line += f"  {mu_:5.3f}±{sd_:.3f}{w:4}"
        print(line)

    print("  " + "-" * (18 + 18 * len(single_methods)))
    line = f"  {'MEAN':>16}"
    for n, _ in single_methods:
        line += f"  {np.mean(totals[n]):>16.4f}"
    print(line)

    # Ranking
    print(f"\n  RANKING")
    h = np.mean(totals['Huang-2017'])
    a = np.mean(totals['Agam-2012'])
    ranked = sorted(single_methods, key=lambda x: np.mean(totals[x[0]]))
    for i, (n, _) in enumerate(ranked, 1):
        m_ = np.mean(totals[n])
        print(f"  #{i}  {n:>16}  {m_:.4f}"
              f"  vs Huang: {(h - m_) / h * 100:+.1f}%"
              f"  vs Agam: {(a - m_) / a * 100:+.1f}%")

    # ── Multi-target ───────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print(f"  MULTI-TARGET GH-JPDA  (2 targets, 2 sensors, GOSPA c=5)")
    print(f"  Multi-seed (seeds 42–46)")
    print(f"{'=' * 80}")
    print(f"\n  {'scenario':>24}  {'Gauss-JPDA':>12}  {'GH-JPDA':>12}  {'Δ':>7}  {'improv%':>8}")
    print("  " + "-" * 72)

    mt_g, mt_gh = [], []
    for sc_id, sc_label in multi_scenarios:
        g_s, gh_s = [], []
        for seed in SEEDS:
            truths, m1, m2 = gen_multi(sc_id, seed=seed)
            _, gs_g = run_multi_tracker(truths, m1, m2, seed=seed, use_gh=False)
            _, gs_gh = run_multi_tracker(truths, m1, m2, seed=seed, use_gh=True)
            g_s.append(np.mean(gs_g))
            gh_s.append(np.mean(gs_gh))
        mg = np.mean(g_s)
        mgh = np.mean(gh_s)
        mt_g.append(mg)
        mt_gh.append(mgh)
        pct = (mg - mgh) / mg * 100
        print(f"  {sc_label:>24}  {mg:>12.4f}  {mgh:>12.4f}  {mgh - mg:>+7.4f}  {pct:>7.1f}%")

    print("  " + "-" * 72)
    mg_all = np.mean(mt_g)
    mgh_all = np.mean(mt_gh)
    print(f"  {'MEAN':>24}  {mg_all:>12.4f}  {mgh_all:>12.4f}  "
          f"{mgh_all - mg_all:>+7.4f}  {(mg_all - mgh_all) / mg_all * 100:>7.1f}%")


if __name__ == '__main__':
    main()
