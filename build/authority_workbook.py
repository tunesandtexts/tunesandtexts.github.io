"""Write the authority-list review workbook from authority.P / authority.G and a built people.json."""
import json, sys, openpyxl
from openpyxl.styles import Font, PatternFill
import authority
from authority_seed2 import P2, NONE2
people_json, out = sys.argv[1], sys.argv[2]
r2 = {k for k, *_ in P2}
p = json.load(open(people_json, encoding='utf-8'))
byk = {x['auth']: x for x in p if 'auth' in x}
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Persons'
ws.append(['Key', 'Round', 'Preferred name', 'Born', 'Died', 'Role', 'GND', 'GND link', 'VIAF', 'Status', 'Texts', 'Tunes',
           'Index forms merged', 'Other printed forms', 'Your notes'])
yellow = PatternFill('solid', fgColor='FFF2CC'); red = PatternFill('solid', fgColor='F8CBAD')
for key, name, b, d, role, forms in authority.P:
    x = byk.get(key, {}); g = authority.G.get(key)
    rnd = 2 if key in r2 else 1
    if rnd == 1:
        st = 'approved (round 1)'
    else:
        st = 'GND ok' if g and g[4] == 'ok' else ('GND – check' if g else 'no GND record found')
    ws.append([key, rnd, name, (g[1] if g and g[1] else b) or '', (g[2] if g and g[2] else d) or '', role, g[0] if g else '',
               f'https://d-nb.info/gnd/{g[0]}' if g else '', g[3] if g else '', st, len(x.get('t', [])), len(x.get('m', [])),
               ' | '.join(forms), ' | '.join(v for v in x.get('variants', []) if v not in forms)[:400], ''])
    if st in ('GND – check', 'no GND record found'):
        for c in ws[ws.max_row]: c.fill = yellow if g else red
    if g: ws.cell(ws.max_row, 8).hyperlink = f'https://d-nb.info/gnd/{g[0]}'
ws2 = wb.create_sheet('Forms'); ws2.append(['Index form (before)', 'Person key', 'Preferred name', 'Round'])
for key, name, b, d, role, forms in authority.P:
    for f in forms: ws2.append([f, key, name, 2 if key in r2 else 1])
ws3 = wb.create_sheet('Next round'); ws3.append(['Index form', 'Texts', 'Tunes', 'Printed forms', 'Suggested action'])
rest = sorted([x for x in p if 'auth' not in x], key=lambda x: -(len(x['t']) + len(x['m'])))
for x in rest:
    if len(x['t']) + len(x['m']) < 5: break
    ws3.append([x['sort'], len(x['t']), len(x['m']), ' | '.join(x.get('variants', []))[:300], ''])
tot = sum(len(x['t']) + len(x['m']) for x in p); a = sum(len(x['t']) + len(x['m']) for x in byk.values())
ws4 = wb.create_sheet('About')
for l in ['Authority list, draft 2 (2026-11-22), built from Tunes and Texts DATA v92.',
          'Round 1 (225 persons) was approved by the owner on 2026-11-22. Round 2 adds the next index entries with 5 or more credits.',
          'Yellow = GND record found but not certain. Red = no GND record found; dates come from hymnological reference works.',
          'Left out of round 2 and kept as printed (not identified with confidence): bare surnames that mix two people (Herrmann, Nicolai, Hille, Wagner, Lange, Fischer),',
          'and Weberbeck, Hartmann, Gratz, Bäßler, Keßler, Bierling, Welter, Winer, Tscherlitzky, Zollikofer, Scheibner, Günther, Jung, Beutler, Schott, Weber G., Wagner C./J. Chr., Gerber, Pezolt, Weida, Lehmann, Ritter A. F., Herrmann J. C., Anderson J., Jonassøn, Ægidius, Kinchen, Lowe, Spaiser, Overholt, Sloan, Cramer C., Salomon, Trümper.',
          f'Coverage: {len(byk)} persons cover {a:,} of {tot:,} author/composer credits ({100*a/tot:.1f}%). The index has {len(p):,} entries (was 2,002).']:
    ws4.append([l])
for w in (ws, ws2, ws3):
    for c in w[1]: c.font = Font(bold=True)
    w.freeze_panes = 'A2'
for col, wd in zip('ABCDEFGHIJKLMNO', [16, 6, 38, 7, 7, 16, 12, 30, 14, 18, 6, 6, 40, 50, 30]): ws.column_dimensions[col].width = wd
for col, wd in zip('ABCD', [34, 16, 38, 7]): ws2.column_dimensions[col].width = wd
for col, wd in zip('ABCDE', [34, 7, 7, 60, 30]): ws3.column_dimensions[col].width = wd
ws4.column_dimensions['A'].width = 140
wb.save(out)
print(len(authority.P), ws3.max_row - 1, sum(1 for r in ws.iter_rows(min_row=2, values_only=True) if r[1] == 2 and r[9] != 'GND ok'))
