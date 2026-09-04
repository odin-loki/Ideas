#!/usr/bin/env python3
"""Remove DOCX-import backslash noise from the Markdown papers.

The Word-to-Markdown pass that produced most of these documents escaped
every parenthesis, bracket, brace, underscore and plus sign it met, so
`GF(2)[x]` reads as `GF\\(2\\)\\[x\\]` in the source. Markdown renders it
correctly, which is why it survived, but it makes the raw text painful to
read, breaks grep, and breaks copy-paste of the code and formulae.

Scope is deliberately narrow:

  * Files carrying real LaTeX are skipped entirely. `ORCA_Research_Paper.md`
    uses `\\( ... \\)` as inline-math delimiters, so unescaping there would
    destroy the mathematics rather than clean it.
  * Only escapes with no Markdown meaning in their position are removed.
    `\\*`, `\\|`, `\\<`, `\\>`, `\\#`, `\\!` and `\\\\` are left alone -
    emphasis, table cells, blockquotes, headings, images and literal
    backslashes all depend on them.
  * Every file is checked afterwards: the visible text must be unchanged,
    and no new Markdown link or list marker may have appeared. A file that
    fails either check keeps its brackets escaped.
"""
import pathlib
import re

LATEX = re.compile(r'\$\$|\\frac|\\mathrm|\\text\{|\\begin\{|\\left|\\sqrt|\\sum|\\alpha|\\Delta')
LINKISH = re.compile(r'\]\(')
LIST_MARKER = re.compile(r'^\s*([-+*]|\d+\.)\s', re.M)


def unescape(text: str) -> str:
    out = text
    # 1. Parentheses and braces: never Markdown syntax, so the escape is
    #    always pure noise.
    out = out.replace(r'\(', '(').replace(r'\)', ')')
    out = out.replace(r'\{', '{').replace(r'\}', '}')
    # 2. Underscores only inside words - l2\_horner, not \_emphasis\_.
    out = re.sub(r'(?<=[A-Za-z0-9])\\_(?=[A-Za-z0-9])', '_', out)
    # 3. Plus, minus and full stop only away from the start of a line, where
    #    they would otherwise become list markers.
    out = re.sub(r'(?<=\S)\\\+', '+', out)
    out = re.sub(r'(?<=\S)\\-', '-', out)
    out = re.sub(r'(?<=\S)\\\.', '.', out)
    # 4. Brackets last, so the caller can back this step out on its own.
    out = out.replace(r'\[', '[').replace(r'\]', ']')
    return out


def visible(text: str) -> str:
    """What a reader sees: backslash-escapes collapse to their character."""
    return re.sub(r'\\([^\\A-Za-z0-9])', r'\1', text)


changed = removed = skipped_latex = reverted = 0
for p in sorted(pathlib.Path('.').rglob('*.md')):
    if '.git' in p.parts:
        continue
    src = p.read_text(encoding='utf-8')
    if LATEX.search(src):
        if re.search(r'\\[()_\[\]{}+]', src):
            skipped_latex += 1
        continue

    out = unescape(src)
    if out == src:
        continue

    # Brackets are the one risky step: [x](y) is a link, \[x\](y) is not.
    if LINKISH.findall(out) != LINKISH.findall(src) or \
       len(LIST_MARKER.findall(out)) != len(LIST_MARKER.findall(src)):
        no_brackets = unescape(src.replace(r'\[', '\x00').replace(r'\]', '\x01'))
        out = no_brackets.replace('\x00', r'\[').replace('\x01', r'\]')
        reverted += 1

    assert visible(out) == visible(src), f'{p}: visible text changed'
    n = src.count('\\') - out.count('\\')
    p.write_text(out, encoding='utf-8')
    changed += 1
    removed += n

print(f'{removed} escapes removed from {changed} files')
print(f'{skipped_latex} LaTeX-bearing files skipped, {reverted} kept their brackets escaped')
