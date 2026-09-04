#!/usr/bin/env python3
"""Repair relative Markdown links that no longer resolve.

Most breakage is one of three mechanical faults:

  depth      a file two directories deep links with a single `../`
  renamed    the target gained or lost a suffix, or became a directory
  relocated  the target moved out of this repository entirely

Each candidate repair is applied only if it actually resolves on disk. A link
that cannot be resolved is left exactly as it is and reported, so nothing is
silently pointed somewhere plausible but wrong.
"""
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path('.').resolve()
LINK = re.compile(r'(\[[^\]]*\]\()\s*([^)]+?)\s*((?:"[^"]*")?\s*\))')

# Folders that left this repository and now have their own. Verified against
# the published site, which links each as a separate product.
RELOCATED = {
    'Cypha': 'https://github.com/odin-loki/cypha',
    'Cell AI': 'https://github.com/odin-loki/cellai',
}
# Renames inside the repo that the links never caught up with.
RENAMED = {
    'Break AES': 'Modelling AES/Break AES with NNs',
    'LICENSE': 'modified-license.md',
}
# Targets whose basename changed. Each right-hand side was confirmed to exist
# before being added; nothing here is a guess at where something "probably" went.
ALIAS = {
    'APES-L Mark I Police Body Armour.md': 'APES-L Mark I',
    'Research Paper - MP-4.6P Guardian LE.md':
        'MP-4.6P Guardian LE/MP-4.6P_Guardian_LE_Research_Paper.md',
    'ORCA_System_Specification_v1.md': 'ORCA_System_Specification.md',
    'CL-20 HE Readme.md': 'README.md',
}

index = {}
for q in ROOT.rglob('*'):
    if '.git' in q.parts:
        continue
    index.setdefault(q.name, []).append(q)


def resolve(src: pathlib.Path, href: str):
    """Return a replacement href, or None if the link is already fine or unfixable."""
    raw = urllib.parse.unquote(href)
    if (src.parent / raw).resolve().exists():
        return None                                   # nothing wrong

    bare = raw.lstrip('./').rstrip('/')
    head = bare.split('/')[0]
    if head in RELOCATED:                             # left the repository
        return RELOCATED[head]
    if head in RENAMED:
        cand = ROOT / RENAMED[head] / '/'.join(bare.split('/')[1:])
        if cand.exists():
            return quote_rel(src, cand)

    # Basename aliases, resolved against the link's own directory prefix.
    parts = raw.rstrip('/').split('/')
    if parts[-1] in ALIAS:
        alt = '/'.join(parts[:-1] + [ALIAS[parts[-1]]])
        for up in range(0, 5):
            cand = (src.parent / ('../' * up) / alt.lstrip('./')).resolve()
            if cand.exists():
                return quote_rel(src, cand)

    tail = raw.lstrip('./').lstrip('/')
    # Wrong number of `../` steps - the commonest fault by far.
    for up in range(0, 5):
        cand = (src.parent / ('../' * up) / tail).resolve()
        if cand.exists() and ROOT in cand.parents or cand == ROOT:
            return quote_rel(src, cand)
    # Target became a directory, or lost/gained a suffix.
    name = pathlib.PurePosixPath(raw.rstrip('/')).name
    for alt in (name, name.removesuffix('.md'), name.removesuffix('.json') + '.md'):
        hits = [h for h in index.get(alt, []) if 'docs/site' not in h.as_posix()]
        if len(hits) == 1:
            return quote_rel(src, hits[0])
    return None


def quote_rel(src: pathlib.Path, target: pathlib.Path) -> str:
    import os
    rel = os.path.relpath(target, src.parent)
    return urllib.parse.quote(rel.replace('\\', '/'))


dry = '--apply' not in sys.argv
fixed = unfixed = 0
for p in sorted(ROOT.rglob('*.md')):
    if '.git' in p.parts or 'docs/site' in p.as_posix():
        continue
    text = p.read_text(encoding='utf-8')
    blank = lambda m: '\x00' * len(m.group(0))
    body = re.sub(r'```.*?```', blank, text, flags=re.S)
    body = re.sub(r'`[^`\n]*`', blank, body)
    out, last, changed = [], 0, False
    for m in LINK.finditer(body):
        href = m.group(2)
        if not href or href.startswith(('http', 'mailto:', '#')):
            continue
        target = href.split('#')[0]
        anchor = href[len(target):]
        new = resolve(p, target)
        if new is None:
            if not (p.parent / urllib.parse.unquote(target)).resolve().exists():
                unfixed += 1
                print(f'  UNFIXED  {p}  ->  {href}')
            continue
        out.append(text[last:m.start(2)]); out.append(new + anchor)
        last = m.end(2); changed = True; fixed += 1
    if changed and not dry:
        out.append(text[last:])
        p.write_text(''.join(out), encoding='utf-8')

print(f'\n{"would fix" if dry else "fixed"}: {fixed}   unfixable: {unfixed}')
