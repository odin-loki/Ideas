"""
Batch-update per-platform README.md and SIM_README.md with §23 lifecycle headlines.
Run from Weapons-Defence/:  python update_lifecycle_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
DEFENCE = ROOT / "Weapons-Defence"
sys.path.insert(0, str(DEFENCE))

import weapon_lifecycle as wl  # noqa: E402
from weapon_lifecycle_configs import PLATFORM_ID_TO_LIFECYCLE  # noqa: E402

# platform_id → folder relative to repo root
PLATFORM_FOLDERS: Dict[str, str] = {
    "mp46m_guardian_pistol": "Weapons-Defence/MP-4.6M Guardian Pistol",
    "mp46p_guardian_le": "Weapons-Police/MP-4.6P Guardian LE",
    "mp46m_defender_pdw": "Weapons-Defence/MP-4.6M Defender PDW",
    "mp68_mark_ii_rifle": "Weapons-Defence/MP-6.8 Mark II Rifle",
    "mas152e_sniper": "Weapons-Defence/MAS-15.2E Anti-Materiel Sniper",
    "57mm_autocannon": "Weapons-Defence/57mm Autocannon",
    "57mm_underbarrel_grenade": "Weapons-Defence/57mm Underbarrel Grenade",
    "57mm_mortar_rpg": "Weapons-Defence/57mm Mortar RPG",
    "140mm_tank_ke": "Weapons-Defence/140mm Tank KE Round",
    "apes_body_armour": "Weapons-Defence/APES Body Armour",
    "apes_l_body_armour": "Weapons-Police/APES-L Mark I",
    "nacs_cbrn": "Weapons-Defence/NACS CBRN",
    "alnicyn_armour": "Weapons-Defence/AlNiCyN Armour",
    "adf_tactical_field_kit": "Weapons-Defence/ADF Tactical Field Kit",
    "caseless_bullets": "Weapons-Defence/Caseless Bullets",
    "combat_drug": "Weapons-Defence/Combat Drug",
    "hel_cms_db": "Weapons-Defence/HEL_CMS_DB Laser AntiAir",
    "hprx_rocketry": "Weapons-Defence/HPR-X Rocketry",
    "hearing_protection": "Weapons-Defence/Hearing Protection",
    "injectable_nutrition": "Weapons-Defence/Injectable Nutrition",
    "military_command_doctrine": "Weapons-Defence/Military Command Doctrine",
    "military_noise_cancellation": "Weapons-Defence/Military Noise Cancellation",
    "obsidian_body_armour": "Weapons-Defence/OBSIDIAN Body Armour",
    "obsidian_x_body_armour": "Weapons-Defence/OBSIDIAN-X Body Armour",
    "rubber_tank_tracks": "Weapons-Defence/Rubber Tank Tracks",
    "tact1_ration": "Weapons-Defence/TACT-1 Tactical Ration",
    "asnp_sports_nutrition": "Weapons-Defence/TACT-1 Tactical Ration/ASNP Sports Nutrition",
    "taipan_missile": "Weapons-Defence/TAIPAN Missile",
    "cl20_high_explosive": "Weapons-Defence/CL-20 High Explosive",
}

LIFECYCLE_ROW_PREFIXES = (
    "MRBF analytic",
    "MRBF simulated",
    "Felt recoil",
    "Bore life service",
    "Barrel SF_yield",
    "FTF rate",
    "Spring fatigue SF",
    "Panel service life",
    "Ceramic tile replacement",
    "Soft panel refresh",
    "Filter cartridge life",
    "Plate service life",
    "Shelf life @ 25",
    "Motor case life",
    "Rubber pad life",
    "Diode array life",
    "Foam plug life",
    "Depot shelf",
    "Protein case shelf",
    "Wearable array service",
    "Scope note",
    "Certified storage",
    "Cold storage shelf",
    "Product shelf",
    "Net noise reduction",
    "Coolant pump service",
    "Nozzle insert life",
    "Electronic muff seal",
    "Battery cycle life",
    "Lifecycle note",
    "Lifecycle (§23)",
    "Certified storage",
)


def _fmt_num(n: float, decimals: int = 0) -> str:
    if decimals == 0:
        return f"{int(round(n)):,}"
    return f"{n:,.{decimals}f}"


def firearm_headline_rows(lc: Dict) -> List[Tuple[str, str]]:
    rel = lc["reliability"]
    parts = lc["parts_life"]
    rec = lc["recoil"]
    struct = lc["structural"]
    rows = [
        ("Bore life service (§23)", f"**{_fmt_num(parts['bore_life_rounds'])} rounds**"),
        ("MRBF analytic (§23)", f"**~{_fmt_num(rel['mrbf_analytic'])} rounds**"),
        ("MRBF simulated (§23)", f"**~{_fmt_num(rel['mrbf_simulated'])} rounds**"),
        ("Felt recoil (§23)", f"**~{rec['felt_recoil_ftlbf']:.3f} ft·lb**"),
        ("Barrel SF_yield (§23)", f"**{struct['barrel_sf_yield']}**"),
        ("FTF rate (§23)", f"**1:{_fmt_num(rel['ftf_rate'])}**"),
    ]
    if struct.get("spring_fatigue_sf") is not None:
        rows.insert(4, ("Spring fatigue SF (§23)", f"**{struct['spring_fatigue_sf']}**"))
    return rows


def generic_headline_rows(lc: Dict) -> List[Tuple[str, str]]:
    cat = lc.get("category", "")
    if cat == "scope":
        note = lc.get("scope_note", "Scope-only — no physics lifecycle model.")
        headline = lc.get("headline", {})
        rows: List[Tuple[str, str]] = []
        if "certified_storage_yr" in headline:
            rows.append(
                ("Certified storage (§23)", f"**{headline['certified_storage_yr']} yr**")
            )
        if not rows:
            rows.append(("Lifecycle (§23)", f"*{note}*"))
        else:
            rows.append(("Lifecycle note (§23)", f"*{note}*"))
        return rows

    headline = lc.get("headline", {})
    label_map = {
        "panel_service_life_yr": "Panel service life (§23)",
        "ceramic_tile_replacement_yr": "Ceramic tile replacement (§23)",
        "soft_panel_refresh_yr": "Soft panel refresh (§23)",
        "filter_cartridge_life_mo": "Filter cartridge life (§23)",
        "plate_service_life_yr": "Plate service life (§23)",
        "shelf_life_25C_mo": "Shelf life @ 25 °C (§23)",
        "motor_case_life_flights": "Motor case life (§23)",
        "nozzle_insert_life_flights": "Nozzle insert life (§23)",
        "rubber_pad_life_km": "Rubber pad life (§23)",
        "diode_array_life_hr": "Diode array life (§23)",
        "coolant_pump_service_hr": "Coolant pump service (§23)",
        "foam_plug_life_mo": "Foam plug life (§23)",
        "electronic_muff_seal_mo": "Electronic muff seal (§23)",
        "wearable_array_service_yr": "Wearable array service (§23)",
        "battery_cycle_life": "Battery cycle life (§23)",
        "certified_storage_yr": "Certified storage (§23)",
        "depot_shelf_cold_chain_mo": "Depot shelf cold-chain (§23)",
        "protein_case_shelf_mo": "Protein case shelf (§23)",
        "cold_storage_shelf_mo": "Cold storage shelf (§23)",
        "product_shelf_mo": "Product shelf (§23)",
        "net_noise_reduction_dB": "Net noise reduction (§23)",
        "formulation_shelf_25C_mo": "Formulation shelf @ 25 °C (§23)",
        "load_carriage_fabric_yr": "Load carriage fabric (§23)",
    }
    rows = []
    limit = 2 if cat == "systems" else 6
    for key, label in label_map.items():
        if key in headline:
            v = headline[key]
            unit = ""
            if "flights" in key:
                unit = " flights"
            elif "cycle" in key:
                unit = " cycles"
            elif "yr" in key:
                unit = " yr"
            elif "mo" in key:
                unit = " mo"
            elif "km" in key:
                unit = " km"
            elif "hr" in key:
                unit = " hr"
            elif "dB" in key:
                unit = " dB"
            if isinstance(v, float) and v == int(v):
                rows.append((label, f"**{_fmt_num(int(v))}{unit}**"))
            elif isinstance(v, int):
                rows.append((label, f"**{_fmt_num(v)}{unit}**"))
            else:
                rows.append((label, f"**{v}{unit}**"))
            if len(rows) >= limit:
                break
    if not rows:
        for k, v in list(headline.items())[:4]:
            rows.append((k.replace("_", " ").title() + " (§23)", f"**{v}**"))
    return rows[:limit]


def sim_readme_lifecycle_row(lc: Dict, lc_name: str) -> Tuple[str, str]:
    cat = lc.get("category", "")
    if cat in ("firearm", "crew_served"):
        rel = lc["reliability"]
        parts = lc["parts_life"]
        rec = lc["recoil"]
        struct = lc["structural"]
        return (
            "**§23 Lifecycle**",
            f"`{lc_name}` — bore life {_fmt_num(parts['bore_life_rounds'])} rd, "
            f"MRBF {_fmt_num(rel['mrbf_analytic'])} analytic / "
            f"{_fmt_num(rel['mrbf_simulated'])} simulated, "
            f"felt recoil {rec['felt_recoil_ftlbf']:.2f} ft·lb, "
            f"barrel SF {struct['barrel_sf_yield']}, "
            f"FTF 1:{_fmt_num(rel['ftf_rate'])}",
        )
    if cat == "scope":
        note = lc.get("scope_note", "Scope-only platform.")
        headline = lc.get("headline", {})
        if headline:
            summary = "; ".join(f"{k}={v}" for k, v in list(headline.items())[:2])
            return ("**§23 Lifecycle**", f"`{lc_name}` — {summary}; {note}")
        return ("**§23 Lifecycle**", note)
    headline = lc.get("headline", {})
    summary = "; ".join(f"{k}={v}" for k, v in list(headline.items())[:3])
    return ("**§23 Lifecycle**", f"`{lc_name}` — {summary or 'service-life model'}")


def _is_lifecycle_row(line: str) -> bool:
    if not line.startswith("|") or line.count("|") < 3:
        return False
    inner = line.split("|")[1].strip()
    return any(inner.startswith(p) for p in LIFECYCLE_ROW_PREFIXES) or "(§23)" in inner


def strip_all_lifecycle_rows(content: str) -> str:
    """Remove §23 lifecycle rows from any table (including misplaced threat tables)."""
    return "\n".join(
        line for line in content.splitlines() if not _is_lifecycle_row(line)
    )


def strip_s23_subsection(content: str) -> str:
    """Remove an existing ### Portfolio §23 block so re-runs are idempotent."""
    lines = content.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("### Portfolio §23"):
            i += 1
            while i < len(lines) and not (
                lines[i].startswith("## ") or lines[i].startswith("### ")
            ):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def lifecycle_path_prefix(is_police: bool) -> str:
    return "../../Weapons-Defence/" if is_police else "../"


def fix_sim_lifecycle_paths(content: str, prefix: str) -> str:
    """Normalize weapon_lifecycle.py / weapons_sim_results.md links to the correct relative prefix."""
    content = content.replace("mp46_lifecycle.py", f"{prefix}weapon_lifecycle.py")
    for wrong in ("../", "../../Weapons-Defence/"):
        if wrong == prefix:
            continue
        content = content.replace(
            f"[`{wrong}weapon_lifecycle.py`]({wrong}weapon_lifecycle.py)",
            f"[`{prefix}weapon_lifecycle.py`]({prefix}weapon_lifecycle.py)",
        )
        content = content.replace(
            f"[`{wrong}weapons_sim_results.md`]({wrong}weapons_sim_results.md)",
            f"[`{prefix}weapons_sim_results.md`]({prefix}weapons_sim_results.md)",
        )
    return content


def _s23_subsection_block(rows: List[Tuple[str, str]], prefix: str = "../") -> List[str]:
    block = [
        "",
        "### Portfolio §23 — service intervals",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    block.extend(f"| {k} | {v} |" for k, v in rows)
    block.extend(
        [
            "",
            f"Source: [`{prefix}weapon_lifecycle.py`]({prefix}weapon_lifecycle.py) / "
            f"[`{prefix}weapons_sim_results.md`]({prefix}weapons_sim_results.md) §23.",
        ]
    )
    return block


def upsert_readme_table(content: str, rows: List[Tuple[str, str]]) -> str:
    """Insert or replace §23 rows in the first 2-column headline metrics table."""
    content = strip_all_lifecycle_rows(content)
    content = strip_s23_subsection(content)
    lines = content.splitlines()

    table_start: Optional[int] = None
    table_end: Optional[int] = None
    headline_end: Optional[int] = None
    section_start: Optional[int] = None
    for i, line in enumerate(lines):
        if re.match(
            r"^## .*(Headline numbers|headline numbers|Headline performance|Headline structure)",
            line,
            re.I,
        ):
            section_start = i
            headline_end = i
            for j in range(i + 1, min(i + 80, len(lines))):
                if lines[j].startswith("## ") and j > i + 1:
                    headline_end = j
                    break
                if (
                    lines[j].startswith("| Metric |")
                    and lines[j].count("|") == 3
                    and "APE-1" not in lines[j]
                    and section_start is not None
                    and (j - section_start) <= 15
                ):
                    table_start = j
                elif table_start is not None and lines[j].startswith("|") and "---" in lines[j]:
                    continue
                elif table_start is not None and lines[j].startswith("|"):
                    table_end = j
                elif table_start is not None and not lines[j].startswith("|"):
                    break
            break

    lifecycle_md = [f"| {k} | {v} |" for k, v in rows]

    if table_start is not None:
        body_start = table_start + 1
        while body_start < len(lines) and "---" in lines[body_start]:
            body_start += 1
        new_body: List[str] = []
        i = body_start
        while i < len(lines) and lines[i].startswith("|"):
            if not _is_lifecycle_row(lines[i]):
                new_body.append(lines[i])
            i += 1
        table_end = i
        updated = lines[:body_start] + new_body + lifecycle_md + lines[table_end:]
        return "\n".join(updated)

    if headline_end is not None and rows:
        insert_at = headline_end
        block = _s23_subsection_block(rows, prefix="../")
        return "\n".join(lines[:insert_at] + block + [""] + lines[insert_at:])

    return content


def strip_s23_sim_sections(content: str) -> str:
    """Remove duplicate ## §23 Lifecycle blocks from SIM_README."""
    lines = content.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "## §23 Lifecycle":
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def _s23_sim_block(
    section_row: Tuple[str, str], lc_name: str, prefix: str = "../"
) -> List[str]:
    return [
        "",
        "## §23 Lifecycle",
        "",
        f"Portfolio lifecycle for **`{lc_name}`** — "
        f"[`{prefix}weapon_lifecycle.py`]({prefix}weapon_lifecycle.py) / "
        f"[`{prefix}weapons_sim_results.md`]({prefix}weapons_sim_results.md) §23.",
        "",
        "| Item | Detail |",
        "|---|---|",
        f"| {section_row[0]} | {section_row[1]} |",
        "",
        f"| Lifecycle results | [`{prefix}weapons_sim_results.md`]({prefix}weapons_sim_results.md) §23 |",
        f"| Lifecycle simulator | [`{prefix}weapon_lifecycle.py`]({prefix}weapon_lifecycle.py) |",
    ]


def _update_inline_s23_table_row(
    lines: List[str], section_row: Tuple[str, str]
) -> None:
    """Update inline §23 row in Relevant / Result tables sections."""
    for i, line in enumerate(lines):
        lower = line.lower()
        if "relevant tables" in lower or "result tables" in lower:
            for j in range(i + 1, min(i + 40, len(lines))):
                if lines[j].startswith("| **§23"):
                    lines[j] = f"| {section_row[0]} | {section_row[1]} |"
                    return
                if lines[j].startswith("---") and j > i + 3:
                    break


def upsert_sim_readme(
    content: str,
    section_row: Tuple[str, str],
    lc_name: str,
    *,
    prefix: str = "../",
    append_footer: bool = True,
) -> str:
    text = fix_sim_lifecycle_paths(content, prefix)
    text = strip_s23_sim_sections(text)
    lines = text.splitlines()

    _update_inline_s23_table_row(lines, section_row)

    if not append_footer:
        return "\n".join(lines).rstrip() + "\n"

    block = _s23_sim_block(section_row, lc_name, prefix)

    # Insert before final Companion documents or footer back-link
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("## Companion documents"):
            return "\n".join(lines[:i] + block + [""] + lines[i:])
        if lines[i].startswith("---"):
            rest = "\n".join(lines[i + 1 : min(i + 4, len(lines))])
            if "Back to" in rest or "simulation coverage" in rest.lower():
                return "\n".join(lines[:i] + block + [""] + lines[i:])

    # Before italic footer line
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("*") and "simulation coverage" in lines[i].lower():
            return "\n".join(lines[:i] + block + [""] + lines[i:])

    return "\n".join(lines + block)


def fix_lifecycle_refs(content: str, is_police: bool) -> str:
    content = content.replace("mp46_lifecycle.py", "weapon_lifecycle.py")
    if is_police:
        content = content.replace(
            "Phases 4–7 + parts-life module",
            "§23 portfolio lifecycle (weapon_lifecycle.py)",
        )
    return content


def process_platform(platform_id: str, lc_data: Dict) -> List[str]:
    folder = ROOT / PLATFORM_FOLDERS[platform_id]
    lc_name = PLATFORM_ID_TO_LIFECYCLE[platform_id]
    lc = lc_data[lc_name]
    is_police = "Weapons-Police" in PLATFORM_FOLDERS[platform_id]
    cat = lc.get("category", "")
    rows = firearm_headline_rows(lc) if cat in ("firearm", "crew_served") else generic_headline_rows(lc)
    sim_row = sim_readme_lifecycle_row(lc, lc_name)
    changed: List[str] = []

    readme = folder / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        text = fix_lifecycle_refs(text, is_police)
        text = upsert_readme_table(text, rows)
        # Ensure §23 cited in headline intro
        if "§23" not in text.split("##")[0] and cat in ("firearm", "crew_served"):
            pass  # optional tagline update skipped
        readme.write_text(text, encoding="utf-8")
        changed.append(str(readme.relative_to(ROOT)))

    sim = folder / "SIM_README.md"
    if sim.exists():
        prefix = lifecycle_path_prefix(is_police)
        text = sim.read_text(encoding="utf-8")
        text = upsert_sim_readme(
            text,
            sim_row,
            lc_name,
            prefix=prefix,
            append_footer=not is_police,
        )
        sim.write_text(text, encoding="utf-8")
        changed.append(str(sim.relative_to(ROOT)))

    return changed


def main() -> int:
    print("Loading lifecycle data…")
    lc_data = wl.run_all()
    all_changed: List[str] = []
    for platform_id in PLATFORM_FOLDERS:
        try:
            changed = process_platform(platform_id, lc_data)
            all_changed.extend(changed)
            print(f"  OK {platform_id}: {len(changed)} files")
        except Exception as exc:
            print(f"  FAIL {platform_id}: {exc}")
    print(f"\nUpdated {len(all_changed)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
