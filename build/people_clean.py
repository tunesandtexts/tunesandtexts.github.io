"""Author / translator / composer index for the Tunes and Texts site (2026-11-20, owner feedback).

Takes the credit strings as the sources print them ("B. Schmolck, d. 1737", "Mel. v. A. Hammerschmid",
"asc. Justus Gesenius, d. 1673", "Rist, Johann") and returns clean personal names, then groups the
spellings of one person under one entry:
  * dates, "d."/"b."/"fl."/"c.", question marks, notes in brackets and prefixes such as Mel. v., asc., after,
    tr., Dr., Rev. are removed; "Surname, Given" is turned round;
  * strings that are not names (Catholic church, Latin hymn, God, reworking, incerti, a hymnal title …) are dropped;
  * spellings are grouped by a loose surname key (Hammerschmid/Hammerschmidt, Fritsch/Fritzsch, Schmolck/Schmolcke)
    and joined when the given names agree: initials join the one full name they fit (J. Rist -> Johann Rist),
    a bare surname joins only when that surname has a single person.
The printed forms are kept as 'variants' for the site. Nothing in the data files is changed.
"""
import re, unicodedata, collections

PARTICLES = {'v.', 'v', 'von', 'van', 'der', 'den', 'de', 'zu', 'la', 'le', 'du', 'of', 'di', 'da', 'y', 'und', 'ten', 'vom'}
NOBLE = re.compile(r'(Braunschw|Wolfenb|Hessen|Sachsen|Saxe|Schwarzburg|Brandenburg|Württemb|Preuß|Prussia|\bLandgraf|\bHerzog|Herzogin|Graf|Gräfin|Duke|Duchess|Count|Countess|Landgr\w*|Fürst\w*|Prinz\w*|Prince\w*|King|Queen|Markgraf\w*|Kurfürst\w*|Elector)\b')
JUNK_WORDS = {
    'mel', 'melodie', 'melody', 'gesangbuch', 'gesangb', 'gb', 'kirche', 'church', 'catholic', 'hymn', 'hymnal', 'hymns', 'psalter',
    'version', 'text', 'latin', 'german', 'english', 'danish', 'golden', 'abc', 'cantionale', 'anhang', 'zeugnis', 'kantate', 'song',
    'secular', 'brethren', 'brüdergemeine', 'liedersammlung', 'liederlust', 'osterhymnus', 'tageweis', 'jahrh', 'schleswig', 'holstein',
    'god', 'incerti', 'incertus', 'autoris', 'anon', 'anonymous', 'unknown', 'unbekannt', 'reworking', 'appears', 'after', 'asc',
    'thy', 'xx', 'alter', 'aus', 'auf', 'nach', 'nobis', 'etc', 'collection', 'source', 'sources', 'see', 'traditional', 'trad',
    'folk', 'volksweise', 'choral', 'chorale', 'psalm', 'ps', 'tune', 'from', 'by', 'in', 'the', 'and', 'with', 'römische',
    'romische', 'römisch', 'rom', 'anonym', 'tafel', 'music', 'musik', 'zugeschrieben', 'oder', 'tafel-music', 'tafel-musik', 'herzens-music', 'anonymus', 'unkn', 'ukjent', 'dansk', 'gebetbuch', 'souterliedekens', 'stuttgart', 'weimar', 'umbildung', 'proverbs', 'his', 'dichter', "sychar's", 'vulpii', 'ohne', 'zweifel', 'vermutlich', 'vielleicht', 'wahrscheinlich', 'breviary', 'brevier', 'missal', 'sequence', 'hymnary', 'page', 'credits', 'both', 'probably',
    'very', 'not', 'test', 'burg', 'leipzig', 'nürnberg', 'wittenberg', 'erfurt', 'straßburg', 'strassburg', 'bohemian', 'moravian',
    'unitas', 'fratrum', 'synod', 'liturgy', 'liturgical', 'office', 'antiphon', 'responsory', 'stanza', 'stanzas', 'st', 'verse',
    'altered', 'alt', 'tr', 'trans', 'cento', 'paraphrase', 'based', 'original', 'orig', 'formed', 'older', 'melodies', 'two',
    'gezogen', 'einer', 'dem', 'des', 'ebenfalls', 'angeblich', 'übertragung', 'sünder', 'spaten', 'für', 'lat', 'holländischen',
}
LONE_JUNK = {'herzog', 'lady', 'mrs', 'mr', 'miss', 'madame', 'baron', 'sir', 'rev', 'dr', 'bishop', 'father', 'brother', 'sister', 'saint', 'st'}
TITLES = re.compile(r'^(?:(?:Dr|Mag|Rev|Prof|Bp|Bishop|Pastor|Inspector|Superint|Pfarrer|Kantor|Cantor|Herr|Lord|Sir)\.?\s+)+')
PREFIX = re.compile(r'^(?:à\s*\d+\s*|Aut\.\s*mel\.\s*|Arien\w*\s+v\.\s*|Mel\.?\s+(?:\w+\s+)*?(?:v\.|von|bei(?:\s*\(von\?\))?)\s+|Mel\.?\s+|'
                    r'asc(?:ribed)?\.?\s*(?:to\s+)?|attr(?:ibuted)?\.?\s*(?:to\s+)?|after\s+|ad\.\s+|tr\.\s+|trans\.\s+|by\s+|von\s+|v\.\s+|'
                    r'nach\s+|bei\s+|\?\s*)+', re.I)
LOWER_PREFIX = re.compile(r'^(?:a\.|b\.|ad\.)\s+')


def ascii_fold(s):
    s = s.replace('ß', 'ss').replace('Æ', 'Ae').replace('æ', 'ae').replace('ø', 'o').replace('Ø', 'O')
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def split_credit(s):
    s = re.sub(r'\s+', ' ', (s or '').replace(' ', ' ')).strip()
    parts = re.split(r'\s*(?:;|\s/\s|\s\|\s|\s&\s|\sand\s|\sund\s|\soder\s|\sor\s)\s*', s)
    return [p for p in parts if p]


def clean_one(s, _tail=True):
    s = s.replace('(?)', ' ').strip(' ,.;:')
    if s.startswith('(') and s.count('(') == 1:
        s = s.strip('()? ')
    m = re.match(r'^(.*?)\s*\(([^)]*)\)?', s)
    if m and m.group(2) and re.fullmatch(r'(?:Mel\.\s*(?:v\.|von)\s*)?(?:[A-ZÄÖÜ][a-z]{0,2}\.\s*)+', m.group(1).strip()) and re.match(r'^[A-ZÄÖÜ][a-zäöüß]+', m.group(2)):
        s = m.group(2)                            # "Mel. v. W. W. (Weßnitzer)" -> "Weßnitzer"
    s = re.sub(r'^(?:[A-ZÄÖÜ]\w+,\s*)?(?:ohne Zweifel|vermutlich|vermutl\.|vielleicht|wahrscheinlich|angeblich)\s+(?:v\.|von)\s+', '', s)
    s = re.sub(r'^(?:Komposition|Tonsatz|Satz|Text|Bearbeitung|Umbildung|Mel\.\s*u\.\s*\w+)\b[^A-Z]*?(?:v\.|von)\s+', '', s)
    s = PREFIX.sub('', s)
    s = LOWER_PREFIX.sub('', s)
    s = re.sub(r'\s*\(.*$', '', s)               # notes in brackets (and an unclosed bracket) to the end
    s = re.sub(r'\s*["“„].*$', '', s)             # quoted first lines
    s = re.sub(r'\s*(?:†|\bd\.|\bb\.|\bfl\.|\bc\.|\bca\.|\bum\b|\bst\.|\btest\.|\bcirca\b).*$', '', s)
    s = re.sub(r'[,\s]*\d.*$', '', s)             # first number (a year, a stanza no.) to the end
    s = re.sub(r',\s*(?:[a-z]|Pfarrer|Kantor|Pastor|Organist|Superint|Bishop|Rector|Kapellmeister|Hofprediger).*$', '', s)
    s = re.sub(r'\s+(?:sen|jun|zugeschrieben|recte)\b.*$', '', s)
    s = s.replace('?', '').strip(' ,.;:-')
    s = TITLES.sub('', s)
    # "Surname, Given" -> "Given Surname" (not for titles such as "Albert, Duke of Prussia")
    m = re.match(r'^([A-ZÄÖÜÆØÅ][\w\'’-]+),\s*([A-ZÄÖÜ][\w.]*(?:\s+[A-ZÄÖÜ][\w.]*){0,2})$', s)
    if m and not NOBLE.search(s):
        s = m.group(2) + ' ' + m.group(1)
    s = re.sub(r'\s*,\s*', ', ', s).strip(' ,.')
    if s.endswith('.') and not re.search(r'\b[A-Z]\.$', s):
        s = s[:-1]
    if _tail and s and not is_name(s):
        m = list(re.finditer(r'\b(?:v\.|von|bei)\s+(?=[A-ZÄÖÜ])', s))
        if m:
            return clean_one(s[m[-1].end():], False)
    return s


def is_name(s):
    if len(s) < 3 or re.search(r'[\d:"“”„=/\[\]]', s):
        return False
    toks = s.replace(',', ' ').split()
    low = [ascii_fold(t).lower().strip('.\'’') for t in toks]
    if any(l in {ascii_fold(w) for w in JUNK_WORDS} for l in low):
        return False
    if len(toks) == 1 and low[0] in LONE_JUNK:
        return False
    if not toks[0].endswith('.') and low[0] in {'of', 'the', 'a', 'an', 'in', 'on', 'for', 'to', 'komposition', 'tonsatz', 'satz', 'herr', 'frau'}:
        return False
    if toks[0][0].islower():
        return False
    for t, l in zip(toks, low):
        if t[0].islower() and l not in PARTICLES and not t.startswith(("d'", "l'")):
            return False
    if all(re.fullmatch(r'[A-ZÄÖÜ]\.?', t) for t in toks):   # initials only ("A. K.")
        return False
    return True


def parts(name):
    """(given tokens, surname, sort surname) for a clean name."""
    toks = name.replace(',', ' ').split()
    if NOBLE.search(name):
        core = [t for t in toks if not NOBLE.search(t) and t.lower().strip('.,') not in PARTICLES]
        return toks, ' '.join(core[:2]), core[0] if core else toks[0]
    i = len(toks) - 1
    sur = [toks[i]]
    while i - 1 >= 1 and toks[i - 1].lower().strip('.') in PARTICLES:
        i -= 1; sur.insert(0, toks[i])
    given = toks[:i]
    real = [t for t in sur if t.lower().strip('.') not in PARTICLES] or sur
    return given, ' '.join(sur), real[-1]


def sur_key(sur):
    s = ascii_fold(sur).lower()
    s = re.sub(r'[^a-z]', '', s)
    for a, b in [('tzsch', 'sch'), ('tsch', 'sch'), ('dt', 't'), ('th', 't'), ('ck', 'k'), ('ph', 'f'), ('ie', 'i'), ('y', 'i'), ('tz', 'z')]:
        s = s.replace(a, b)
    s = re.sub(r'(.)\1+', r'\1', s)
    s = s[:-1] if s.endswith('e') and len(s) > 4 else s
    return s[:-1] + 't' if s.endswith('d') else s


def initial(t):
    return ascii_fold(t)[0].upper()


def full_given(given):
    return [g for g in given if len(g.rstrip('.')) > 2 and not g.endswith('.')]


# English, Latin and Danish forms of German given names count as the same name (Philip = Philipp, Frederick = Friedrich)
GIVEN_EQ = {}
for group in ['johann johannes john johan jan joh hans', 'philipp philip philippus phil', 'friedrich frederick frederik friederich fridericus', 'christoph christopher christophorus',
              'heinrich henry henrik henricus', 'georg george georgius jorgen', 'karl carl charles carolus', 'matthaus matthew matthaeus mattheus', 'paul paulus',
              'jakob jacob jacobus james', 'wilhelm william guilielmus', 'ludwig lewis louis ludovicus', 'martin martinus', 'michael michel', 'nikolaus nicolaus nicholas nicolai niels',
              'ernst ernest ernestus', 'andreas andrew', 'petrus peter pieter', 'thomas tomas', 'joachim', 'balthasar balthaser', 'gottfried godfrey', 'katharina catherine catharina',
              'sebastian bastian', 'salomo salomon solomon', 'kaspar caspar casparus jasper', 'melchior', 'valentin valentinus', 'bartholomaus bartholomew', 'erdmann erdman',
              'benjamin', 'david', 'emilie emily aemilie', 'luise louisa louise', 'elisabeth elizabeth', 'anna anne', 'maria mary']:
    words = group.split()
    for w in words:
        GIVEN_EQ[w] = words[0]


def gnorm(z):
    z = ascii_fold(z).lower().rstrip('.')
    full = GIVEN_EQ.get(z)
    if full:
        return full
    return re.sub(r'(.)\1+', r'\1', z.replace('ph', 'f').replace('th', 't').replace('c', 'k').replace('y', 'i'))


def compatible(g_short, g_long):
    """Do these given-name lists fit one person? J. -> Johann, Joh. -> Johann, Ahasv. -> Ahasverus."""
    if not g_short:
        return True
    a = [g for g in g_short if g.lower().strip('.') not in PARTICLES]
    b = [g for g in g_long if g.lower().strip('.') not in PARTICLES]
    if len(a) > len(b):
        return False
    for x, y in zip(a, b):
        xs, ys = gnorm(x), gnorm(y)
        if not (x.endswith('.') or len(xs) <= 2 or y.endswith('.') or len(ys) <= 2):
            if xs == ys or (len(xs) >= 4 and len(ys) >= 4 and (xs.startswith(ys) or ys.startswith(xs))):
                continue
            if GIVEN_EQ.get(ascii_fold(x).lower()) and GIVEN_EQ.get(ascii_fold(y).lower()):
                return False                                   # two different known names (Johann / Jakob)
            import difflib
            if difflib.SequenceMatcher(None, xs, ys).ratio() >= 0.8:   # Salamo / Salomo, Freidrich / Friedrich
                continue
            return False
        # abbreviations: compare the folded raw letters
        xs, ys = re.sub(r'(.)\1+', r'\1', ascii_fold(x).lower().rstrip('.').replace('ph', 'f').replace('c', 'k')), re.sub(r'(.)\1+', r'\1', ascii_fold(y).lower().rstrip('.').replace('ph', 'f').replace('c', 'k'))
        if x.endswith('.') or len(xs) <= 2 or y.endswith('.') or len(ys) <= 2:
            k = min(len(xs), len(ys))
            if xs[:k] != ys[:k]:
                return False
        elif xs != ys and not (ys.startswith(xs) or xs.startswith(ys)):
            return False
    return True


def build(entries):
    """entries: list of (credit string, kind 't'|'m', record id). Returns (people list, rejected Counter, raw->slugs map)."""
    raw_clean = collections.defaultdict(list)   # clean name -> [(kind, id, raw)]
    rejected = collections.Counter()
    for credit, kind, rid in entries:
        for p in split_credit(credit)[:4]:
            c = clean_one(p)
            if c and is_name(c):
                raw_clean[c].append((kind, rid, p))
            elif p.strip():
                rejected[p.strip()] += 1
    groups = collections.defaultdict(list)       # surname key -> clean names
    for c in raw_clean:
        g, sur, sortsur = parts(c)
        groups[sur_key(sur) if not NOBLE.search(c) else 'noble:' + ascii_fold(sur).lower()].append(c)
    # an abbreviated surname (Prätor.) joins the one longer surname it begins
    for k in sorted(groups, key=len):
        if k.startswith('noble:') or len(k) < 6:
            continue
        longer = [o for o in groups if o != k and o.startswith(k) and not o.startswith('noble:')]
        if len(longer) == 1:
            groups[longer[0]].extend(groups.pop(k))
    people = []
    for key, names in groups.items():
        if key.startswith('noble:'):
            cl = names
            best = min(cl, key=lambda n: (n.count('.'), -len(n)))
            t, m, raws = [], [], collections.Counter()
            for n in cl:
                for kind, rid, raw in raw_clean[n]:
                    (t if kind == 't' else m).append(rid); raws[raw] += 1
            people.append({'name': best, 'sort': best, 'letter': (ascii_fold(best)[:1] or '#').lower(),
                           't': sorted(set(t)), 'm': sorted(set(m)), 'variants': [r for r, _ in raws.most_common() if r != best][:12]})
            continue
        info = {n: parts(n) for n in names}
        cnt = {n: len(raw_clean[n]) for n in names}
        # clusters seeded by names with a full given name, most complete first
        seeds = sorted([n for n in names if full_given(info[n][0])],
                       key=lambda n: (-len(full_given(info[n][0])), -cnt[n], n))
        clusters = []
        for n in seeds:
            for cl in clusters:
                if compatible(info[n][0], info[cl[0]][0]) or compatible(info[cl[0]][0], info[n][0]):
                    cl.append(n); break
            else:
                clusters.append([n])
        rest = [n for n in names if n not in seeds]
        loose = []
        for n in rest:
            g = info[n][0]
            fits = [cl for cl in clusters if compatible(g, info[cl[0]][0])]
            if g and len(fits) == 1:
                fits[0].append(n)
            elif not g and len(clusters) == 1:
                clusters[0].append(n)
            else:
                loose.append(n)
        # initials-only forms that fit no full name: group by their initials
        byinit = collections.defaultdict(list)
        for n in loose:
            byinit[' '.join(initial(t) for t in info[n][0] if t.lower().strip('.') not in PARTICLES)].append(n)
        for ini, ns in byinit.items():
            ns.sort(key=lambda n: (-len(info[n][0]), -cnt[n], n))
            clusters.append(ns)
        bare = [cl for cl in clusters if all(not info[n][0] for n in cl)]
        other = [cl for cl in clusters if any(info[n][0] for n in cl)]
        if bare and len(other) == 1:                 # "Lobwasser" joins "A. Lobwasser" when it is the only one
            for cl in bare:
                other[0].extend(cl); clusters.remove(cl)
        for cl in clusters:
            best = max(cl, key=lambda n: (len(full_given(info[n][0])), len(info[n][0]), cnt[n], -len(n)))
            g, sur, sortsur = info[best]
            t, m, raws = [], [], collections.Counter()
            for n in cl:
                for kind, rid, raw in raw_clean[n]:
                    (t if kind == 't' else m).append(rid); raws[raw] += 1
            sort = (sortsur + (', ' + ' '.join(x for x in g) if g else '')) if not NOBLE.search(best) else best
            people.append({'name': best, 'sort': sort, 'letter': (ascii_fold(sortsur)[:1] or '#').lower(),
                           't': sorted(set(t)), 'm': sorted(set(m)),
                           'variants': [r for r, _ in raws.most_common() if r != best][:12]})
    return people, rejected, raw_clean
