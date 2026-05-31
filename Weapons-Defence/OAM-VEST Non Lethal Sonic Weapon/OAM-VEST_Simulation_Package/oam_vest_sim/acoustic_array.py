"""
OAM-VEST Simulation Package
array.py — Phased array geometry, gain, beam steering, and OAM vortex beams

Models the dual-panel 4-ring concentric circular array.
Supports:
  - On-axis array gain calculation
  - Per-element phase computation for arbitrary focus point
  - OAM vortex beam with topological charge l
  - AM modulation envelope
  - Multi-target phase superposition
  - Holographic null steering for bystander exclusion
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from physics import C_SOUND, spl_to_pa, pa_to_spl, alpha_db_per_m

# ─── Array geometry ────────────────────────────────────────────────────────────

@dataclass
class Ring:
    """Single concentric ring of transducer elements."""
    n_elements:  int
    radius_m:    float
    label:       str
    primary_mode: str   # "deterrence", "OAM", "vestibular_AM", "parametric"

    def element_positions(self) -> np.ndarray:
        """
        Returns (N, 3) array of element (x, y, z) positions.
        Ring lies in the z=0 plane, centred at origin.
        """
        angles = np.linspace(0, 2*np.pi, self.n_elements, endpoint=False)
        x = self.radius_m * np.cos(angles)
        y = self.radius_m * np.sin(angles)
        z = np.zeros(self.n_elements)
        return np.column_stack([x, y, z])

    def element_angles(self) -> np.ndarray:
        """Azimuthal angles of elements in radians."""
        return np.linspace(0, 2*np.pi, self.n_elements, endpoint=False)


# Default OAM-VEST ring configuration (per panel)
DEFAULT_RINGS = [
    Ring(n_elements=200, radius_m=0.600, label="Ring1_outer",  primary_mode="deterrence"),
    Ring(n_elements=152, radius_m=0.500, label="Ring2",        primary_mode="OAM"),
    Ring(n_elements=100, radius_m=0.350, label="Ring3",        primary_mode="vestibular_AM"),
    Ring(n_elements=60,  radius_m=0.150, label="Ring4_inner",  primary_mode="parametric"),
]
# Total: 512 elements per panel — achieves 162 dB per panel, 173 dB dual-panel combined


@dataclass
class ArrayPanel:
    """
    Single circular phased array panel.
    Origin at panel face centre. Beam propagates in +z direction.
    """
    rings:          List[Ring] = field(default_factory=lambda: DEFAULT_RINGS)
    freq_hz:        float = 3000.0
    spl_per_elem:   float = 108.0    # dB at 1m per element at 50W

    def __post_init__(self):
        self._positions = None  # cached

    @property
    def n_elements(self) -> int:
        return sum(r.n_elements for r in self.rings)

    @property
    def positions(self) -> np.ndarray:
        """(N, 3) array of all element positions."""
        if self._positions is None:
            parts = [r.element_positions() for r in self.rings]
            self._positions = np.vstack(parts)
        return self._positions

    @property
    def ring_indices(self) -> List[slice]:
        """Slice objects mapping each ring to positions array."""
        slices = []
        start = 0
        for r in self.rings:
            slices.append(slice(start, start + r.n_elements))
            start += r.n_elements
        return slices

    def wavelength(self) -> float:
        return C_SOUND / self.freq_hz

    def on_axis_gain_db(self) -> float:
        """On-axis array gain: G = 20*log10(N)."""
        return 20.0 * np.log10(self.n_elements)

    def source_spl(self) -> float:
        """Total on-axis SPL at 1m from array."""
        return self.spl_per_elem + self.on_axis_gain_db()

    def beam_half_angle_deg(self, n_eff: Optional[int] = None) -> float:
        """
        Approximate beam half-angle (3dB point).
        Uses sinc approximation for circular aperture.
        """
        N = n_eff or self.n_elements
        lam = self.wavelength()
        # Effective aperture radius
        r_eff = np.mean([r.radius_m for r in self.rings])
        D_eff = 2 * r_eff
        return np.degrees(np.arcsin(0.886 * lam / (D_eff * np.sqrt(N / 100))))

    # ─── Phase computation ────────────────────────────────────────────────────

    def focus_phases(self, focus_point: np.ndarray) -> np.ndarray:
        """
        Per-element phases to focus beam at a 3D point.
        phi_n = 2*pi/lambda * (R_ref - |r_n - focus|)

        focus_point: (3,) array, metres from panel centre
        Returns: (N,) array of phases in radians
        """
        lam = self.wavelength()
        k   = 2.0 * np.pi / lam
        pos = self.positions  # (N, 3)
        # Distance from each element to focus point
        dists = np.linalg.norm(pos - focus_point, axis=1)
        # Reference distance = distance from array centre to focus
        R_ref = np.linalg.norm(focus_point)
        phases = k * (R_ref - dists)
        return phases % (2.0 * np.pi)

    def oam_phases(self, topological_charge: int, ring_idx: int = 1) -> np.ndarray:
        """
        OAM vortex beam phase winding for a specific ring.
        phi_n = 2*pi*l*n/N (helical phase ramp around aperture)

        Returns full (N,) phase array with OAM applied only to selected ring.
        """
        phases = np.zeros(self.n_elements)
        ring   = self.rings[ring_idx]
        sl     = self.ring_indices[ring_idx]
        N      = ring.n_elements
        n_arr  = np.arange(N)
        phases[sl] = 2.0 * np.pi * topological_charge * n_arr / N
        return phases

    def steering_phases(self, az_deg: float, el_deg: float) -> np.ndarray:
        """
        Far-field beam steering phases.
        phi_n = k * (x_n * sin(az)*cos(el) + y_n * sin(el))
        """
        lam    = self.wavelength()
        k      = 2.0 * np.pi / lam
        az     = np.radians(az_deg)
        el     = np.radians(el_deg)
        pos    = self.positions
        ux     = np.sin(az) * np.cos(el)
        uy     = np.sin(el)
        phases = k * (pos[:, 0] * ux + pos[:, 1] * uy)
        return phases % (2.0 * np.pi)

    def null_steering_phases(self, null_point: np.ndarray,
                              focus_phases: np.ndarray) -> np.ndarray:
        """
        Add a holographic null at null_point to existing phase set.
        Superpose anti-phase contribution from inner ring to cancel at null.
        """
        null_phases  = self.focus_phases(null_point)
        inner_sl     = self.ring_indices[-1]
        combined     = focus_phases.copy()
        # Flip phase of inner ring by pi to create destructive interference at null
        combined[inner_sl] = (null_phases[inner_sl] + np.pi) % (2.0 * np.pi)
        return combined

    def superpose_targets(self, target_phases: List[np.ndarray],
                           weights: Optional[List[float]] = None) -> np.ndarray:
        """
        Superpose phase sets for multiple simultaneous targets.
        Uses complex amplitude superposition: sum of phasors, normalised.

        Returns combined phase array and per-beam SPL penalty (dB).
        """
        N = len(target_phases)
        if weights is None:
            weights = [1.0 / N] * N
        combined = np.zeros(self.n_elements, dtype=complex)
        for phases, w in zip(target_phases, weights):
            combined += w * np.exp(1j * phases)
        magnitude = np.abs(combined)
        phase_out = np.angle(combined) % (2.0 * np.pi)
        # SPL penalty: coherent combination efficiency
        avg_mag   = np.mean(magnitude)
        penalty   = 20.0 * np.log10(max(avg_mag, 1e-10))
        return phase_out, penalty


# ─── Dual panel model ─────────────────────────────────────────────────────────

class DualPanelArray:
    """
    Two co-mounted panels, separated by offset_m in x, coherently combined.
    Combined source SPL = single_panel_spl + coherent_gain_db
    """

    def __init__(self, panel_sep_m: float = 0.5, freq_hz: float = 3000.0,
                 spl_per_elem: float = 108.0):
        self.sep      = panel_sep_m
        self.panel_l  = ArrayPanel(freq_hz=freq_hz, spl_per_elem=spl_per_elem)
        self.panel_r  = ArrayPanel(freq_hz=freq_hz, spl_per_elem=spl_per_elem)
        # Offset panel positions
        self._offset_l = np.array([-panel_sep_m / 2, 0, 0])
        self._offset_r = np.array([ panel_sep_m / 2, 0, 0])

    @property
    def n_total(self) -> int:
        return self.panel_l.n_elements + self.panel_r.n_elements

    def coherent_gain_db(self) -> float:
        """
        Coherent combination gain from two panels.
        Power sum: +6 dB. Phase-coherent bonus: +3 to +5 dB (conservative +5 dB).
        """
        return 6.0 + 5.0  # 11 dB total

    def source_spl(self) -> float:
        """Combined on-axis SPL at 1m."""
        single = self.panel_l.source_spl()
        return single + self.coherent_gain_db()

    def focus_phases(self, focus_point: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Focus phases for both panels, accounting for panel offsets."""
        fp_l = focus_point - self._offset_l
        fp_r = focus_point - self._offset_r
        return (self.panel_l.focus_phases(fp_l),
                self.panel_r.focus_phases(fp_r))


# ─── Array gain analysis ──────────────────────────────────────────────────────

def array_gain_table() -> List[dict]:
    """
    Table of array gain, beam half-angle for various N.
    Used in report generation.
    """
    results = []
    for N in [16, 32, 64, 128, 256, 512, 1024]:
        gain  = 20.0 * np.log10(N)
        lam   = C_SOUND / 3000.0
        d     = lam / 2
        bha   = np.degrees(np.arcsin(min(0.886 * lam / (N * d), 1.0)))
        results.append({"N": N, "gain_db": round(gain, 1),
                         "beam_half_angle_deg": round(bha, 3)})
    return results


# ─── OAM angular stimulus ─────────────────────────────────────────────────────

def oam_canal_stimulus(mod_freq_hz: float, topological_charge: int = 1) -> float:
    """
    Angular velocity stimulus delivered to semicircular canal by OAM beam.
    omega = 2*pi*f_mod * l   (rad/s)
    Cupula threshold: ~2 rad/s
    """
    return 2.0 * np.pi * mod_freq_hz * topological_charge


def oam_nystagmus_margin(mod_freq_hz: float, l: int = 1) -> float:
    """
    Ratio of OAM stimulus to nystagmus induction threshold.
    >1.0 means nystagmus will be induced.
    """
    from physics import NYSTAGMUS_THRESHOLD
    return oam_canal_stimulus(mod_freq_hz, l) / NYSTAGMUS_THRESHOLD
