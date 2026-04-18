"""
Render Markdown corpus to static HTML under docs/site/ and regenerate docs/index.html.
Run from repo root: python tools/build_github_pages.py
"""
from __future__ import annotations

import html
import json
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = DOCS / "site"
SKIP_PREFIXES = ("docs", ".git")

MD_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
    "markdown.extensions.tables",
    "markdown.extensions.toc",
    "markdown.extensions.fenced_code",
]


def iter_markdown_files() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in p.parts):
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_PREFIXES:
            continue
        out.append(p)
    return sorted(out)


def strip_leading_comment(md: str) -> str:
    """Remove HTML comment prologue (converted-from-docx lines)."""
    md = md.lstrip("\ufeff")
    if md.startswith("<!--"):
        end = md.find("-->")
        if end != -1:
            md = md[end + 3 :].lstrip()
    return md


def render_page(
    display_rel: Path, index_href: str, css_href: str, body_html: str, title: str
) -> str:
    safe_title = html.escape(title)
    crumb = html.escape(str(display_rel))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{safe_title}</title>
  <link rel="stylesheet" href="{css_href}"/>
</head>
<body>
  <header class="page-bar">
    <a class="home" href="{index_href}">Index</a>
    <span class="path">{crumb}</span>
  </header>
  <main class="prose">
{body_html}
  </main>
</body>
</html>
"""


def main() -> int:
    md_files = iter_markdown_files()
    if not md_files:
        print("No markdown files found outside docs/.")
        return 1

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    for src in md_files:
        rel = src.relative_to(ROOT)
        text = src.read_text(encoding="utf-8", errors="replace")
        text = strip_leading_comment(text)
        body = md.convert(text)
        md.reset()

        html_rel = rel.with_suffix(".html")
        out_path = SITE / html_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        title = rel.stem.replace("_", " ")
        index_href = Path(
            os.path.relpath(DOCS / "index.html", out_path.parent)
        ).as_posix()
        css_href = Path(
            os.path.relpath(DOCS / "assets" / "site.css", out_path.parent)
        ).as_posix()
        out_path.write_text(
            render_page(html_rel, index_href, css_href, body, title),
            encoding="utf-8",
            newline="\n",
        )

    # Build navigation tree by top-level folder
    by_top: dict[str, list[Path]] = defaultdict(list)
    for src in md_files:
        rel = src.relative_to(ROOT)
        top = rel.parts[0]
        by_top[top].append(rel)

    sections: list[dict] = []
    for top in sorted(by_top.keys(), key=str.lower):
        items = []
        for rel in sorted(by_top[top], key=lambda p: str(p).lower()):
            href = "site/" + "/".join(quote(part, safe="/") for part in rel.with_suffix(".html").parts)
            items.append({"title": rel.stem, "href": href})
        sections.append({"name": top, "items": items})

    tree_path = DOCS / "tree.json"
    tree_path.write_text(json.dumps({"sections": sections}, indent=2), encoding="utf-8")

    # Static index.html (works without JS; tree.json for optional enhancements)
    index_lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8"/>',
        '  <meta name="viewport" content="width=device-width, initial-scale=1"/>',
        "  <title>Ideas — research &amp; notes</title>",
        '  <link rel="stylesheet" href="assets/site.css"/>',
        "</head>",
        "<body>",
        '  <div class="hero">',
        "    <h1>Ideas</h1>",
        "    <p>Personal research archive: papers, specs, and code sketches. Browse by topic below, or open the repository on GitHub for raw Markdown and source files.</p>",
        "  </div>",
        '  <nav class="toc" aria-label="Topics">',
    ]
    for sec in sections:
        esc_name = html.escape(sec["name"])
        index_lines.append(f'    <details class="topic" open>')
        index_lines.append(f"      <summary>{esc_name} <span class=\"count\">({len(sec['items'])})</span></summary>")
        index_lines.append("      <ul>")
        for it in sec["items"]:
            index_lines.append(
                f'        <li><a href="{html.escape(it["href"])}">{html.escape(it["title"])}</a></li>'
            )
        index_lines.append("      </ul>")
        index_lines.append("    </details>")
    index_lines.extend(
        [
            "  </nav>",
            '  <footer class="foot">',
            "    <p>Generated static pages from Markdown. Rebuild with <code>python tools/build_github_pages.py</code> after edits.</p>",
            "  </footer>",
            "</body>",
            "</html>",
        ]
    )
    (DOCS / "index.html").write_text("\n".join(index_lines) + "\n", encoding="utf-8", newline="\n")

    (DOCS / ".nojekyll").touch()

    print(f"Rendered {len(md_files)} pages under {SITE.relative_to(ROOT)}")
    print(f"Wrote {tree_path.relative_to(ROOT)} and docs/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
