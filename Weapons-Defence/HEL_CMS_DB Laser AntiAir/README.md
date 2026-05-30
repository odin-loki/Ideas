# HEL-CMS/DB — High-Energy Laser Counter-Munitions System

> **A directed-energy weapon concept:** a fully autonomous, truck-mounted 280–300 kW fiber laser air-defence platform powered by a megawatt-class Sr-90 radioisotope diamond battery power plant. Covers the full aerial threat spectrum from micro-UAVs to cruise missiles with zero fuel logistics tail. Physics is first-principles validated; the power source sits at TRL 2–3.

---

## What this folder is

This is a paired engineering specification + research paper for the HEL-CMS/DB (**High-Energy Laser Counter-Munitions System / Diamond Battery**). The system addresses a single bottleneck in mobile high-energy laser weapons: power. Conventional 300 kW laser systems require diesel generators drawing 700 kW continuously — a fuel logistics chain that is a tactical vulnerability and a principal reason the US Army's 300 kW IFPC-HEL "Valkyrie" programme was discontinued in March 2026.

HEL-CMS/DB replaces the generator entirely with four TDB-1M Sr-90 thermal-betavoltaic hybrid modules producing 1 MW(e), eliminating the fuel tail and enabling continuous, unlimited-duration operation on a 20-year isotope service life.

---

## 📑 Source documents

| Document | Role |
|---|---|
| [`HEL_CMS_DB_Full_Spec.md`](HEL_CMS_DB_Full_Spec.md) | Engineering specification (v2.0, physics-validated). 12 parts covering beam physics, laser subsystem, adaptive optics, sensors and tracking, power subsystem, thermal management, platform, autonomous fire control, survivability, cost analysis, and development roadmap. All engagement numbers derived from first-principles simulation. |
| [`HEL_CMS_DB_Research_Paper.md`](HEL_CMS_DB_Research_Paper.md) | Academic research paper. Reviews the state of the art in HEL weapons (Iron Beam, DragonFire, HELIOS/IFPC-HEL), betavoltaic and RTG technology, and the Bristol/UKAEA C-14 diamond battery demonstration. Presents the full physics simulation, 20-year TCO model, and phased development strategy. 46 references. |

---

## 🎯 Headline numbers (simulation-verified)

### Laser performance

| Threat | Dwell to kill @ 3 km | Dwell to kill @ 5 km | Status |
|---|---|---|---|
| Micro-UAV | 0.2 s | 0.3 s | ✓ Full envelope |
| Combat UAV (Shahed-class) | 0.7 s | 0.8 s | ✓ Full envelope |
| Mortar 60 mm | 2.0 s | 2.0 s | ✓ Full envelope |
| Rocket 122 mm | 4.9 s | 5.1 s | ✓ Full envelope |
| Cruise missile (standard skin) | 12.3 s | 12.6 s | ✓ 4–7 km kill envelope |
| Cruise missile (ablative coated) | 29.4 s | 30.3 s | ✗ Requires Block 3 upgrade |

**Hard kill envelope at 280 kW:** 4–7 km against standard cruise missiles in clear conditions. Below 4 km, the engagement window is insufficient at this power level — physical constraint, not engineering limitation.

**Irradiance at range (clear, 300 kW):** 421.8 W/cm² at 500 m; 408.0 W/cm² at 3 km; 395.9 W/cm² at 5 km. Nearly flat — the 30 cm aperture maintains lethal flux across the operational envelope.

### Beam director

| Parameter | Value |
|---|---|
| Optical power | 280 kW (28 modules, 10 kW each) |
| Combining method | Spectral beam combining (SBC), 1,740 lines/mm grating |
| Aperture | 300 mm |
| Beam quality M² | ≤ 1.5 (combined) |
| Pointing jitter | < 0.5 µrad RMS |
| Gimbal slew | ≥ 270°/s (custom high-torque direct-drive) |
| AO loop bandwidth | ~1,176 Hz closed-loop |
| Deformable mirror | 241 actuators, hexagonal close-pack |

### Power subsystem (TDB-1M)

| Parameter | Per module | 4-module array |
|---|---|---|
| Isotope | Sr-90 as SrTiO₃ | — |
| Core mass | 200 kg | 800 kg |
| Electrical output | 250 kW(e) | 1,000 kW(e) |
| Shield mass | ~3,320 kg | ~13,280 kg |
| Platform | — | Oshkosh M1070 HET + semi-trailer |
| TRL | 2–3 (conceptual) | — |

The shielding mass (13,280 kg for four modules) is the dominant mass driver and the reason the platform is a semi-trailer rather than a HEMTT.

### Cost and TCO

| Metric | Value |
|---|---|
| Prototype unit cost | $73.5M |
| Series production (units 2–10) | $47.8M |
| Mature production (unit 11+) | $33.1M |
| 20-year TCO (HEL-CMS/DB) | **$71.8M** |
| 20-year TCO (conventional generator HEL) | $123.6M |
| Saving vs conventional over 20 years | **$51.8M per unit** |
| Break-even vs conventional | **4.7 years** |
| Per-engagement cost (cruise missile) | **< $0.50** |
| Per-engagement cost (micro-UAV) | **< $0.01** |

---

## 🧠 System overview

**Sensor suite:** Ku-band 17 GHz AESA (4 faces, 32×32 per face, 360° coverage); MWIR 1,024×1,024 InSb FPA @ 100 Hz; 16-element acoustic array; 2–18 GHz ESM receiver; Mode 5 / Mode S IFF.

**Autonomous fire control:** Human-on-the-loop — machine decides, 200 ms veto window. 13-class AI classifier (radar doppler + micro-doppler + IR signature + ESM fusion) at < 150 ms inference. ROE uploaded at mission start, cryptographically signed, dual-key change authority.

**Platform:** Oshkosh M1070 HET tractor + custom 35-tonne air-ride semi-trailer. Total GVW ~32,650 kg. Setup time: 4 minutes (autonomous). Crew: 0.

**Network integration:** Link 16 / JREAP-C, IBCS STANAG 5516, BFT-2, Mode 5 IFF, Ka-band SATCOM. Standalone mode retains full autonomous capability with onboard sensors.

---

## 🚧 Honest caveats

- **TDB-1M power source is TRL 2–3.** The Bristol/UKAEA C-14 diamond battery (December 2024) demonstrated microwatts. The TDB-1M is proposed at 250 kW(e) per module — a nine-order-of-magnitude gap. Physics is consistent; engineering implementation at this power density is unsolved. A phased development strategy is documented: Phase 1 uses a conventional diesel generator (TRL 9) while TDB technology matures.
- **280 kW kills cruise missiles only above 4 km.** Below 4 km, the CM engagement window closes. Mitigation: network early engagement at 6–7 km; 500 kW Block 3 upgrade extends kill floor to 2.5 km.
- **Saturation attacks exceed single-aperture capacity.** As demonstrated in simulation, a six-simultaneous-threat scenario sees the CM kill consume the available window, leaving fast-closing rockets and mortars. A kinetic close-in layer (Starstreak, AHEAD) is required for sub-2 km saturation threats.
- **Ablative-coated cruise missiles multiply dwell to ~29 s** — beyond the engagement window at 300 kW. Guidance bay aim-point (uncoated glass/composite) is the mitigation.
- **Classification banners are illustrative.** No real classification, no real programme office.

---

## 🔗 Related work in this repo

- [`../../../Diamond Batterys/`](../../../Diamond%20Batterys/) — ADB/TDB diamond battery series that provides the power architecture referenced here
- [`../../../Weapons-Defence/`](../../) — parent portfolio; see `weapons_simulation.py` for the common simulation infrastructure
- [`../../../Filtering/`](../../../Filtering/) — GH-SR-IMM tracking (relevant to the MWIR + radar sensor fusion problem)
- [`../../../Asset Tracking Algorithm/`](../../../Asset%20Tracking%20Algorithm/) — ARIA-INTEL multi-target intelligence engine

---

[← Back to Weapons-Defence README](../README.md)
