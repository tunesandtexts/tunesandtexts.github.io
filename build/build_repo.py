#!/usr/bin/env python3
"""Assemble the tunesandtexts.github.io repository from a release folder.

usage: python3 build_repo.py <release folder> <repo folder>

Copies the release (data/, docs) into the repo, writes the repo README, the
site's sources page and file list, and one Excel workbook of every CSV.
Run build_site_data.py first (it writes <repo>/site-data/).
"""
import csv, json, os, re, shutil, sys
import markdown
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

REL, REPO = sys.argv[1], sys.argv[2]

# 1. release files
if os.path.exists(os.path.join(REPO, 'data')):
    shutil.rmtree(os.path.join(REPO, 'data'))
shutil.copytree(os.path.join(REL, 'data'), os.path.join(REPO, 'data'))
for f in ['DATA_DICTIONARY.md', 'SOURCES.md', 'CHANGELOG.md', 'SOURCE_AUDIT.csv', 'TRIMS.csv', 'manifest.json']:
    shutil.copy(os.path.join(REL, f), os.path.join(REPO, f))

# 2. README: the release README, with the 'Quality notes' paragraph de-duplicated (it was repeated three
#    times in the 2026-11-20b export) and a section on the website.
readme = open(os.path.join(REL, 'README.md'), encoding='utf-8').read()


def dedupe_sentences(par):
    out, seen = [], set()
    for s in re.split(r'(?<=[.)])\s+(?=[A-Z])', par):
        k = re.sub(r'\s*\([^)]*\)', '', s).strip()
        if k in seen:
            continue
        seen.add(k)
        out.append(s)
    return ' '.join(out)


readme = re.sub(r'(## Quality notes\n)(.+?)(\n\n## )', lambda m: m.group(1) + dedupe_sentences(m.group(2)) + m.group(3), readme, flags=re.S)
site = """## Website
**https://tunesandtexts.github.io/** (live once this repository is public) — search any first line, follow a hymn's family of translations from the German original, see each Zahn tune's opening notes with a link to the scan, search by melody, and compare two hymnals. A *Scholar view* switch shows the sources, evidence tags and reasoning on every line.

The site is static (no server): `index.html`, `assets/` and `site-data/`, which is built from `data/core/` by `build/build_site_data.py`. To rebuild after a data change:

```
python3 build/build_site_data.py . site-data
python3 build/build_repo.py <release folder> .   # only when a new release export replaces data/
```

To try it locally: `python3 -m http.server` in this folder, then open http://localhost:8000/.

"""
readme = readme.replace('## Folders\n', site + '## Folders\n', 1)
readme = readme.replace("- `data/core/` — the database proper.",
                        "- `data/core/` — the database proper.\n- `downloads/` — every table in one Excel workbook.\n"
                        "- `index.html`, `assets/`, `site-data/` — the website; `build/` — the scripts that build it.")
readme = readme.replace('open an issue on the repository.',
                        'use **Suggest a correction** on any page of the site, open an issue on this repository, or write to intuitufidei@gmail.com.')
open(os.path.join(REPO, 'README.md'), 'w', encoding='utf-8').write(readme)

# 3. sources page for the site
src = open(os.path.join(REL, 'SOURCES.md'), encoding='utf-8').read()
src = re.sub(r'^# Sources\s*\n', '', src)
html = markdown.markdown(src, extensions=['tables'])
html = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<)"]+[^\s<)".,;])', r'<a href="\1" rel="noopener">\1</a>', html)
open(os.path.join(REPO, 'site-data', 'sources.html'), 'w', encoding='utf-8').write(html)

# 4. Excel workbook of every CSV
os.makedirs(os.path.join(REPO, 'downloads'), exist_ok=True)
wb = Workbook(write_only=False)
wb.remove(wb.active)
csvs = []
for root, _, files in os.walk(os.path.join(REPO, 'data')):
    for f in sorted(files):
        if f.endswith('.csv'):
            csvs.append(os.path.join(root, f))
order = {'core': 0, 'sources': 1, 'work': 2}
csvs.sort(key=lambda p: (order.get(os.path.basename(os.path.dirname(p)), 9), os.path.basename(p)))
readme_ws = wb.create_sheet('README')
readme_ws.append(['Tunes and Texts: Lutheran Hymns in German, Scandinavian and English — release 0.9, provisional, under review'])
readme_ws.append(['Built from DATA v90, Zahn master v16, Zahn texts and links v9 (release 2026-11-20b). One sheet per CSV file in data/; columns are explained in DATA_DICTIONARY.md.'])
readme_ws.append(['CC0 1.0 for the project\'s own contributions; values drawn from sources remain subject to their terms (SOURCES.md).'])
readme_ws.append([])
readme_ws.append(['Sheet', 'File', 'Rows', 'Columns'])
readme_ws['A1'].font = Font(bold=True, size=13)
for c in readme_ws[5]:
    c.font = Font(bold=True)
used = set()
hdr_fill = PatternFill('solid', fgColor='E8ECEB')
for p in csvs:
    rel = os.path.relpath(p, REPO).replace(os.sep, '/')
    name = os.path.splitext(os.path.basename(p))[0]
    sheet = name[:31]
    i = 2
    while sheet.lower() in used:
        sheet = name[:28] + f'_{i}'
        i += 1
    used.add(sheet.lower())
    ws = wb.create_sheet(sheet)
    with open(p, encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    for r in rows:
        ws.append([(v if len(v) < 32000 else v[:31990] + '…') for v in r])
    if rows:
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = hdr_fill
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions
        for j, h in enumerate(rows[0], 1):
            width = min(60, max(10, len(h) + 2, *(len(r[j - 1]) for r in rows[1:200] if len(r) >= j)) if len(rows) > 1 else len(h) + 2)
            ws.column_dimensions[ws.cell(1, j).column_letter].width = width
    readme_ws.append([sheet, rel, max(0, len(rows) - 1), len(rows[0]) if rows else 0])
readme_ws.column_dimensions['A'].width = 34
readme_ws.column_dimensions['B'].width = 52
xlsx = os.path.join(REPO, 'downloads', 'Tunes_and_Texts_0.9_provisional.xlsx')
wb.save(xlsx)

# 5. file list for the site's data page
files = []
for p in csvs:
    rel = os.path.relpath(p, REPO).replace(os.sep, '/')
    with open(p, encoding='utf-8-sig') as f:
        n = sum(1 for _ in csv.reader(f)) - 1
    files.append({'path': rel, 'rows': n, 'bytes': os.path.getsize(p)})
for f in ['README.md', 'DATA_DICTIONARY.md', 'SOURCES.md', 'CHANGELOG.md', 'SOURCE_AUDIT.csv', 'TRIMS.csv', 'manifest.json']:
    files.append({'path': f, 'rows': None, 'bytes': os.path.getsize(os.path.join(REPO, f))})
json.dump(files, open(os.path.join(REPO, 'site-data', 'files.json'), 'w'), ensure_ascii=False)
print('csvs', len(csvs), 'xlsx', os.path.getsize(xlsx))
