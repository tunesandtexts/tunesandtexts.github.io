"""Release 0.9 extras (2026-11-23): files built from the site data so the downloads carry what the website shows.
 data/core/persons.csv        authority list: one row per identified author/translator/composer (preferred name, dates, role,
                              GND and VIAF IDs, the printed forms merged into the person, number of texts and tunes)
 data/core/text_guidance.csv  per text: place in the family tree, the original's own / borrowed melodies, other melodies,
                              and the copyright guidance (status + basis). Guidance only, not legal advice.
Usage: python3 rel_extras_v1.py <release dir> <site-data dir>"""
import sys, json, csv, os
REL, SD = sys.argv[1:3]
P = json.load(open(f'{SD}/people.json', encoding='utf-8'))
T = {t[0]: t for t in json.load(open(f'{SD}/texts.json', encoding='utf-8'))}
L = json.load(open(f'{SD}/links.json', encoding='utf-8'))
G = {'own': 0, 'supp': 0, 'struct': 0, 'also': 1, 'structalso': 1}
by = {}
for l in L:
    if l[3] != 'x': by.setdefault(l[0], []).append(l)
def root(i):
    seen = set()
    while T.get(i) and T[i][5] and i not in seen: seen.add(i); i = T[i][5]
    return i
with open(f'{REL}/data/core/persons.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Person key', 'Preferred name', 'Name (display)', 'Born', 'Died', 'Role', 'GND', 'GND URL', 'VIAF', 'Texts (n)', 'Tunes (n)', 'Printed forms', 'Text IDs', 'Zahn nos.'])
    for p in sorted((p for p in P if 'auth' in p), key=lambda p: p['sort']):
        g = p.get('gnd', '')
        w.writerow([p['auth'], p['sort'], p['name'], p.get('born', ''), p.get('died', ''), p.get('role', ''), g, f'https://d-nb.info/gnd/{g}' if g else '',
                    p.get('viaf', ''), len(p['t']), len(p['m']), ' | '.join(p.get('variants', [])), ' '.join(p['t']), ' '.join(p['m'])])
PD = {'pd': 'public domain', 'pd70': 'likely public domain (life + 70)', 'cr': 'probably in copyright', '': 'not known'}
with open(f'{REL}/data/core/text_guidance.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['Text ID', 'Language', 'First line', 'Place in family tree', 'Original (top of tree)', "Original's own tune(s)", "Original's borrowed tune(s)", 'Other melodies', 'Copyright status (guidance)', 'Copyright basis'])
    for i, t in sorted(T.items()):
        r = root(i); fam = (by.get(i, []) + (by.get(r, []) if r != i else []))
        orig = {l[1] for l in fam if G.get(l[2]) == 0}; also_only = False
        if not orig: orig = {l[1] for l in fam if G.get(l[2]) == 1}; also_only = bool(orig)
        mine = [l[1] for l in by.get(i, [])]
        def kind(n):
            for l in fam:
                if l[1] == n and G.get(l[2]) == 0 and l[5] in (0, 1): return l[5]
        own = sorted({n for n in orig if n in mine and not also_only and kind(n) == 1})
        bor = sorted({n for n in orig if n in mine and (also_only or kind(n) == 0)})
        oth = sorted({n for n in mine if n not in orig}) if orig else []
        w.writerow([i, t[1], t[2], 'translation' if t[5] else 'original', r, ' '.join(own), ' '.join(bor), ' '.join(oth), PD[t[10] or ''], t[11] or ''])
print('persons', sum(1 for p in P if 'auth' in p), 'texts', len(T))
