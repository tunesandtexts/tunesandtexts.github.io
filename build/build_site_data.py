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
import csv, json, os, re, sys, collections, unicodedata, datetime, difflib

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

def julian_url(page):
    """Julian, Dictionary of Hymnology (1907), on archive.org: vol. 1 (pp. 1-878) has no page numbers, so its
    leaves are addressed as n<page+23> (checked on pp. 320, 677, 760, 836, 872); vol. 2 uses the printed page numbers
    (checked on pp. 880, 881, 909, 1369, 1749)."""
    p = int(page)
    if p <= 878:
        return f'https://archive.org/details/dictionaryofhymn01lond/page/n{p + 23}/mode/1up'
    return f'https://archive.org/details/dictionaryofhymn02lond/page/{p}/mode/1up'


def julian_links(ref):
    out = []
    for m in re.finditer(r'p\.\s*(\d{1,4})\s*(i{1,2})?\b', ref or ''):
        lab = f'Julian p. {m.group(1)}' + (f' {m.group(2)}' if m.group(2) else '')
        if lab not in [x[0] for x in out]:
            out.append([lab, julian_url(m.group(1))])
    return out


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
    links += julian_links(r['Julian'])
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
        link(r['Text ID'], no, rel, '', 'Zahn register (vol. V) p. ' + clean(r['Register page (Zahn vol. V)']) + '; tune in vol. ' + clean(r['Tune in Zahn vol.']) + ('; ' + clean(r['Register note']) if clean(r['Register note']) else ''))
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
    # code: (full title, year, place and publisher, language, kind). Titles and imprints of the hymnary.org hymnals
    # checked on their hymnary.org hymnal pages 2026-11-20 (hymnary codes in brackets where ours is shortened).
    'TLH': ('The Lutheran Hymnal', '1941', 'St. Louis: Concordia Publishing House [hymnary LH1941]', 'en', 'hymnal'),
    'LW': ('Lutheran Worship', '1982', 'St. Louis: Concordia Publishing House [hymnary LW1982]', 'en', 'hymnal'),
    'ELH': ('Evangelical Lutheran Hymnary', '1996', 'St. Louis: MorningStar Music Publishers [hymnary ELH1996]', 'en', 'hymnal'),
    'LSB': ('Lutheran Service Book', '2006', 'St. Louis: Concordia Publishing House [hymnary LSB2006]', 'en', 'hymnal'),
    "CW'93": ('Christian Worship: A Lutheran Hymnal', '1993', 'Milwaukee: Northwestern Publishing House [hymnary CWLH1993]', 'en', 'hymnal'),
    "CW'21": ('Christian Worship: Hymnal', '2021', 'Milwaukee: Northwestern Publishing House [hymnary CWH2021]', 'en', 'hymnal'),
    'LBW': ('Lutheran Book of Worship', '1978', 'Minneapolis: Augsburg Publishing House; Philadelphia: Board of Publication, Lutheran Church in America [hymnary LBoW1978]', 'en', 'hymnal'),
    'WOV': ('With One Voice', '1995', 'Minneapolis: Augsburg Fortress [hymnary WOV]', 'en', 'hymnal'),
    'CWS': ('Christian Worship: Supplement', '2008', 'Milwaukee: Northwestern Publishing House [hymnary CWS2008]', 'en', 'hymnal'),
    "HS'98": ('Hymnal Supplement 98', '1998', 'St. Louis: Concordia Publishing House [hymnary HS1998]', 'en', 'hymnal'),
    'ELHB': ('Evangelical Lutheran Hymn-Book', '1912', 'St. Louis: Concordia Publishing House [hymnary ELHB1912]', 'en', 'hymnal'),
    'LHy1913': ('The Lutheran Hymnary', '1913', 'Minneapolis: Augsburg Publishing House [hymnary LHPN1913]', 'en', 'hymnal'),
    'HOoS1901': ('Hymnal and Order of Service for Churches and Sunday-Schools', '1901', 'Rock Island, Ill.: Lutheran Augustana Book Concern', 'en', 'hymnal'),
    'HOoS1926': ('The Hymnal and Order of Service', '1926', 'Rock Island, Ill.: Augustana Book Concern', 'en', 'hymnal'),
    'HCH1927': ('Hymnal for Church and Home', '1927', 'Blair, Neb.: Danish Lutheran Publishing House [hymnary HCH11927]', 'en', 'hymnal'),
    'HFCH1928': ('Hymnal for Church and Home, 2nd ed.', '1928', 'Blair, Neb.: Danish Lutheran Publishing House', 'en', 'hymnal'),
    'HCH1949': ('Hymnal for Church and Home, 4th ed.', '1949', 'Blair, Neb.: Lutheran Publishing House [hymnary HCH41949]', 'en', 'hymnal'),
    'AEHT1920': ('The Annex: Evangelical Hymns Translated and Original, 2nd ed.', '1920', 'Blair, Neb.: Danish Lutheran Publishing House', 'en', 'hymnal'),
    'CBfE1863': ('The Chorale Book for England', '1863', 'London: Longman, Green, Longman, Roberts, and Green (tr. Catherine Winkworth)', 'en', 'hymnal'),
    'Bacon1883': ('The Hymns of Martin Luther, Set to Their Original Melodies', '1883', 'New York: Charles Scribner\'s Sons (ed. Leonard Woolsey Bacon and Nathan H. Allen)', 'en', 'hymnal'),
    'LGHS1856': ('Lyra Germanica: Hymns for the Sundays and Chief Festivals of the Christian Year', '1856', 'New York: Thomas N. Stanford (tr. Catherine Winkworth)', 'en', 'collection'),
    'LG1881': ('Lyra Germanica, new edition', '1881', 'London: Longmans, Green, and Co. (tr. Catherine Winkworth)', 'en', 'collection'),
    'HLLT1884': ('Hymns from the Land of Luther', '1884', 'London: T. Nelson and Sons (tr. Jane Borthwick and Sarah Findlater)', 'en', 'collection'),
    'PGSS1867': ("Paul Gerhardt's Spiritual Songs", '1867', 'London: Alexander Strahan (tr. John Kelly)', 'en', 'collection'),
    'PGTG1756': ('Psalmodia Germanica, or The German Psalmody, 2nd ed.', '1732', 'London: G. Smith (tr. John Christian Jacobi)', 'en', 'collection'),
    'Julian': ('A Dictionary of Hymnology, 2nd ed.', '1907', 'London: John Murray (ed. John Julian)', 'en', 'reference'),
    'Hymnoglypt': ('Hymnoglypt (blog of Matthew Carver)', '', 'matthaeusglyptes.blogspot.com; posts read up to 2026-11-12', 'en', 'reference'),
    'Pontoppidan 1740': ('Pontoppidan, Den nye Psalme-Bog', '1740', 'Copenhagen (ed. Erik Pontoppidan)', 'da', 'hymnal'),
    'DDS2002': ('Den Danske Salmebog', '2002', 'Copenhagen: Det Kgl. Vajsenhus\' Forlag (data: salmer dataset, Lasse Hjorth Madsen)', 'da', 'hymnal'),
    'K1893': ('Kirkesalmebog: efter offentlig foranstaltning', '1893', 'Bergen: Ed. B. Giertsen', 'no', 'hymnal'),
    'MBLK1897': ('M. B. Landstads Kirkesalmebog og "Nokre Salmar" ved E. Blix', '1897', 'Norsk Salmebog-Samlag', 'no', 'hymnal'),
    'PSNE1890': ('Psalmebog, udgiven af Synoden for den norske evangelisk-lutherske Kirke i Amerika, 2nd ed.', '1890', 'Decorah, Iowa: Synodens Forlag', 'no', 'hymnal'),
    'SLKA1919': ('Salmebog for Lutherske Kristne i Amerika', '1919', 'Minneapolis: Den Forenede Kirkes Forlag', 'no', 'hymnal'),
    'Belsheim, 150 Salmer (1876)': ('Belsheim, 150 Salmer', '1876', '', 'no', 'hymnal'),
    'NoS1985': ('Norsk salmebok', '1985', 'Oslo: Verbum', 'no', 'hymnal'),
    'N13': ('Norsk salmebok', '2013', 'Church of Norway', 'no', 'hymnal'),
    'DSPB1885': ('Svenska Psalm-Boken af år 1819, förenad med Koral-bok och Svenska messan', '1892', 'Chicago: Engberg-Holmberg Publishing Co.', 'sv', 'hymnal'),
    'Virsikirja 1986': ('Suomen evankelis-luterilaisen kirkon virsikirja', '1986', 'Finnish hymnal, approved 1986', 'fi', 'hymnal'),
    'Vanha virsikirja 1701': ('Vanha virsikirja', '1701', 'the old Finnish hymnal', 'fi', 'hymnal'),
    'CSPD1952 (Cithara Sanctorum – Písně duchovní)': ('Cithara Sanctorum – Písně duchovní', '1952', 'edition of 1952 [hymnary CSPD1952]', 'cs', 'hymnal'),
    'Evangelický zpěvník 2021 (EZ21, ČCE)': ('Evangelický zpěvník (Českobratrská církev evangelická)', '2021', 'Prague: ČCE', 'cs', 'hymnal'),
    'Evanjelický spevník': ('Evanjelický spevník (ECAV na Slovensku)', '1992', 'text edition (owner\'s copy)', 'sk', 'hymnal'),
}
appear = []
hcount = collections.Counter()
hlang = {}
for name, idc, titlec, langdef in [('hymnal_appearances.csv', 'EN ID', 'Title', 'en'),
                                   ('scandinavian_appearances.csv', 'Text ID(s)', 'First line', None),
                                   ('other_language_appearances.csv', 'Text ID(s)', 'First line', None)]:
    for r in rd(name):
        h = clean(r['Hymnal'])
        zt = ' '.join(tune_nos(r.get('Zahn tune', '')))
        tm = clean(r.get('Tune match', ''))
        for tid in ID_RE.findall(r[idc]):
            if tid in texts:
                jl = julian_links(r['Number']) if h == 'Julian' else []
                appear.append([tid, h, clean(r['Number']), clean(r[titlec]), zt, clean(r.get('Tune name', '')),
                               'c' if 'check' in tm.lower() or 'differs' in tm.lower() else '', jl[0][1] if jl else ''])
                hcount[h] += 1
                hlang.setdefault(h, collections.Counter())[texts[tid][1]] += 1
hymnals = []
for h, n in sorted(hcount.items(), key=lambda x: x[0].lower()):
    title, year, pub, lang, kind = HYMNALS.get(h, (h, '', '', hlang[h].most_common(1)[0][0], 'hymnal'))
    hymnals.append({'code': h, 'slug': slug(h), 'name': title + (f' ({year})' if year else ''), 'title': title, 'year': year,
                    'pub': pub, 'lang': lang, 'kind': kind, 'n': n, 'named': h in HYMNALS})

# ---------------------------------------------------------------- tune names (hymnary) -> Zahn
tunenames = collections.defaultdict(list)
for r in rd('tune_names_to_zahn.csv'):
    st = clean(r['Status'])
    if st.startswith('no Zahn'):
        continue
    for no in tune_nos(r['Zahn no.']):
        tunenames[no].append([clean(r['Tune name (hymnary)']), 'c' if 'check' in st else ''])

# ---------------------------------------------------------------- people (cleaned and merged: people_clean.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import people_clean
entries = [(t[3], 't', t[0]) for t in texts.values() if t[1] not in ('fi', 'cs', 'sk', 'pl', 'es') and 'nd' not in t[7] and t[3]]
entries += [(tu[7], 'm', tu[0]) for tu in tunes if tu[7]]
plist, rejected_credits, _ = people_clean.build(entries)
import authority
_n_before = len(plist)
plist, _auth_used, _auth_missing = authority.apply(plist)
print(f'people: {_n_before} entries -> {len(plist)} after authority list ({len(_auth_used)} authority persons)')
if _auth_missing: print('authority forms not found in index:', _auth_missing)
cnt = collections.Counter()
for p in sorted(plist, key=lambda p: -(len(p['t']) + len(p['m']))):
    base = slug(p['name'])
    cnt[base] += 1
    p['slug'] = base if cnt[base] == 1 else f'{base}-{cnt[base]}'
plist.sort(key=lambda p: slug(p['sort']))
with open(os.path.join(OUT, '..', 'build', 'people_rejected.tsv') if os.path.isdir(os.path.join(OUT, '..', 'build')) else os.devnull, 'w', encoding='utf-8') as f:
    f.write('credit as printed\tcount\n' + ''.join(f'{k}\t{v}\n' for k, v in rejected_credits.most_common()))

# ---------------------------------------------------------------- own or borrowed tune (2026-11-23)
# Zahn prints each tune under the text it first appeared with. For a Zahn-register link (own / supplement), l[5] = 1 when
# that heading is this text (the tune first appeared with it: its own tune), 0 when the heading is another text (the hymn
# borrowed an older tune), '' when the register's first line is too short to tell. Other links get ''.
def _words(s):
    s = ''.join(c for c in unicodedata.normalize('NFKD', (s or '').lower()) if not unicodedata.combining(c))
    s = s.replace('th', 't').replace('y', 'i').replace('ß', 'ss')
    return re.sub(r'\[[^\]]*\]|\([^)]*\)', ' ', s)
def _key(s):
    return re.sub(r'[^a-z ]', '', _words(s)).split()
_tune_head = {u[0]: u[5] for u in tunes}
_nat = collections.Counter()
for l in links:
    v = ''
    if l[2] in ('own', 'supp') and l[1] in _tune_head:
        a, b = _key(texts[l[0]][2]), _key(_tune_head[l[1]])
        k = min(len(a), len(b), 4)
        if k >= 2 and len(a) >= 2:
            v = 1 if (a[:k] == b[:k] or difflib.SequenceMatcher(None, ' '.join(a[:k]), ' '.join(b[:k])).ratio() >= 0.85
                      or (k >= 3 and a[1:k] == b[1:k])) else 0
    l.append(v)
    _nat[(l[2], v)] += 1
print('own/borrowed:', dict(_nat))

# ---------------------------------------------------------------- public-domain guidance (2026-11-22)
# t[10] = pd | pd70 | cr | '' (unknown), t[11] = reason. Guidance only, not legal advice.
#   pd   printed in a book before 1931 (US public domain), hymnary says Public Domain, or every credited person died by 1930
#   pd70 every credited person died 1931-1955 and no printing before 1931 found: public domain where the term is life + 70; check the US
#   cr   hymnary gives a copyright notice, or a credited person died 1956 or later (or was born 1900 or later)
_hy_year = {h['code']: int(h['year']) for h in hymnals if str(h.get('year') or '').isdigit()}
_first_print = {}
for a in appear:
    y = _hy_year.get(a[1])
    if y and (a[0] not in _first_print or y < _first_print[a[0]][0]):
        _first_print[a[0]] = (y, a[1])
_persons = collections.defaultdict(list)
for p in plist:
    for tid in p['t']:
        _persons[tid].append(p)
_copyright = {}
for r in rd('en_texts.csv'):
    col = next((c for c in r if c.startswith('Copyright (hymnary')), None)
    if col and r[col].strip():
        _copyright[r['EN ID']] = r[col].strip()
def _yr(v):
    return int(v) if str(v or '').isdigit() else None
for tid, t in texts.items():
    fp = _first_print.get(tid)
    ty = _yr(t[8])
    cpr = _copyright.get(tid, '')
    ps = _persons.get(tid, [])
    deaths = [_yr(p.get('died')) for p in ps]
    if any(p.get('auth') in ('carver', 'neuendorf') for p in ps):   # living translators
        deaths = [d if p.get('auth') not in ('carver', 'neuendorf') else 9999 for d, p in zip(deaths, ps)]
    births = [_yr(p.get('born')) for p in ps]
    code, why = '', ''
    if ty and ty < 1931:
        code, why = 'pd', f'first printed {ty}'
    elif fp and fp[0] < 1931:
        code, why = 'pd', f'printed in {fp[1]} ({fp[0]})'
    elif 'public domain' in cpr.lower() and '©' not in cpr:
        code, why = 'pd', 'hymnary.org: Public Domain'
    elif '©' in cpr or 'permission' in cpr.lower():
        code, why = 'cr', 'hymnary.org: ' + cpr[:120]
    elif ps and all(d and d <= 1930 for d in deaths):
        code, why = 'pd', 'all credited persons died by ' + str(max(deaths))
    elif any((d and d >= 1956) or (not d and b and b >= 1900) for d, b in zip(deaths, births)):
        code, why = 'cr', 'a credited person died 1956 or later, or is living'
    elif ps and all(d and d <= 1955 for d in deaths):
        code, why = 'pd70', 'all credited persons died by ' + str(max(deaths)) + '; first printing found is 1931 or later'
    if code == 'pd' and '©' in cpr:
        why += '; hymnary.org gives a copyright notice for a later version: ' + cpr[:100]
    t[10:] = [code, why]
_pdc = collections.Counter(t[10] for t in texts.values())
print('public domain guidance:', dict(_pdc))

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
        'base': (lambda m: f'DATA v{m.group(1)}, Zahn master v{m.group(2)}, Zahn texts and links v{m.group(3)}' if m else '')(
            re.search(r'DATA v(\d+), Zahn master v(\d+) and Zahn texts and links v(\d+)', open(os.path.join(REL, 'README.md'), encoding='utf-8').read())),
        'texts': len(texts), 'langs': langs, 'tunes': len(tunes), 'links': len(links),
        'appearances': len(appear), 'hymnals': len(hymnals), 'people': len(plist)}
dump('meta.json', meta)
print(json.dumps(meta, ensure_ascii=False))
print(sizes, 'details', dsz, len(details), 'files')
print('badges parent', collections.Counter(t[6] for t in texts.values() if t[5]))
print('badges links', collections.Counter((l[2], l[3]) for l in links))
print('unnamed hymnals', [h['code'] for h in hymnals if not h['named']])
