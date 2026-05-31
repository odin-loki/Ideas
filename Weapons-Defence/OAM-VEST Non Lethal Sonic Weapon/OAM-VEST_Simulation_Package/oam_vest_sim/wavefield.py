"""
OAM-VEST Simulation Package
wavefield.py — 2D Finite-Difference Time-Domain (FDTD) acoustic wavefield

Simulates the pressure field in a 2D cross-section (x-z plane).
Supports:
  - Point source array with per-element phase and amplitude
  - Pressure field accumulation (RMS over time)
  - Beam pattern extraction
  - OAM wavefront topology visualisation (phase map)

Note: Full 3D FDTD is computationally expensive. This module uses
a 2D approximation (valid for the far-field beam pattern in the
principal plane). For safety zone verification, results should be
scaled with the known 3D spreading law verified in physics.py.
"""

import numpy as np
from typing import Optional, Tuple, List
from physics import C_SOUND, RHO_AIR, spl_to_pa


class FDTD2D:
    """
    2D FDTD acoustic pressure solver.

    Grid: x horizontal (across beam), z axial (along beam propagation).
    Sources placed at z=0.

    Governing equations (linearised acoustics):
        dp/dt = -rho*c^2 * div(v)
        rho * dv/dt = -grad(p)

    Discretised with Yee-like staggered grid, Mur absorbing boundaries.
    """

    def __init__(self, x_size_m: float = 10.0, z_size_m: float = 120.0,
                 dx_m: float = 0.05, freq_hz: float = 3000.0,
                 cfl: float = 0.4):
        """
        x_size_m:  transverse domain width (m)
        z_size_m:  axial domain length (m)
        dx_m:      spatial step (m) — must satisfy dx < lambda/8 for accuracy
        freq_hz:   primary frequency (sets time step via CFL)
        cfl:       Courant-Friedrichs-Lewy number (<= 1/sqrt(2) for stability)
        """
        self.dx     = dx_m
        self.dz     = dx_m
        self.Lx     = x_size_m
        self.Lz     = z_size_m
        self.freq   = freq_hz
        self.lam    = C_SOUND / freq_hz

        # Sanity check: need at least 8 points per wavelength
        assert dx_m < self.lam / 8, \
            f"dx={dx_m:.4f}m too coarse for {freq_hz}Hz (need dx < {self.lam/8:.4f}m)"

        self.Nx     = int(x_size_m / dx_m) + 1
        self.Nz     = int(z_size_m / dx_m) + 1
        self.dt     = cfl * dx_m / (C_SOUND * np.sqrt(2.0))

        # Field arrays: pressure p, velocity vx, vz
        self.p      = np.zeros((self.Nx, self.Nz))
        self.vx     = np.zeros((self.Nx, self.Nz))
        self.vz     = np.zeros((self.Nx, self.Nz))

        # Accumulated RMS pressure
        self.p_rms_acc = np.zeros((self.Nx, self.Nz))
        self.n_steps   = 0

        # Source list: each entry is (ix, iz, amplitude, phase_rad)
        self.sources: List[Tuple[int, int, float, float]] = []

        # Time
        self.t = 0.0

        # Mur boundary coefficients
        self._mur_coeff = (C_SOUND * self.dt - self.dx) / \
                          (C_SOUND * self.dt + self.dx)

        # Previous boundary values for Mur ABC
        self._p_prev_xmin = np.zeros(self.Nz)
        self._p_prev_xmax = np.zeros(self.Nz)
        self._p_prev_zmax = np.zeros(self.Nx)

    def grid_index(self, x_m: float, z_m: float) -> Tuple[int, int]:
        """Convert physical coordinates to grid indices."""
        ix = int(round(x_m / self.dx))
        iz = int(round(z_m / self.dz))
        return (np.clip(ix, 0, self.Nx-1),
                np.clip(iz, 0, self.Nz-1))

    def add_source(self, x_m: float, z_m: float,
                   amplitude_pa: float, phase_rad: float = 0.0):
        """Add a point source at physical coordinates."""
        ix, iz = self.grid_index(x_m, z_m)
        self.sources.append((ix, iz, amplitude_pa, phase_rad))

    def add_linear_array(self, x_positions: np.ndarray,
                          amplitudes: np.ndarray, phases: np.ndarray,
                          z_m: float = 0.0):
        """Add a linear array of sources at z=z_m, varying x positions."""
        for x, amp, phi in zip(x_positions, amplitudes, phases):
            self.add_source(x, z_m, amp, phi)

    def _inject_sources(self):
        """Inject source pressure at current time step."""
        omega = 2.0 * np.pi * self.freq
        for ix, iz, amp, phi in self.sources:
            self.p[ix, iz] += amp * np.sin(omega * self.t + phi)

    def _update_velocity(self):
        """Update particle velocity from pressure gradient."""
        coeff = self.dt / (RHO_AIR * self.dx)
        self.vx[:-1, :] -= coeff * (self.p[1:, :] - self.p[:-1, :])
        self.vz[:, :-1] -= coeff * (self.p[:, 1:] - self.p[:, :-1])

    def _update_pressure(self):
        """Update pressure from velocity divergence."""
        coeff = self.dt * RHO_AIR * C_SOUND**2 / self.dx
        self.p[1:,  :] -= coeff * (self.vx[1:,  :] - self.vx[:-1, :])
        self.p[:,  1:] -= coeff * (self.vz[:, 1: ] - self.vz[:, :-1])

    def _apply_mur_abc(self):
        """
        First-order Mur absorbing boundary conditions on all four edges.
        Prevents reflections from domain boundaries.
        """
        c = self._mur_coeff
        # xmin boundary
        new_xmin = self.p[1, :].copy()
        self.p[0, :] = self._p_prev_xmin + c * (new_xmin - self.p[0, :])
        self._p_prev_xmin = new_xmin
        # xmax boundary
        new_xmax = self.p[-2, :].copy()
        self.p[-1, :] = self._p_prev_xmax + c * (new_xmax - self.p[-1, :])
        self._p_prev_xmax = new_xmax
        # zmax boundary
        new_zmax = self.p[:, -2].copy()
        self.p[:, -1] = self._p_prev_zmax + c * (new_zmax - self.p[:, -1])
        self._p_prev_zmax = new_zmax
        # zmin: sources are at z=0, no ABC needed (source boundary)

    def step(self, n: int = 1):
        """Advance simulation by n time steps."""
        for _ in range(n):
            self._inject_sources()
            self._update_velocity()
            self._update_pressure()
            self._apply_mur_abc()
            # Accumulate RMS
            self.p_rms_acc += self.p ** 2
            self.n_steps   += 1
            self.t         += self.dt

    def run(self, n_periods: float = 20.0):
        """
        Run simulation for n_periods acoustic cycles.
        Enough for steady-state to establish.
        """
        n_total = int(n_periods / (self.freq * self.dt))
        self.step(n_total)

    @property
    def p_rms(self) -> np.ndarray:
        """RMS pressure field (Pa)."""
        if self.n_steps == 0:
            return np.zeros_like(self.p)
        return np.sqrt(self.p_rms_acc / self.n_steps)

    @property
    def spl_field(self) -> np.ndarray:
        """SPL field (dB) from RMS pressure."""
        from physics import P_REF
        rms = self.p_rms
        with np.errstate(divide='ignore', invalid='ignore'):
            spl = 20.0 * np.log10(np.where(rms > 0, rms / P_REF, 1e-30))
        return spl

    @property
    def x_axis(self) -> np.ndarray:
        """Physical x coordinates (m)."""
        return np.linspace(-self.Lx / 2, self.Lx / 2, self.Nx)

    @property
    def z_axis(self) -> np.ndarray:
        """Physical z coordinates (m)."""
        return np.linspace(0, self.Lz, self.Nz)

    def beam_pattern(self, z_m: float = 10.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract transverse beam pattern at axial distance z_m.
        Returns (x_positions, spl_values).
        """
        iz = int(round(z_m / self.dz))
        iz = np.clip(iz, 0, self.Nz - 1)
        return self.x_axis, self.spl_field[:, iz]

    def axial_profile(self, x_m: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract axial SPL profile along z at transverse position x_m.
        Returns (z_positions, spl_values).
        """
        ix = int(round((x_m + self.Lx / 2) / self.dx))
        ix = np.clip(ix, 0, self.Nx - 1)
        return self.z_axis, self.spl_field[ix, :]


def build_linear_array_fdtd(n_elements: int = 32, spacing_m: float = 0.057,
                              freq_hz: float = 3000.0,
                              spl_per_elem: float = 108.0,
                              phases: Optional[np.ndarray] = None,
                              domain_z_m: float = 80.0) -> FDTD2D:
    """
    Build and configure a 2D FDTD simulation for a linear array.
    (Linear approximation for the principal plane cut of the circular array.)

    n_elements:    number of elements
    spacing_m:     element spacing (m)
    freq_hz:       operating frequency
    spl_per_elem:  SPL at 1m per element
    phases:        per-element phases (radians). Default: all zeros (broadside).
    domain_z_m:    axial domain size
    """
    total_width = n_elements * spacing_m
    domain_x    = max(total_width * 2.5, 10.0)
    dx          = min(C_SOUND / freq_hz / 10.0, 0.04)   # lambda/10

    sim = FDTD2D(x_size_m=domain_x, z_size_m=domain_z_m,
                 dx_m=dx, freq_hz=freq_hz)

    amp  = spl_to_pa(spl_per_elem)
    xs   = np.linspace(-total_width / 2, total_width / 2, n_elements)
    if phases is None:
        phases = np.zeros(n_elements)

    sim.add_linear_array(xs, np.full(n_elements, amp), phases, z_m=0.0)
    return sim


def oam_phase_map(n_elements: int, topological_charge: int = 1) -> np.ndarray:
    """
    Compute OAM phase values around a circular ring for visualisation.
    Returns (n_elements,) phase array in radians [0, 2*pi*l].
    """
    n = np.arange(n_elements)
    return (2.0 * np.pi * topological_charge * n / n_elements) % (2.0 * np.pi)
