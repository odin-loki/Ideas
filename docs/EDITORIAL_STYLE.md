# House style for the Ideas library

These rules apply to **Markdown** in this repository and to how the **GitHub Pages** builder (`tools/build_github_pages.py`) interprets content.

## Titles and headings

- One **document title** in the first lines: either a single `# Title` or a plain first line (the site infers a title).
- Use **ATX headings** (`#` … `###`). Avoid skipping levels (`#` then `###`) unless the middle level is unused on purpose.
- Do not use `##` for **table cell values** (e.g. energies like `15.2 J`)—use bold or table cells instead.
- Numbered sections: prefer `## 2. Related work` style consistently within a file.

## Mathematics

- Inline: `\( a^2 + b^2 \)` or `$a^2 + b^2$` (pick one convention per file; the site runs **KaTeX** on `\(...\)`, `\[...\]`, and `$$...$$`).
- Display: `\[ \sum_{i=1}^n x_i \]` or `$$ ... $$`.
- Never split formulas with Markdown italics (`*...*`) in the middle of `O(N^2)`-style expressions—use proper delimiters (see fixes in `UHPM_Research_Paper.md`).
- Unicode superscripts are fine when unambiguous (e.g. `x¹⁰` in field polynomials).

## Emphasis

- Prefer `**bold**` for strong emphasis in body text.
- `__underline__` in Markdown renders as bold, not underline—avoid using it for “title lines” except briefly; prefer `#` / `##` or `**`.

## Tables

- Use **GitHub-flavored pipe tables** when data is tabular.
- Avoid “fake tables” built from stacked `__Header__` lines unless you are deliberately mimicking ASCII art; even then, prefer pipes or a fenced monospace block with a caption.

## Code

- Fenced blocks with language tags: ` ```python `, ` ```verilog `, etc.
- Inline code with single backticks; avoid bare ` ``` ` for math—use math delimiters instead.

## Figures and links

- Images: `![caption](relative/path.png)`; if the asset does not exist, say so in prose.
- Badges / links: no empty targets like `](` — use `#` or a real URL.

## Front matter (optional)

Not required. If you add YAML later, keep a single block at the top:

```yaml
---
title: "Paper title"
summary: "One sentence for indexes."
---
```

(The current static builder does not require this; summaries are inferred from text.)

## After editing

1. `python tools/normalize_markdown_corpus.py` — only if you pasted Word content or see `\.` / stray anchors.
2. `python tools/build_github_pages.py` — refresh `docs/site/` and topic pages.
3. Commit both source `.md` and regenerated `docs/` when the site should update.
