#!/usr/bin/env python3
"""Build the site data (site-data/*.json) for tunesandtexts.github.io from a
Tunes and Texts release folder (CSV export of DATA v90 / Master v16 / texts v9).

usage: python3 build_site_data.py <release folder> <out folder>

Reads only data/core/*.csv. Writes:
  texts.json     one array per text  [id, lang, first line, author, meter, parent, parent badge, flags, year]
  tunes.json     one array per Zahn tune
  links.json     text-tune links     [text id, tune no, relation, badge]
  appear.json    hymnal appearances  [text id, hymnal code, number, printed first line]
  hymnals.json   hymnal list
  tunenames.json Zahn no -> hymnary tune names (for 'listen / scores' links)
  people.json    author / translator / composer index
  details/<bucket>.json   every non-empty column of each row, for the scholar view
  meta.json      counts + build date
"""
import csv, json, os, re, sys, collections, unicodedata, datetime

REL, OUT = sys.argv[1], sys.argv[2]
CORE = os.path.join(REL, 'data', 'core')
os.makedirs(os.path.join(OUT, 'details'), exist_ok=True)


def rd(name):
    with open(os.path.join(CORE, name), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip()


def slug(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s or 'x'


def badge(s):
    """Map a free-text status/basis to '', 'p' (probable), 'c' (check), 'x' (rejected)."""
    s = clean(s).lower()
    if not s:
        return ''
    if s.startswith('rejected'):
        return 'x'
    if re.match(r'(check|review|ambiguous|not identified|uncertain)', s):
        return 'c'
    if re.match(r'(confirmed|certain|accepted|exact|melody confirmed|own melody)', s) and 'probable' not in s[:40]:
        return ''
    if re.search(r'\bcheck\b', s[:60]):
        return 'c'
    if re.search(r'probable|provisional|fuzzy|prefix|\bkn\b|\bsc\b|\bjv\b|possible|scanned text', s):
        return 'p'
    return ''


# ---------------------------------------------------------------- details
details = collections.defaultdict(dict)


def bucket(key):
    m = re.match(r'([A-Z]{2})-(\d+)', key)
    if m:
        return f'{m.group(1)}{int(m.group(2)) // 250}'
    m = re.match(r'(\d+)', key)
    return f'Z{int(m.group(1)) // 250}' if m else 'misc'


def row_fields(row):
    """[[column, value, url?], ...] — 'X URL' columns are folded into X."""
    out = []
    keys = list(row.keys())
    for k in keys:
        if k.endswith(' URL') and k[:-4] in row:
            continue
        v = clean(row[k])
        u = clean(row.get(k + ' URL', ''))
        if not v and not u:
            continue
        if v.startswith('http') and not u:
            u = v
        out.append([k, v, u] if u else [k, v])
    return out


def add_detail(key, section, fields):
    details[bucket(key)].setdefault(key, []).append([section, fields])


# ---------------------------------------------------------------- texts
texts = {}   # id -> list
LANG = {'Danish': 'da', 'Norwegian': 'no', 'Swedish': 'sv', 'Nynorsk': 'nn', 'Finnish': 'fi',
        'Czech': 'cs', 'Slovak': 'sk', 'Polish': 'pl', 'Spanish': 'es'}
ID_RE = re.compile(r'\b(?:DE|DA|NO|SV|FI|CS|SK|PL|ES|EN)-\d{4,5}\b')


def first_id(s):
    m = ID_RE.search(s or '')
    return m.group(0) if m else ''


def year_of(s):
    m = re.search(r'\b(1[2-9]\d\d|20[0-2]\d)\b', s or '')
    return m.group(1) if m else ''


def put(tid, lang, first, author, meter, parent, pb, flags, year='', basis=''):
    basis = clean(basis)
    if len(basis) > 400:
        basis = basis[:397] + '…'
    texts[tid] = [tid, lang, clean(first), clean(author), clean(meter), parent, pb, flags, year, basis]


# German: Zahn register
for r in rd('zahn_texts.csv'):
    tid = r['Text ID']
    first = r['First line (cleaned)']
    for c in ['First line correction (QC2 r4 2026-11-15)', 'First line correction (QC2 r5 2026-11-16)',
              'First line correction (QC3 2026-11-20)']:
        v = clean(r.get(c))
        if v and not v.upper().startswith('NOT '):
            first = v
    flags = []
    if clean(r.get('First line correction (QC2 r4 2026-11-15)')).upper().startswith('NOT '):
        flags.append('nd')
    author = clean(r.get('Author (Carver post, QC2 r5)')) or clean(r['Text author'])
    if author == '?':
        author = ''
    put(tid, 'de', first, author, r['Meter (normalized)'], '', '', flags, clean(r['Earliest own-tune year']))
    add_detail(tid, 'Zahn text register (zahn_texts.csv)', row_fields(r))

# German: added by the project
for r in rd('de_texts_added.csv'):
    tid = r['Text ID']
    st = clean(r['Status'])
    flags = ['added']
    if st.upper().startswith('DUPLICATE'):
        flags.append('dup:' + first_id(st[9:]))
    if st.upper().startswith('NOT A GERMAN') or clean(r['First-line QC (2026-11-13)']).upper().startswith('NOT '):
        flags.append('nd')
    if st.lower().startswith('title only'):
        flags.append('title')
    first = clean(r.get('First line, fuller form (Carver post, QC2 r5)')) or r['First line (KGB 1862 spelling)']
    author = (clean(r.get('Author (Carver post, QC2 r5)')) or clean(r.get('Author (hymnary German page, QC2 r4)'))
              or clean(r.get('Author (hymnary, 2026-11-14)')))
    put(tid, 'de', first, author, r['Meter (normalized)'], '', '', flags, year_of(r.get('Date (first known)')))
    add_detail(tid, 'German text added by the project (de_texts_added.csv)', row_fields(r))

# English
for r in rd('en_texts.csv'):
    tid = r['EN ID']
    basis = clean(r['DE link basis'])
    recheck = clean(r['German link re-check (QC 2026-11-13)'])
    parent = clean(r['Translated from (DE ID)'])
    flags = []
    up = basis.upper()
    if up.startswith(('TITLE', 'NOT A TRANSLATION', 'ENGLISH ORIGINAL', 'NOT A GERMAN TEXT')):
        flags.append('title' if up.startswith('TITLE') else 'notr')
        if not up.startswith('TITLE'):
            parent = ''
    if clean(r['First-line QC (2026-11-13)']).upper().startswith('NOT '):
        flags.append('nd')
    if clean(r['Duplicate of (EN ID)']):
        flags.append('dup:' + clean(r['Duplicate of (EN ID)']))
    pb = badge(recheck) if recheck.lower().startswith(('confirmed', 'kept', 'relinked')) and False else badge(basis)
    # Julian evidence tags: PR certain; SC/JV/KN probable
    if re.search(r'\bPR\b', basis) or basis.lower().startswith(('provisional de', 'new de')):
        pb = ''
    links = []
    if clean(r['hymnary URL']):
        links.append(['hymnary.org', clean(r['hymnary URL'])])
    if clean(r['Hymnoglypt post (Carver) URL']):
        links.append(['Hymnoglypt (Carver)', clean(r['Hymnoglypt post (Carver) URL'])])
    if clean(r['Julian URL']):
        links.append(['Julian', clean(r['Julian URL'])])
    if links:
        flags.append({'links': links})
    author = clean(r['Translator (standard)']) or clean(r['Translator'])
    put(tid, 'en', r['English first line'], author, r['Meter (normalized)'], parent if parent else '', pb if parent else '', flags,
        '', basis + (' | re-check: ' + recheck if recheck else ''))
    add_detail(tid, 'English text (en_texts.csv)', row_fields(r))

# Danish / Norwegian / Swedish
for r in rd('scandinavian_texts.csv'):
    tid = r['Text ID']
    lang = LANG.get((clean(r['Language']).split() or ['?'])[0], 'xx')
    parent = first_id(r['Translated from'])
    pb = badge(r['Link status'])
    nyn = clean(r['Nynorsk version of'])
    if nyn and first_id(nyn):
        parent = first_id(nyn)
        pb = 'c' if 'check' in nyn else ''
    if clean(r['Relation']).lower().startswith(('danish original', 'swedish original', 'latin original')) and not parent:
        pb = ''
    flags = []
    if clean(r['First-line QC (2026-11-13)']).upper().startswith('NOT '):
        flags.append('nd')
    same = first_id(r['Same text as (QC 2026-11-13)'])
    if same:
        flags.append('same:' + same)
    put(tid, lang, r['First line'], r['Translator(s)'], r['Meter (normalized)'], parent, pb if parent else '', flags,
        '', ' | '.join(x for x in [clean(r['Relation']), clean(r['Link status']), clean(r['Source'])] if x))
    add_detail(tid, 'Scandinavian text (scandinavian_texts.csv)', row_fields(r))

# Finnish / Czech / Slovak / Polish / Spanish
for r in rd('other_language_texts.csv'):
    tid = r['Text ID']
    lang = LANG.get((clean(r['Language']).split() or ['?'])[0], 'xx')
    parent = first_id(r['Translated from'])
    st = clean(r['Link status'])
    pb = badge(st)
    if st.lower().startswith('confirmed'):
        pb = ''
    credit = clean(r['Author / translator credit (as in the source)'])
    put(tid, lang, r['First line'], credit, '', parent, pb if parent else '', [], clean(r['Into the hymnal (year)']),
        ' | '.join(x for x in [clean(r['Relation']), st, clean(r['Basis'])] if x))
    add_detail(tid, 'Other-language text (other_language_texts.csv)', row_fields(r))

# drop parents that point nowhere
for t in texts.values():
    if t[5] and t[5] not in texts:
        t[7].append('parent?:' + t[5])
        t[5] = ''
        t[6] = ''

# ---------------------------------------------------------------- tunes
ARCH = {'1': '1508283124bsb11304498', '2': '1508284209bsb11304500', '3': '1508285990bsb11304501',
        '4': '1508286757bsb11304502', '5': '1508287113bsb11304503'}
ROMAN = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V'}
tunes = []
tune_ids = set()
for r in rd('zahn_tunes.csv'):
    no = clean(r['Zahn no.'])
    page = clean(r['Zahn page'])
    pc = clean(r['Page correction (QC2 r4 2026-11-15)'])
    if pc and re.match(r'\d+', pc):
        page = re.match(r'\d+', pc).group(0)
    vol = clean(r['Vol.'])
    comp = clean(r['Composer (corrected)']) or clean(r['Composer / attribution'])
    src = clean(r['Earliest source (corrected)']) or clean(r['First source (as cited by Zahn)'])
    yr = clean(r['Source year (corrected)']) or clean(r['Source year'])
    author = clean(r['Text author (corrected)']) or clean(r['Text author'])
    scan = f'https://archive.org/details/{ARCH[vol]}/page/{page}/mode/1up' if vol in ARCH and page.isdigit() else ''
    tunes.append([no, ROMAN.get(vol, vol), page, clean(r['Meter type']), clean(r['Syllable pattern']),
                  clean(r['Text incipit']), author, comp, src, yr, clean(r['Key signature']),
                  clean(r['Time signature']), clean(r['Melodic incipit']), clean(r['Confidence']),
                  clean(r['Intervals (semitones)']), clean(r['Same melody as (Zahn)']), scan,
                  clean(r['Duplicate of row'])])
    tune_ids.add(no)
    add_detail(no, 'Zahn tune (zahn_tunes.csv)', row_fields(r))


def tune_nos(s):
    return [x for x in re.split(r'[\s,;/]+', clean(s)) if x and x in tune_ids]


# ---------------------------------------------------------------- links
links = []
seen = set()
ev = []
evi = {}


def link(tid, no, rel, b, e=''):
    key = (tid, no, rel)
    if key in seen or tid not in texts:
        return
    seen.add(key)
    e = clean(e)[:300]
    if e not in evi:
        evi[e] = len(ev)
        ev.append(e)
    links.append([tid, no, rel, b, evi[e]])


for r in rd('zahn_text_tune_links.csv'):
    rel = 'own' if r['Relation'].startswith('written') else ('also' if r['Relation'].startswith('also') else 'supp')
    for no in tune_nos(r['Zahn no(s). in master']):
        link(r['Text ID'], no, rel, '', 'Zahn register, vol. ' + clean(r['Zahn volume']) + ' p. ' + clean(r['Register page']) + ('; ' + clean(r['Register note']) if clean(r['Register note']) else ''))
    add_detail(r['Text ID'], 'Zahn register: text–tune link (zahn_text_tune_links.csv)', row_fields(r))


def rel_of(s):
    s = clean(s).lower()
    if s.startswith('zahn: melody listed'):
        return 'struct'
    if s.startswith('zahn: melody the source text is also'):
        return 'structalso'
    if 'own melody' in s:
        return 'own'
    if s.startswith('printed with'):
        return 'printed'
    if s.startswith(('sung to', 'named as tune', 'melody named', 'also sung')):
        return 'sung'
    return 'sung'


for name, idc, stc, label in [('en_tune_links.csv', 'EN ID', 'Source', 'English–tune link (en_tune_links.csv)'),
                              ('scandinavian_tune_links.csv', 'Text ID', 'Status', 'Scandinavian–tune link (scandinavian_tune_links.csv)'),
                              ('other_language_tune_links.csv', 'Text ID', 'Status', 'Other-language–tune link (other_language_tune_links.csv)')]:
    for r in rd(name):
        rel = rel_of(r['Relation'])
        st = clean(r.get(stc, ''))
        b = badge(st)
        if name == 'en_tune_links.csv':
            b = '' if rel.startswith('struct') else badge(st)
        if rel.startswith('struct') and b == '':
            pass
        nos = tune_nos(r['Zahn no.'])
        vf = tune_nos(r.get('Variant family (chosen by incipit)', ''))
        e = ' | '.join(x for x in [clean(r['Relation']), clean(r.get('Source', '')), clean(r.get('Evidence', '')),
                                    clean(r.get('Status', '')), ('via ' + clean(r['Via DE ID'])) if clean(r.get('Via DE ID', '')) else '',
                                    (clean(r.get('Hymnal', '')) + ' ' + clean(r.get('Number', ''))).strip()] if x)
        for no in nos:
            link(r[idc], no, rel, b, e)
        for no in vf:
            link(r[idc], no, 'variant', b, 'variant family chosen by incipit | ' + e)
        add_detail(r[idc], label, row_fields(r))

# ---------------------------------------------------------------- appearances + hymnals
HYMNALS = {
    # code: (name, language, kind)
    'TLH': ('The Lutheran Hymnal (1941)', 'en', 'hymnal'),
    'LW': ('Lutheran Worship (1982)', 'en', 'hymnal'),
    'ELH': ('Evangelical Lutheran Hymnary (1996)', 'en', 'hymnal'),
    'LSB': ('Lutheran Service Book (2006)', 'en', 'hymnal'),
    "CW'93": ('Christian Worship (1993)', 'en', 'hymnal'),
    "CW'21": ('Christian Worship (2021)', 'en', 'hymnal'),
    'LBW': ('Lutheran Book of Worship (1978)', 'en', 'hymnal'),
    'WOV': ('With One Voice (1995)', 'en', 'hymnal'),
    'CWS': ('Christian Worship: Supplement (2008)', 'en', 'hymnal'),
    "HS'98": ('Hymnal Supplement 98', 'en', 'hymnal'),
    'ELHB': ('Evangelical Lutheran Hymn-Book (1911/12)', 'en', 'hymnal'),
    'CBfE1863': ('The Chorale Book for England (1863)', 'en', 'hymnal'),
    'Bacon1883': ('Bacon & Allen, The Hymns of Martin Luther (1883)', 'en', 'hymnal'),
    'Julian': ('Julian, A Dictionary of Hymnology (1907)', 'en', 'reference'),
    'Hymnoglypt': ("Matthew Carver's Hymnoglypt (blog)", 'en', 'reference'),
    'Pontoppidan 1740': ('Pontoppidan, Den nye Psalme-Bog (1740)', 'da', 'hymnal'),
    'Belsheim, 150 Salmer (1876)': ('Belsheim, 150 Salmer (1876)', 'no', 'hymnal'),
    'DDS2002': ('Den Danske Salmebog (2002)', 'da', 'hymnal'),
    'N13': ('Norsk salmebok (2013)', 'no', 'hymnal'),
    'NoS1985': ('Norsk salmebok (1985)', 'no', 'hymnal'),
    'Virsikirja 1986': ('Virsikirja (Finnish hymnal, 1986)', 'fi', 'hymnal'),
    'Vanha virsikirja 1701': ('Vanha virsikirja (1701)', 'fi', 'hymnal'),
    'CSPD1952 (Cithara Sanctorum – Písně duchovní)': ('Cithara Sanctorum – Písně duchovní (1952 ed.)', 'cs', 'hymnal'),
    'Evanjelický spevník': ('Evanjelický spevník (Slovak)', 'sk', 'hymnal'),
    'Evangelický zpěvník 2021 (EZ21, ČCE)': ('Evangelický zpěvník (ČCE, 2021)', 'cs', 'hymnal'),
}
appear = []
hcount = collections.Counter()
hlang = {}
for name, idc, titlec, langdef in [('hymnal_appearances.csv', 'EN ID', 'Title', 'en'),
                                   ('scandinavian_appearances.csv', 'Text ID(s)', 'First line', None),
                                   ('other_language_appearances.csv', 'Text ID(s)', 'First line', None)]:
    for r in rd(name):
        h = clean(r['Hymnal'])
        for tid in ID_RE.findall(r[idc]):
            if tid in texts:
                appear.append([tid, h, clean(r['Number']), clean(r[titlec])])
                hcount[h] += 1
                hlang.setdefault(h, collections.Counter())[texts[tid][1]] += 1
hymnals = []
for h, n in sorted(hcount.items(), key=lambda x: x[0].lower()):
    name, lang, kind = HYMNALS.get(h, (h, hlang[h].most_common(1)[0][0], 'hymnal'))
    hymnals.append({'code': h, 'slug': slug(h), 'name': name, 'lang': lang, 'kind': kind, 'n': n,
                    'named': h in HYMNALS})

# ---------------------------------------------------------------- tune names (hymnary) -> Zahn
tunenames = collections.defaultdict(list)
for r in rd('tune_names_to_zahn.csv'):
    st = clean(r['Status'])
    if st.startswith('no Zahn'):
        continue
    for no in tune_nos(r['Zahn no.']):
        tunenames[no].append([clean(r['Tune name (hymnary)']), 'c' if 'check' in st else ''])

# ---------------------------------------------------------------- people
people = collections.defaultdict(lambda: {'t': [], 'm': []})


def person_names(s):
    s = clean(s)
    s = re.sub(r'^Mel\.\s*(v\.|von|bei \(von\?\)|bei)\s*', '', s)
    out = []
    for p in re.split(r'\s*(?:;| / | \| )\s*', s):
        p = re.sub(r'\s*,?\s*\(?\d{4}\s*[-–]\s*\d{0,4}\)?\.?$', '', p).strip(' ,.')
        p = p.strip('()')
        if len(p) >= 3 and not re.match(r'^(\?|anon|unknown|unbekannt)', p, re.I):
            out.append(p)
    return out


for t in texts.values():
    if t[1] in ('fi', 'cs', 'sk', 'pl', 'es') or 'nd' in t[7]:
        continue
    for p in person_names(t[3])[:4]:
        people[p]['t'].append(t[0])
for tu in tunes:
    for p in person_names(tu[7])[:3]:
        people[p]['m'].append(tu[0])
plist = []
for name, v in people.items():
    plist.append({'name': name, 'slug': slug(name), 't': v['t'], 'm': v['m']})
# de-duplicate slugs
cnt = collections.Counter()
for p in sorted(plist, key=lambda p: -(len(p['t']) + len(p['m']))):
    cnt[p['slug']] += 1
    if cnt[p['slug']] > 1:
        p['slug'] += f'-{cnt[p["slug"]]}'
plist.sort(key=lambda p: slug(p['name']))

# ---------------------------------------------------------------- write


def dump(name, obj, lines=False):
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as f:
        if lines and isinstance(obj, list):
            f.write('[\n' + ',\n'.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in obj) + '\n]\n')
        else:
            json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(path)


sizes = {}
sizes['texts.json'] = dump('texts.json', sorted(texts.values()), True)
sizes['tunes.json'] = dump('tunes.json', tunes, True)
sizes['links.json'] = dump('links.json', links, True)
sizes['evidence.json'] = dump('evidence.json', ev, True)
sizes['appear.json'] = dump('appear.json', appear, True)
sizes['hymnals.json'] = dump('hymnals.json', hymnals, True)
sizes['tunenames.json'] = dump('tunenames.json', tunenames)
sizes['people.json'] = dump('people.json', plist, True)
dsz = 0
for b, d in details.items():
    dsz += dump(f'details/{b}.json', d)
langs = collections.Counter(t[1] for t in texts.values())
meta = {'built': datetime.date.today().isoformat(), 'release': '0.9 provisional',
        'base': 'DATA v90, Zahn master v16, Zahn texts and links v9 (release 2026-11-20b)',
        'texts': len(texts), 'langs': langs, 'tunes': len(tunes), 'links': len(links),
        'appearances': len(appear), 'hymnals': len(hymnals), 'people': len(plist)}
dump('meta.json', meta)
print(json.dumps(meta, ensure_ascii=False))
print(sizes, 'details', dsz, len(details), 'files')
print('badges parent', collections.Counter(t[6] for t in texts.values() if t[5]))
print('badges links', collections.Counter((l[2], l[3]) for l in links))
print('unnamed hymnals', [h['code'] for h in hymnals if not h['named']])
