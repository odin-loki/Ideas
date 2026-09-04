#!/usr/bin/env python3
"""Repair CP1252 bytes stranded inside otherwise-UTF-8 Markdown.

Five source documents are not valid UTF-8: a Windows editor wrote single
CP1252 bytes into files that are UTF-8 everywhere else, so GitHub renders
them as replacement characters. Each stray byte is mapped back to the
character it stood for and re-encoded.

Two bytes are mapped by context rather than by the CP1252 table, because
the table's answer is wrong here:

  0x98  CP1252 says small-tilde. Every one of the 78 occurrences sits in
        "activation energy _ 10 kJ/mol", "n* _ 836", "calibrated at
        _ 700 mm RHA" - it is an approximation sign.
  0x9d  Undefined in CP1252. All 313 occurrences are the vertical edges
        of ASCII box diagrams inside fenced code blocks whose corners are
        drawn with "+-", so the character is a plain pipe.

Characters that were already collapsed to "?" before these files were
saved (Greek letters, superscript minus, x-double-dot) are NOT guessed
at - a "?" is indistinguishable from a real question mark.
"""
import pathlib

FILES = [
    'AUDIT_README_VS_SOURCE.md',
    'Weapons-Defence/Common Architecture and Components.md',
    'Weapons-Defence/NACS CBRN/NACS_Specification.md',
    'Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Specification.md',
    'Weapons-Police/MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Research_Paper.md',
]

MAP = {
    0x85: '…', 0x96: '–', 0x97: '—',
    0x98: '≈',   # context, not CP1252's small tilde
    0x99: '™',
    0x9d: '|',   # context: box-diagram vertical, undefined in CP1252
    0xa7: '§', 0xa8: '¨', 0xb0: '°', 0xb1: '±', 0xb2: '²', 0xb3: '³',
    0xb5: 'µ', 0xb7: '·', 0xb9: '¹', 0xd7: '×',
    0xe7: 'ç', 0xe9: 'é', 0xff: 'ÿ',
}


def repair(raw: bytes) -> tuple[str, int]:
    out, i, n = [], 0, 0
    while i < len(raw):
        b = raw[i]
        if b < 0x80:
            out.append(chr(b)); i += 1; continue
        for ln in (2, 3, 4):                      # already-valid UTF-8 stays
            try:
                out.append(raw[i:i + ln].decode('utf-8')); i += ln; break
            except UnicodeDecodeError:
                continue
        else:
            if b not in MAP:
                raise SystemExit(f'unmapped stray byte 0x{b:02x} at offset {i}')
            out.append(MAP[b]); i += 1; n += 1
    return ''.join(out), n


total = 0
for f in FILES:
    p = pathlib.Path(f)
    text, n = repair(p.read_bytes())
    p.write_text(text, encoding='utf-8')
    print(f'  {n:5d} bytes repaired  {f}')
    total += n
print(f'{total} stray bytes repaired across {len(FILES)} files')
