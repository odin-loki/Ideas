"""GH-SR-IMM filter and NIG conjugate-posterior helpers."""

from __future__ import annotations

import numpy as np
from scipy.special import kv as bessel_k

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT


def bessel_k_safe(nu: float, x: float) -> float:
    if x < 1e-12:
        return 1e18 if nu == 0 else 1e15 / (nu + 1)
    try:
        v = float(bessel_k(nu, x))
        return v if np.isfinite(v) and v > 0 else (1e-300 if x > 50 else 1.0)
    except Exception:
        return 1.0


def eig_posterior(chi: float, psi: float) -> float:
    """E[1/V | nu] for NIG conjugate update."""
    chi, psi = max(chi, 1e-8), max(psi, 1e-8)
    x = np.sqrt(chi * psi)
    if x > 700:
        return np.sqrt(psi / chi)
    r = bessel_k_safe(2, x) / max(bessel_k_safe(1, x), 1e-300)
    return float(np.clip(np.sqrt(psi / chi) * np.clip(r, 0.5, 10.0), 1e-6, 1e6))


def ev_posterior(chi: float, psi: float) -> float:
    """E[V | nu] for NIG conjugate update."""
    chi, psi = max(chi, 1e-8), max(psi, 1e-8)
    x = np.sqrt(chi * psi)
    if x > 700:
        return np.sqrt(chi / psi)
    r = bessel_k_safe(0, x) / max(bessel_k_safe(1, x), 1e-300)
    return float(np.clip(np.sqrt(chi / psi) * np.clip(r, 0.01, 2.0), 1e-6, 1e6))


def reff(nu_sq: float, R: float, chi: float, psi: float) -> float:
    return R / max(eig_posterior(chi + nu_sq, psi), 1e-6)


def nig_update(chi: float, psi: float, nu_sq: float, alpha: float = 0.02) -> tuple[float, float]:
    chi_eff = chi + nu_sq
    chi_new = max((1 - alpha) * chi + alpha * ev_posterior(chi_eff, psi), 0.01)
    psi_new = max((1 - alpha) * psi + alpha * eig_posterior(chi_eff, psi), 0.01)
    return chi_new, psi_new


def state_transition() -> np.ndarray:
    F = np.eye(4)
    F[0, 2] = DT
    F[1, 3] = DT
    return F


def process_noise(q: float) -> np.ndarray:
    return np.array([
        [DT ** 3 / 3 * q, 0, DT ** 2 / 2 * q, 0],
        [0, DT ** 3 / 3 * q, 0, DT ** 2 / 2 * q],
        [DT ** 2 / 2 * q, 0, DT * q, 0],
        [0, DT ** 2 / 2 * q, 0, DT * q],
    ])


class GHSRIMM:
    """Generalised Hyperbolic Square-Root Interacting Multiple Model filter."""

    def __init__(self, cfg: AGINSConfig = DEFAULT_CONFIG):
        fc = cfg.filter
        self.F = state_transition()
        self.QL = [process_noise(q) for q in fc.process_noise]
        self.Tr = np.array(fc.imm_transition)
        self.nis_gate = fc.nis_gate
        self.nig_alpha = fc.nig_forgetting
        self.x = [np.zeros(4) for _ in range(3)]
        self.S = [np.eye(4) * 0.5 for _ in range(3)]
        self.mu = np.array(fc.imm_initial_mu, dtype=float)
        self.chi = np.full((3, 2), 1.0)
        self.psi = np.full((3, 2), 1.0)
        self.ok = False

    def init(self, x0: np.ndarray, P0: np.ndarray) -> None:
        S0 = np.linalg.cholesky(P0 + 1e-9 * np.eye(4))
        for i in range(3):
            self.x[i] = x0.copy()
            self.S[i] = S0.copy()
        self.ok = True

    def _predict_model(self, i: int) -> None:
        n = 4
        S = self.S[i]
        Q = self.QL[i]
        xp = self.F @ self.x[i]
        Xp = self.F @ (S * np.sqrt(2 * n))
        Sq = np.linalg.cholesky(Q + 1e-12 * np.eye(4))
        A = np.vstack([(Xp / np.sqrt(2 * n)).T, Sq.T])
        try:
            _, R = np.linalg.qr(A, mode="reduced")
            Sp = R[:4, :4].T
            for j in range(4):
                if Sp[j, j] < 0:
                    Sp[:, j] *= -1
        except Exception:
            Sp = np.linalg.cholesky(self.F @ (S @ S.T) @ self.F.T + Q + 1e-9 * np.eye(4))
        self.x[i] = xp
        self.S[i] = Sp

    def _update_position(self, i: int, z: np.ndarray, Rm: np.ndarray) -> float:
        H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
        P = self.S[i] @ self.S[i].T
        nu = z - H @ self.x[i]
        Si = H @ P @ H.T + Rm
        try:
            NIS = float(nu @ np.linalg.inv(Si) @ nu)
        except Exception:
            return 1.0
        if NIS > self.nis_gate:
            return NIS
        Rb = np.trace(Rm) / 2
        nq = float(nu @ np.linalg.inv(Rm) @ nu) / 2
        Re = np.clip(reff(nq, Rb, self.chi[i, 0], self.psi[i, 0]), Rb * 0.5, Rb * 10.0)
        self.chi[i, 0], self.psi[i, 0] = nig_update(
            self.chi[i, 0], self.psi[i, 0], nq, self.nig_alpha
        )
        Ra = Rm * (Re / Rb)
        Sa = H @ P @ H.T + Ra
        K = P @ H.T @ np.linalg.inv(Sa)
        xu = self.x[i] + K @ nu
        IKH = np.eye(4) - K @ H
        Pu = IKH @ P @ IKH.T + K @ Ra @ K.T
        Pu = (Pu + Pu.T) / 2 + 1e-10 * np.eye(4)
        try:
            self.S[i] = np.linalg.cholesky(Pu)
        except Exception:
            pass
        self.x[i] = xu
        return NIS

    def _update_speed(self, i: int, z_spd: float, r_spd: float) -> None:
        vn, ve = self.x[i][2], self.x[i][3]
        sp = np.sqrt(vn ** 2 + ve ** 2)
        if sp < 0.3:
            return
        P = self.S[i] @ self.S[i].T
        Hs = np.array([0.0, 0.0, vn / sp, ve / sp])
        nu = z_spd - sp
        nq = nu ** 2 / max(r_spd, 1e-9)
        Re_s = np.clip(reff(nq, r_spd, self.chi[i, 0], self.psi[i, 0]), r_spd * 0.3, r_spd * 5.0)
        Sa = float(Hs @ P @ Hs) + Re_s
        K = P @ Hs / max(Sa, 1e-12)
        xu = self.x[i] + K * nu
        Pu = (np.eye(4) - np.outer(K, Hs)) @ P
        Pu = (Pu + Pu.T) / 2 + 1e-10 * np.eye(4)
        try:
            self.S[i] = np.linalg.cholesky(Pu)
        except Exception:
            pass
        self.x[i] = xu

    def _update_heading(self, i: int, hm: float, hv: float, gate_deg: float) -> None:
        vn, ve = self.x[i][2], self.x[i][3]
        sp = np.sqrt(vn ** 2 + ve ** 2)
        if sp < 0.3:
            return
        P = self.S[i] @ self.S[i].T
        Hh = np.array([0, 0, -ve / sp ** 2, vn / sp ** 2])
        nu = (hm - np.arctan2(ve, vn) + np.pi) % (2 * np.pi) - np.pi
        if abs(nu) > np.radians(gate_deg):
            return
        nq = nu ** 2 / max(hv, 1e-9)
        Re = np.clip(reff(nq, hv, self.chi[i, 1], self.psi[i, 1]), hv * 0.5, hv * 8.0)
        self.chi[i, 1], self.psi[i, 1] = nig_update(
            self.chi[i, 1], self.psi[i, 1], nq, self.nig_alpha
        )
        Sa = float(Hh @ P @ Hh) + Re
        K = P @ Hh / max(Sa, 1e-12)
        xu = self.x[i] + K * nu
        Pu = (np.eye(4) - np.outer(K, Hh)) @ P
        Pu = (Pu + Pu.T) / 2 + 1e-10 * np.eye(4)
        try:
            self.S[i] = np.linalg.cholesky(Pu)
        except Exception:
            pass
        self.x[i] = xu

    def predict(self) -> None:
        if not self.ok:
            return
        c = self.Tr.T @ self.mu
        mij = (self.Tr * self.mu[:, None]) / np.maximum(c[None, :], 1e-12)
        xm = [sum(mij[i, j] * self.x[i] for i in range(3)) for j in range(3)]
        Sm = []
        for j in range(3):
            Pm = sum(
                mij[i, j] * (self.S[i] @ self.S[i].T + np.outer(self.x[i] - xm[j], self.x[i] - xm[j]))
                for i in range(3)
            )
            Pm = (Pm + Pm.T) / 2 + 1e-9 * np.eye(4)
            try:
                Sm.append(np.linalg.cholesky(Pm))
            except Exception:
                Sm.append(np.eye(4) * 0.1)
        for j in range(3):
            self.x[j] = xm[j]
            self.S[j] = Sm[j]
        for i in range(3):
            self._predict_model(i)

    def update(
        self,
        zp: np.ndarray | None,
        Rp: np.ndarray | None,
        zspd: float | None,
        rspd: float | None,
        zh: float | None,
        Rh: float | None,
        heading_gate_deg: float = 18.0,
    ) -> np.ndarray:
        if not self.ok:
            return np.zeros(4)
        L = np.ones(3)
        for i in range(3):
            if zp is not None and Rp is not None:
                NIS = self._update_position(i, zp, Rp)
                P = self.S[i] @ self.S[i].T
                H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
                Si = H @ P @ H.T + Rp
                L[i] *= np.exp(-0.5 * NIS) / max(
                    2 * np.pi * np.sqrt(np.linalg.det(Si)), 1e-30
                )
            if zspd is not None and rspd is not None:
                self._update_speed(i, zspd, rspd)
            if zh is not None and Rh is not None:
                self._update_heading(i, zh, Rh, heading_gate_deg)
        s = (self.mu * L).sum()
        self.mu = (self.mu * L) / s if s > 1e-15 else np.full(3, 1 / 3)
        return np.array(sum(self.mu[i] * self.x[i] for i in range(3)))

    def model_probs(self) -> np.ndarray:
        return self.mu.copy()
