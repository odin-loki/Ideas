# docs — GitHub Pages Site

> **📄 Overview**: GitHub Pages root: [`index.html`](index.html), shared CSS, **generated** `site/` mirror of the Markdown corpus.

---

## 📄 Overview

**docs** is the root directory for the GitHub Pages static site. This folder contains the `index.html` entry point, shared CSS, and the generated `site/` mirror of the Markdown corpus.

### Key Components

- **index.html**: Main entry point for the GitHub Pages site
- **site/**: Generated mirror of the Markdown corpus
- **assets/**: Shared assets (CSS, images, fonts)
- **topics/**: Topic-specific site content
- **README.md**: This maintainer notes file

---

## 📁 Directory Structure

| Directory | Role |
|--|--|
| **index.html** | Site entry point |
| **site/** | Generated Markdown mirror |
| **assets/** | Shared site assets |
| **topics/** | Topic content |
| **tree.json** | Directory tree metadata |

---

## 🔧 Site Generation

The **`tools/`** directory contains the site generation tools:

- **`build_github_pages.py`**: Main site builder
- **`editorial_inventory.py`**: Folder inventory generator
- **`normalize_markdown_corpus.py`**: Markdown normalizer
- **`convert_docx_to_markdown.py`**: DOCX converter

---

## 📋 Editorial Standards

For new content, follow **[`EDITORIAL_STYLE.md`](EDITORIAL_STYLE.md)**:

- One `#` document title in first lines
- ATX headings (`#`, `##`, `###`)
- GFM pipe tables for data grids
- `**bold**` for emphasis (not `__`)

See **[`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md)** for editorial workflow.

---

## 🛠️ Tooling

| Tool | Purpose |
|--|--|
| **`build_github_pages.py`** | Build the GitHub Pages site |
| **`editorial_inventory.py`** | Generate folder inventory |
| **`normalize_markdown_corpus.py`** | Normalize Markdown |
| **`convert_docx_to_markdown.py`** | Convert DOCX to Markdown |

---

## 🔗 Links

- [../README.md](../README.md) — Main project README
- [../EDITORIAL_ROADMAP.md](../EDITORIAL_ROADMAP.md) — Editorial roadmap
- [`EDITORIAL_STYLE.md`](EDITORIAL_STYLE.md) — House style guide

---

## 🛡️ About This Folder

This folder serves as the **maintainer notes** area for the `docs/` tree. It documents:
- Site structure and generation
- Editorial standards and workflow
- Tooling and automation

---

> **✨ Welcome to the docs folder — where research meets web presentation.**