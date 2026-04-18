"""
Convert every .docx under the repo root to Markdown (same basename), then remove the .docx.
Run from repo root: python tools/convert_docx_to_markdown.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import mammoth

ROOT = Path(__file__).resolve().parents[1]
SKIP_NAME = {".git", "__pycache__", ".venv", "venv", "node_modules"}


def path_is_skipped(path: Path) -> bool:
    return any(p in SKIP_NAME or p == ".git" for p in path.parts)


def main() -> int:
    docx_files = sorted(p for p in ROOT.rglob("*.docx") if not path_is_skipped(p))
    if not docx_files:
        print("No .docx files found.")
        return 0

    ok = 0
    failed: list[tuple[Path, str]] = []

    for docx in docx_files:
        rel = docx.relative_to(ROOT)
        try:
            with open(docx, "rb") as f:
                result = mammoth.convert_to_markdown(f)
            md_text = result.value
            if result.messages:
                for m in result.messages:
                    print(f"  note {rel}: {m}")

            out = docx.with_suffix(".md")
            header = f"<!-- Converted from `{docx.name}` — source was Word (.docx). -->\n\n"
            out.write_text(header + md_text, encoding="utf-8", newline="\n")
            docx.unlink()
            print(f"OK: {rel} -> {out.name}")
            ok += 1
        except Exception as e:
            failed.append((docx, str(e)))
            print(f"FAIL: {rel}: {e}")

    print(f"\nDone: {ok} converted, {len(failed)} failed.")
    for p, err in failed:
        print(f"  - {p.relative_to(ROOT)}: {err}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
