#!/usr/bin/env python3
"""Report relative Markdown links that do not resolve.

Run from the repository root:  python3 tools/check_links.py

Exits non-zero when anything is broken, so it can gate a commit. Fenced code
is skipped so SMILES strings and array indexing are not mistaken for links,
and unencoded spaces inside (...) are handled - Markdown permits them.
"""
import pathlib, re, urllib.parse, sys, collections
# Markdown allows unencoded spaces inside (...) so match to the closing paren,
# then strip any title. Skip fenced code so SMILES strings aren't read as links.
LINK = re.compile(r'\[[^\]]*\]\(\s*([^)]+?)\s*(?:"[^"]*")?\s*\)')
broken = collections.Counter(); total = 0
for p in sorted(pathlib.Path('.').rglob('*.md')):
    if '.git' in p.parts: continue
    t = p.read_text(encoding='utf-8', errors='replace')
    t = re.sub(r'```.*?```', '', t, flags=re.S)
    for m in LINK.finditer(t):
        h = m.group(1).split('#')[0].strip()
        if not h or h.startswith(('http', 'mailto:', '#')): continue
        total += 1
        if not (p.parent / urllib.parse.unquote(h)).resolve().exists():
            broken[f'{p} -> {h}'] += 1
print(f'{sum(broken.values())} broken of {total} relative links')
for k in list(broken)[:12]: print('   ', k)

raise SystemExit(1 if sum(broken.values()) else 0)
