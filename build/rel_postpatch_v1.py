"""Release 0.9 doc fixes after docs_v5 + docs_patch (2026-11-23). Usage: python3 rel_postpatch_v1.py <release dir> <Zahn texts version, e.g. 12> <date>
 - 'fixed in DATA v9x' -> v90 (docs_v5 rewrites the QC-of-v89 sentence with the current DATA version)
 - Zahn texts and links version and the review date in the README
 - data dictionary: the renamed Text-Tune columns, persons.csv, text_guidance.csv, 'First line before spell check'
 - README: one line on the files new in this build"""
import re, sys
R, ZV, DATE = sys.argv[1:4]
f = f'{R}/README.md'; s = open(f, encoding='utf-8').read()
s = re.sub(r'fixed in DATA v9\d', 'fixed in DATA v90', s)
s = re.sub(r'Zahn texts and links v\d+', f'Zahn texts and links v{ZV}', s)
s = re.sub(r'under review \(2026-11-\d\d\)', f'under review ({DATE})', s)
if 'persons.csv' not in s:
    s = s.replace('## ', f'**New in this build ({DATE}):** `data/core/persons.csv` (authority list of 377 authors, translators and composers with dates and GND/VIAF IDs) and `data/core/text_guidance.csv` (place in the family tree, own/borrowed tunes, copyright guidance per text); German and Danish first lines spell/OCR-checked.\n\n## ', 1)
open(f, 'w', encoding='utf-8').write(s)
f = f'{R}/DATA_DICTIONARY.md'; s = open(f, encoding='utf-8').read()
s = s.replace('| Tune in Zahn vol. | 11,789 | II | — |', '| Tune in Zahn vol. | 11,789 | II | Volume of Zahn that holds the tune (I–V; "V (Ergänzungen)" = the supplements). Not the volume of the register. |')
s = s.replace('| Register page (Zahn vol. V) | 11,789 | 501 | — |', '| Register page (Zahn vol. V) | 11,789 | 501 | Page of Zahn\'s first-line register, which is printed in Band V, pp. 501–556. |')
if 'persons.csv (core' not in s:
    s += '''

## persons.csv (core, added 2026-11-23)
Authority list: one row per identified author, translator or composer. **Person key** stable ID; **Preferred name** "Surname, Given"; **Name (display)**; **Born / Died** years (German National Library GND where it has the person, otherwise hymnological reference works); **Role**; **GND / GND URL / VIAF** authority-file IDs; **Texts (n) / Tunes (n)** and **Text IDs / Zahn nos.** the texts and tunes credited to the person; **Printed forms** the credits as printed in the sources that were merged into this person. 377 persons, about 83 % of author/composer credits; the rest stay as printed.

## text_guidance.csv (core, added 2026-11-23)
One row per text. **Place in family tree**: original (no original linked above it) or translation; **Original (top of tree)** the text at the top. **Original's own tune(s)**: Zahn tunes of the original that Zahn prints under the original itself (they first appeared with it). **Original's borrowed tune(s)**: tunes the original was sung to that Zahn prints under another text (an original with only "also sung to" tunes counts as borrowed). **Other melodies**: tunes linked to this text that the original does not have. **Copyright status (guidance)**: public domain (printed in a book before 1931, hymnary.org "Public Domain", or every credited person died by 1930) / likely public domain, life + 70 (every credited person died 1931–1955, no printing before 1931 found) / probably in copyright (hymnary.org © notice, or a credited person died 1956 or later or is living) / not known; **Copyright basis** the reason. Guidance from dates, not legal advice.

**First line before spell check (2026-11-23)** (scandinavian_texts, de_texts_added, zahn_texts): the first line before the 2026-11-23 spell/OCR check of German and Danish first lines; empty where nothing changed.
'''
open(f, 'w', encoding='utf-8').write(s)
print('ok')
