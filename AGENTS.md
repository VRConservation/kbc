# Instructions for Organizing and Updating base

## Overview
This is a knowledge base for the HELP charter and is based on documents placed in the following folder: ~/1-projects/HELP/kb_charter/base. 

Open it in Obsidian directly, and it also builds and publishes as a Zensical site on GitHub Pages.

The github repo for this knowledge base is at https://github.com/VRConservation/kbc the website is https://3point.xyz/kbc

Each file has YAML frontmatter, including a `tags` field or will have a tag field or hashtag added if no frontmatter. The `tags` field drives the organization: each tag maps to a topic page in `notes/`. `notes/` is the site's `docs_dir`.

Prioritize the ability to search and recall specific items.

## Commands

Defined in `~/.zshrc`; each vault has its own `AGENTS.md`, so the prompt is just `ingest` in both.

| Command | Runs in | Vault |
| --- | --- | --- |
| `ingest kbc` | `~/1-projects/HELP/kb_charter/base` | This knowledge base (HELP charter) |
| `ingest` or `ingest clips` | `~/3-resources/Obsidian/Clippings` | The Obsidian Clippings knowledge base |
| `ingest -h` | — | Show usage |

`ingest kbc` runs `opencode run --auto 'ingest'` in this folder, which reads this file and does the workflow below end to end, including the push.

## Folder structure

```
- (repo root)        -- Obsidian vault + new files folder at ~/1-projects/HELP/kb_charter/base; new clipped .md files land here
- processed/         -- ingested files moved here after processing (gitignored, stays local, never pushed)
- notes/             -- markdown pages for the organized topic notes; also the site docs_dir
- notes/index.md     -- table of contents of all the notes pages + "Latest Finds"
- notes/log.md       -- append-only record of all operations
- notes/Catalog.md   -- auto-generated inventory of all topic pages (do not edit by hand; rebuilt by build.py on every build and gitignored)
- notes/stylesheets/extra.css -- card colors for the grid-cards home page
```

## Workflow

Always `git pull` to fetch the latest changes from GitHub first.

- Look at all `.md` files in the repo root (base).
- Process each file and all notes inside using the processing instructions below.
- Once processed, move the original file to the `processed/` folder (gitignored). Note: the clipping is ingested into `notes/` as brief, searchable topic entries; the full source clipping stays in `processed/` for reference.
- **Site constraint**: `notes/` is the site's `docs_dir`. Any `.md` file linked from a topic page (e.g. a long bibliography or source document) must also live inside `notes/` for the link to resolve on the published site. If a clipping's content is linked rather than summarized inline, copy the file into `notes/` before moving the original to `processed/`.

## Processing Instructions

When the user adds a new `.md` file to the repo root and asks you to ingest it:

* Read the new file's YAML frontmatter, especially the `tags` field.
* Visit the `source` URL (if present) and generate an accurate short description (1-2 lines).
* Identify the main topic from the frontmatter tags.
* Read `notes/index.md` first to find relevant topic pages.
* Map each frontmatter tag to a topic page:
  - `wob` →  `WOB`
  - `data wg` → `Data`
  - `confi`, `confi wg`, `conservtion finance` → `WOB`
  - `charter` → `Charter`
  - `origin`, `history`, `foundation` → `Baseline`
 
  - *any other tag* → create a new topic page named Title_Case from the tag
  - *untagged/empty tag* → prompt for a tag
* Add a new item to the main topic page, keeping newer notes at the top.
* Add back-links ([[page-name]]) to connect related topics. If a related topic page does not exist, create it.
* Update `notes/index.md` with new pages and one-line descriptions (grid cards).
* Append an entry to `notes/log.md` with the date, source name, and what changed.

## Update the Website

This folder is published as a Zensical site on GitHub Pages via GitHub Actions (`.github/workflows/deploy.yml` already exists, and runs `python build.py`). After ingesting new notes:

- Update the "Latest Finds" section in `notes/index.md` with the 5 most recently added notes, each from a different topic page. Don't pick these from Misc.
- Add any new topic page to the `nav` in `mkdocs.yml` and to the grid cards in `notes/index.md`, otherwise it will build but not appear in the site navigation.
- Commit and push to GitHub (`git add`, `git commit`, `git push`) so the site rebuilds and redeploys automatically. `processed/` stays gitignored and is never pushed.

## Topic Page Format

Every note topic page should follow this structure:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.
**Last updated**: Date of most recent update.

---

- [title](url): description. Related: [[Other_Topic]]. Keywords: keyword one, keyword two
```

## Note Formatting Instructions

- Use Markdown format for each note.
- Use a bullet point for each note.
- For notes with URLs:
  - Format: `[title](url): <description> <keywords>`
  - Add a 1-2 line description from the URL.
- For notes with just text:
  - Format: `*Title*: <description> <keywords>`
  - For notes up to 100 characters, add verbatim. For longer notes, summarize to 100 characters.
- Add 3-6 keywords that best describe the note and aid recall.
- Link related topics using [[wiki-links]] throughout the text.

## Rules

- Keep page filenames Title Case with underscores (e.g. `Remote_Sensing.md`), matching the `[[Page_Name]]` used in Related links.
- Write in clear, plain language.
- Always update `notes/log.md` after changes.
