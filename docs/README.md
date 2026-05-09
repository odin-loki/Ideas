# docs — static-site assets and house style guide

> **What's actually here.** A small static site (`index.html`, shared CSS / `assets/`, generated `site/` mirror, `topics/` and `tree.json`) plus the house style guide for the corpus. The build pipeline that originally produced `site/` is not currently checked into the repo.

---

## 📁 Contents

| Item | Role |
|---|---|
| [`index.html`](index.html) | Site entry point (browsable directly or via GitHub Pages if enabled) |
| [`assets/`](assets/) | Shared site assets (CSS, fonts) |
| [`site/`](site/) | Generated mirror of the Markdown corpus (HTML + JSON, produced offline) |
| [`topics/`](topics/) | Topic-page content |
| [`tree.json`](tree.json) | Directory-tree metadata used by the site |
| [`.nojekyll`](.nojekyll) | Tells GitHub Pages to skip Jekyll processing |
| [`EDITORIAL_STYLE.md`](EDITORIAL_STYLE.md) | **House style guide** — formatting conventions used across every README in this repository |

---

## 📋 Editorial style (summary of `EDITORIAL_STYLE.md`)

For new content, follow [`EDITORIAL_STYLE.md`](EDITORIAL_STYLE.md). The shortlist:

- One `#` document title in the first lines.
- ATX headings (`#`, `##`, `###`).
- GFM pipe tables for data grids.
- `**bold**` for emphasis (not `__`).
- Use the per-folder README as the index for that topic — every folder has one, including the smallest.

---

## 🛠 About the site mirror

The `site/` directory contains a generated HTML mirror of the Markdown corpus. **The build pipeline that produced it is not currently part of this repository** (an earlier `tools/` directory and `build_github_pages.py` were referenced but are no longer present). Treat `site/` as a static snapshot.

To enable GitHub Pages from `/docs`: **Settings → Pages → deploy from `main`, folder `/docs`**.

---

[← Back to main README](../README.md)
