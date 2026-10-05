import re
from datetime import datetime
from pathlib import Path

SKIP_PAGES = ('index.md', 'log.md', 'Catalog.md')


def count_notes(content):
    urls = len(re.findall(r'^- \[(?!\[)', content, re.MULTILINE))
    text_notes = len(re.findall(r'^- \*', content, re.MULTILINE))
    return urls + text_notes


def on_config(config):
    docs_dir = Path(config['docs_dir'])
    catalog_path = docs_dir / 'Catalog.md'

    rows = []
    for path in sorted(docs_dir.glob('*.md')):
        if path.name in SKIP_PAGES or path == catalog_path:
            continue
        created = datetime.fromtimestamp(path.stat().st_mtime).strftime('%m-%d-%Y')
        n = count_notes(path.read_text())
        rows.append((path.stem, created, n))

    total_files = len(rows)
    total_notes = sum(n for _, _, n in rows)

    lines = [
        '# Catalog',
        '',
        '',
        '**Summary**: Inventory of all topic pages — each category/file, when it was created, and how many notes it contains. Auto-generated on every build; do not edit by hand.',
        f'**Last updated**: {datetime.now().strftime("%m-%d-%Y")}.',
        '',
        '---',
        '',
        f'**{total_files} topic pages, {total_notes} notes** across {total_files} categories.',
        '',
        '| Category | File | Date created | Notes |',
        '|---|---|---|---|',
    ]
    for name, created, n in rows:
        title = name.replace('_', ' ')
        lines.append(f'| {title} | {name}.md | {created} | {n} |')

    lines += ['', '## Notes per category', '']
    for name, created, n in rows:
        lines.append(f'- **{name.replace("_", " ")}** ({name}.md, created {created}): {n} notes')

    catalog_path.write_text('\n'.join(lines) + '\n')

    def count_items(filepath):
        path = docs_dir / filepath
        if path.exists():
            return count_notes(path.read_text())
        return 0

    def update_nav(nav_items):
        result = []
        for item in nav_items:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                new_dict = {}
                for title, value in item.items():
                    if isinstance(value, str) and value.endswith('.md') and value not in SKIP_PAGES:
                        n = count_items(value)
                        new_dict[f"{title} ({n})"] = value
                    elif isinstance(value, list):
                        new_dict[title] = update_nav(value)
                    else:
                        new_dict[title] = value
                result.append(new_dict)
        return result

    config['nav'] = update_nav(config['nav'])
    return config
