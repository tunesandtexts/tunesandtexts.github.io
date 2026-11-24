"""Apply the curated authority list (authority_seed + authority_gnd) to the people index built by people_clean.
Each index entry whose sort form is listed for an authority person is merged into that person, which then
carries the preferred name, dates, GND and VIAF."""
import re, unicodedata
import os
from authority_seed import P as P1
from authority_gnd import G
from authority_seed2 import P2, ADD
P = [(k, n, b, d, r, f + ADD.get(k, [])) for k, n, b, d, r, f in P1] + P2
G = dict(G)
for _l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gnd_round2_raw.txt'), encoding='utf-8'):
    _k, _g, _n, _b, _d, _v, _s = _l.rstrip('\n').split('|')
    G[_k] = (_g, _b, _d, _v, 'check' if _s == 'check' else 'ok')

def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).lower().strip()

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', fold(s)).strip('-')

def apply(people):
    form2key = {}
    for key, name, b, d, role, forms in P:
        for f in forms:
            form2key[fold(f)] = key
    by_key, out, used = {}, [], set()
    for p in people:
        k = form2key.get(fold(p['sort']))
        if not k:
            out.append(p); continue
        used.add(fold(p['sort']))
        if k not in by_key:
            by_key[k] = {'forms': [], 't': set(), 'm': set(), 'variants': []}
        a = by_key[k]
        a['forms'].append(p['name']); a['t'].update(p['t']); a['m'].update(p['m'])
        a['variants'].extend([p['name']] + p.get('variants', []))
    for key, name, b, d, role, forms in P:
        if key not in by_key:
            continue
        a = by_key[key]
        g = G.get(key)
        born, died = (g[1] or str(b or ''), g[2] or str(d or '')) if g else (str(b or ''), str(d or ''))
        disp = re.sub(r'^(.*?), (.*?)( \(.*\))?$', lambda m: m.group(2) + ' ' + m.group(1) + (m.group(3) or ''), name) if ',' in name and not re.search(r'Herzog|Landgraf|Graf|Fürstin', name) else name
        seen, var = set(), []
        for v in a['variants']:
            if v != disp and v not in seen:
                seen.add(v); var.append(v)
        e = {'name': disp, 'sort': name, 'letter': (fold(name)[:1] or '#'), 't': sorted(a['t']), 'm': sorted(a['m']),
             'variants': var[:16], 'born': born, 'died': died, 'role': role, 'auth': key}
        if g:
            e['gnd'] = g[0]
            if g[3]: e['viaf'] = g[3]
            if g[4] == 'check': e['check'] = 1
        out.append(e)
    missing = sorted(f for f in form2key if f not in used)
    return out, by_key, missing
