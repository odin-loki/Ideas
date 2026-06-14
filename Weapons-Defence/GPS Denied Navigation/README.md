# AGINS — Autonomous GPS-Independent Navigation System

> **A simulation-validated passive multi-modal navigation stack fusing celestial geometry, magnetic anomaly matching, sky polarisation, pedestrian/vehicle step mechanics, and inertial dead-reckoning through the GH-SR-IMM filter.** Headline design: ship (FOG-grade) **30 m** mean error clear sky / **57 m** in storm; soldier (MEMS) **26 m** open terrain / **61 m** urban — all GPS-jam unaffected at **~500 g**, **<2 W** (soldier) or **~30 kg**, **~50 W** (ship).

> **Genre note.** Commercial Sensitive / defence-technology register is adopted for tonal coherence with the rest of `Weapons-Defence/`. No real procurement programme, classified release, or fielded prototype data is implied. **Navigation numbers trace to the standalone `agins_sim` package in this folder; the core filter is defined in [`../../Filtering/`](../../Filtering/).**

---

## What this folder is

AGINS is a **complete platform subfolder**: operator specification, dedicated Python simulation suite (`agins_sim_package`), and cross-links to the portfolio filtering research. Unlike cartridge-level weapons in the parent [`../weapons_simulation.py`](../weapons_simulation.py), AGINS carries its own navigation physics because multi-modal sensor fusion, MagNav map matching, celestial fixes, and IMM manoeuvre routing are outside the Tier-1/Tier-2 ballistics tables.

**Reading order for new readers:**

1. **This README** — navigation and headline numbers.
2. [`papers/AGINS_Specification.md`](papers/AGINS_Specification.md) — full technical reference (Parts I–VII: architecture, applications, BOM, economics, IP, limitations).
3. [`papers/AGINS_Research_Paper.md`](papers/AGINS_Research_Paper.md) — formal design-and-validation narrative (Parts I–XII, convergence in Part X).
4. [`SIM_README.md`](SIM_README.md) — how to re-run simulations and interpret ship vs soldier tracks.
5. Run [`platform_simulation.py`](platform_simulation.py) — consolidated navigation performance report.
6. [`../../Filtering/GH_SR_IMM_Research_Paper.md`](../../Filtering/GH_SR_IMM_Research_Paper.md) — formal filter definition (GH-SR-IMM).

---

## Source documents

| Document | Format | Role |
|---|---|---|
| [`papers/AGINS_Specification.md`](papers/AGINS_Specification.md) | Technical reference | Filter architecture, sensor suites, applications catalogue, BOM, economics, IP, limitations — **start here** |
| [`papers/AGINS_Research_Paper.md`](papers/AGINS_Research_Paper.md) | Academic research paper | Parts I–XII: subsystem design, simulation validation, **Part X convergence**, 90 references |
| [`SIM_README.md`](SIM_README.md) | Simulation documentation | Module map, headline table, filter cross-refs |
| [`platform_simulation.py`](platform_simulation.py) | Local entry script | Runs full `agins_sim` suite |
| [`agins_sim_package/`](agins_sim_package/) | Python package | Ship + soldier Monte Carlo modules, GH-SR-IMM core |
| [`archive/`](archive/) | Legacy scripts | Superseded `nav_sim_soldier.py` — historical only |

### Simulation modules (`agins_sim_package/agins_sim/`)

| Module | File | Role |
|---|---|---|
| Filter | [`filter/gh_sr_imm.py`](agins_sim_package/agins_sim/filter/gh_sr_imm.py) | GH-SR-IMM: NIG posterior, SR-CKF, IMM bank, GRIA α gate |
| Baseline KF | [`filter/standard_kf.py`](agins_sim_package/agins_sim/filter/standard_kf.py) | Standard Kalman comparison track |
| Ship platform | [`platforms/ship.py`](agins_sim_package/agins_sim/platforms/ship.py) | FOG-grade maritime Monte Carlo (clear sky, storm) |
| Soldier platform | [`platforms/soldier.py`](agins_sim_package/agins_sim/platforms/soldier.py) | MEMS dismounted Monte Carlo (open, urban, mixed) |
| Environments | [`scenarios/environments.py`](agins_sim_package/agins_sim/scenarios/environments.py) | Sky fraction, urban magnetic disturbance, night flags |
| Sensors | [`sensors/`](agins_sim_package/agins_sim/sensors/) | Celestial, MagNav, polar compass, PDR speed, IMU |
| Config | [`config.py`](agins_sim_package/agins_sim/config.py) | Platform parameters and scenario seeds |
| Report | `reports/generate.py` | Markdown + JSON consolidated output *(via `run_all.py`)* |

---

## Headline numbers (simulation-validated)

| Metric | Value |
|---|---|
| Filter | **GH-SR-IMM** (NIG + SR-CKF + 3-model IMM + GRIA α gate) |
| Sensor modalities | **5** — celestial, magnetic, polarised sky, PDR speed, inertial |
| Ship mean error (clear sky) | **37 m** sim / **30 m** spec (P90 **66 m** / **50 m**) |
| Ship mean error (6 hr storm) | **57 m** (P90 **91 m**) |
| Soldier mean error (open, night) | **26 m** (P90 **57 m**) |
| Soldier mean error (urban patrol) | **61 m** (P90 **91 m**) |
| PDR-only DR (soldier) | **103 m** mean |
| Raw MEMS DR (soldier) | **336 m** mean |
| GH-SR-IMM vs Kalman (manoeuvre) | **+52 % to +87 %** improvement |
| Soldier SWaP | **~500 g**, **<2 W** |
| Ship SWaP | **~30 kg**, **~50 W** |
| Soldier unit cost (target) | **$8K–15K** |
| Ship unit cost (target) | **$150K–300K** |

See [`SIM_README.md`](SIM_README.md) for methodology, scenario matrix, and limitations.

---

## Simulation verification

```bash
python platform_simulation.py
```

Or from the package directory:

```bash
cd agins_sim_package
pip install -r agins_sim/requirements.txt
python run_all.py
```

Reports: `agins_sim_package/agins_sim/outputs/agins_sim_report.md`

Optional JSON summary:

```bash
python platform_simulation.py --json
```

---

## Cross-references

| Related system | Folder |
|---|---|
| GH-SR-IMM filter (definition) | [`../../Filtering/`](../../Filtering/) |
| GH-SR-IMM research paper | [`../../Filtering/GH_SR_IMM_Research_Paper.md`](../../Filtering/GH_SR_IMM_Research_Paper.md) |
| GRIA α quality gate (algebra) | [`../../Compression Algorithms/`](../../Compression%20Algorithms/) |
| MT-X Leviathan (platform consumer) | [`../Leviathon Tank/`](../Leviathon%20Tank/) |
| TAIPAN-1 (terminal guidance adjacency) | [`../TAIPAN Missile/`](../TAIPAN%20Missile/) |
| Battle Sim (platform-state estimation) | [`../../Battle Sim/`](../../Battle%20Sim/) |

---

## Honest framing

- **Not a fielded navigation system.** Concept and simulation only; no instrumented field trials or live MagNav survey validation.
- **Separate simulator.** Do not expect AGINS rows in [`../weapons_sim_results.md`](../weapons_sim_results.md).
- **Accuracy gap vs GPS.** 10–30× worse than military GPS in nominal conditions; decisive advantage is **operation in GPS-denied environments** where GPS gives zero.
- **Urban ceiling.** ~60 m mean error without visual odometry or map matching; remedies documented in Part VII of the specification.
- **Filter provenance.** GH-SR-IMM is shared with the [`Filtering/`](../../Filtering/) research folder; navigation-specific IMM tuning and GRIA gate thresholds are AGINS trade secrets in the spec.

[← Weapons-Defence](../README.md)
