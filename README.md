# Alias

`ingest kbc` runs this knowledge base from the terminal. It goes to the `~/1-projects/HELP/kb_charter/base` vault, ingests the new files, and spins them up to the mkdocs site.

Plain `ingest` (no argument) runs the Obsidian Clippings vault at `~/3-resources/Obsidian/Clippings`. `ingest clips` does the same explicitly. Both are defined in `~/.zshrc`, and each vault carries its own `AGENTS.md` telling opencode what to do.

# HELP Knowledge-Base Charter (KBC)

A searchable personal knowledge base generated from an [Obsidian](https://obsidian.md/)
vault of clipped notes and bookmarks. New items are added to the ~/kb_charter/base folder; opencode reads each file's frontmatter `tags` and
files it into the right topic page in `notes/`. Published automatically to
GitHub Pages on every push to `main`.

The site uses an [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) layout styled after [spatialthoughts/notes](https://spatialthoughts.github.io/notes/),
with a grid-cards home page grouped by theme.

## Live site

- [kb_charter](https://vrconservation.github.io/kbc/) — main site which is also the same as [3point.xyz/kbc](https://3point.xyz/kbc)
- [Repository](https://github.com/VRConservation/kbc)

## What's included

| File / folder                  | Purpose                                                                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `notes/`                       | The vault's published topic pages — this is the MkDocs `docs_dir` and also a normal folder of Markdown files, so it works in Obsidian too. |
| `notes/index.md`               | Grid-cards table of contents + "Latest Finds" highlights, shown as the site's home page.                                                   |
| `notes/log.md`                 | Append-only changelog of ingestion operations.                                                                                             |
| `notes/Catalog.md` | Auto-generated inventory of all topic pages and note counts (do not edit by hand; rebuilt on every build and gitignored). |
| `processed/` | Notes that have been ingested into `notes/` (gitignored, stays local, never pushed). |
| `AGENTS.md` | Instructions opencode follows to process files from the repo root into topic pages in `notes/`, and to keep the site in sync. |
| `mkdocs.yml` | Site configuration — theme, navigation, plugins. |
| `hooks.py` | Auto-generates `Catalog.md` and adds a live note-count, e.g. `WOB (4)`, next to each topic in the site navigation. |
| `requirements.txt` | Pinned Python packages needed to build the site. |
| `.gitignore` | Keeps `processed/`, `site/`, `.venv/` and the generated `notes/Catalog.md` out of the repo. |
| `.github/workflows/deploy.yml` | GitHub Actions workflow that builds and deploys the site to GitHub Pages on every push to `main`. |
| `.obsidian/` | Minimal Obsidian vault config, so this folder opens as a vault immediately. |

## How it works

Each file is a Markdown file with YAML frontmatter, including a `tags`
field. The `tags` field drives the organization — each tag maps to a topic page
in `notes/`. See `notes/index.md` for the current list of topics. If the file does not have YAML frontmatter a tag with # will be added to indicate which part of mkdocs to go to.

## Adding notes

Drop a new file into the ~/base folder, then run `ingest kbc` (or just ask opencode to ingest it). It will read `AGENTS.md`, find or create the right topic page based on the frontmatter `tags`, add the entry with backlinks and keywords, update `notes/index.md` and `notes/log.md`, move the file to `processed/`, and sync the site.

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open `http://127.0.0.1:8000` to preview. To build a static copy:

```bash
mkdocs build
```

## Deploying

Push to `main`; `.github/workflows/deploy.yml` builds the site with MkDocs and deploys it to GitHub Pages. GitHub Pages is already set to **Settings → Pages → Build and deployment → Source → GitHub Actions** for this repo. The live site is https://3point.xyz/kbc.
