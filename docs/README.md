This directory powers **GitHub Pages** for the Ideas repository.

- **`index.html`** — Landing page with a topic index.
- **`assets/site.css`** — Shared styles for the landing page and generated article pages.
- **`site/`** — Generated HTML (one page per Markdown file in the repo). Regenerate with `python tools/build_github_pages.py` from the repository root.
- **`tree.json`** — Machine-readable index (same structure as the landing page lists).
- **`.nojekyll`** — Disables Jekyll so static files are served as-is.

Do not edit files under `site/` by hand; they are overwritten when you run the build script.
