# HELP Knowledge-Base Charter (KBC)

A searchable personal knowledge base generated from an [Obsidian](https://obsidian.md/)
vault of clipped notes and bookmarks. New items are added to the ~/kb_charter/base folder; opencode reads each file's frontmatter `tags` and
files it into the right topic page in `notes/`. Published automatically to
GitHub Pages on every push to `main`.

The site is built with [Zensical](https://zensical.org/) (the successor to MkDocs,
built by the same team as Material for MkDocs) using the Material theme, styled after [spatialthoughts/notes](https://spatialthoughts.github.io/notes/),
with a grid-cards home page grouped by theme.

## Live site

- [kb_charter](https://vrconservation.github.io/kbc/) — main site which is also the same as [3point.xyz/kbc](https://3point.xyz/kbc)
- [Repository](https://github.com/VRConservation/kbc)

## What's included

| File / folder                  | Purpose                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `notes/`                       | The vault's published topic pages — this is the site's `docs_dir` and also a normal folder of Markdown files, so it works in Obsidian too. |
| `notes/index.md`               | Grid-cards table of contents + "Latest Finds" highlights, shown as the site's home page.                                                   |
| `notes/log.md`                 | Append-only changelog of ingestion operations.                                                                                             |
| `notes/Catalog.md` | Auto-generated inventory of all topic pages and note counts (do not edit by hand; rebuilt on every build and gitignored). |
| `processed/` | Notes that have been ingested into `notes/` (gitignored, stays local, never pushed). |
| `AGENTS.md` | Instructions opencode follows to process files from the repo root into topic pages in `notes/`, and to keep the site in sync. |
| `mkdocs.yml` | Site configuration — theme, navigation, plugins. |
| `build.py` | Pre-build step Zensical can't do itself: regenerates `Catalog.md`, adds a live note-count e.g. `WOB (4)` next to each topic in the navigation, writes `mkdocs.generated.yml`, then runs the build. Use `python build.py --serve` to preview. |
| `requirements.txt` | Pinned Python packages needed to build the site. |
| `.gitignore` | Keeps `processed/`, `site/`, `.venv/` and the generated `notes/Catalog.md` out of the repo. |
| `.github/workflows/deploy.yml` | GitHub Actions workflow that builds and deploys the site to GitHub Pages on every push to `main`. |
| `.obsidian/` | Minimal Obsidian vault config, so this folder opens as a vault immediately. |

## How it works

Each file is a Markdown file with YAML frontmatter, including a `tags`
field. The `tags` field drives the organization — each tag maps to a topic page
in `notes/`. See `notes/index.md` for the current list of topics. If the file does not have YAML frontmatter a tag with # will be added to indicate which topic page it belongs to.

## Adding notes

Drop a new file into the ~/base folder, then run `ingest kbc` (or just ask opencode to ingest it). It will read `AGENTS.md`, find or create the right topic page based on the frontmatter `tags`, add the entry with backlinks and keywords, update `notes/index.md` and `notes/log.md`, move the file to `processed/`, and sync the site.

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py --serve
```

Open `http://127.0.0.1:8000` to preview. To build a static copy into `site/`:

```bash
python build.py
```

`build.py` must be used rather than calling `zensical` directly — it regenerates
`notes/Catalog.md` and bakes the nav note counts into `mkdocs.generated.yml`.

## Deploying

Push to `main`; `.github/workflows/deploy.yml` runs `python build.py` and deploys the site to GitHub Pages. GitHub Pages is already set to **Settings → Pages → Build and deployment → Source → GitHub Actions** for this repo. The live site is https://3point.xyz/kbc.

## Terminal commands (this PC only)

These aliases live in `~/.zshrc` and are local to this machine — nothing here is needed to build or read the site. See the `## Commands` section of `AGENTS.md` for the same table.

| Command | Runs in |
| --- | --- |
| `ingest kbc` | `~/1-projects/HELP/kb_charter/base` — this vault |
| `ingest` or `ingest clips` | `~/3-resources/Obsidian/Clippings` — the Obsidian Clippings vault |
| `ingest -h` | Show usage |

Each vault carries its own `AGENTS.md`, so both run `opencode run --auto 'ingest'` in their folder; only the folder differs.
