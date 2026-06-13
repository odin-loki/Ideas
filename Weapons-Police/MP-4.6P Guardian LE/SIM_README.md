# MP-4.6P Guardian LE — simulation documentation

## Engine path

| Layer | File | Role |
|---|---|---|
| Tier-1 ballistics | [`../../Weapons-Defence/weapons_simulation.py`](../../Weapons-Defence/weapons_simulation.py) | Cartridge `4.6x22mm`, weapon `MP-4.6P Guardian LE` |
| Tier-2 aux | Same engine | §6 SPL, §10 barrel life, §11 peak recoil (muzzle brake 42 %) |
| Tier-3 lifecycle | [`../../Weapons-Defence/weapon_lifecycle.py`](../../Weapons-Defence/weapon_lifecycle.py) | §23 — structural SF, Archard bore life, parts-life table, 7-mode Bernoulli MC |
| Results | [`../../Weapons-Defence/weapons_sim_results.md`](../../Weapons-Defence/weapons_sim_results.md) | Authoritative tables |

## Simulator keys

- **Cartridge:** `4.6x22mm` (calibrated MV 396 m/s, P_max 246 MPa)
- **Weapon:** `MP-4.6P Guardian LE`
- **Platform ID:** `mp46p_guardian_le`

## Re-run

```bash
python platform_simulation.py
```

Full portfolio:

```bash
cd ../../Weapons-Defence
python weapons_simulation.py
```

## Claim anchors (spec §15)

| Claim | §23 / results field |
|---|---|
| MV 396 m/s | weapons table + cartridge row |
| ME 259 J | weapons table |
| Felt recoil 0.078 ft·lb | `tier3.weapon_lifecycle["MP-4.6P Guardian LE"].recoil` |
| MRBF 20 548 analytic | `reliability.mrbf_analytic` |
| MRBF ~30 000 simulated | `reliability.mrbf_simulated` |
| FTF 1:80 000 | `reliability.ftf_rate` |
| Bore life 24 000 rd | `parts_life.bore_life_rounds` |
| Barrel SF_yield 2.42 | `structural.barrel_sf_yield` |

## Result tables for this platform

| Topic | `weapons_sim_results.md` section |
|---|---|
| Ballistics | §1 (`4.6x22mm`), §2 (`MP-4.6P Guardian LE`) |
| Barrel life | §10 |
| Peak recoil force | §11 |
| **§23 Lifecycle** | `MP-4.6P Guardian LE` — bore life 24,000 rd, MRBF 20,548 analytic / 30,000 simulated, felt recoil 0.08 ft·lb, barrel SF 2.42, FTF 1:80,000 |

## Back-port note

The military [`MP-4.6M Guardian Pistol`](../../Weapons-Defence/MP-4.6M%20Guardian%20Pistol/) and [`MP-4.6M Defender PDW`](../../Weapons-Defence/MP-4.6M%20Defender%20PDW/) now share the same §23 lifecycle module and Tier-2 surface-engineering reliability framework documented first in the LE spec Appendix A.
