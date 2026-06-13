# Weapons-Defence portfolio — simulation results

_Output of `weapons_simulation.py`. All numbers in this folder's specification sheets and research papers should match these._

## 1. Cartridges — internal & external ballistics

| Cartridge | Bore | Bullet | MV | ME | P_max | Recoil impulse |
|---|---|---|---|---|---|---|
| 4.6x30mm | 4.65 mm | 2.6 g | 501 m/s | 326 J | 180 MPa (26107 psi) | 1.65 N·s |
| 4.6x30mm_PDW | 4.65 mm | 2.6 g | 542 m/s | 382 J | 180 MPa (26107 psi) | 1.79 N·s |
| 4.6x22mm | 4.65 mm | 3.3 g | 396 m/s | 259 J | 246 MPa (35679 psi) | 1.46 N·s |
| 5.7x28mm | 5.70 mm | 2.0 g | 661 m/s | 437 J | 180 MPa (26107 psi) | 1.78 N·s |
| 6.8x51mm | 6.85 mm | 8.7 g | 731 m/s | 2324 J | 307 MPa (44538 psi) | 9.62 N·s |
| 5.56x45mm | 5.70 mm | 4.0 g | 939 m/s | 1764 J | 374 MPa (54295 psi) | 6.42 N·s |
| 7.62x51mm | 7.82 mm | 9.5 g | 820 m/s | 3192 J | 355 MPa (51524 psi) | 12.02 N·s |
| 15.2x115mm | 15.20 mm | 64.0 g | 781 m/s | 19505 J | 258 MPa (37361 psi) | 82.07 N·s |
| 14.5x114mm | 14.50 mm | 64.0 g | 948 m/s | 28755 J | 295 MPa (42812 psi) | 108.78 N·s |
| 57x347mm | 57.00 mm | 2400.0 g | 948 m/s | 1077666 J | 257 MPa (37308 psi) | 4397.13 N·s |
| 57mm_LV_grenade | 57.00 mm | 350.0 g | 149 m/s | 3872 J | 109 MPa (15788 psi) | 52.71 N·s |
| 57mm_mortar | 57.00 mm | 1400.0 g | 187 m/s | 24427 J | 111 MPa (16048 psi) | 267.41 N·s |
| 140mm_KE | 140.00 mm | 6400.0 g | 1698 m/s | 9227097 J | 199 MPa (28794 psi) | 48904.64 N·s |

## 2. Weapons — per-platform numbers

| Weapon | Cartridge | Empty mass | Mag | Action | MV | ME | P_max | Free recoil |
|---|---|---|---|---|---|---|---|---|
| MP-4.6M Pistol | 4.6x30mm | 0.92 kg | 20 | rotating bolt, short recoil | 501 m/s | 326 J | 180 MPa | 1.5 J (1.1 ft·lb) |
| MP-4.6P Guardian LE | 4.6x22mm | 0.85 kg | 20 | gas-operated delayed blowback | 396 m/s | 259 J | 246 MPa | 1.2 J (0.9 ft·lb) |
| MP-4.6M Defender PDW | 4.6x30mm_PDW | 2.10 kg | 40 | rotating bolt, short recoil + buffered bolt-carrier | 542 m/s | 382 J | 180 MPa | 0.8 J (0.6 ft·lb) |
| MP-6.8 Mark II Rifle | 6.8x51mm | 4.10 kg | 20 | short-stroke gas piston, rotating bolt | 731 m/s | 2324 J | 307 MPa | 11.3 J (8.3 ft·lb) |
| MAS-15.2E Sniper | 15.2x115mm | 13.20 kg | 8 | bolt action, three-lug rotating bolt | 781 m/s | 19505 J | 258 MPa | 255.2 J (188.2 ft·lb) |
| 57 mm Autocannon | 57x347mm | 350.00 kg | 120 | dual-feed externally powered rotary | 948 m/s | 1077666 J | 257 MPa | 27621.1 J (20372.3 ft·lb) |
| 57 mm Underbarrel GL | 57mm_LV_grenade | 2.40 kg | 1 | single-shot break-action under-barrel | 149 m/s | 3872 J | 109 MPa | 578.8 J (426.9 ft·lb) |
| 57 mm Mortar/RPG | 57mm_mortar | 7.20 kg | 1 | muzzle-loaded dual-mode tube | 187 m/s | 24427 J | 111 MPa | 4965.9 J (3662.7 ft·lb) |
| 140 mm Tank Gun | 140mm_KE | 3400.00 kg | 1 | vertical sliding-block breech, electrothermal-chemical | 1698 m/s | 9227097 J | 198 MPa | 351715.2 J (259411.8 ft·lb) |

## 3. Armour-piercing performance vs RHA (mm)

Small-arms calibres tabulated at 0 / 100 / 300 / 500 / 800 / 1 000 / 1 500 m. Autocannon and tank calibres at 0 / 500 / 1 000 / 2 000 / 3 000 m.

| Cartridge | 0 m | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m | 2000 m |
|---|---|---|---|---|---|---|---|---|
| 4.6x30mm | 3.8 | 3.1 | 2.2 | 1.8 | 1.5 | 1.3 | — | — |
| 4.6x30mm_PDW | 4.2 | 3.4 | 2.3 | 1.9 | 1.5 | 1.3 | — | — |
| 4.6x22mm | 3.1 | 2.7 | 2.2 | 2.0 | 1.7 | — | — | — |
| 5.7x28mm | 2.6 | 1.8 | 1.0 | 0.7 | 0.5 | — | — | — |
| 6.8x51mm | 11.1 | 10.1 | 8.1 | 6.5 | 4.7 | 3.9 | — | — |
| 5.56x45mm | 7.7 | 6.6 | 4.8 | 3.4 | 2.0 | 1.6 | — | — |
| 7.62x51mm | 9.7 | 8.6 | 6.7 | 5.1 | 3.3 | 2.7 | 2.1 | — |
| 15.2x115mm | 42.0 | 39.6 | 35.1 | 31.0 | 25.5 | 22.3 | 16.0 | — |
| 14.5x114mm | 36.9 | 34.9 | 31.2 | 27.6 | 22.8 | 19.9 | 14.0 | 9.9 |

| Heavy cartridge | 0 m | 500 m | 1000 m | 2000 m | 3000 m | 4000 m |
|---|---|---|---|---|---|---|
| 57x347mm | 139.7 | 125.4 | 113.0 | 0.0 | — | — |
| 140mm_KE | 867.1 | 698.1 | 540.9 | 326.7 | 215.7 | 0.0 |

## 4. Trajectory — velocity (m/s) vs range

| Cartridge | 0 m | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m | 2000 m |
|---|---|---|---|---|---|---|---|---|
| 4.6x30mm | 501.0 | 433.7 | 338.4 | 299.2 | 255.6 | 230.7 | — | — |
| 4.6x30mm_PDW | 542.0 | 469.7 | 357.4 | 308.4 | 263.1 | 237.3 | — | — |
| 4.6x22mm | 396.0 | 357.1 | 315.4 | 288.9 | 254.9 | — | — | — |
| 5.7x28mm | 660.8 | 510.1 | 323.8 | 264.2 | 197.5 | — | — | — |
| 6.8x51mm | 730.9 | 680.2 | 584.5 | 498.8 | 392.7 | 343.7 | — | — |
| 5.56x45mm | 939.1 | 846.1 | 671.5 | 519.2 | 353.5 | 309.1 | — | — |
| 7.62x51mm | 819.8 | 753.0 | 627.2 | 515.5 | 382.1 | 330.2 | 272.1 | — |
| 15.2x115mm | 780.7 | 749.2 | 687.9 | 629.1 | 547.5 | 497.7 | 392.2 | — |
| 14.5x114mm | 947.9 | 911.5 | 840.3 | 771.3 | 672.8 | 610.9 | 474.1 | 369.4 |

| Heavy cartridge | 0 m | 500 m | 1000 m | 2000 m | 3000 m | 4000 m |
|---|---|---|---|---|---|---|
| 57x347mm | 947.7 | 877.0 | 808.3 | 678.4 | — | — |
| 57mm_LV_grenade | 148.7 | — | — | — | — | — |
| 57mm_mortar | 186.8 | 162.1 | — | — | — | — |
| 140mm_KE | 1698.1 | 1561.5 | 1428.5 | 1178.8 | 934.3 | 708.6 |

## 5. Suppressor attenuation (peak dB reduction)

| Weapon | Chamber vol | Suppressor vol | Baffles | Attenuation |
|---|---|---|---|---|
| MP-4.6M Pistol integral | 1.0 cm³ | 80 cm³ | 6 | 40.0 dB |
| MP-4.6M Defender PDW | 1.0 cm³ | 180 cm³ | 8 | 40.0 dB |
| MP-6.8 Mark II Rifle | 3.5 cm³ | 410 cm³ | 7 | 40.0 dB |
| MAS-15.2E Sniper | 39.0 cm³ | 1800 cm³ | 10 | 40.0 dB |

## 6. Muzzle blast & hearing-protection stack (peak SPL, dB)

Calibration: 5.56 carbine ≈ 165 dB / 158 dB; 7.62 rifle ≈ 166 / 159; .50 BMG ≈ 178 / 170; 120 mm tank ≈ 187. The shooter-ear column is ~7 dB below muzzle; layered hearing-protection columns add foam plug (−22), double plug+muff (−28), or double + TACS personal active cancellation (−28 + 25). The unsuppressed peak SPL exceeds OSHA ceiling (140 dB) for every weapon in this folder.

| Weapon | Muzzle (unsup) | Ear (unsup) | Muzzle (sup) | Ear (sup) | Ear + plug | Ear + double | Ear + double + TACS |
|---|---|---|---|---|---|---|---|
| MP-4.6M Pistol | 163.4 | 156.4 | 123.4 | 116.4 | 94.4 | 88.4 | 63.4 |
| MP-4.6P Guardian LE | 164.0 | 157.0 | 164.0 | 157.0 | 135.0 | 129.0 | 104.0 |
| MP-4.6M Defender PDW | 164.0 | 157.0 | 124.0 | 117.0 | 95.0 | 89.0 | 64.0 |
| MP-6.8 Mark II Rifle | 166.2 | 159.2 | 126.2 | 119.2 | 97.2 | 91.2 | 66.2 |
| MAS-15.2E Sniper | 165.0 | 158.0 | 125.0 | 118.0 | 96.0 | 90.0 | 65.0 |
| 57 mm Autocannon | 164.2 | 157.2 | 164.2 | 157.2 | 135.2 | 129.2 | 104.2 |
| 57 mm Underbarrel GL | 163.1 | 156.1 | 163.1 | 156.1 | 134.1 | 128.1 | 103.1 |
| 57 mm Mortar/RPG | 162.6 | 155.6 | 162.6 | 155.6 | 133.6 | 127.6 | 102.6 |
| 140 mm Tank Gun | 163.8 | 156.8 | 163.8 | 156.8 | 134.8 | 128.8 | 103.8 |

## 7. Zeroed bullet drop from sight-line (cm, small arms)

Bullet drop measured from the optical sight line for a scope-height-over-bore of 4 cm, with each cartridge bisection-zeroed at its canonical range (100 m for service rifles; 100 m for the PDW; 100 m for the pistol; 500 m for the 15.2 mm sniper).

| Cartridge | Zero | 50 m | 100 m | 200 m | 300 m | 500 m | 800 m | 1000 m | 1500 m |
|---|---|---|---|---|---|---|---|---|---|
| 4.6x30mm | 100 m | +8.1 | +0.1 | -58.9 | -181.5 | -712.0 | -2350.6 | -4152.3 | -12368.7 |
| 4.6x30mm_PDW | 100 m | +7.2 | +0.1 | -50.9 | -157.0 | -628.9 | -2130.6 | -3801.7 | -11484.1 |
| 4.6x22mm | 100 m | +11.1 | +0.1 | -83.5 | -248.3 | -904.4 | -2784.2 | -4809.7 | -13180.3 |
| 5.7x28mm | 100 m | +6.0 | +0.1 | -41.7 | -151.1 | -661.5 | -2610.6 | -5066.0 | -19818.0 |
| 6.8x51mm | 100 m | +4.7 | +0.1 | -24.7 | -76.1 | -268.9 | -865.5 | -1583.8 | -4909.6 |
| 5.56x45mm | 100 m | +3.8 | +0.2 | -17.6 | -52.0 | -194.4 | -718.9 | -1422.6 | -5214.7 |
| 7.62x51mm | 100 m | +4.3 | +0.2 | -21.0 | -62.0 | -226.3 | -777.3 | -1454.9 | -4892.3 |
| 15.2x115mm | 100 m | +4.4 | +0.2 | -20.9 | -61.0 | -206.2 | -613.4 | -1043.9 | -2894.7 |
| 14.5x114mm | 100 m | +3.5 | +0.1 | -16.0 | -44.2 | -145.7 | -420.3 | -712.5 | -1959.3 |

## 8. Wind drift at 10 mph (4.47 m/s) full-value crosswind

| Cartridge | 100 m | 300 m | 500 m | 800 m | 1000 m | 1500 m |
|---|---|---|---|---|---|---|
| 4.6x30mm | 6.8 cm | 65.0 cm | 169.3 cm | 388.7 cm | 580.8 cm | — |
| 4.6x30mm_PDW | 6.2 cm | 61.4 cm | 169.0 cm | 394.5 cm | 589.3 cm | — |
| 4.6x22mm | 6.2 cm | 49.3 cm | 120.5 cm | 277.9 cm | — | — |
| 5.7x28mm | 9.6 cm | 102.8 cm | 275.0 cm | 663.9 cm | — | — |
| 6.8x51mm | 2.3 cm | 22.0 cm | 65.7 cm | 186.9 cm | 309.8 cm | — |
| 5.56x45mm | 2.6 cm | 26.3 cm | 83.0 cm | 257.8 cm | 436.1 cm | — |
| 7.62x51mm | 2.4 cm | 23.6 cm | 72.2 cm | 213.3 cm | 358.9 cm | 839.3 cm |
| 15.2x115mm | 1.2 cm | 11.4 cm | 32.9 cm | 90.0 cm | 147.1 cm | 369.9 cm |
| 14.5x114mm | 0.9 cm | 8.9 cm | 25.8 cm | 70.8 cm | 116.3 cm | 297.7 cm |

*Heavy-weapon wind drift (heavy cartridges):*
| Heavy cartridge | 500 m | 1000 m | 2000 m | 3000 m |
|---|---|---|---|---|
| 57x347mm | 0.09 m | 0.39 m | 1.72 m | — |
| 57mm_LV_grenade | — | — | — | — |
| 57mm_mortar | 0.98 m | — | — | — |
| 140mm_KE | 0.06 m | 0.24 m | 1.04 m | 2.68 m |

## 9. Hatcher max effective range (`KE > 80 J` personnel threshold) + supersonic range

| Cartridge | Max effective range (m, KE > 80 J) | Supersonic range (m) | Muzzle (fps) |
|---|---|---|---|
| 4.6x30mm | 878 | 301 | 1644 |
| 4.6x30mm_PDW | 928 | 376 | 1778 |
| 4.6x22mm | > 3,500 m (sim cap) | 176 | 1299 |
| 5.7x28mm | 452 | 276 | 2168 |
| 6.8x51mm | > 3,500 m (sim cap) | 1030 | 2398 |
| 5.56x45mm | > 3,500 m (sim cap) | 855 | 3081 |
| 7.62x51mm | > 3,500 m (sim cap) | 955 | 2690 |
| 15.2x115mm | > 3,500 m (sim cap) | > 3,500 m (sim cap) | 2561 |
| 14.5x114mm | > 3,500 m (sim cap) | > 3,500 m (sim cap) | 3110 |
| 57x347mm | > 6,000 m (sim cap) | > 6,000 m (sim cap) | 3109 |
| 57mm_LV_grenade | > 6,000 m (sim cap) | 0 | 488 |
| 57mm_mortar | > 6,000 m (sim cap) | 0 | 613 |
| 140mm_KE | > 10,000 m (sim cap) | > 10,000 m (sim cap) | 5571 |

## 10. Barrel life and sustained-fire thermal limit

Barrel life is rounds-to-throat-erosion at the spec'd chamber pressure, calibrated against M4 (10 000 rd chrome-lined 5.56), M14 (7 500 rd 7.62), M2HB (10 000 rd .50 Stellite), GAU-8 (6 000 rd 30 mm), M256 (700–1 000 rd 120 mm tank). Sustained-fire bound is set by barrel-thermal capacity (quick-change barrels treated as 1.5×).

| Weapon | Liner | Barrel mass | Life (rounds) | Sustained rpm (thermal) |
|---|---|---|---|---|
| MP-4.6M Pistol | stellite | 0.30 kg | 302,501 | 250 |
| MP-4.6P Guardian LE | chrome | 0.28 kg | 176,870 | 250 |
| MP-4.6M Defender PDW | stellite | 0.45 kg | 302,501 | 250 |
| MP-6.8 Mark II Rifle | stellite | 1.30 kg | 80,398 | 250 |
| MAS-15.2E Sniper | stellite | 4.40 kg | 22,753 | 131 |
| 57 mm Autocannon | chrome | 120.00 kg | 1,166 | 80 |
| 57 mm Underbarrel GL | chrome | 0.55 kg | 69,500 | 126 |
| 57 mm Mortar/RPG | chrome | 1.80 kg | 21,122 | 57 |
| 140 mm Tank Gun | stellite | 1850.00 kg | 618 | 114 |

## 11. Peak recoil force (sprung-stock, muzzle-brake corrected)

Peak shoulder force at the stock-pad assuming parabolic energy dissipation over `stock_travel_mm`. Muzzle-brake efficiency is the fraction of recoil impulse redirected laterally. The 140 mm uses a 600 mm hydraulic recoil stroke (the tank gun, not a shoulder weapon).

| Weapon | Free recoil (J) | Stock travel | Brake eff. | Peak force (N) | (lbf) |
|---|---|---|---|---|---|
| MP-4.6M Pistol | 1.5 | 4.0 mm | 0 % | 559 | 126 |
| MP-4.6P Guardian LE | 1.2 | 4.0 mm | 42 % | 158 | 35 |
| MP-4.6M Defender PDW | 0.8 | 18.0 mm | 0 % | 63 | 14 |
| MP-6.8 Mark II Rifle | 11.3 | 20.0 mm | 35 % | 358 | 80 |
| MAS-15.2E Sniper | 255.2 | 45.0 mm | 65 % | 1042 | 234 |
| 57 mm Autocannon | 27621.1 | 60.0 mm | 55 % | 139832 | 31437 |
| 57 mm Underbarrel GL | 578.8 | 18.0 mm | 0 % | 48237 | 10845 |
| 57 mm Mortar/RPG | 4965.9 | 50.0 mm | 40 % | 53632 | 12058 |
| 140 mm Tank Gun | 351715.2 | 600.0 mm | 55 % | 178056 | 40031 |

## 12. RHA penetration at NATO 60°-from-vertical obliquity (mm)

Normal incidence numbers are taken from §3 and reduced by `cos(θ)^n`, with `n = 1.6` for hardened-core small arms (Tate/Krupp) and `n = 0.7` for long-rod APFSDS (the rod yaws into normal-incidence behaviour above ~1 km/s).

| Cartridge | 0 m (normal) | 0 m (60°) | 300 m (60°) | 500 m (60°) | 1000 m (60°) |
|---|---|---|---|---|---|
| 4.6x30mm | 3.8 | 1.3 | 0.7 | 0.6 | 0.4 |
| 4.6x30mm_PDW | 4.2 | 1.4 | 0.8 | 0.6 | 0.4 |
| 4.6x22mm | 3.1 | 1.0 | 0.7 | 0.7 | — |
| 5.7x28mm | 2.6 | 0.9 | 0.3 | 0.2 | — |
| 6.8x51mm | 11.1 | 3.7 | 2.7 | 2.1 | 1.3 |
| 5.56x45mm | 7.7 | 2.5 | 1.6 | 1.1 | 0.5 |
| 7.62x51mm | 9.7 | 3.2 | 2.2 | 1.7 | 0.9 |
| 15.2x115mm | 42.0 | 13.9 | 11.6 | 10.2 | 7.4 |
| 14.5x114mm | 36.9 | 12.2 | 10.3 | 9.1 | 6.6 |
| 57x347mm | 139.7 | 86.0 | — | 77.2 | 69.6 |
| 140mm_KE | 867.1 | 533.8 | — | 429.7 | 333.0 |

## 13. Body-armour V50 ballistic-limit + back-face deformation

V50 is the projectile velocity at which the armour panel is defeated 50 % of the time. Threats below V50 are stopped; reported BFD is the clay-witness depression (NIJ 0101.06 method) and must remain `< 44 mm` to pass. Threats above V50 are PERFORATED.


**Soft IIIA (Kevlar/UHMWPE, 5.5 kg/m²)**

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm) | 390 m/s | 436.0 m/s | STOPPED | 44.0 mm |
| 5.7 × 28 mm SS190 (716 m/s, 2.0 g) | 716 m/s | 760.0 m/s | STOPPED | 44.0 mm |
| 5.56 × 45 NATO M855 (940 m/s, 4.0 g) | 940 m/s | 537.0 m/s | PERFORATED | — mm |
| 7.62 × 51 NATO M80 ball (820 m/s, 9.5 g) | 820 m/s | 383.0 m/s | PERFORATED | — mm |
| .30-06 M2 AP (878 m/s, 10.8 g) | 878 m/s | 144.0 m/s | PERFORATED | — mm |
| 7.62 × 54R B-32 AP (820 m/s, 10.4 g) | 820 m/s | 147.0 m/s | PERFORATED | — mm |
| 12.7 × 99 NATO M2 AP (890 m/s, 46.0 g) | 890 m/s | 81.0 m/s | PERFORATED | — mm |
| 15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm) | 781 m/s | 61.0 m/s | PERFORATED | — mm |

**NIJ III (steel + composite, 11.2 kg/m²)**

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm) | 390 m/s | 818.0 m/s | STOPPED | 12.5 mm |
| 5.7 × 28 mm SS190 (716 m/s, 2.0 g) | 716 m/s | 1426.0 m/s | STOPPED | 11.4 mm |
| 5.56 × 45 NATO M855 (940 m/s, 4.0 g) | 940 m/s | 1008.0 m/s | STOPPED | 44.0 mm |
| 7.62 × 51 NATO M80 ball (820 m/s, 9.5 g) | 820 m/s | 719.0 m/s | PERFORATED | — mm |
| .30-06 M2 AP (878 m/s, 10.8 g) | 878 m/s | 471.0 m/s | PERFORATED | — mm |
| 7.62 × 54R B-32 AP (820 m/s, 10.4 g) | 820 m/s | 482.0 m/s | PERFORATED | — mm |
| 12.7 × 99 NATO M2 AP (890 m/s, 46.0 g) | 890 m/s | 264.0 m/s | PERFORATED | — mm |
| 15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm) | 781 m/s | 198.0 m/s | PERFORATED | — mm |

**NIJ IV (B4C + UHMWPE, 25 kg/m²)**

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm) | 390 m/s | 1352.0 m/s | STOPPED | 2.6 mm |
| 5.7 × 28 mm SS190 (716 m/s, 2.0 g) | 716 m/s | 2358.0 m/s | STOPPED | 2.4 mm |
| 5.56 × 45 NATO M855 (940 m/s, 4.0 g) | 940 m/s | 1667.0 m/s | STOPPED | 21.0 mm |
| 7.62 × 51 NATO M80 ball (820 m/s, 9.5 g) | 820 m/s | 1189.0 m/s | STOPPED | 44.0 mm |
| .30-06 M2 AP (878 m/s, 10.8 g) | 878 m/s | 880.0 m/s | STOPPED | 44.0 mm |
| 7.62 × 54R B-32 AP (820 m/s, 10.4 g) | 820 m/s | 900.0 m/s | STOPPED | 44.0 mm |
| 12.7 × 99 NATO M2 AP (890 m/s, 46.0 g) | 890 m/s | 493.0 m/s | PERFORATED | — mm |
| 15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm) | 781 m/s | 371.0 m/s | PERFORATED | — mm |

**APES military (16-layer + 12 mm B4C tile, 35 kg/m²)**

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm) | 390 m/s | 1600.0 m/s | STOPPED | 1.5 mm |
| 5.7 × 28 mm SS190 (716 m/s, 2.0 g) | 716 m/s | 2790.0 m/s | STOPPED | 1.3 mm |
| 5.56 × 45 NATO M855 (940 m/s, 4.0 g) | 940 m/s | 1972.0 m/s | STOPPED | 11.6 mm |
| 7.62 × 51 NATO M80 ball (820 m/s, 9.5 g) | 820 m/s | 1407.0 m/s | STOPPED | 28.4 mm |
| .30-06 M2 AP (878 m/s, 10.8 g) | 878 m/s | 1041.0 m/s | STOPPED | 44.0 mm |
| 7.62 × 54R B-32 AP (820 m/s, 10.4 g) | 820 m/s | 1065.0 m/s | STOPPED | 44.0 mm |
| 12.7 × 99 NATO M2 AP (890 m/s, 46.0 g) | 890 m/s | 583.0 m/s | PERFORATED | — mm |
| 15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm) | 781 m/s | 438.0 m/s | PERFORATED | — mm |

**APES-L police (10-layer + 8 mm B4C, 22 kg/m²)**

| Threat | Threat v | V50 | Outcome | BFD |
|---|---|---|---|---|
| 9 mm 124 gr ball (390 m/s, 8.0 g, 9 mm) | 390 m/s | 1268.0 m/s | STOPPED | 3.3 mm |
| 5.7 × 28 mm SS190 (716 m/s, 2.0 g) | 716 m/s | 2212.0 m/s | STOPPED | 3.0 mm |
| 5.56 × 45 NATO M855 (940 m/s, 4.0 g) | 940 m/s | 1564.0 m/s | STOPPED | 26.2 mm |
| 7.62 × 51 NATO M80 ball (820 m/s, 9.5 g) | 820 m/s | 1116.0 m/s | STOPPED | 44.0 mm |
| .30-06 M2 AP (878 m/s, 10.8 g) | 878 m/s | 825.0 m/s | PERFORATED | — mm |
| 7.62 × 54R B-32 AP (820 m/s, 10.4 g) | 820 m/s | 844.0 m/s | STOPPED | 44.0 mm |
| 12.7 × 99 NATO M2 AP (890 m/s, 46.0 g) | 890 m/s | 462.0 m/s | PERFORATED | — mm |
| 15.2 × 115 APYT (781 m/s, 64.0 g, sabot 8.5 mm) | 781 m/s | 348.0 m/s | PERFORATED | — mm |

## 14. HE-Frag warhead — Gurney velocity, Mott fragment count, Carlton lethal area

| Warhead | Explosive | Charge mass | Shell mass | v_frag | Fragments | A_L | r_eff |
|---|---|---|---|---|---|---|---|
| 57 mm Underbarrel HE-Frag | Comp B | 0.12 kg | 0.18 kg | 1909 m/s | 720 (pre-scored) | 11 m² | 1.9 m |
| 57 mm Mortar HE | Comp B | 0.40 kg | 0.85 kg | 1666 m/s | 1,700 (natural) | 33 m² | 3.3 m |
| 57 mm Autocannon HE-Frag | Comp B | 0.55 kg | 1.65 kg | 1443 m/s | 6,600 (pre-scored) | 117 m² | 6.1 m |
| 140 mm Multi-Effect HE-Frag | CL-20 | 4.20 kg | 2.20 kg | 3064 m/s | 8,800 (pre-scored) | 1173 m² | 19.3 m |

## 15. Shaped-charge (HEAT) RHA penetration (static, normal incidence)

Birkhoff jet penetration assuming a standard copper liner at ~22° half-angle, jet length ≈ 0.7 × CD. Calibrated against published RPG-7 PG-7VL (93 mm CD, ~500 mm RHA), Hellfire (177 mm, ~1 100 mm), and TOW-2A (152 mm, ~900 mm).

| Warhead | Charge dia | Explosive | Liner | RHA pen (mm) | Calibres |
|---|---|---|---|---|---|
| 57 mm Underbarrel HEAT | 55 mm | RDX | copper | 41 | 0.75 CD |
| 57 mm Mortar/RPG HEAT | 55 mm | CL-20 | copper | 43 | 0.78 CD |
| 57 mm Autocannon HEDP | 50 mm | RDX | copper | 37 | 0.74 CD |
| 140 mm Multi-Effect HEAT | 130 mm | CL-20 | copper | 103 | 0.79 CD |

## 16. HPR-X rocket trajectory (Tsiolkovsky + ICAO drag integration)

Single (V1, V3) or two-stage (V2) APCP solid rockets. High-angle apogee shot is near-vertical (85–88°); range shot is 35° optimum. Drag uses subsonic `C_d ≈ 0.55`, supersonic `0.65`.

| Vehicle | Launch angle | Apogee | TOF | 35° max range | 35° apogee |
|---|---|---|---|---|---|
| HPR-X V1 (civ-amateur, 75 mm) | 88.0° | 5,782.0 m | 73.7 s | 6,408.0 m | 2,147.0 m |
| HPR-X V2 (two-stage 98→75 mm) | 85.0° | 7,914.0 m | 99.7 s | 7,342.0 m | 2,901.0 m |
| HPR-X V3 (152 mm SOF spotter) | 35.0° | 2,523.0 m | 45.4 s | 6,502.0 m | 2,523.0 m |

*Stage burnout details (high-angle shot):*
| Vehicle | Stage | Burnout v | Burnout alt | Burnout t |
|---|---|---|---|---|
| HPR-X V1 (civ-amateur, 75 mm) | V1 L1390 single | 1093.5 m/s | 1,209.0 m | 2.11 s |
| HPR-X V2 (two-stage 98→75 mm) | V2 M booster | 1024.9 m/s | 1,384.0 m | 2.61 s |
| HPR-X V2 (two-stage 98→75 mm) | V2 K sustainer | 1477.6 m/s | 3,917.0 m | 4.61 s |
| HPR-X V3 (152 mm SOF spotter) | V3 N5800 | 1293.3 m/s | 1,221.0 m | 3.21 s |

## 17. Energetic detonation chemistry (Kamlet–Jacobs)

Detonation pressure `P_CJ` and detonation velocity `D` from the Kamlet–Jacobs (1968) empirical correlation, plus Gurney constant `√(2E)` used in the fragmentation table.

| Explosive | ρ (g/cm³) | P_CJ (GPa) | VOD (km/s) | Q (kJ/g) | Brisance (TNT=100) | Gurney √(2E) (m/s) |
|---|---|---|---|---|---|---|
| CL-20 | 2.04 | 45.3 | 9.75 | 6.4 | 205.0 | 3100 |
| HMX | 1.905 | 36.7 | 8.95 | 5.69 | 166.0 | 2970 |
| RDX | 1.806 | 32.9 | 8.6 | 5.49 | 149.0 | 2930 |
| Comp B | 1.715 | 27.7 | 8.02 | 5.05 | 125.0 | 2700 |
| TNT | 1.654 | 22.1 | 7.25 | 4.3 | 100.0 | 2440 |
| PETN | 1.77 | 30.8 | 8.37 | 5.81 | 139.0 | 2930 |
| ANFO | 0.84 | 6.9 | 5.3 | 3.91 | 31.0 | 1800 |

## 18. TACS active acoustic cancellation depth (Nelson–Elliott bound)

Theoretical cancellation depth (dB) at the target zone as a function of source-control-source distance and frequency. Personal variant uses a 16-element ANC array, Mobile and Fixed use 64-element arrays. The A-weighted average row sums all six octave bands.

| Variant | 125 Hz | 250 Hz | 500 Hz | 1 kHz | 2 kHz | 4 kHz | A-weighted avg |
|---|---|---|---|---|---|---|---|
| Personal (3-5 m zone, 16-element wearable) | 40.0 | 40.0 | 40.0 | 39.1 | 32.1 | 25.1 | 36.3 |
| Mobile (8-15 m zone, 64-element vehicle) | 43.6 | 43.6 | 41.4 | 37.4 | 30.4 | 23.4 | 36.0 |
| Fixed (30-60 m zone, 64-element installation) | 43.6 | 41.4 | 37.4 | 33.4 | 26.4 | 19.4 | 32.4 |

## 19. Tank-track pad noise reduction (steel vs HNBR rubber)

At a 300 Hz drive frequency (typical track frequency at 30 km/h):

- Steel-on-steel transmissibility: **-22.3 dB**
- HNBR composite transmissibility: **-43.1 dB**
- **Net free-field SPL reduction: 20.8 dB**

Within the published 15–20 dB range for rubber track pads.

## 20. Combat-drug one-compartment PK (80 kg subject, oral)

| Drug | Dose | t_max | C_max | t½ | AUC |
|---|---|---|---|---|---|
| Caffeine 200 mg PO | 200.0 mg | 0.8 h | 4069.5 ng/mL | 5.0 h | 32652 ng·h/mL |
| Modafinil 200 mg PO | 200.0 mg | 2.24 h | 2113.1 ng/mL | 14.0 h | 47496 ng·h/mL |
| Dextroamphetamine 10 mg PO | 10.0 mg | 2.26 h | 21.4 ng/mL | 10.0 h | 359 ng·h/mL |
| Reference stimulant stack — caffeine 100 mg (HSX7 proxy) | 100.0 mg | 0.8 h | 2034.7 ng/mL | 5.0 h | 16326 ng·h/mL |
| Reference stimulant stack — modafinil 100 mg (HSX7 proxy) | 100.0 mg | 2.24 h | 1056.5 ng/mL | 14.0 h | 23748 ng·h/mL |

## 21. Injectable-nutrition osmolality

Safe peripheral-IV bound: `< 600 mOsm/kg`. Safe central-line bound: `< 1 800 mOsm/kg` (Plumb / Holliday-Segar).

| Formulation | Osmolality | Peripheral safe? | Central safe? |
|---|---|---|---|
| Injectable Food baseline (1 200 kcal/L) | 3037 mOsm/kg | NO | NO |
| Injectable Food field-ration (1 800 kcal/L) | 4436 mOsm/kg | NO | NO |
| Saline reference (0.9 %) | 308 mOsm/kg | YES | YES |
| Standard TPN reference | 2280 mOsm/kg | NO | NO |

## 22. TACT-1 ration shelf life (Q10 = 2 Arrhenius, 36-month baseline @ 25 °C)

| Temperature | Shelf life |
|---|---|
| 4 °C | 154.3 months |
| 25 °C | 36.0 months |
| 35 °C | 18.0 months |
| 49 °C | 6.8 months |
| 60 °C | 3.2 months |

## 23. Portfolio lifecycle — structural, parts life, reliability

### 23.0 Firearms and crew-served weapons

| Platform | Category | Felt recoil (ft·lb) | Barrel SF_yield | Bore life (rd) | MRBF analytic | MRBF simulated | FTF rate |
|---|---|---|---|---|---|---|---|
| MP-4.6P Guardian LE | firearm | 0.078 | 2.42 | 24,000 | 20,548 | 30,000 | 1:80,000 |
| MP-4.6M Pistol | firearm | 0.11 | 3.35 | 75,000 | 20,270 | 10,000 | 1:80,000 |
| MP-4.6M Defender PDW | firearm | 0.125 | 3.48 | 75,000 | 19,996 | 15,000 | 1:80,000 |
| MP-6.8 Mark II Rifle | firearm | 1.631 | 1.99 | 25,000 | 15,656 | 15,000 | 1:55,000 |
| MAS-15.2E Sniper | firearm | 39.717 | 2.11 | 1,500 | 35,613 | 30,000 | 1:120,000 |
| 57 mm Autocannon | crew_served | 3675.949 | 1.45 | 1,166 | 8,375 | 10,000 | 1:35,000 |
| 57 mm Underbarrel GL | firearm | 160.262 | 1.41 | 5,000 | 13,857 | 30,000 | 1:40,000 |
| 57 mm Mortar/RPG | crew_served | 227.281 | 1.84 | 8,000 | 11,041 | 15,000 | 1:25,000 |
| 140 mm Tank Gun | crew_served | 22915.411 | 2.23 | 618 | 3,502 | 3,750 | 1:8,000 |

#### 23.0.1 Firearm component parts-life

**MP-4.6P Guardian LE**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Barrel (416R + chrome + DLC ports) | 18,000 | 24,000 | Archard bore erosion |
| Recoil spring (17-7 PH) | 50,000 | 120,000 | Goodman infinite-life |
| Extractor hook (H13 + DLC) | 40,000 | 150,000 | Hook wear + spring preload |
| Magazine feed lips (440C laser-formed) | 25,000 | 80,000 | Lip spring-set |
| DLC sliding surfaces batch | 15,000 | 30,000 | Coating wear budget |

**MP-4.6M Pistol**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Barrel (416R + Stellite-21 throat) | 50,000 | 75,000 | Archard + Stellite erosion |
| Rotating bolt lugs (H13) | 35,000 | 50,000 | S-N fatigue SF>3 |
| Integral suppressor K-baffles (Inconel 718) | 18,000 | 25,000 | Blast-face erosion |
| Recoil spring (MP35N) | 10,000 | 15,000 | Goodman infinite-life |
| Extractor / ejector (S7 + DLC) | 18,000 | 25,000 | Hook + cam wear |

**MP-4.6M Defender PDW**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Barrel (416R + Stellite-21) | 50,000 | 75,000 | Archard + sustained-fire thermal |
| Buffered bolt-carrier (H13 + Ti countermass) | 14,000 | 20,000 | Carrier rail wear + buffer stack |
| Integral suppressor (180 cm³ Inconel) | 20,000 | 30,000 | Baffle erosion @ 850 rpm bound |
| Buffer spring stack (Elgiloy) | 20,000 | 30,000 | Compression set |
| Feed ramp / magazine well (7075-T6) | 18,000 | 25,000 | Peening + DLC wear |

**MP-6.8 Mark II Rifle**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Barrel (chrome + Stellite-21 throat) | 18,000 | 25,000 | Archard accuracy-retention |
| Gas piston / op-rod (Ni-Cr-Mo) | 35,000 | 80,000 | Wear + carbon fouling |
| Bolt carrier group (Carpenter 158) | 40,000 | 100,000 | Lug peening + cam path |
| Suppressor baffles (Inconel 718) | 12,000 | 22,000 | Blast-face erosion |
| Buffer spring (chrome-silicon) | 30,000 | 70,000 | Goodman infinite-life |

**MAS-15.2E Sniper**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Barrel (Stellite-21 lined, quick-change) | 1,000 | 1,500 | Throat erosion / sub-MOA bound |
| Integral suppressor (Inconel K-baffles) | 1,000 | 1,500 | Blast-face erosion |
| Bolt lugs (Carpenter 158) | 8,000 | 20,000 | Lug bearing fatigue |
| Firing pin spring (music wire) | 1,400 | 2,000 | Wahl fatigue |
| Magazine spring (17-7 PH) | 1,400 | 2,000 | Compression set |

**57 mm Autocannon**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Chrome-Stellite barrel liner | 800 | 1,166 | Throat erosion @ 257 MPa |
| Hydraulic recoil buffer seals | 5,000 | 10,000 | Seal extrusion + fluid loss |
| Dual-feed sprocket / link belt | 15,000 | 40,000 | Link fatigue + peening |
| Rotary breech cluster | 20,000 | 50,000 | Cam-track wear |
| Thermal sleeve / cooling jacket | 3,000 | 8,000 | 80 rpm sustained thermal bound |

**57 mm Underbarrel GL**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Chrome-lined launch tube | 3,500 | 5,000 | Low-pressure rifling wear |
| Break-action hinge pin (17-4 PH) | 2,000 | 6,000 | Bearing wear + lock-up |
| Leaf sight / quadrant mount | 4,000 | 10,000 | Vibration loosening |
| Firing pin / striker (H13) | 3,000 | 8,000 | Tip mushrooming |

**57 mm Mortar/RPG**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Chrome-lined tube (muzzle-loader) | 5,000 | 8,000 | Spalling + obturation ring wear |
| Baseplate / bipod pivot (7075-T6) | 3,000 | 10,000 | Fretting + soil impact |
| Trigger / firing pin (RPG mode) | 2,000 | 6,000 | Pin tip wear |
| Spiral-groove obturation ring | 1,500 | 4,000 | Gas-cut erosion |

**140 mm Tank Gun**

| Component | Warn @ rd | Replace @ rd | Model |
|---|---|---|---|
| Stellite-21 bore liner (chrome clad) | 500 | 700 | Throat erosion @ ETC pulse |
| Sliding-block breech (maraging steel) | 800 | 2,000 | Lug bearing + gas seal |
| Hydraulic recoil system (600 mm stroke) | 400 | 1,000 | Seal pack + fluid degradation |
| ETC plasma injector electrodes | 200 | 500 | Arc erosion per shot |
| Thermal sleeve / fume extractor | 600 | 1,500 | Erosion + carbon fouling |

### 23.1 Armour, sustainment, and systems platforms

| Platform | Category | Primary metric | Headline |
|---|---|---|---|
| APES Body Armour | armour | calendar_years | panel_service_life_yr=12; ceramic_tile_replacement_yr=5; soft_panel_refresh_yr=8; strike_face_dlc_recoat_yr=3 |
| APES-L Mark I Body Armour | armour | calendar_years | panel_service_life_yr=10; ceramic_tile_replacement_yr=4; soft_panel_refresh_yr=6 |
| NACS CBRN | systems | calendar_months | filter_cartridge_life_mo=6; suit_fabric_service_yr=5; valve_diaphragm_service_mo=12 |
| AlNiCyN Armour | armour | calendar_years | plate_service_life_yr=15; spall_liner_refresh_yr=7; areal_density_kg_m2=28 |
| ADF Tactical Field Kit | sustainment | calendar_years | load_carriage_fabric_yr=8; hydration_bladder_yr=2; IFAK_sterile_pack_mo=36 |
| Caseless Bullets (BPC) | sustainment | calendar_months | protein_case_shelf_mo=24; cook_off_safe_temp_C=93; humidity_storage_max_pct=60 |
| Combat Drug | sustainment | calendar_months | depot_shelf_cold_chain_mo=36; room_temp_hold_hr=72; autoinjector_shelf_mo=24 |
| HEL-CMS/DB | systems | operating_hours | diode_array_life_hr=10000; coolant_pump_service_hr=5000; beam_window_recoat_hr=2000 |
| HPR-X Rocketry | systems | flight_cycles | motor_case_life_flights=50; nozzle_insert_life_flights=30; avionics_battery_cycles=200 |
| Hearing Protection | systems | calendar_months | foam_plug_life_mo=6; electronic_muff_seal_mo=24; earplug_NRR_derated_dB=22 |
| Injectable Nutrition | sustainment | calendar_months | formulation_shelf_25C_mo=18; osmolality_limit_mOsm_kg=600; cold_chain_shelf_mo=30 |
| TACS Military Noise Cancellation | systems | calendar_years | wearable_array_service_yr=8; vehicle_array_service_yr=10; battery_cycle_life=500 |
| Rubber Tank Tracks | systems | distance_km | rubber_pad_life_km=8000; road_wheel_bearing_km=12000; net_noise_reduction_dB=20.8 |
| TACT-1 Mark II Ration | sustainment | calendar_months | shelf_life_25C_mo=36.0; shelf_life_49C_mo=6.8; shelf_life_4C_mo=154.3; shelf_life_35C_mo=18.0; shelf_life_60C_mo=3.2 |
| ASNP Sports Nutrition | sustainment | calendar_months | product_shelf_mo=24; opened_container_days=30 |
| CL-20 High Explosive | sustainment | calendar_months | cold_storage_shelf_mo=240; room_temp_hold_days=14; stabilizer_depletion_pct_yr=0.5 |

#### 23.1.1 Component service thresholds

**APES Body Armour**

| Component | Warn | Replace | Model |
|---|---|---|---|
| B4C dragon-scale tile array | 4 yr | 5 yr | Tile fracture + edge spall |
| 16-layer Kevlar/UHMWPE soft stack | 6 yr | 8 yr | UV + flex fatigue |
| Non-Newtonian shear-thickening pad | 3 yr | 5 yr | Polymer chain scission |
| Titanium strike-point inserts | 8 yr | 12 yr | Peening + DLC wear |

**APES-L Mark I Body Armour**

| Component | Warn | Replace | Model |
|---|---|---|---|
| 8 mm B4C tile (police panel) | 3 yr | 4 yr | Multi-hit spall |
| 10-layer soft stack (22 kg/m²) | 4 yr | 6 yr | Duty-cycle flex fatigue |
| Carrier mesh + MOLLE webbing | 2 yr | 4 yr | Abrasion + UV |

**NACS CBRN**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Activated-carbon / HEPA filter canister | 4 mo | 6 mo | Breakthrough time @ 5 mg/m³ |
| Butyl / PTFE laminate suit | 3 yr | 5 yr | Permeation + seam fatigue |
| Exhalation valve diaphragm | 8 mo | 12 mo | Elastomer set + tear |

**AlNiCyN Armour**

| Component | Warn | Replace | Model |
|---|---|---|---|
| AlNiCyN reaction-sintered tile | 10 yr | 15 yr | Micro-crack + moisture ingress |
| UHMWPE spall liner | 5 yr | 7 yr | Delamination |

**ADF Tactical Field Kit**

| Component | Warn | Replace | Model |
|---|---|---|---|
| 500D Cordura load carriage | 5 yr | 8 yr | Abrasion + UV |
| Hydration bladder (TPU) | 1 yr | 2 yr | Biofilm + seam leak |
| Sterile IFAK consumables | 24 mo | 36 mo | Sterility expiry |

**Caseless Bullets (BPC)**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Protein-cased round (BPC) | 18 mo | 24 mo | Protein denaturation + moisture |
| Nitrocellulose propellant wafer | 18 mo | 30 mo | Stabilizer depletion |

**Combat Drug**

| Component | Warn | Replace | Model |
|---|---|---|---|
| HSX7 depot ampoule (2–8 °C) | 30 mo | 36 mo | Peptide aggregation |
| Autoinjector mechanism | 18 mo | 24 mo | Spring + seal ageing |

**HEL-CMS/DB**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Fiber-coupled diode stack | 8,000 hr | 10,000 hr | Junction degradation @ 40 kW |
| Deionised coolant loop pump | 3,500 hr | 5,000 hr | Seal + bearing wear |
| Fused-silica output window (DLC) | 1,500 hr | 2,000 hr | Plasma pitting |

**HPR-X Rocketry**

| Component | Warn | Replace | Model |
|---|---|---|---|
| CFRP motor case (152 mm) | 35 flights | 50 flights | Pressure-cycle fatigue |
| Graphite nozzle insert | 20 flights | 30 flights | Ablation + throat growth |
| GPS / INS avionics battery | 150 cycles | 200 cycles | Li-ion capacity fade |

**Hearing Protection**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Slow-recovery foam earplug | 4 mo | 6 mo | Cell collapse + contamination |
| Electronic muff gel seal | 18 mo | 24 mo | Elastomer hardening |

**Injectable Nutrition**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Peripheral-safe isotonic bag | 12 mo | 18 mo | Lipid oxidation Q10 |
| Central-line hypertonic vial | 24 mo | 30 mo | Cold-chain integrity |

**TACS Military Noise Cancellation**

| Component | Warn | Replace | Model |
|---|---|---|---|
| 16-element wearable ANC array | 6 yr | 8 yr | MEMS mic drift + flex fatigue |
| Vehicle roof phased array | 7 yr | 10 yr | Vibration + connector corrosion |
| Li-poly wearable battery | 400 cycles | 500 cycles | Capacity fade @ 1C |

**Rubber Tank Tracks**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Segmented rubber road-wheel pad | 6,000 km | 8,000 km | Chunking + heat build-up |
| Road-wheel bearing cartridge | 9,000 km | 12,000 km | Roller fatigue + seal |
| Torsion bar bushing (elastomer) | 5,000 km | 7,500 km | Compression set |

**TACT-1 Mark II Ration**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Main meal retort pouch | 30 mo | 36 mo | Q10 lipid oxidation @ 25 °C |
| Electrolyte / snack bar | 24 mo | 30 mo | Moisture ingress |
| Flameless ration heater (Mg-Fe) | 48 mo | 60 mo | Mg powder oxidation |

**ASNP Sports Nutrition**

| Component | Warn | Replace | Model |
|---|---|---|---|
| Electrolyte powder sachet | 18 mo | 24 mo | Clumping + vitamin degradation |
| Protein / carb gel pouch | 12 mo | 18 mo | Maillard browning |

**CL-20 High Explosive**

| Component | Warn | Replace | Model |
|---|---|---|---|
| CL-20 pressed pellet lot | 180 mo | 240 mo | Stabilizer @ −18 °C |
| PBX binder batch | 120 mo | 180 mo | HMX / binder phase separation |

### 23.2 Scope-only platforms (no physics lifecycle)

- **Military Command Doctrine** — Doctrinal force-structure and training-duration targets — no physics lifecycle model.
- **OBSIDIAN Body Armour** — Hypothetical carbyne / STF suit — no runnable ballistic lifecycle model.
- **OBSIDIAN-X Body Armour** — Full-body hypothetical armour — no runnable lifecycle model.
- **TAIPAN-1 Missile** — Flight dynamics validated by taipan1_sim.py — no portfolio §23 lifecycle slice.


---

_Tier-1 methodology: Le Duc / Powley closed-form internal ballistics, G7 / G1 drag-table point-mass external integration with ICAO atmosphere, De Marre and Lanz–Odermatt terminal-ballistics correlations against 290 BHN RHA._

_Tier-2 methodology: Westin (1975) muzzle-blast SPL fit; Didion / Bagnold wind-drift; bisection-zeroed drop integration; Hatcher max-effective-range with 80 J KE threshold; calibrated bore-wear and barrel-thermal models against M4 / M14 / M2HB / GAU-8 / M256 anchors; Tate / Krupp obliquity correction; Lambert-Jonas / Recht-Ipson V50 with composite-factor calibration; clay-witness BFD; Gurney cylindrical-charge velocity, Mott fragment distribution, Carlton lethal-area; Birkhoff steady-state jet shaped-charge; Tsiolkovsky-plus-drag rocketry; Kamlet-Jacobs (1968) detonation physics; Nelson-Elliott (1992) ANC cancellation bound; 1-DOF mass-spring-damper for track-pad vibration; one-compartment oral PK; Plumb / Holliday-Segar osmolality; Q10 = 2 Arrhenius lipid oxidation. See `weapons_simulation.py` for implementation._