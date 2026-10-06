#!/usr/bin/env python3
"""Pre-build step for Zensical: replaces the MkDocs hooks.py functionality.

Zensical has no `hooks:` support, so the two things hooks.py used to do at
config time are done here instead:

  1. Regenerate notes/Catalog.md (gitignored, inventory of topic pages).
  2. Inject per-page note counts into the nav titles ("Baseline (12)").

The nav rewrite is textual on purpose: mkdocs.yml uses `!!python/name:` YAML
tags for the emoji extensions, which a round-trip through PyYAML cannot
preserve. Everything outside the `nav:` block is left byte-identical.

Usage:  python build.py           build the site into site/
        python build.py --serve   build, then preview with live reload

Writes mkdocs.generated.yml, then runs `zensical build -f` (or `zensical serve`).
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "notes"
SKIP_PAGES = ("index.md", "log.md", "Catalog.md")
SRC_CONFIG = ROOT / "mkdocs.yml"
OUT_CONFIG = ROOT / "mkdocs.generated.yml"

NAV_ITEM_RE = re.compile(r"^(\s*)-\s+([^:]+):\s+(\S+\.md)\s*$")
NAV_SECTION_RE = re.compile(r"^(\s*)-\s+([^:]+):\s*$")


def count_notes(content):
    urls = len(re.findall(r"^- \[(?!\[)", content, re.MULTILINE))
    text_notes = len(re.findall(r"^- \*", content, re.MULTILINE))
    return urls + text_notes


def build_catalog():
    rows = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        if path.name in SKIP_PAGES:
            continue
        created = datetime.fromtimestamp(path.stat().st_mtime).strftime("%m-%d-%Y")
        rows.append((path.stem, created, count_notes(path.read_text())))

    total_files = len(rows)
    total_notes = sum(n for _, _, n in rows)

    lines = [
        "# Catalog",
        "",
        "",
        "**Summary**: Inventory of all topic pages — each category/file, when it was "
        "created, and how many notes it contains. Auto-generated on every build; "
        "do not edit by hand.",
        f'**Last updated**: {datetime.now().strftime("%m-%d-%Y")}.',
        "",
        "---",
        "",
        f"**{total_files} topic pages, {total_notes} notes** across {total_files} categories.",
        "",
        "| Category | File | Date created | Notes |",
        "|---|---|---|---|",
    ]
    for name, created, n in rows:
        lines.append(f"| {name.replace('_', ' ')} | {name}.md | {created} | {n} |")

    lines += ["", "## Notes per category", ""]
    for name, created, n in rows:
        lines.append(
            f"- **{name.replace('_', ' ')}** ({name}.md, created {created}): {n} notes"
        )

    (DOCS_DIR / "Catalog.md").write_text("\n".join(lines) + "\n")
    return total_files, total_notes


def count_items(filepath):
    path = DOCS_DIR / filepath
    return count_notes(path.read_text()) if path.exists() else 0


def split_nav(text):
    """Return (before, nav_block, after) for the top-level `nav:` block."""
    lines = text.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.rstrip("\n") == "nav:":
            start = i
            break
    if start is None:
        return text, None, ""

    end = len(lines)
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if line.strip() and not line[0].isspace() and not line.lstrip().startswith("#"):
            end = j
            break

    return "".join(lines[:start]), lines[start:end], "".join(lines[end:])


def annotate_nav(block_lines):
    out = []
    for line in block_lines:
        item = NAV_ITEM_RE.match(line.rstrip("\n"))
        if item:
            indent, title, target = item.groups()
            if target in SKIP_PAGES:
                out.append(line)
            else:
                out.append(
                    f"{indent}- {title} ({count_items(target)}): {target}\n"
                )
            continue
        out.append(line)
    return out


def main():
    serve = "--serve" in sys.argv

    total_files, total_notes = build_catalog()
    print(f"catalog: {total_files} topic pages, {total_notes} notes")

    text = SRC_CONFIG.read_text()
    before, nav_block, after = split_nav(text)
    if nav_block is None:
        print("warning: no top-level nav: block found", file=sys.stderr)
        generated = text
    else:
        generated = before + "".join(annotate_nav(nav_block)) + after

    OUT_CONFIG.write_text(generated)
    print(f"wrote {OUT_CONFIG.relative_to(ROOT)}")

    cmd = ["zensical", "serve" if serve else "build", "-f", str(OUT_CONFIG)]
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
