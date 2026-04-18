# Ideas

A personal research and engineering archive: long-form papers (Markdown), code experiments, and specifications across algorithms, materials, economics, and systems design. This repository is structured so you can browse it on **GitHub** or as a static **website** via GitHub Pages.

## Browse as a website (GitHub Pages)

The folder [`docs/`](docs/) contains a generated static site (plus [`docs/index.html`](docs/index.html) as the home page).

1. Create a new repository on GitHub and push this folder (see below).
2. In the repo: **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Choose branch **main** (or your default branch) and folder **`/docs`**, then save.

After a short build, the site is available at:

`https://<your-username>.github.io/<repository-name>/`

Rebuild the HTML mirror after you change Markdown in the project root:

```bash
pip install -r requirements.txt
python tools/build_github_pages.py
```

Word documents were converted once with `python tools/convert_docx_to_markdown.py` (original `.docx` files were removed after conversion).

## Repository layout

| Area | Role |
|------|------|
| [`tools/`](tools/) | Scripts: DOCX→Markdown import, static site build |
| [`docs/`](docs/) | GitHub Pages entry (`index.html`, `assets/`, generated `site/`) |
| Top-level folders | Topic areas (e.g. `Cypha/`, `Weapons/`, `Economics/`) with Markdown, Python, PDFs, etc. |

## Upload to Git

From this directory:

```bash
git init
git add .
git commit -m "Initial commit: Ideas archive with GitHub Pages"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

Replace `<you>` and `<repo>` with your GitHub username and repository name.

## License

Content is provided as-is for personal and research reference; add a `LICENSE` file if you want to specify terms.
