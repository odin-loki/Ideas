"""Standard Kalman filter baseline for AGINS fusion."""

from __future__ import annotations

import numpy as np

from agins_sim.config import AGINSConfig, DEFAULT_CONFIG, DT
from agins_sim.filter.gh_sr_imm import process_noise, state_transition


class StandardKF:
    """Linear KF with separate scalar speed and heading updates."""

    def __init__(self, cfg: AGINSConfig = DEFAULT_CONFIG):
        self.F = state_transition()
        self.Q = process_noise(cfg.filter.kf_process_noise)
        self.nis_gate = cfg.filter.nis_gate
        self.x = np.zeros(4)
        self.P = np.eye(4) * 0.5
        self.ok = False

    def init(self, x0: np.ndarray, P0: np.ndarray) -> None:
        self.x = x0.copy()
        self.P = P0.copy()
        self.ok = True

    def predict(self) -> None:
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        self.P = (self.P + self.P.T) / 2

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
            return self.x
        if zp is not None and Rp is not None:
            H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
            S = H @ self.P @ H.T + Rp
            nu = zp - H @ self.x
            if float(nu @ np.linalg.inv(S) @ nu) <= self.nis_gate:
                K = self.P @ H.T @ np.linalg.inv(S)
                self.x += K @ nu
                self.P = (np.eye(4) - K @ H) @ self.P
        if zspd is not None and rspd is not None:
            vn, ve = self.x[2], self.x[3]
            sp = np.sqrt(vn ** 2 + ve ** 2)
            if sp > 0.3:
                Hs = np.array([0.0, 0.0, vn / sp, ve / sp])
                nu = zspd - sp
                Sa = float(Hs @ self.P @ Hs) + rspd
                K = self.P @ Hs / max(Sa, 1e-12)
                self.x += K * nu
                self.P = (np.eye(4) - np.outer(K, Hs)) @ self.P
        if zh is not None and Rh is not None:
            vn, ve = self.x[2], self.x[3]
            sp = np.sqrt(vn ** 2 + ve ** 2)
            if sp > 0.3:
                Hh = np.array([0, 0, -ve / sp ** 2, vn / sp ** 2])
                nu = (zh - np.arctan2(ve, vn) + np.pi) % (2 * np.pi) - np.pi
                if abs(nu) <= np.radians(heading_gate_deg):
                    Sh = float(Hh @ self.P @ Hh) + Rh
                    K = self.P @ Hh / max(Sh, 1e-12)
                    self.x += K * nu
                    self.P = (np.eye(4) - np.outer(K, Hh)) @ self.P
        self.P = (self.P + self.P.T) / 2 + 1e-9 * np.eye(4)
        return self.x.copy()
