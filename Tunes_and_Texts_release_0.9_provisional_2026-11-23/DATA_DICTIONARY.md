# Data dictionary — Tunes and Texts: Lutheran Hymns in German, Scandinavian and English, release 0.9 (provisional, under review)

Generated 2026-11-20 from the 0.9 CSV export (DATA v95, Zahn tune master v16, Zahn texts and links v9; columns trimmed per SOURCE_AUDIT.csv are not listed). One section per CSV file: every column, how many rows have a value, an example, and what it means. Columns ending in **URL** hold the link that the spreadsheet cell to their left carried (Zahn scan, hymnary.org page, Julian page, source scan).

**IDs:** tunes = Zahn no. (with a/b/c variant); texts = DE-/DA-/NO-/SV-/FI-/CS-/SK-/PL-/ES- + number (DE-00001–05897 from Zahn's register, higher DE numbers added by us — provisional unless a source is given); English = EN-xxxxx; sources = vol. VI bibliography numbers.
**Status words:** confirmed (checked against the source or two agreeing sources) / probable / check (needs a look) / structural (implied by another link).
**Evidence tags in 'DE link basis' (Julian rows, DATA v24 on):** PR printed page (certain) · SC Julian's scanned text, IMSLP copy (probable) · JV Julian 1907 scanned text, archive.org (probable) · KN Claude's judgement only (probable).
**Anonymisation:** the project owner's review columns are headed "Owner's review …"; notes say "owner".
**REJECTED links** are kept, never deleted: Status 'REJECTED (who, date: why) | was: …'. **DUPLICATE** German texts are kept and name the text that replaces them.

## Core tables (the database proper)

### en_texts.csv (7,389 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'EN Texts'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| EN ID | 7,389 | EN-00001 | Project ID of an English text: one per distinct first line per translator. |
| English first line | 7,389 | All Glory Be to God on High | English first line. |
| hymnary | 7,389 | ▶ hymnary text | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 7,389 | https://hymnary.org/text/all_glory_be_to_god_on_high_and_tha | Link carried by 'hymnary' (as a URL). |
| Translated from (DE ID) | 6,228 | DE-00295 | The German (or Danish…) text this translates. |
| DE link basis | 7,368 | exact; confirmed by hymnary German-title search 2026-11-08 | How the German link was made, and how sure it is (e.g. "probable"). |
| German first line (KGB 1862) | 439 | Allein Gott in der höh' sei ehr | German first line in the spelling of the Kirchen-Gesangbuch 1862 index. |
| KGB no. | 439 | 1 | Number in the Kirchen-Gesangbuch 1862. |
| Authors (hymnary) | 2,893 | Catherine Winkworth; Nikolaus Decius / Gilbert E. Doan, 1930 | Author/translator credits as hymnary.org gives them. |
| Tune names (hymnals) | 1,151 | ALLEIN GOTT IN DER HOEH SEI EHR / ALLEIN GOTT IN DER HÖH / A | Tune names this text is printed with in our hymnal exports. |
| Zahn tune(s) as printed in hymnals | 414 | 4457 | Zahn numbers of those tunes. |
| View tune: Zahn tune(s) as printed in hymnals | 414 | ▶ 4457 (III, p. 80) | Link to the Zahn scan of the first of those tunes. |
| View tune: Zahn tune(s) as printed in hymnals URL | 414 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: Zahn tune(s) as printed in hymnals' (as a URL). |
| Translation group (candidate) | 138 | EN-00007 | EN ID of the text this one is probably a version of (same translation, altered). |
| Hymnals | 5,179 | CW'21 935, CW'93 263, ELH 35, ELHB 261, HFCH1928 2, HOoS1901 | Hymnals (hymnary codes) or source posts the text appears in. |
| hymnary text ID | 3,198 | all_glory_be_to_god_on_high_and_thanks_f all_glory_be_to_god | hymnary.org textAuthNumber (URL: hymnary.org/text/<id>). |
| Origin | 7,389 | KGB 1862 comparison index | Where this English text entered our list (hymnary German list, Carver, Julian, KGB index …). |
| Spelling variants | 151 | All Glory Be to God on High / All glory be to God on high | Other spellings/forms of the first line seen in sources. |
| Match key (EN) | 7,388 | all glory be to god on high | Normalized first line used for matching. |
| German first line (Carver post title) | 1,955 | Kommt her und schaut, kommt | For Carver's translations: the title of his post (the German first line). |
| Translator | 3,683 | Catherine Winkworth | Translator. |
| hymnary: original language German | 3,000 | yes | yes = hymnary marks the text's original language as German. |
| Julian | 2,843 | p. 425 ii: in C. U. (Dalston Hospital H. Bh, 1848) | Julian, Dictionary of Hymnology (1907): page and note where the translation is listed. |
| Julian URL | 43 | https://archive.org/details/dictionaryofhymn02lond/page/1287 | Link carried by 'Julian' (as a URL). |
| Candidates | 66 | DE-05905; DE-05909 (KGB 53 / 78 — moved here 2026-11-13: no  | Possible German originals (ID: first line (score)) when the link is not settled. |
| ELH Handbook | 255 | ELH 35: original German "Allein Gott in der Höh’ sei Ehr’" | Note from the Evangelical Lutheran Hymnary Handbook. |
| First-line note (moved out of the first line, 2026-11-08) | 52 | x2 | Notes that had been part of the first line (e.g. "x2"), or notes on how a row was added. |
| hymnary German-title search (2026-11-08) | 662 | confirmed by hymnary search: Allein Gott in der Höh sei Ehr | Result of searching hymnary for the German title. |
| Meter (normalized) | 4,350 | 8.7.8.7.8.8.7 | Syllables per line, dot-separated; L.M./C.M./S.M. and D written out. |
| Meter source | 4,351 | hymnary | Where the meter came from (register, tunes, hymnary, inherited). |
| Free Lutheran Chorale-Book (Neuendorf, 2026-11-10) | 71 | Sts. 4–8, 9b, Christopher J. Neuendorf, 2018 (sts. 1–3, 9a T | Neuendorf credit + URL when an EN text has the same first line as one of his (often a different or older translation) |
| Hymnoglypt post (Carver) | 1,955 | https://matthaeusglyptes.blogspot.com/2008/10/kommt-her-und- | URL of Matthew Carver's Hymnoglypt blog post with this translation (added DATA v42). |
| Hymnoglypt post (Carver) URL | 1,955 | https://matthaeusglyptes.blogspot.com/2008/10/kommt-her-und- | Link carried by 'Hymnoglypt post (Carver)' (as a URL). |
| Hymnoglypt link basis (2026-11-13) | 1,955 | title | How the post was matched: by title, or by title + English first line found in the post. Where Carver revised a translation, the row listing both dates links to the later post; duplicate rows (see 'Duplicate of (EN ID)') link to the post dated as in their own 'Hymnals' cell (DATA v43). |
| Duplicate of (EN ID) | 27 | EN-00447 | Set on the later of two rows holding the same Carver translation (same post, same first line; entered twice by the 2026-11-11 gap-fill): the EN ID of the earlier row. Nothing deleted (DATA v43). |
| First line before QC (2026-11-13) | 40 | O heilige Dreifaltigkeit | The first line as it stood before the QC fix of 2026-11-13 (filled only where 'First line' / 'English first line' was repaired). |
| First-line QC (2026-11-13) | 73 | NOT A TEXT — import artifact (QC 2026-11-13, owner's answer) | QC note on the first line (2026-11-13): how it was repaired and how sure (certain / probable), or a flag — NOT A FIRST LINE / NOT AN ENGLISH (GERMAN) LINE / TITLE / check. Rows flagged NOT … are kept, not deleted; leave them out of first-line searches. |
| Translator (standard) | 4,279 | Catherine Winkworth | Translator in one standard form (full name where the source makes it clear, e.g. 'Miss Winkworth' → Catherine Winkworth; 'alt.', dates and OCR slips removed); blank where the printed value is unreadable or not a translator. 'Translator' keeps the value as printed. |
| Translator standard basis (QC 2026-11-13) | 4,325 | as printed | How 'Translator (standard)' was made: as printed / standardised (name form, title, OCR, 'alt.') / incomplete name — as printed / anonymous — book named / unreadable — left blank. |
| German link before re-check (2026-11-13) | 336 | DE-04369 / exact / German author (hymnary): possible: author | The German link and its basis before the QC re-check of 2026-11-13 (filled only on the 337 rows whose link had rested on an author guess: 'possible: …'). |
| German link re-check (QC 2026-11-13) | 356 | confirmed — confirmed: hymnary.org German Title "O Lamm Gott | Outcome of the re-check: confirmed (hymnary.org German Title), kept (probable — Claude by meaning), relinked old → new, or link removed (old ID moved to Candidates), with the basis. |
| QC2 round 1 (2026-11-14) | 11 | relinked — KGB 1862 line is Luther's 'Dies sind die heil'gen | Note from that quality-control round (what was checked or changed). |
| QC2 round 2 (2026-11-14) | 493 | relinked DE-00804 → DE-00805 (certain); hymnary credits M. C | Note from that quality-control round (what was checked or changed). |
| Copyright (hymnary, 2026-11-14) | 3,197 | © 2006 Concordia Publishing House // Tr. © 1978 Lutheran Boo | Copyright note hymnary.org gives for the text. |
| QC2 round 3 (2026-11-14) | 561 | linked to DE-05664 (probable) | Note from that quality-control round (what was checked or changed). |
| QC2 round 4 (2026-11-15) | 98 | owner 2026-11-16: 3498a, later altered form (English hymnals | Note from that quality-control round (what was checked or changed). |
| QC2 round 5 (2026-11-16) | 25 | owner 2026-11-16: Borthwick's "How blessed from the bonds of | Note from that quality-control round (what was checked or changed). |
| QC2 round 6 (2026-11-16) | 53 | KGB 1862 no. 135 and hymnary (H. Held) — Zahn DE-03275 "Komm | Note from that quality-control round (what was checked or changed). |
| QC2 round 7 (2026-11-19) | 97 | Carver's post: "Allmächtiger ewiger Gott, der du die Welt re | Note from that quality-control round (what was checked or changed). |
| Original language (QC2 r7, owner 2026-11-19) | 68 | Latin original — Zahn lists the Latin text DE-04973 "Te deum | Original language when it is not German (e.g. Latin), as decided in QC #2 round 7. |
| QC2 round 8 (2026-11-19) | 3 | Carver's post: "Gelobet sei der Herre" (L. Helmbold), 12-lin | Note from that quality-control round (what was checked or changed). |
| First line before spell check (2026-11-20) | 245 | Now our worship weet is o'er | The English first line as it stood before the spell check of 2026-11-20 (DATA v91–v92; filled only where the first line was corrected: OCR errors, typos, soft hyphens, words in capitals). |

### en_tune_links.csv (3,914 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'EN-Tune links'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| EN ID | 3,914 | EN-00001 | Project ID of an English text: one per distinct first line per translator. |
| hymnary | 3,914 | ▶ hymnary text | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 3,914 | https://hymnary.org/text/all_glory_be_to_god_on_high_and_tha | Link carried by 'hymnary' (as a URL). |
| Zahn no. | 3,914 | 4457 | Zahn melody number as used for joins (variants may be written 25.1; see Zahn no._Original). |
| View tune: Zahn no. | 3,914 | ▶ 4457 (III, p. 80) | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 3,914 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: Zahn no.' (as a URL). |
| Relation | 3,914 | Zahn: melody listed under the source text | Kind of link (printed with this tune in a hymnal / melody listed under the source text / named as Mel. …). |
| Via DE ID | 3,318 | DE-00295 | German text through which the tune link was inherited. |
| Source | 3,914 | Zahn register via Texts sheet | Where the row comes from. |
| Hymnal | 90 | CBfE1863 | Hymnal code (hymnary) or book. |
| Number | 90 | 1 | Number in that hymnal. |
| Tune name | 90 | Allein Gott in der Höh' sei Ehr' | Tune name as printed. |
| Variant family (chosen by incipit) | 45 | 624 | The variant (a/b/c) of the Zahn melody whose opening matches the printed tune. |
| View tune: Variant family (chosen by incipit) | 45 | ▶ 624 (I, p. 172) | Link to that variant's scan. |
| View tune: Variant family (chosen by incipit) URL | 45 | https://archive.org/details/1508283124bsb11304498/page/172/m | Link carried by 'View tune: Variant family (chosen by incipit)' (as a URL). |

### scandinavian_texts.csv (1,106 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Scandinavian texts'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 1,106 | DA-0001 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| Language | 1,106 | Danish | Danish / Norwegian (Bokmål, Nynorsk) / Swedish. |
| First line | 1,106 | Ak, himmelsøde Ord | First line as printed. |
| Danish first line (GGG, modern spelling) | 39 | Bort, verden, af mit sind og øje | Danish first line from Gesangbuch-GGG lists, modern spelling. |
| Owner's decision | 0 |  | The owner's decision on this row in the 2026-11-10 review (sheet column was 'Your decision'). |
| Translated from | 601 | DE-04701 | DE ID of the German original. |
| Relation | 1,075 | translation of German | Kind of link (printed with this tune in a hymnal / melody listed under the source text / named as Mel. …). |
| Translator(s) | 237 | Brorson | Translator(s). |
| Nynorsk version of | 14 | NO-0001 | Text ID of the Bokmål/Danish text this Nynorsk text renders. |
| German author(s) | 527 | L. Laurenti | Author of the German original. |
| Link status | 1,104 | review: 3 texts by this author in Zahn | How sure the link to the German original is, and how it was made (older status kept after "was:"). |
| Candidates | 503 | DE-05206: Wach auf, mein Herz, die Nacht (0.33) / DE-03979:  | Possible German originals (ID: first line (score)) when the link is not settled. |
| Credits (hymnary) | 407 | SLKA1919: Lau. Laurenti; Brorson | Credits as hymnary gives them. |
| Hymnals | 1,104 | PSNE1890 302, SLKA1919 636 | Hymnals (hymnary codes) or source posts the text appears in. |
| Tune(s) | 490 | H.O.C. Zinck 1801 | Tunes named for this text in our sources. |
| Spelling variants | 281 | Allevegne hvor jeg vanker | Other spellings/forms of the first line seen in sources. |
| Old ID(s) | 350 | NO-0003 | Earlier IDs of this text (see ID changes sheets). |
| Note | 942 | printed unrevised in Norwegian books; NO-0003 retired → DA-0 | Notes. |
| Attribution (HM register, as printed) | 140 | Ps. 130 - Martin Luther 1524 | Attribution printed in the HM 2004 register. |
| Source | 612 | HM 2004 no. 1, Reformation hymn register no. 1 | Where the row comes from. |
| Den Danske Salmebog 2002 | 132 | no. 508: Bryd frem, mit hjertes trang at lindre | Number and first line in Den Danske Salmebog 2002. |
| First line printed in | 570 | Norwegian book | Which book the first line is taken from. |
| Match key (DA/NO spelling-normalized) | 1,102 | ak himelsøde ord | Normalized first line used for matching. |
| Meter (normalized) | 225 | 7.6.7.6.7.6.7.6 | Syllables per line, dot-separated; L.M./C.M./S.M. and D written out. |
| Meter source | 225 | Norsk salmebok 2013 meter register (Norwegian form, N13 338) | Where the meter came from (register, tunes, hymnary, inherited). |
| N13 no. (Norsk salmebok 2013) | 108 | 338 | Number in Norsk salmebok 2013. |
| N13 meter code (Haavik) | 56 | 8.26 8.0-j-7.6.7.6.7.6.7.6 | Haavik's meter code for N13. |
| N13 register (KM 2012): author / translator / melody | 88 | Gerhardt, Paul / tr. Brorson, Hans Adolph / mel. Teschner, M | N13 register entry. |
| Belsheim 1876: German original (probable) | 39 | DE-01371 (new) | Belsheim's (1876) German original, probable; existing links not changed. |
| Owner's review 2026-11-10 | 45 | yes — accepted: DE-00828: Dein Heil, o Christ, nicht zu vers | The owner's decision on this row in the 2026-11-10 review. |
| Pontoppidan 1740 review: German original (2026-11-10) | 538 | DE-00183 Ach sagt mir nichts von Gold — confirmed; German ti | The German original found in the 1740 review (ID, first line, confidence, basis, hymn no.) — shown even where our own 'Translated from' differs; never used to overwrite it. |
| Owner's review 2026-11-12 | 18 | Q8: Danish original by P. J. Vinstrup (hymnary.org) — not 'H | The owner's decisions from 2026-11-12 on (decision pages), or a change made on the owner's instructions; dated entries separated by ' | '. |
| First line before QC (2026-11-13) | 23 | O siel | The first line as it stood before the QC fix of 2026-11-13 (filled only where 'First line' / 'English first line' was repaired). |
| First-line QC (2026-11-13) | 23 | completed from the owner's 1740 transcription (stanza 1, fir | QC note on the first line (2026-11-13): how it was repaired and how sure (certain / probable), or a flag — NOT A FIRST LINE / NOT AN ENGLISH (GERMAN) LINE / TITLE / check. Rows flagged NOT … are kept, not deleted; leave them out of first-line searches. |
| Same text as (QC 2026-11-13) | 28 | DA-0308 (Norwegian-book and Danish forms of one text; checke | The other ID under which the same Danish/Norwegian text is entered (Norwegian-book form and Den Danske Salmebog 2002 form of one translation), checked by Claude 2026-11-13; both rows point to each other. |
| Troens rare Klenodie 1894 (QC 2026-11-13) | 137 | confident: TrK no. 100, p. 132 (Troens rare Klenodie) — http | Where the text is in Troens rare Klenodie (1894 ed.), and what that check found. |
| Author/translator (from Troens rare Klenodie) | 65 | tr. Brorson (TrK no. 267, p. 350; German original DE-04093)  | Author/translator credit taken from Troens rare Klenodie. |
| QC2 round 1 (2026-11-14) | 3 | German link DE-00882 removed (wrong author guess) | Note from that quality-control round (what was checked or changed). |
| First line before spell check (2026-11-23) | 57 | Dit Navn, o Jesu, loker mig | — |

### scandinavian_tune_links.csv (1,003 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Scandinavian–Tune links'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 1,003 | DA-0020 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| First line | 1,003 | Far dog fort [as printed in Norwegian book] | First line as printed. |
| Zahn no. | 1,003 | 4791 4792 4793 | Zahn melody number as used for joins (variants may be written 25.1; see Zahn no._Original). |
| View tune: Zahn no. | 1,003 | ▶ 4791 (III, p. 191) +2 | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 1,003 | https://archive.org/details/1508285990bsb11304501/page/191/m | Link carried by 'View tune: Zahn no.' (as a URL). |
| Relation | 1,003 | Zahn: melody listed under the source text | Kind of link (printed with this tune in a hymnal / melody listed under the source text / named as Mel. …). |
| Via DE ID | 707 | DE-01597 | German text through which the tune link was inherited. |
| Evidence | 1,003 | Zahn register via Texts sheet | What the link rests on. |
| Status | 1,003 | structural (like EN) | how sure the row is: confirmed / probable / check (see README) |
| Variant family (chosen by incipit) | 0 |  | The variant (a/b/c) of the Zahn melody whose opening matches the printed tune. |
| Owner's review 2026-11-10 | 81 | yes — accepted: 346 (owner 2026-11-10) | The owner's decision on this row in the 2026-11-10 review. |
| Owner's review 2026-11-12 | 59 | Q11: owner — Breitendich p. 71 = Zahn 350a (more ornamented, | The owner's decisions from 2026-11-12 on (decision pages), or a change made on the owner's instructions; dated entries separated by ' | '. |

### scandinavian_english_links.csv (38 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Scandinavian–English links'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Danish text ID | 38 | DA-0402 | DA- text ID. |
| Danish first line | 38 | Over Kedron JEsus træder Med frivillig | First line as printed in Pontoppidan 1740. |
| Where | 38 | Pontoppidan 1740 no. 76 | Source of the Danish text. |
| EN ID (if in our English list) | 6 | EN-00545 | EN ID when the English text is already in EN Texts. |
| English first line | 38 | Over Kidron Jesus treadeth | English first line. |
| hymnary | 38 | ▶ hymnary search | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 38 | https://hymnary.org/search?qu=Over%20Kidron%20Jesus%20treade | Link carried by 'hymnary' (as a URL). |
| Authors / translator (hymnary) | 38 | T. H. Kingo, 1634-1703 ; J. Jeffrey; M. DeGarmeaux, b. 1958 | Credits on hymnary.org. |
| Earliest year in our hymnals | 38 | 1901 | Earliest hymnal year among our hymnary exports (the public-domain date check). |
| Hymnals | 38 | ELH1996, HCH11927, HFCH1928, HOoS1901, HOoS1926, LHPN1913 | Hymnals (hymnary codes) or source posts the text appears in. |
| hymnary text | 38 | https://hymnary.org/text/over_kedron_jesus_treadeth | hymnary.org text page. |
| Status | 38 | confirmed (Claude 2026-11-10: matched by first-line meaning  | how sure the row is: confirmed / probable / check (see README) |

### de_texts_added.csv (2,066 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'New DE texts'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 2,066 | DE-05898 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| First line (KGB 1862 spelling) | 2,066 | Herr! Öffne mir die herzensthür | First line (KGB 1862 spelling). |
| Match key | 2,066 | her ofne mir die herzenstur | Lower-case, umlauts folded, ß→ss, th→t, ey→ei, doubled letters collapsed: used for matching across sources. |
| Source | 2,066 | Kirchen-Gesangbuch 1862, no. 5 | Where the row comes from. |
| Status | 2,051 | provisional — not found in Zahn register | how sure the row is: confirmed / probable / check (see README) |
| Closest Zahn texts | 42 | DE-04517: Öffne mir die Perlenpforten / DE-02277: Herr, höre | Nearest texts in Zahn's list (ID: first line), to show it is not there. |
| Best score | 41 | 0.69 | Similarity of the closest one (1 = identical). |
| Meter (normalized) | 957 | 8.8.8.8 | Syllables per line, dot-separated; L.M./C.M./S.M. and D written out. |
| Meter source | 959 | its English translations (hymnary), same meter assumed | Where the meter came from (register, tunes, hymnary, inherited). |
| Note | 448 | stanza 5 | Notes. |
| First line before QC (2026-11-13) | 18 | Warum sollen dich so schmerzen (Alt.) | The first line as it stood before the QC fix of 2026-11-13 (filled only where 'First line' / 'English first line' was repaired). |
| First-line QC (2026-11-13) | 3 | title (stanza of the Latin hymn), not a German first line | QC note on the first line (2026-11-13): how it was repaired and how sure (certain / probable), or a flag — NOT A FIRST LINE / NOT AN ENGLISH (GERMAN) LINE / TITLE / check. Rows flagged NOT … are kept, not deleted; leave them out of first-line searches. |
| Author (hymnary, 2026-11-14) | 920 | Johannes Olearius | Author, from hymnary.org or (where noted) another source. |
| Author source (hymnary, 2026-11-14) | 920 | hymnary German text with the same first line: herr_offne_mir | Where that author comes from. |
| Date (first known) | 214 | by 1876 | Earliest known date of the text. |
| Date source | 214 | hymnary: earliest hymnal listed for the German text (11 hymn | Where that date comes from. |
| Tune (hymnary) | 101 | [Sei uns mit Jubelschalle] | Tune name from hymnary.org. |
| hymnary German text page | 171 | ▶ hymnary (German) | hymnary.org page of the German text, if there is one. |
| hymnary German text page URL | 171 | https://hymnary.org/text/sei_uns_mit_jubelschalle_christkind | Link carried by 'hymnary German text page' (as a URL). |
| Author (hymnary German page, QC2 r4) | 11 | Adriaan Valerius (hymnary German page; ours kept: Caroline H | Author on that hymnary.org German page (QC #2 round 4). |
| Author (Carver post, QC2 r5) | 1,058 | J. Heermann, 1630 | Author named in Carver's Hymnoglypt post (QC #2 round 5). |
| Author check (QC2 r5) | 1,058 | filled from Carver's post (https://matthaeusglyptes.blogspot | How the author was checked. |
| First line, fuller form (Carver post, QC2 r5) | 18 | Freuet euch, ihr Gotteskinder, / preiset mit mir Gottes Mach | Longer form of the first line as Carver gives it. |
| QC2 round 5 (2026-11-16) | 10 | not a duplicate of DE-02258/DE-02259 "Herr Gott Vater im Him | Note from that quality-control round (what was checked or changed). |
| QC2 round 6 (2026-11-16) | 27 | not a duplicate of DE-05616 (probable): Pontoppidan 1740 no. | Note from that quality-control round (what was checked or changed). |
| QC2 round 7 (2026-11-19) | 11 | meter still check (step 4): acrostic hymn; Carver's stanza c | Note from that quality-control round (what was checked or changed). |
| QC2 round 8 (2026-11-19) | 1 | new: Helmbold's Benedictus hymn (12 lines, tune "Nun lob mei | Note from that quality-control round (what was checked or changed). |
| First line before spell check (2026-11-23) | 9 | Salve caput cruentatum, stanza 5 | — |

### becker_psalter_schuetz.csv (159 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Becker Psalter (Schütz)'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Psalm | 159 | 1 | Psalm number (part in brackets). |
| SWV | 159 | 97 | Schütz-Werke-Verzeichnis number (97–255). |
| First line (Schütz 1628/1661) | 159 | Wer nicht sitzt im Gottlosen Rat | First line as titled in the SWV catalogue (Schütz's text). |
| DE ID | 159 | DE-05490 | German text ID (Zahn_texts_and_links Texts) |
| DE first line | 159 | Wer nicht sitzt im gottlosen Rat | First line of that German text in our list. |
| Text author | 152 | C. Becker | Author as Zahn (or our list) gives it. |
| DE source | 159 | Zahn text list | Where the German text comes from (Zahn text list / New DE texts). |
| Schütz tune(s) in Zahn | 100 | 538 | Zahn numbers of Schütz's own melody for this psalm (Schütz 1628 / Becker–Schütz 1661 / Dresden 1676). |
| Other Zahn tunes of the text | 41 | 4514 | Other Zahn melodies printed under the same German text. |
| Carver EN ID | 150 | EN-01577 | EN ID of Carver's translation (Hymnoglypt). |
| Carver English first line | 150 | Who heeds not what th’ ungodly say, | First line of Carver's translation. |
| Carver post (German title) | 150 | Wer nicht sitzt im Gottlosen Rath | Title of Carver's blog post (the German he translated). |
| Carver post date | 150 | 2024-04-30 | Date of the post. |
| Carver note | 19 | Luther's (or another older) text taken into Becker's psalter | How the Carver match was made, or why there is none. |
| Gaps | 60 | no Carver translation; no Schütz melody in Zahn (borrowed tu | What is still missing for this psalm. |

### translators.csv (29 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Translators'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Owner's decision | 0 |  | The owner's decision on this row in the 2026-11-10 review (sheet column was 'Your decision'). |
| Translator (surname key) | 29 | landstad | Translator's surname, lower case, as used to group credits. |
| Nationality (provisional) | 29 | Norwegian | Translator's nationality as far as known; '(?)' = unsure. |
| Credits | 29 | 130 | Number of hymnal credits found for this translator. |

### hymnal_appearances.csv (7,906 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Hymnal appearances'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| EN ID | 7,906 | EN-00001 | Project ID of an English text: one per distinct first line per translator. |
| hymnary | 7,906 | ▶ hymnary text | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 7,906 | https://hymnary.org/text/all_glory_be_to_god_on_high_and_tha | Link carried by 'hymnary' (as a URL). |
| Title | 7,900 | All Glory Be to God on High | Title as printed in the hymnal. |
| Hymnal | 7,906 | CW'21 | Hymnal code (hymnary) or book. |
| Number | 7,904 | 935 | Number in that hymnal. |
| Tune name | 2,699 | ALLEIN GOTT IN DER HÖH SEI EHR | Tune name as printed. |
| Meter | 1,614 | 8.7.8.7.8.8.7 | Meter as printed. |
| Zahn tune | 1,107 | 4457 | Zahn number of the tune printed. |
| View tune: Zahn tune | 1,107 | ▶ 4457 (III, p. 80) | Link to its scan. |
| View tune: Zahn tune URL | 1,107 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: Zahn tune' (as a URL). |
| Tune match | 2,453 | one Zahn tune (incipit agrees) | How the printed tune was matched to Zahn. |
| Authors | 5,943 | Nikolaus Decius, c. 1485-after 1546; Catherine Winkworth, 18 | Authors/translators as printed. |
| hymnary text ID | 2,593 | all_glory_be_to_god_on_high_who_hath_our | hymnary.org textAuthNumber (URL: hymnary.org/text/<id>). |
| Source | 7,906 | LCMS index via TLH 237 (title sim 1.00) | Where the row comes from. |
| Variant family (chosen by incipit) | 129 | 624 | The variant (a/b/c) of the Zahn melody whose opening matches the printed tune. |
| View tune: Variant family (chosen by incipit) | 129 | ▶ 624 (I, p. 172) | Link to that variant's scan. |
| View tune: Variant family (chosen by incipit) URL | 129 | https://archive.org/details/1508283124bsb11304498/page/172/m | Link carried by 'View tune: Variant family (chosen by incipit)' (as a URL). |

### scandinavian_appearances.csv (1,760 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Scandinavian appearances'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID(s) | 1,660 | NO-0001 | Our text ID(s) for this appearance. |
| Hymnal | 1,760 | SLKA1919 | Hymnal code (hymnary) or book. |
| Number | 1,760 | 273 | Number in that hymnal. |
| First line | 1,760 | Af Dybsens Nød jeg raabe maa | First line as printed. |
| Authors | 945 | Luther; Landstad | Authors/translators as printed. |
| Tune name | 910 | [Ack! hjertans ve] | Tune name as printed. |
| Language | 1,741 | Norwegian | Danish / Norwegian (Bokmål, Nynorsk) / Swedish. |

### other_language_texts.csv (475 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Other-language texts'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 475 | FI-0001 | Project text ID: FI- Finnish, CS- Czech (Tranoscius tradition), SK- Slovak, PL- Polish, ES- Spanish + number. |
| Language | 475 | Finnish | Language of the text (Finnish; Czech of the Tranoscius tradition; Slovak). |
| First line | 475 | Avaja porttis, ovesi | First line as printed. |
| Translated from | 366 | DE-03524 | ID of the text this translates: the German original (DE-), or for Slovak texts the Czech text (CS-) they revise. |
| Relation | 475 | translation of German (via Swedish) | How the text relates to its source, or how the text relates to the tune. |
| Link status | 475 | confirmed: virsikirja.fi names the original | How sure the link to the German original is, and how it was made (older status kept after "was:"). |
| German first line (our list) | 343 | Macht hoch die Thür | First line of the linked German text, as in our German lists. |
| Original title (as named in the source) | 161 | Macht hoch die Tür | The German original as the source names it (virsikirja.fi for Finnish). |
| Candidates / note | 116 | DE-02638 Ich glaub an Einen Gott allein (Matth. Greiter) / D | For unidentified rows: the credited author's German texts in our lists, as candidates. |
| Author / translator credit (as in the source) | 415 | Georg Weissel 1642. Ruots. Jakob Arrhenius 1694. Suom. virsi | Author and translator credit as printed or given by the source. |
| Via Swedish (FI) | 71 | yes: Jakob Arrhenius 1694 | For Finnish: the Swedish translation the Finnish one was made from, if the source says so. |
| First translation into this language | 160 | virsikirjaan 1701 | Who first translated it into this language, and when (as the source gives it). |
| Into the hymnal (year) | 70 | 1701 | Year the text entered the Finnish hymnal. |
| Hymnals | 469 | Virsikirja 1986 2; Vanha virsikirja 1701 107 | Hymnals (hymnary codes) or source posts the text appears in. |
| Melody note (as printed) | 166 | Ruotsissa 1697. | The hymnal's melody note, as printed (Finnish). |
| Vanha virsikirja 1701 no. | 22 | 107 | Number in the old Finnish hymnal (Vanha virsikirja, 1701). |
| 1701 first line (Väinölä stanza index) | 22 | Sun porttis, oves avaja | First line in the 1701 hymnal, from Väinölä's stanza index. |
| 1701 match | 22 | probable (Claude, old vs modern Finnish first line) | How sure the 1701 identification is. |
| German original (via CS, for SK) | 40 | DE-00063 | For Slovak texts: the German original reached through the Czech text. |
| Basis | 475 | virsikirja.fi (Väinölä, Virsikirjamme virret): original titl | What the German link rests on. |
| Source | 475 | virsikirja.fi (Virsikirja 1986, no. 2); credits checked agai | Where the row comes from. |
| Note | 243 | QC2 B16 (2026-11-19): was linked to Zahn DE-00730 "Dank sei  | Notes. |
| Melody note: meaning (Claude) | 166 | melody from Sweden, 1697 (Swedish psalmbook) | What the melody note says, in English (folk variant, Swedish psalmbook melody, composer + year…). |
| EZ21 (Evangelický zpěvník 2021): no. / first line | 15 | 415: Ach, zůstaň svou milostí při nás, Pane Kriste | Number and first line (modern form) of the same Czech text in the Evangelický zpěvník 2021 (EZ21), if it is there. |
| EZ21 credits (words | music) | 15 | words: Josua Stegmann, Christliches Gebet Büchlein, 1627 / S | Words and music credits EZ21 gives for that hymn (as printed in its OpenLP export). |
| EZ21 check (2026-11-20) | 15 | agrees: same Czech text; EZ21 credits Josua Stegmann 1627 | What the EZ21 credit says about our German link: agrees / identifies the original / possible / different song. |

### other_language_tune_links.csv (361 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Other-language–Tune links'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 361 | FI-0001 | Project text ID: FI- Finnish, CS- Czech (Tranoscius tradition), SK- Slovak, PL- Polish, ES- Spanish + number. |
| First line | 361 | Avaja porttis, ovesi | First line as printed. |
| Zahn no. | 361 | 5844 5845a 5845b 5846 5847 5848 5849 5850 | Zahn melody number as used for joins (variants may be written 25.1; see Zahn no._Original). |
| View tune: Zahn no. | 361 | ▶ 5844 (III, p. 552) +7 | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 361 | https://archive.org/details/1508285990bsb11304501/page/552/m | Link carried by 'View tune: Zahn no.' (as a URL). |
| Relation | 361 | Zahn: melody listed under the source text | How the text relates to its source, or how the text relates to the tune. |
| Via DE ID | 361 | DE-03524 | German text through which the tune link was inherited. |
| Evidence | 361 | Zahn register via Texts sheet (German link from virsikirja.f | The evidence the link rests on. |
| Status | 361 | structural (like EN) | confirmed / probable / check / structural (see top of page). |
| Variant family (chosen by incipit) | 9 | variant family: 4360 4361c | All a/b/c forms of one melody, when they fit equally. |

### other_language_appearances.csv (494 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Other-language appearances'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID(s) | 494 | FI-0001 | Project text ID: FI- Finnish, CS- Czech (Tranoscius tradition), SK- Slovak, PL- Polish, ES- Spanish + number. |
| Hymnal | 494 | Virsikirja 1986 | Hymnal. |
| Number | 494 | 2 | Hymn number in that hymnal. |
| First line | 494 | Avaja porttis, ovesi | First line as printed. |
| Authors | 414 | Georg Weissel 1642 | Author credit as given by the hymnal. |
| Language | 494 | Finnish | Language of the text (Finnish; Czech of the Tranoscius tradition; Slovak). |

### tune_names_to_zahn.csv (1,783 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Tune names → Zahn'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Tune name (hymnary) | 1,783 | OLD HUNDREDTH | Tune name on hymnary.org. |
| Incipit (scale degrees) | 1,735 | 117651233332143 | Opening notes as scale degrees (hymnary). |
| Uses | 1,783 | 37 | How many hymnal appearances use this name. |
| Zahn no. | 432 | 8359 | Zahn melody number as used for joins (variants may be written 25.1; see Zahn no._Original). |
| View tune: Zahn no. | 432 | ▶ 8359 (V, p. 129) | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 432 | https://archive.org/details/1508287113bsb11304503/page/129/m | Link carried by 'View tune: Zahn no.' (as a URL). |
| Status | 1,783 | no Zahn match | how sure the row is: confirmed / probable / check (see README) |
| Zahn candidates | 557 | 8359 | Zahn melodies that fit the name and opening. |
| View tune: Zahn candidates | 557 | ▶ 8359 (V, p. 129) | Link to the first candidate. |
| View tune: Zahn candidates URL | 557 | https://archive.org/details/1508287113bsb11304503/page/129/m | Link carried by 'View tune: Zahn candidates' (as a URL). |
| Incipit scores | 557 | 8359:1.00 | Opening similarity per candidate. |
| Zahn texts with this name | 588 | DE-05610 | German texts whose first line is the tune name. |
| Name match | 1,783 | name~ | How the name matched (= exact, ~ close). |
| QC2 round 7–8 (2026-11-19) | 24 | probable — chosen by incipit between DIFFERENT Zahn melodies | Note from that quality-control round (what was checked or changed). |

### tune_evidence.csv (531 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Tune evidence'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 531 | EN-00005 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| First line | 180 | Bryd frem, mit Hjertes Trang at lindre [as printed in Norweg | First line as printed. |
| Hymnal | 280 | ELHB | Hymnal code (hymnary) or book. |
| Number | 280 | 1 | Number in that hymnal. |
| Tune name | 280 | HERR JESU CHRIST, DICH ZU UNS WEND | Tune name as printed. |
| Source of evidence | 531 | ELHB 1911 music edition, tune header | Where the evidence was found. |
| Evidence (as printed) | 531 | And bless us , more than in past days , | The words as printed. |
| Zahn no. | 178 | 3735b | Zahn melody number as used for joins (variants may be written 25.1; see Zahn no._Original). |
| View tune: Zahn no. | 178 | ▶ 3735b (II, p. 487) | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 178 | https://archive.org/details/1508284209bsb11304500/page/487/m | Link carried by 'View tune: Zahn no.' (as a URL). |
| Why | 178 | composer neander | Reason for the suggestion. |
| Candidates (score) | 488 | 624:0 | Candidate Zahn tunes with scores. |
| Existing printed-tune link | 199 | 624 | Zahn tune already linked from the hymnals. |
| View tune: Existing printed-tune link | 199 | ▶ 624 (I, p. 172) | Link to that tune. |
| View tune: Existing printed-tune link URL | 199 | https://archive.org/details/1508283124bsb11304498/page/172/m | Link carried by 'View tune: Existing printed-tune link' (as a URL). |
| Linked DE | 13 | DE-02471 | German text currently linked. |
| Suggested DE | 8 | DE-03466 | German text the evidence points to. |
| Status | 531 | no agreement | how sure the row is: confirmed / probable / check (see README) |

### zahn_tunes.csv (9,538 rows)

From: Master_File_linked_v16.xlsx, sheet 'Sheet1'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Zahn no. | 9,538 | 1 | Zahn's tune number as printed (a/b/c… = variant forms). This is the ID used by every link table. |
| Zahn no._Original | 9,538 | 1 | — |
| Vol. | 9,538 | 1 | Zahn volume (1–5). |
| Zahn page | 9,538 | 5 | Printed page in that volume. |
| Meter type | 9,537 | Zweizeilig, jambisch | Zahn's meter class (lines, foot). |
| Syllable pattern | 9,381 | 8.8 (9.9) | Syllables per line, dot-separated (the tune's meter). |
| Relation | 5,526 | Zu demselben Text | Kind of link (printed with this tune in a hymnal / melody listed under the source text / named as Mel. …). |
| Text incipit | 9,522 | Ich wollt, daß ich daheime wär | First line of the text Zahn prints the melody under. |
| Text author | 8,250 | H. v. Laufenberg | Author as Zahn (or our list) gives it. |
| Composer / attribution | 4,881 | Mel. nach Dr. Arnolds Übertragung | As printed by Zahn. |
| First source (as cited by Zahn) | 9,537 | Straßburger Handschrift 1430 | Zahn's citation of the earliest source. |
| Source year | 9,468 | 1430 | Year of the first source (as printed). |
| Key signature | 9,537 | 1b | e.g. 2b, 1#, 0. |
| Time signature | 9,304 | C | As printed. |
| First note | 9,501 | D4 | First note of the melody. |
| Final note | 9,297 | D4 | Last note (usually the tonic). |
| Melodic incipit | 9,501 | D4 G4 F4 D4 C4 C4 F4 G4 A4 F4 A4 F4 C5 A4 G4 | Opening notes, scientific pitch (C4 = middle C). |
| Later sources | 5,430 | Wackernagel 1860; Hille 1886 | Later sources Zahn cites. |
| Notes | 9,147 | Manuscript burned 1870; melody after Arnold's transcription. | Extraction notes. |
| Confidence | 9,538 | low | Extraction confidence (high / medium / low). |
| Source_File | 9,538 | zahn1rest\zahn_vol1_p5-12.csv | CSV the row was extracted from. |
| Bibl. no. | 9,474 | 1324 | Number of that source in the vol. VI bibliography (zahn_vol6_sources_linked.csv). |
| Bibl. short form | 9,474 | Hommel, Volkslieder 1864 | Short form of the vol. VI bibliography entry. |
| Bibl. link | 9,537 | not in vol 6 | How the source was matched: auto / checked / likely / unclear / not in vol 6. |
| Duplicate of row | 79 | 2 | Set when the same Zahn no. was transcribed twice; ignore that row. |
| Standard citation | 9,474 | Hommel, Volkslieder 1864, Nr. 247 | Citation: source + number. |
| Zahn corrections (Erg./Nachträge) | 609 | [Bd. V Erg. A p.389] earlier source: Older source found duri | Zahn's own corrections (Ergänzungen/Nachträge) for this tune. |
| Text author (corrected) | 94 | Michael Statler | Text author per Zahn's corrections. |
| Composer (corrected) | 632 | J. G. Schicht (?) / F. Hommel | Corrected by Zahn's Ergänzungen or filled from his composer list (see Composer fill source / check). |
| Earliest source (corrected) | 126 | Babst 1551, II, 37 | Earlier source per Zahn's corrections. |
| Source year (corrected) | 141 | 1551 | From Zahn's corrections. |
| Same melody as (Zahn) | 28 | 1624 | Zahn's own statement that two numbers are the same melody (printed twice). |
| Correction basis | 340 | earlier source — see Zahn corrections column | What the corrected columns rest on. |
| Composer fill source (Zahn vol. V list, 2026-11-07) | 650 | Zahn V Erfinder no. 302 (p. 464), exact no.; Zahn V Erfinder | Entry in Zahn's composer list that names this tune. |
| Composer fill check | 650 | two composers cite it; entry hedges: zugeschrieben | Caveats on that composer entry. |
| Intervals (semitones) | 9,501 | +5 -2 -3 -2 0 +5 +2 +2 -4 +4 -4 +7 -3 -2 | Key-independent incipit: steps between notes (+2 = up a whole tone). |
| Contour (U/D/R) | 9,501 | UDDDRUUUDUDUDD | Up / down / repeat shape of the incipit. |
| Same opening as (melodic search) | 437 | 3125 | Other Zahn nos. whose first 10+ intervals are the same (or differ by one note). |
| Same tune in another key? (melodic search) | 129 | 3335 | Other Zahn nos. with the same notes relative to the final note. |
| Incipit correction (2026-11-10) | 7 | 2026-11-13 Final note was: E4 — Zahn vol. I p. 6 (BSB scan 1 | Old incipit and the scan it was corrected from. |
| QC check (2026-11-13) | 262 | twin rows 14/15 agree now (final note D4, read on the scan) | Result of the 2026-11-13 check of this tune row against the Zahn scans and the vol. 6 bibliography: leap printed in Zahn (correct), twin rows reconciled, source year slip corrected, or year/link OK or to check. |
| Composer fill recheck (QC2 2026-11-14) | 650 | J. G. Schicht: (?) — tune no. not in the stored part of the  | Re-reading of the composer fill against Zahn's composer list (QC #2, B04): kept, marked (?) or removed, with the reason. |
| Incipit correction (QC2 r3 2026-11-14) | 7 | was: D5 B4 A4 G4 D4 F#4 F#4 E4 D4 G4 F#4 G4 C5 B4 A4 — Zahn  | Correction to the opening notes from the scan (QC #2 round 3). |
| Page correction (QC2 r4 2026-11-15) | 1 | 504 (heading, number, composer and source on p. 504 — BSB OC | Correction to the Zahn page (QC #2 round 4). |
| Incipit correction (QC2 r4 owner 2026-11-16) | 20 | was: A4 A4 A4 B4 A4 A4 G#4 A4 A4 B4 C5 B4 — Zahn vol. 1 p. 9 | Correction to the opening notes, checked by the owner on the scan. |
| Incipit correction (QC2 r5 owner 2026-11-16) | 3 | was: F4 D5 Bb4 Eb5 Bb4 G4 A4 Bb4 D5 C5 A4 Bb4 C5 F4 Bb4 A4 G | Correction to the opening notes, checked by the owner on the scan. |
| Incipit correction (QC2 r6 owner 2026-11-16) | 5 | was: C5 B4 E5 D#5 C5 E5 C5 A4 G4 F#4 E4 G4 A4 B4 B4 C#5 — Za | Correction to the opening notes, checked by the owner on the scan. |

### zahn_texts.csv (5,897 rows)

From: Zahn_texts_and_links_v12.xlsx, sheet 'Texts'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Text ID | 5,897 | DE-00001 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| First line (cleaned) | 5,897 | Abba, lieber Vater, höre | German first line, OCR-corrected; register spelling kept in Register spelling(s). |
| Match key | 5,897 | aba lieber vater hore | Lower-case, umlauts folded, ß→ss, th→t, ey→ei, doubled letters collapsed: used for matching across sources. |
| Register spelling(s) if different | 546 | Ach Gott, ich falle dir zu Fuße | Spelling in Zahn's register when the cleaned first line differs. |
| Text author | 4,405 | B. Schmolck | Author as Zahn (or our list) gives it. |
| Meter (syllables) | 4,651 | 8.7.8.7.7.7 | Syllables per line. |
| Meter type | 4,748 | Sechszeilig, trochäisch | Zahn's meter class (lines, foot). |
| Own tunes (n) | 5,897 | 1 | Number of Zahn melodies printed under this text. |
| Also-sung-to tunes (n) | 5,897 | 0 | Number of other melodies the register says it was sung to. |
| Own tunes (Zahn nos.) | 4,748 | 3670 | Melodies Zahn lists under this text (written for it). |
| Also-sung-to tunes (Zahn nos.) | 1,992 | 3448a | Melodies the register says the text is also sung to. |
| Earliest own-tune year | 5,880 | 1738 | Year of the earliest of its own melodies. |
| Earliest own tune (Zahn no.) | 5,880 | 3670 | That melody. |
| Earliest own-tune source | 5,880 | König 1738, S. 132 | Its source. |
| Register page(s) | 5,897 | 501 | Page in Zahn's vol. V text register. |
| Register notes | 51 | see Ergänzungen vol. II, p. 638 | Note in the register. |
| First line cleaned? | 519 | yes | yes = the first line was corrected. |
| Cleanup source | 530 | first line corrected from master incipit of Zahn 2747 | How it was corrected. |
| Meter (normalized) | 5,754 | 8.7.8.7.7.7 | Syllables per line, dot-separated; L.M./C.M./S.M. and D written out. |
| Meter source | 5,754 | Zahn register | Where the meter came from (register, tunes, hymnary, inherited). |
| Author note (QC2 2026-11-14) | 49 | hymnary credits: Friedrich Layritz (filled; owner OK 2026-11 | Note on the author attribution (QC #2). |
| First line correction (QC2 r4 2026-11-15) | 103 | NOT A FIRST LINE | Corrected first line (QC #2 round 4). |
| First line correction basis | 103 | register OCR junk (page/volume note or a single word), not a | Basis for that correction. |
| First line correction (QC2 r5 2026-11-16) | 16 | Preist, Menschen, Gott durch eure Lieder | Corrected first line (QC #2 round 5). |
| First line correction basis (QC2 r5) | 16 | certain: the register line itself reads "Preist, Menschen, G | Basis for that correction. |
| Author (Carver post, QC2 r5) | 100 | Anon., 1673? | Author named in Carver's Hymnoglypt post (QC #2 round 5). |
| Author basis (Carver post, QC2 r5) | 100 | Carver: anonymous (Zahn none) — https://matthaeusglyptes.blo | Basis for the author taken from Carver's post. |
| First line correction (QC3 2026-11-20) | 21 | Allmächtiger, ewiger Gott | Corrected first line (QC #3: OCR damage in Zahn's register; the register spelling is kept in "Register spelling(s) if different"). |
| First line correction basis (QC3) | 21 | QC3 2026-11-20: register OCR "Allmäthtiger, ewiger Gott" → " | Basis for that correction. |
| First line before spell check (2026-11-23) | 17 | Ach | — |

### zahn_text_tune_links.csv (11,789 rows)

From: Zahn_texts_and_links_v12.xlsx, sheet 'Text-Tune'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Link ID | 11,789 | L-00001 | Text–tune link ID. |
| Text ID | 11,789 | DE-00001 | Project text ID: DE-xxxxx German, DA-/NO-/SV-xxxx Scandinavian. |
| First line (as in register) | 11,789 | Abba, lieber Vater, höre | First line as printed in the register. |
| Tune no. (as printed in register) | 11,789 | 3670 | Tune number as printed. |
| Zahn no(s). in master | 11,789 | 3670 | Matching Zahn number(s) in the master file. |
| Match | 11,789 | exact | How the printed number matched the master (exact / letter added …). |
| Relation | 11,789 | written for / borrowed | Kind of link (printed with this tune in a hymnal / melody listed under the source text / named as Mel. …). |
| Tune in Zahn vol. | 11,789 | II | Volume of Zahn that holds the tune (I–V; "V (Ergänzungen)" = the supplements). Not the volume of the register. |
| Register page (Zahn vol. V) | 11,789 | 501 | Page of Zahn's first-line register, which is printed in Band V, pp. 501–556. |
| Register note | 90 | see Ergänzungen vol. II, p. 638 | Register note. |
| Tune meter | 11,595 | 8.7.8.7.7.7 | Meter of the tune. |
| Tune composer / attribution | 6,011 | Mel. bei (von?) König | Composer as Zahn prints it. |
| Tune source year | 11,720 | 1738 | Year of the tune's first source. |
| Zahn: printed twice (identical tune) | 38 | 4198=7843 | Zahn numbers that are the same melody printed twice. |
| Register CSV row | 11,789 | 2 | Row in the register CSV. |
| Tune composer (corrected / filled, master v16) | 807 | G. Weber (?) | Tune composer from Zahn master v16 (corrected, or filled from Zahn's composer list; "(?)" = hedged). |
| Tune source year (corrected, master v16) | 208 | 1698 | Tune source year from Zahn master v16 (corrected). |

## Source tables (one per source read)

### breitendich_1764_melodies.csv (194 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Breitendich 1764 melodies'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Breitendich printed page | 194 | 1 | Page number printed in Breitendich's Choral-Bog (1764). |
| PDF page | 194 | 21 | Page of the PDF scan. |
| Melody heading (as printed) | 194 | Kom, Hedningers Frelser sand | Melody title as printed at the head of the page. |
| Verses | 174 | 8 | Number of stanza lines printed under the melody. |
| German melody (Claude) | 88 | Nun komm der Heiden Heiland | German melody this Danish melody is (Claude's identification by name; '(per Berggreen)' = Berggreen's note names it). |
| View tune: German melody (Claude) | 84 | ▶ 1174 (I, p. 314) by name | Link text for the Zahn scan of the (first) tune in 'German melody (Claude)'. |
| View tune: German melody (Claude) URL | 84 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: German melody (Claude)' (as a URL). |
| DE ID | 85 | DE-03990 | German text ID (Zahn_texts_and_links Texts) |
| German first line (Zahn) | 85 | Nun komm der Heiden Heiland | First line of that German text in Zahn's register. |
| Zahn melodies of that text | 82 | 1174 1175 | All Zahn tunes listed under that German text. |
| View tune: Zahn melodies of that text | 82 | ▶ 1174 (I, p. 314) +1 | Link text for the Zahn scan of the (first) tune in 'Zahn melodies of that text'. |
| View tune: Zahn melodies of that text URL | 82 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: Zahn melodies of that text' (as a URL). |
| Form confirmed in Lindeman 1873 (Norway) | 25 | 1174 | Zahn form of the tune confirmed by the same melody in Lindeman's Koralbog 1873. |
| View tune: Form confirmed in Lindeman 1873 (Norway) | 25 | ▶ 1174 (I, p. 314) | Link text for the Zahn scan of the (first) tune in 'Form confirmed in Lindeman 1873 (Norway)'. |
| View tune: Form confirmed in Lindeman 1873 (Norway) URL | 25 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: Form confirmed in Lindeman 1873 (Norway)' (as a URL). |
| Status | 193 | German melody confirmed by opening notes (read by eye 2026-1 | how sure the row is: confirmed / probable / check (see README) |
| Opening read by eye (disputed melodies only) | 84 | G4 G4 F4 B4 A4 G4 A4 G4 (read 2026-11-10) | Opening notes read on the scan (pitch names, C4 = middle C), with the date read. |
| Notes check | 83 | opening read by eye 2026-11-10 matches Zahn 1174 | Result of comparing that opening with the Zahn incipit. |
| Berggreen no. (10th ed.) | 33 | 65 | Number of the melody in Berggreen (10th edition). |
| German (Berggreen) | 16 | Auf meinen lieben Gott | German melody Berggreen names for it. |
| Berggreen check | 33 | NEW: German melody named by Berggreen | How Berggreen's note compares with our identification: NEW / AGREE / check. |
| Berggreen note (excerpt, OCR) | 33 | Fryd dig, du Kristi Brud (Auf meinen lieben Gott); af Jacob  | Short OCR excerpt of Berggreen's origin note. |
| Owner's review 2026-11-10 | 29 | left as is — low priority — left as recorded (owner 2026-11- | The owner's decision on this row in the 2026-11-10 review. |
| Owner's review 2026-11-12 | 22 | Q14: same tune — Zahn 4297a (owner 2026-11-12) | The owner's decisions from 2026-11-12 on (decision pages), or a change made on the owner's instructions; dated entries separated by ' | '. |
| Opening read 2026-11-12 (Claude) | 9 | Breitendich p. 30 'O Drøvelse, o Hierte-Vee', read: E5 C5 A4 | Claude's reading of the melody's opening notes on the Breitendich page image (C4 = middle C) and the comparison with the Zahn incipit; dated entries. |

### breitendich_cross_references.csv (280 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Breitendich cross-references'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Breitendich page (where printed) | 280 | 3 | Breitendich page whose cross-reference list contains this line. |
| Line as OCR read it (tesseract deu_latf) | 280 | Bar glad, du hellige Chriſtenhed. LNel- Jeſu ſode Hukommelſe | The list line as the Fraktur OCR read it: hymn first line … 'Mel.' melody name … 'Pag.' page. |
| Sends to Breitendich page | 280 | 124 | The melody page the line sends the hymn to. |
| Matched 1740 hymn no. | 174 | 4 | 1740 hymn the line was matched to (only when the match score ≥ 75). |
| Match score (0–100) | 280 | 93 | Fuzzy match score between the OCR line's opening and the 1740 first line. |
| 1740 first line | 174 | vaer glad du hellige christenhed | The matched 1740 first line (normalised). |
| Used | 21 | yes | 'yes' = this line was used for a tune decision in DATA v40. |

### foltmar_1785_melodies.csv (93 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Foltmar 1785 melodies'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| PDF page | 93 | 8 | Page of the PDF scan. |
| MS page | 92 | 1 | Page number written in Foltmar's manuscript. |
| No. | 92 | 1 | Melody number in Foltmar. |
| Heading (as written) | 93 | Alleeneste Gud i Himmerig | Melody title as written. |
| Verses | 86 | 5 | Number of stanza lines under the melody. |
| Note on the page (read by eye) | 33 | (earlier copy of No. 1) | Any note written on the page, as read. |
| Breitendich 1764 page | 86 | 60 | Page of the same melody in Breitendich 1764. |
| German melody (via Breitendich/Berggreen) | 54 | Allein Gott in der Höh sei Ehr | German melody it is, as identified through Breitendich or Berggreen. |
| DE ID | 51 | DE-00295 | German text ID (Zahn_texts_and_links Texts) |
| Lindeman 1873 no. | 32 | 89 | Number of the same melody in Lindeman's Koralbog 1873. |
| Berggreen no. | 28 | 2 | Number of the same melody in Berggreen. |
| Zahn no. | 54 | 4457 | Zahn melody number (with variant letter) |
| View tune: Zahn no. | 54 | ▶ 4457 (III, p. 80) | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 54 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: Zahn no.' (as a URL). |
| Zahn no. from | 54 | Lindeman 1873 form | Where the Zahn number came from (Lindeman form, earliest tune of the text, or Claude's note). |
| Status | 93 | confirmed via Lindeman 1873 form checked on the Zahn scan (C | how sure the row is: confirmed / probable / check (see README) |
| Claude note | 5 | Foltmar: "synges paa Guds Søn er kommen af Himmelen"; openin | Claude's note on an unusual case. |
| Owner's review 2026-11-10 | 4 | yes — accepted: 4430 (owner 2026-11-10) | The owner's decision on this row in the 2026-11-10 review. |

### foltmar_1785_register.csv (301 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Foltmar 1785 register'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Hymn (register, as read) | 301 | Ach Gud du kiæreste Fader | Hymn first line as read in Foltmar's register. |
| Foltmar page | 276 | 34 | Page the register sends the hymn to. |
| Melody title itself (•) | 72 | • | • = the register line is itself a melody title. |
| Foltmar melody No. | 275 | 33 | Number of the melody on that page. |
| Melody heading | 275 | Frisk op min Siel forsage ej | That melody's heading. |
| German melody | 182 | Frisch auf, mein Seel, verzage nicht | German melody it is (via Breitendich/Berggreen). |
| Zahn no. | 187 | 7578 | Zahn melody number (with variant letter) |
| View tune: Zahn no. | 187 | ▶ 7578 (IV, p. 476) | Link to the Zahn scan (archive.org) at the tune's page; "+n" = more numbers in the cell. |
| View tune: Zahn no. URL | 187 | https://archive.org/details/1508286757bsb11304502/page/476/m | Link carried by 'View tune: Zahn no.' (as a URL). |
| Pontoppidan 1740 no. | 265 | 223 | 1740 hymn matched to this register line. |
| … 1740 first line | 265 | Ach! Gud, du kereste Fader min | First line of that 1740 hymn. |
| … 1740 Mel. | 173 | Frisk op, min siel ec. | The 'Mel.' line printed for it in 1740. |
| … 1740 identified tune | 227 | Frisk op, min siel | Tune identified for it in the 1740 project data. |
| Pontoppidan match | 265 | probable (0.91) | How sure the match to the 1740 hymn is (probable/check, with similarity score). |
| DA Text ID | 94 | DA-0186 | Our Danish text ID for the same hymn. |
| … DA first line | 94 | Af Adams fald er plat forderffd | Its first line in our list. |
| DA match | 94 | probable (1.00) | How sure that match is (with score). |
| Foltmar vs 1740 Mel. | 244 | same melody | Whether Foltmar and the 1740 'Mel.' line give the same melody. |
| Review 2026-11-10 (Claude) | 18 | register line illegible — match unreliable | Claude's judgement of a flagged difference: resolved (same melody) / real difference / match unreliable / check |

### lindeman_1873_older_melodies.csv (77 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Lindeman 1873 older melodies'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Lindeman no. | 77 | 85 | Melody number in Lindeman's Koralbog (1873). |
| Page (PDF) | 77 | 5 | Page of the PDF scan. |
| Melody name (Lindeman) | 77 | Af Høiheden oprunden er | Melody name as printed. |
| Landstad hymns (Salme nos.) | 77 | 140 19 45 71 | Landstad hymnal numbers sung to it, as listed by Lindeman. |
| Opening as read (notes) | 77 | C4 G4 E4 C4 G4 A4 A4 G4 G4 A4 B4 C5 B4 A4 A4 G4 E4 | Opening notes read on the scan (C4 = middle C). |
| German text named by Claude | 49 | DE-05610 Wie schön leuchtet der Morgenstern | German text whose tune this is (Claude's identification). |
| Best tune of that text | 49 | 5873 | Zahn tune of that text whose incipit fits best. |
| View tune: Best tune of that text | 49 | ▶ 5873 (III, p. 565) | Link text for the Zahn scan of the (first) tune in 'Best tune of that text'. |
| View tune: Best tune of that text URL | 49 | https://archive.org/details/1508285990bsb11304501/page/565/m | Link carried by 'View tune: Best tune of that text' (as a URL). |
| Score | 49 | 1 | Incipit similarity (0–1) for that tune. |
| Best Zahn match overall | 77 | 5873 | Best-fitting incipit among all Zahn tunes. |
| View tune: Best Zahn match overall | 77 | ▶ 5873 (III, p. 565) | Link text for the Zahn scan of the (first) tune in 'Best Zahn match overall'. |
| View tune: Best Zahn match overall URL | 77 | https://archive.org/details/1508285990bsb11304501/page/565/m | Link carried by 'View tune: Best Zahn match overall' (as a URL). |
| Overall score | 77 | 1 | Its similarity (0–1). |
| Its text | 77 | Ich bin ja, Herr, in deiner Macht | Text that tune belongs to in Zahn. |
| 2nd/3rd | 77 | 4520 0.92 ; 8359 0.86 | Next best overall matches with scores. |
| Proposed Zahn no. | 52 | 5873 | Zahn number proposed for the melody. |
| View tune: Proposed Zahn no. | 52 | ▶ 5873 (III, p. 565) | Link text for the Zahn scan of the (first) tune in 'Proposed Zahn no.'. |
| View tune: Proposed Zahn no. URL | 52 | https://archive.org/details/1508285990bsb11304501/page/565/m | Link carried by 'View tune: Proposed Zahn no.' (as a URL). |
| Status | 77 | melody confirmed: matches a tune of the German text | how sure the row is: confirmed / probable / check (see README) |
| Re-check 2026-11-09 (contour vs all Zahn tunes of the text) | 14 | 4457 with the repeated 2nd note dropped (F A Bb C … vs F A A | Result of the 2026-11-09 re-check. |
| Zahn scan check 2026-11-10 | 18 | Wie schön leuchtet (8359): Lindeman no. 85 = C G E C G A A G | Result of checking against the Zahn scan on 2026-11-10. |
| Owner's review 2026-11-10 | 11 | left as is — low priority — left as recorded (owner 2026-11- | The owner's decision on this row in the 2026-11-10 review. |

### belsheim_1876.csv (156 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Belsheim 1876'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| No. | 156 | 1 | Hymn number in Belsheim's Salmer (1876). |
| Page | 156 | 3 | Page. |
| First line | 156 | Op, thi Dagen nu frembryder | First line as printed. |
| First line source | 156 | K1893 (Landstad numbering) | Where the first line was taken from (K1893 by Landstad number, or read on the page). |
| Landstad (L.) | 144 | 95 | Landstad hymnal number given by Belsheim. |
| Landstad no. status | 144 | confirmed (K1893 first line) | Whether that number was confirmed. |
| Hauge (H.) | 126 | 33 | Hauge hymnal number given. |
| Guldberg (G.) | 62 | 50 | Guldberg hymnal number given. |
| Kingo (K.) | 38 | 54 | Kingo hymnal number given. |
| Tune ("Som:") | 94 | Jeg vil mig Herren love | Melody named after 'Som:'. |
| Original language | 156 | German | Original language of the hymn per Belsheim's note. |
| Author (Belsheim note) | 156 | Johan Anastasius Freylinghausen (1670–1739) | Author named in Belsheim's note. |
| Translator (Belsheim note) | 55 | Brorson | Translator named in Belsheim's note. |
| Bible / note | 73 | Matth. 21, 1–9 | Bible reference or other note. |
| Hymnal refs as read (OCR) | 156 | (8. 95. HD. 4 2 | The hymnal reference line as OCR read it. |
| Parse note | 18 | printed no. read as 39 | Note on how a doubtful number was read. |
| Our text ID | 56 | DA-0092 | Our ID for the same text. |
| Matched by | 56 | K1893 no. = Landstad no. | How it was matched to our text. |
| German candidates (same author, if not identified) | 20 | DE-00306 Aller Welten Herrscher / DE-00356 Allweiser Schöpfe | Zahn texts by the same author, as candidates (not a link). |
| German original (DE ID) | 48 | DE-00415 | German original identified. |
| German original first line | 48 | Auf auf, weil der Tag erschienen | Its first line. |
| German original status | 72 | probable (Belsheim author note + first line) | How sure the German original is. |
| Som: → Zahn (proposed) | 51 | 346 (probable) | Zahn tune proposed from the 'Som:' melody name. |
| View tune: Som: → Zahn (proposed) | 51 | ▶ 346 (I, p. 98) | Link text for the Zahn scan of the (first) tune in 'Som: → Zahn (proposed)'. |
| View tune: Som: → Zahn (proposed) URL | 51 | https://archive.org/details/1508283124bsb11304498/page/98/mo | Link carried by 'View tune: Som: → Zahn (proposed)' (as a URL). |
| Lindeman 1873 → Zahn | 59 | 346 (Lindeman no. 98, re-checked) | Zahn tune of the same melody in Lindeman 1873. |
| View tune: Lindeman 1873 → Zahn | 59 | ▶ 346 (I, p. 98) +1 | Link text for the Zahn scan of the (first) tune in 'Lindeman 1873 → Zahn'. |
| View tune: Lindeman 1873 → Zahn URL | 59 | https://archive.org/details/1508283124bsb11304498/page/98/mo | Link carried by 'View tune: Lindeman 1873 → Zahn' (as a URL). |

### belsheim_1876_tunes.csv (94 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Belsheim 1876 – tunes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Belsheim no. | 94 | 2 | Hymn number in Belsheim 1876. |
| Our text ID | 28 | DA-0044 | Our ID for the same text. |
| First line | 94 | Hvorledes skal jeg møde | First line as printed. |
| Som (as read) | 94 | Jeg vil mig Herren love | Melody name after 'Som:' as read. |
| Som (cleaned) | 94 | Jeg vil mig Herren love | Same, spelling corrected. |
| German melody text (DE ID) | 51 | DE-05167 | German text the melody name stands for. |
| German first line | 51 | Vom Himmel hoch da komm ich her | Its first line. |
| Basis | 51 | melody name = German "Vom Himmel hoch da komm ich her" (iden | Why that German text was chosen. |
| Zahn melodies of that text | 51 | 297d 344a 344b 344c 344d 346 | All Zahn tunes of that text. |
| View tune: Zahn melodies of that text | 51 | ▶ 297d (I, p. 81) +5 | Link text for the Zahn scan of the (first) tune in 'Zahn melodies of that text'. |
| View tune: Zahn melodies of that text URL | 51 | https://archive.org/details/1508283124bsb11304498/page/81/mo | Link carried by 'View tune: Zahn melodies of that text' (as a URL). |
| Proposed Zahn no. (earliest own tune) | 51 | 346 | Zahn tune proposed (earliest tune of the text). |
| View tune: Proposed Zahn no. (earliest own tune) | 51 | ▶ 346 (I, p. 98) | Link text for the Zahn scan of the (first) tune in 'Proposed Zahn no. (earliest own tune)'. |
| View tune: Proposed Zahn no. (earliest own tune) URL | 51 | https://archive.org/details/1508283124bsb11304498/page/98/mo | Link carried by 'View tune: Proposed Zahn no. (earliest own tune)' (as a URL). |
| Status | 94 | no German melody identified (Danish/Norwegian melody or not  | how sure the row is: confirmed / probable / check (see README) |
| Lindeman 1873 melody (by Landstad no.) | 58 | No. 122 Jeg vil mig Herren love | Melody Lindeman 1873 gives for the same Landstad number. |
| Lindeman → Zahn | 39 | 346 | Zahn tune of that Lindeman melody. |
| View tune: Lindeman → Zahn | 39 | ▶ 346 (I, p. 98) | Link text for the Zahn scan of the (first) tune in 'Lindeman → Zahn'. |
| View tune: Lindeman → Zahn URL | 39 | https://archive.org/details/1508283124bsb11304498/page/98/mo | Link carried by 'View tune: Lindeman → Zahn' (as a URL). |
| Lindeman status | 58 | no clear Zahn match (probably a Scandinavian melody) | How sure the Lindeman–Zahn match is. |
| Som: proposal vs Lindeman | 39 | same Zahn melody | Whether the 'Som:' proposal and Lindeman agree. |
| Resolved 2026-11-10 (via Lindeman / Zahn scan) | 19 | probable: Zahn 2781 — Lindeman 1873 no. 114 (melody of this  | Outcome when disagreements were resolved on 2026-11-10. |
| Owner's review 2026-11-10 | 10 | yes — accepted: 2781 (owner 2026-11-10) | The owner's decision on this row in the 2026-11-10 review. |

### berggreen_origins.csv (143 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Berggreen origins'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Berggreen no. (10th ed.) | 143 | 1 | Melody number in Berggreen (10th edition). |
| PDF page | 132 | 16 | Page of the PDF scan. |
| Melody title (Berggreen) | 143 | „zum zeugniss frommer Christen, so vor uns gewest sind." Lig | Melody title as printed (OCR). |
| German title (Berggreen) | 47 | Allein Gott in der Höh sei Ehr | German melody title Berggreen gives. |
| DE ID | 41 | DE-00295 | German text ID (Zahn_texts_and_links Texts) |
| German first line (Zahn) | 41 | Allein Gott in der Höh sei Ehr | Matching first line in Zahn's register. |
| Zahn melodies of that text | 40 | 4457 | All Zahn tunes of that text. |
| View tune: Zahn melodies of that text | 40 | ▶ 4457 (III, p. 80) | Link text for the Zahn scan of the (first) tune in 'Zahn melodies of that text'. |
| View tune: Zahn melodies of that text URL | 40 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: Zahn melodies of that text' (as a URL). |
| Origin note (OCR, Berggreen) | 143 | „zum zeugniss frommer Christen, so vor uns gewest sind." Lig | Berggreen's origin note (OCR, may be garbled). |

### kingo_hymnal_melody_lines.csv (59 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Kingo hymnal melody lines'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| PDF page | 59 | 15 | Page of the PDF scan (Kingo hymnal, 1833 printing). |
| Column | 59 | 1 | Column of the printed page. |
| Heading (OCR, 2 lines before) | 59 | i faindrægtighed. Kyrie eleiſou, Elev diſſe to Vers, under | Text just above the melody line (OCR, often garbled). |
| Melody line (OCR) | 59 | FF: + ben Melodie; — | The melody line as OCR read it. |
| Kind | 59 | named | named = a melody is named; egen = own melody; forrige = same as the previous hymn. |
| Melody name (OCR) | 51 | i IEſu føde hukommelfe, | The melody name as OCR read it. |
| Melody matched to | 35 | Jesu søde Hukommelse (Breitendich p. 124) | Melody it was matched to (Breitendich page or Lindeman no.). |
| Match score | 50 | 0.74 | Name similarity (0–1). |
| DE ID (via melody) | 18 | DE-03044 | German text of that melody. |
| View tune: DE ID (via melody) | 18 | ▶ 1573 (I, p. 413) by name | Link text for the Zahn scan of the (first) tune in 'DE ID (via melody)'. |
| View tune: DE ID (via melody) URL | 18 | https://archive.org/details/1508283124bsb11304498/page/413/m | Link carried by 'View tune: DE ID (via melody)' (as a URL). |
| German / Zahn (via melody) | 18 | Jesu dulcis memoria | Its German first line (or Zahn no.). |
| First line (OCR) | 57 | j €) su, føde JEfu , dig | Hymn first line as OCR read it. |
| Pontoppidan 1740 no. (same first line) | 29 | 204 | 1740 hymn with the same first line. |
| … its first line | 29 | O! JEsu, søde JEsu, dig | First line of that 1740 hymn. |
| … its Mel. (1740) | 24 | JEsu søde hukommelse. | The 1740 'Mel.' line. |
| … its identified tune (1740 data) | 26 | JESU DULCIS MEMORIA | Tune identified in the 1740 project data. |
| Pontoppidan match | 29 | check (0.77) | How sure the 1740 match is (with score). |
| Kingo vs Pontoppidan melody | 20 | same melody name | Whether the two books name the same melody. |
| DA Text ID (same first line) | 9 | DA-0051 | Our Danish text ID with the same first line. |
| … DA first line | 9 | Jeg arme Synder træde maa | Its first line. |
| DA match | 9 | probable (0.92) | How sure that match is (with score). |
| Review 2026-11-10 (Claude) | 5 | resolved: same melody — Foltmar No. 31 "Mit Haab og Trøst" i | Claude's judgement of a flagged difference: resolved (same melody) / real difference / match unreliable / check |

### guldberg_1779_melody_lines.csv (159 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Guldberg 1779 melody lines'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| PDF page | 159 | 16 | Page of the PDF scan (Guldberg 1779). |
| Hymn no. (Guldberg, OCR) | 104 | 10 | Hymn number in Guldberg's hymnal (1779), as OCR read it. |
| Mel. line (OCR) | 157 | "zu Mel. Ef lidef Bart fad Infkeligt 26. / | The 'Mel.' line as OCR read it. |
| Melody name (OCR) | 159 | Ef lidef Bart fad Infkeligt 26. | The melody name as OCR read it. |
| Melody matched to | 124 | Et lidet Barn saa lysteligt (Breitendich p. 4) | Melody it was matched to (Breitendich page or Lindeman no.). |
| Match score | 159 | 0.6 | Name similarity (0–1). |
| DE ID (via melody) | 83 | DE-01336 | German text of that melody. |
| View tune: DE ID (via melody) | 83 | ▶ 7870 (IV, p. 589) by name | Link text for the Zahn scan of the (first) tune in 'DE ID (via melody)'. |
| View tune: DE ID (via melody) URL | 83 | https://archive.org/details/1508286757bsb11304502/page/589/m | Link carried by 'View tune: DE ID (via melody)' (as a URL). |
| German / Zahn (via melody) | 83 | Ein Kindelein so löbelich | Its German first line (or Zahn no.). |
| First line (OCR) | 159 | Ama heyt min Siel! vær hierteglad ! Mik i | Hymn first line as OCR read it. |
| Next line (OCR) | 144 | bled her Fred gan Jorden 3 Frngt ey jog . | The line after the first line (OCR). |
| Pontoppidan 1740 no. (same first line) | 49 | 216 | 1740 hymn with the same first line. |
| … its first line | 49 | Syng, min mund, bliv stedse ved | First line of that 1740 hymn. |
| … its Mel. (1740) | 49 | Siunge vi af hiertens gr. (Ger incipit: Singe nun, erfreuter | The 1740 'Mel.' line. |
| … its identified tune (1740 data) | 42 | SINGEN WIR AUS HERZENSGRUND | Tune identified in the 1740 project data. |
| Pontoppidan match | 49 | check (0.76) | How sure the 1740 match is (with score). |
| Guldberg vs Pontoppidan melody | 49 | same melody name | Whether the two books name the same melody. |
| DA Text ID (same first line) | 18 | DA-0039 | Our Danish text ID with the same first line. |
| … DA first line | 18 | Hvi vil du dig saa klage | Its first line. |
| DA match | 18 | probable (0.93) | How sure that match is (with score). |
| Review 2026-11-10 (Claude) | 10 | resolved: same melody — Foltmar puts Jesu dine dybe Vunder u | Claude's judgement of a flagged difference: resolved (same melody) / real difference / match unreliable / check |
| Owner's review 2026-11-10 | 0 |  | The owner's decision on this row in the 2026-11-10 review. |

### pontoppidan_1740_check.csv (549 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Pontoppidan 1740 check'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Owner's note | 0 |  | The owner's note on this row (sheet column was 'Your note'). |
| No. | 549 | 1 | Hymn number in Pontoppidan's Den nye Psalme-Bog (1740). |
| Page | 549 | 1 | Page. |
| Danish first line (1740) | 549 | Kom, hedningers Frelser sand | First line as printed in 1740. |
| Hymn author (1740 data) | 549 | Martin Luther (based on Ambrose's Veni redemptor gentium) | Author in the 1740 project data. |
| Source title (1740 data) | 218 | NUN KOMM, DER HEIDEN HEILAND | Original (German/Latin) title in the 1740 project data. |
| → German text (from 1740 data) | 164 | DE-03990: Nun komm der Heiden Heiland | Our German text matched to that title. |
| Same Danish text elsewhere (our ID) | 134 | DA-0205 | Our ID for the same Danish text in other hymnals. |
| Its hymnals | 134 | Danish Reformation hymnals (HM 2004 register) | Hymnals where that text appears. |
| → German text (independent) | 45 | DE-03990: Nun komm der Heiden Heiland | German link of that text from other sources (independent check). |
| Reformation books (salmer.dsl.dk) | 108 | Thomissøn 1569 | Danish Reformation hymnals containing it (salmer.dsl.dk). |
| Reformation title (modern spelling) | 108 | Kom hedningers frelser sand | Its title there, modern spelling. |
| HM 2004 no. | 106 | 222 | Number in the Hymnologiske Meddelelser 2004 register. |
| Original per HM 2004 | 65 | German: Nu kom der Heyden heyland | Original first line given by the HM 2004 register. |
| → German text (HM 2004) | 55 | DE-03990: Nun komm der Heiden Heiland | Our German text for it. |
| TEXT check | 549 | AGREE | Whether the 1740 German link agrees with the independent sources. |
| AUTHOR check | 182 | AGREE | Whether the 1740 author agrees with the German text's author in Zahn. |
| Mel. as printed (1740) | 447 | (continues tune of Hymn 1/2) | The 'Mel.' line as printed (owner's transcription). |
| Mel. = 1740 hymn no. | 298 | 368 | 1740 hymn whose first line the 'Mel.' line names. |
| Mel. text elsewhere (our ID) | 188 | DA-0207 | Our ID for that melody's text. |
| → its German text | 68 | DE-05167: Vom Himmel hoch da komm ich her | German text of that melody. |
| Identified tune (1740 data) | 447 | NUN KOMM, DER HEIDEN HEILAND | Tune identified in the 1740 project data. |
| View tune: Identified tune (1740 data) | 277 | ▶ 1174 (I, p. 314) by name | Link text for the Zahn scan of the (first) tune in 'Identified tune (1740 data)'. |
| View tune: Identified tune (1740 data) URL | 277 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: Identified tune (1740 data)' (as a URL). |
| Tune ID confidence (1740 data) | 549 | verified | Confidence given in the 1740 data (verified, own_tune, no_match …). |
| TUNE check | 549 | no Mel. printed | Whether the identified tune agrees with the 'Mel.' line's German text. |
| English (1740 data) | 92 | Savior of the Nations, Come | English translation title in the 1740 data. |
| Translator (1740 data) | 178 | William M. Reynolds | Translator in the 1740 data (a few cells hold a title by mistake). |
| ENGLISH check | 92 | AGREE | Whether that English text is in our list and linked to the same German. |
| Breitendich 1764 melody (page) | 189 | Kom, Hedningers Frelser sand (p. 1, via own melody (first li | Breitendich melody (and page) for the hymn. |
| German (Claude, from Breitendich name) | 130 | Nun komm der Heiden Heiland | German melody the Breitendich melody is (Claude, by name). |
| View tune: German (Claude, from Breitendich name) | 124 | ▶ 1174 (I, p. 314) by name | Link text for the Zahn scan of the (first) tune in 'German (Claude, from Breitendich name)'. |
| View tune: German (Claude, from Breitendich name) URL | 124 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: German (Claude, from Breitendich name)' (as a URL). |
| Breitendich TUNE check | 141 | AGREE | Whether Breitendich agrees with the 1740 tune. |
| Kingo hymnal: sung as (OCR) | 29 | Fra Himmelen høyt komme vi nu her (Breitendich p. 10) (PDF p | Melody named in the Kingo hymnal (OCR). |
| Kingo vs 1740 Mel. | 20 | same melody name | Whether Kingo and 1740 name the same melody. |
| Guldberg 1779: Mel. (OCR) | 49 | Mit Barn! feygt den fande Gud (no. 70, PDF p. 68; first-line | Melody named in Guldberg 1779 (OCR). |
| Guldberg vs 1740 Mel. | 49 | same melody name | Whether Guldberg and 1740 name the same melody. |
| Note (2026-11-10) | 14 | probable tune: Zahn 2164 — Breitendich p. 3 = Auf meinen lie | Note from the 2026-11-10 review. |
| Foltmar 1785 melody (register) | 237 | No. 22 Kom Hedningers Frelser sand (p. 23; register 'Kom Hed | Foltmar melody (from his register) for the hymn. |
| Foltmar vs 1740 Mel. | 237 | same melody | Whether Foltmar and 1740 give the same melody. |
| Review 2026-11-10 (Kingo/Guldberg/Foltmar differences) | 24 | Foltmar: resolved: same melody (1740 Mel. cell garbled; tune | Outcome of reviewing the differences on 2026-11-10. |
| Owner's review 2026-11-10 | 8 | yes — accepted: 2164 (Zahn) instead of NUN KOMM, DER HEIDEN  | The owner's decision on this row in the 2026-11-10 review. |
| Owner's review 2026-11-12 | 202 | Q14: Breitendich p. 2 = Zahn 4297a (owner 2026-11-12) | The owner's decisions from 2026-11-12 on (decision pages), or a change made on the owner's instructions; dated entries separated by ' | '. |

### pontoppidan_1740_breitendich.csv (189 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Pontoppidan – Breitendich'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| No. | 189 | 1 | 1740 hymn number. |
| Danish first line (1740) | 189 | Kom, hedningers Frelser sand | First line as printed in 1740. |
| Mel. as printed (1740) | 122 | (continues tune of Hymn 1/2) | The 'Mel.' line as printed (owner's transcription). |
| Matched via | 189 | own melody (first line) | How the Breitendich melody was found: the hymn's own first line or its 'Mel.' line. |
| Breitendich melody | 189 | Kom, Hedningers Frelser sand | Breitendich 1764 melody title. |
| Breitendich page | 189 | 1 | Its page. |
| German (Claude, from Breitendich name) | 130 | Nun komm der Heiden Heiland | German melody it is (Claude, by name). |
| View tune: German (Claude, from Breitendich name) | 124 | ▶ 1174 (I, p. 314) by name | Link text for the Zahn scan of the (first) tune in 'German (Claude, from Breitendich name)'. |
| View tune: German (Claude, from Breitendich name) URL | 124 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: German (Claude, from Breitendich name)' (as a URL). |
| Identified tune (1740 data) | 156 | NUN KOMM, DER HEIDEN HEILAND | Tune identified in the 1740 project data. |
| View tune: Identified tune (1740 data) | 106 | ▶ 1174 (I, p. 314) by name | Link text for the Zahn scan of the (first) tune in 'Identified tune (1740 data)'. |
| View tune: Identified tune (1740 data) URL | 106 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'View tune: Identified tune (1740 data)' (as a URL). |
| Breitendich check | 141 | AGREE | Whether Breitendich agrees with the 1740 tune. |

### neuendorf_translations.csv (70 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Neuendorf translations'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| English title | 70 | A Child Is Born in Bethlehem | English title on lutheranchoralebook.com. |
| hymnary | 70 | ▶ hymnary search | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 70 | https://hymnary.org/search?qu=A%20Child%20Is%20Born%20in%20B | Link carried by 'hymnary' (as a URL). |
| German (or Latin) original | 70 | Ein Kind geborn zu Bethlehem (Puer natus in Bethlehem) | Original first line given on the page. |
| Author / source (as on the page) | 70 | Latin, 13th c.; German, Geistliche Lieder, Leipzig, 1545 | Author/source as given on the page. |
| Neuendorf credit (as on the page) | 70 | Tr. Christopher J. Neuendorf, 2014 | Translation credit as given on the page. |
| Kind | 70 | full translation | full translation / some stanzas / revision or composite. |
| DE ID | 59 | DE-01332 | German text ID (Zahn_texts_and_links Texts) |
| German first line (Zahn texts) | 59 | Ein Kind geborn zu Bethlehem | Matching first line in Zahn's register. |
| Match | 70 | exact | How the printed number matched the master (exact / letter added …). |
| Own tunes (Zahn nos.) | 58 | 192a 192b | Melodies Zahn lists under this text (written for it). |
| View tune: Own tunes (Zahn nos.) | 58 | ▶ 192a (I, p. 53) +1 | Link text for the Zahn scan of the (first) tune in 'Own tunes (Zahn nos.)'. |
| View tune: Own tunes (Zahn nos.) URL | 58 | https://archive.org/details/1508283124bsb11304498/page/53/mo | Link carried by 'View tune: Own tunes (Zahn nos.)' (as a URL). |
| Earliest own tune (Zahn no.) | 59 | 192a | That melody. |
| View tune: Earliest own tune (Zahn no.) | 59 | ▶ 192a (I, p. 53) | Link text for the Zahn scan of the (first) tune in 'Earliest own tune (Zahn no.)'. |
| View tune: Earliest own tune (Zahn no.) URL | 59 | https://archive.org/details/1508283124bsb11304498/page/53/mo | Link carried by 'View tune: Earliest own tune (Zahn no.)' (as a URL). |
| URL | 70 | https://www.lutheranchoralebook.com/texts/a-child-is-born-in | Page address. |
| Page last modified | 70 | 2020-04-26 | Date the page was last changed. |
| Owner's review 2026-11-10 | 19 | left as is — low priority — left as recorded (owner 2026-11- | The owner's decision on this row in the 2026-11-10 review. |

### hm_2004_register.csv (432 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'HM 2004 register'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| HM no. | 432 | 1 | Number in the Hymnologiske Meddelelser 2004 register of Danish Reformation hymns. |
| DA ID | 153 | DA-0114 | Our Danish text ID. |
| Danish first line (as printed) | 432 | Aff dybhedszens nøedh roeber iegh tiil tigh | Danish first line in the old spelling given by the register. |
| Original first line (as printed) | 225 | Auss tieffer not schrey ich zu dir | Original (German/Low German/Latin) first line given by the register. |
| Original language | 225 | German | Language of that original. |
| Author / source (as printed) | 282 | Ps. 130 - Martin Luther 1524 | Author or source as given by the register. |
| pdf page | 432 | 11 | Page of the register PDF. |
| DE ID | 161 | DE-00513 | German text ID (Zahn_texts_and_links Texts) |
| DE match | 161 | prefix | How the original was matched to our German text (exact/prefix/fuzzy + score). |
| Zahn first line | 157 | Aus tiefer Not schrei ich | First line of that German text in Zahn's register. |
| Line printed in German? | 44 | yes | yes = the Danish book printed the line in German. |
| Same text in Norwegian books (DA/NO ID) | 17 | NO-0151 | Our ID for the same text in Norwegian books. |
| In GGG Danish index | 8 | Lovet være du, Jesus Krist! | Its first line in the GGG Danish index, if listed. |

### chorale_book_1863.csv (190 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Chorale Book 1863'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| no | 190 | 1 | Number in the Chorale Book for England (1863). |
| tune | 184 | Allein Gott in der Höh' sei Ehr' | Tune named. |
| german | 190 | Allein Gott in der Höh' sei Ehr' | German first line given. |
| author | 190 | N. von Hofe, 1529 | Author and year given. |
| english | 190 | All glory be to God on High | English first line. |
| hymnary | 190 | ▶ hymnary search | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 190 | https://hymnary.org/search?qu=All%20glory%20be%20to%20God%20 | Link carried by 'hymnary' (as a URL). |
| DE | 147 | DE-00295 | Our German text ID. |
| de_how | 190 | exact | How the German link was made. |
| tune_text | 182 | DE-00295 | German text the tune name belongs to. |
| zahn | 31 | 4457 | Zahn tune number. |
| View tune: zahn | 31 | ▶ 4457 (III, p. 80) | Link text for the Zahn scan of the (first) tune in 'zahn'. |
| View tune: zahn URL | 31 | https://archive.org/details/1508285990bsb11304501/page/80/mo | Link carried by 'View tune: zahn' (as a URL). |
| en_id | 190 | EN-00001 | Our EN ID. |
| status | 190 | existing EN | Whether the EN text was already in our list, and any difference. |

### elh_handbook.csv (646 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'ELH Handbook'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| ELH | 646 | 112 | Hymn number in the Evangelical Lutheran Hymnary (1996). |
| English | 646 | A Boy is born in Bethlehem | English first line. |
| EN ID | 294 | EN-02552 | Project ID of an English text: one per distinct first line per translator. |
| hymnary | 294 | ▶ hymnary text | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 294 | https://hymnary.org/text/a_great_and_mighty_wonder | Link carried by 'hymnary' (as a URL). |
| Original language (detected) | 536 | Danish/Norwegian | Original language, detected from the article. |
| Original first line (ELH Handbook) | 262 | Et Barn er født i Bethlehem, | Original first line quoted in the Handbook article. |
| DE | 186 | DE-01332 | Our German text ID. |
| German link basis | 206 | German first line quoted in the ELH Handbook article (fuzzy) | How it was matched. |
| EN text's German link before | 241 | DE-01340 | German link the EN text had before this check. |
| Result | 186 | EN text not found | AGREE / CONFLICT / EN text not found. |
| Same Scand. text (our ID) | 2 | DA-0188 | Our ID for the Danish/Norwegian original. |
| Its German link | 1 | DE-01332 | That text's German link. |
| German lines quoted in article | 82 | Ein Kind geboren zu Bethlehem. | German lines the article quotes. |
| Translator(s) named | 101 | John Mason Neale | Translators named in the article. |

### elh_handbook_tunes.csv (413 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'ELH Handbook tunes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Tune (ELH Handbook) | 413 | A SOLIS ORTUS* (CHRISTUM WIR SOLLEN LOBEN) | Tune name heading in the ELH Handbook. |
| ELH nos. | 413 | 267 | ELH hymn numbers using the tune. |
| Zahn text with this name | 135 | DE-00015 | Zahn text whose first line is the tune name. |

### elhb_1911_tunes.csv (601 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'ELHB 1911 tunes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| ELHB no. | 589 | 1 | Hymn number in the Evangelical Lutheran Hymn-Book. |
| First line (hymnary) | 601 | Lord Jesus Christ, to us attend | First line from hymnary.org. |
| Tune (hymnary) | 529 | HERR JESU CHRIST, DICH ZU UNS WEND | Tune name from hymnary.org. |
| Tune (1911 music ed., OCR) | 370 | SWEET Savior , bless us ere we go ; | Meant to hold the tune name from the 1911 music edition; the OCR often caught a text line instead — unreliable. |
| Meter (1911) | 335 | L. M. | Meter printed in the 1911 music edition (OCR). |
| Composer / source (1911) | 300 | And bless us , more than in past days , | Meant to hold the composer/source line; often a text line (OCR misread) — unreliable. |
| Year | 221 | 1680 | Year printed with the tune (OCR). |

### julian_article_rows.csv (2,936 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Julian article rows'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Julian page | 2,936 | 4 ii | Page of Julian (1907 ed.) the row was taken from. |
| German heading (Julian, OCR) | 2,936 | Christum wir sollen loben schon | German first line heading the article section (OCR). |
| DE ID | 2,792 | DE-00669 | German text ID (Zahn_texts_and_links Texts) |
| Zahn / DB first line | 2,792 | Christum wir sollen loben schon | Matching first line in our German list. |
| Match score | 2,936 | 1 | Similarity (0–1). |
| English first line (Julian, OCR) | 2,936 | To Christ be now our homage paid | English translation first line Julian lists (OCR). |
| Julian list | 2,936 | not in C. U. | Which list Julian puts it in: in C. U. (common use) / not in C. U. |
| Translator | 1,226 | Miss Fry | Translator. |
| Year | 2,409 | 1748 | Year Julian gives. |
| Printed in | 1,341 | Sunday Magazine | Book Julian says it was printed in. |
| Existing EN ID | 913 | EN-05464 | EN text already in our list. |
| hymnary | 2,936 | ▶ hymnary search | Link to the text on hymnary.org (or a hymnary search on the first line). |
| hymnary URL | 2,936 | https://hymnary.org/search?qu=To%20Christ%20be%20now%20our%2 | Link carried by 'hymnary' (as a URL). |
| Proposed action | 2,936 | new EN text | What the import proposed (new EN text / enrich / hold). |
| Confidence | 2,936 | high | Extraction confidence (high / medium / low). |
| Context (Julian, OCR) | 2,909 |  as No. 154 in pt. iii. of the Moravian H. Bk., 1748, No. 21 | Surrounding Julian text (OCR). |
| Applied | 2,936 | new EN-05608 | What was done (e.g. new EN ID). |
| Re-read 2026-11-11 (sub-heading) | 185 | Erwachet, Harf und Psalter → DE-07255 | Result of re-reading Julian's numbered sub-headings (DATA v16). |

### hymnoglypt_left_out.csv (72 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Hymnoglypt left out'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Left out because | 72 | Latin hymn | Why this Hymnoglypt post was not added as a translation. |
| Number | 72 | 2009-10-05 | Number in that hymnal. |
| Post title | 72 | Grates nunc omnes | The post's title. |
| Hymnoglypt URL | 72 | https://matthaeusglyptes.blogspot.com/2009/10/grates-nunc-om | Link carried by 'Hymnoglypt' (as a URL). |

### norsk_salmebok_1985.csv (106 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Norsk salmebok 1985'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| NoS 1985 no. | 106 | 5 | Number in Norsk salmebok (1985). |
| Norwegian first line(s) (OCR) | 95 | Gjør døren høy, gjør porten vid | Norwegian first line(s), OCR of the register. |
| Norsk salmebok 2013 no. | 66 | 5 | Number in Norsk salmebok 2013. |
| German author (register) | 106 | Barth, Christian Gottlieb | German author named by the register. |
| Translator(s) (register) | 40 | Holm, Niels Johannes | Translator(s) named by the register. |
| Same text in our list | 42 | NO-0051 | Our ID for the same text. |
| Its German link | 8 | DA-0026 | That text's German link. |
| Candidates (author's Zahn texts, word likeness) | 83 | DE-04299: O Jesu Christ, dein Kripplein ist (0.00) | Zahn texts by the author, ranked by word likeness (suggestions, not links). |
| Author in Zahn | 106 | no | yes = the author has texts in Zahn's register. |
| N13 meter (Haavik) | 66 | 8.8.8.8 | Meter from the N13 meter list. |
| Author's Zahn texts with the same meter (suggestion only) | 8 | DE-01775: Gelobet seist du, Jesu Christ | Zahn texts by the author with the same meter (suggestions). |

### n13_versemaal_haavik.csv (120 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'N13 versemål (Haavik)'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| N13 no. | 120 | 5 | Number in Norsk salmebok 2013. |
| First line (N13) | 120 | Gjør døren høy, gjør porten vid | First line. |
| Meter (normalized, refrain lines included) | 120 | 8.8.8.8 | Syllables per line, refrain included. |
| Meter without refrain | 120 | 8.8.8.8 | Syllables per line, refrain left out. |
| Our text ID(s) | 41 | DA-0026, NO-0051 | Our IDs for the same text. |

### n13_german_authors_km_2012.csv (83 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'N13 German authors (KM 2012)'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| German author (register) | 83 | Agricola, Johannes | German author named in the Kirkemøtet 2012 register. |
| KM 2012 no. | 83 | 265 | Number in the Kirkemøtet 2012 proposal. |
| N13 no. | 81 | 277 | Number in Norsk salmebok 2013. |
| Norwegian first line | 83 | Gladelig vil vi halleluja kvede | Norwegian first line. |
| N13 meter | 81 | 11.11.11.11 | Meter from the N13 meter list. |
| Translator(s) | 78 | Landstad, Magnus Brostrup | Translator(s) named in the register. |
| Our text ID(s) | 29 | NO-0052, DA-0308 | Our IDs for the same text. |
| German link now | 23 | DE-00295 | German link those texts have now. |
| Identification (Claude) | 52 | DE-00983: Der Mond ist aufgegangen | German original identified by Claude. |
| Auto: author + meter/composer best | 26 | DE-03055 | Best automatic candidate from author + meter/composer. |
| Auto basis | 26 | meter | What the automatic candidate rests on. |
| Author's Zahn texts | 83 | 3 | How many texts by the author are in Zahn's register. |
| Candidates (scored) | 49 | DE-03055: Jesu, Jehovah, ich such und verlange (meter) | Scored candidates (suggestions, not links). |
| Note | 4 | auto: Schmücke dich (meter + Crüger) — but the Norwegian tit | Notes. |

### troens_rare_klenodie_1894.csv (355 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Troens rare Klenodie 1894'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| TrK ID | 355 | TRK-001 | Our ID for the hymn in Troens rare Klenodie. |
| Hymn no. (1894 ed.) | 226 | 1 | Hymn number in the 1894 edition. |
| Hymn no. basis | 355 | first hymn of the book (p. 1); OCR had read "3" — fixed 2026 | How that number was found. |
| Part | 355 | Troens rare Klenodie | Part of the book. |
| Page | 355 | 1 | Page. |
| Scan (Project Runeberg) | 355 | ▶ scan 0047 | Link to the page scan on Project Runeberg. |
| Scan (Project Runeberg) URL | 355 | https://runeberg.org/bhklenodie/0047.html | Link carried by 'Scan (Project Runeberg)' (as a URL). |
| First line (register, OCR) | 355 | Fryd dig! du IEsu Bruud | First line as in the register (OCR). |
| First line (on the page, OCR) | 353 | Fryd dig! du JEsn Brund, Saa stor rn Hlfrre | First line as printed on the page (OCR). |
| Melody (OCR) | 189 | Hiertelig mig nu længer | Melody line as printed (OCR). |
| Register-to-page match score | 355 | 0.88 | How well the register line matches the page line (0–1). |
| Texts in this database (QC 2026-11-13) | 119 | DA-0092 (confident) | Our Danish/Norwegian text IDs for this hymn. |
| Note | 355 | OCR is unproofread: spelling as read by the machine — always | Notes. |

## Work logs (checks, ID changes)

### julian_ocr_check_2026_11_11.csv (1,688 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Julian OCR check 2026-11-11'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| EN ID | 1,688 | EN-00065 | English text (EN Texts). |
| English first line | 1,688 | The new-born Child this early morn | As on EN Texts. |
| DE ID (v19) | 1,688 | DE-00804 | German link before the pass (DATA v19). |
| German first line (v19) | 1,688 | Das neugeborne Kindelein, das allerliebste | Its first line. |
| Julian page | 1,688 | 1014 | Page of Julian (1907 ed.) the row was taken from. |
| Result of the pass | 1,688 | another German text fits the heading better — read | What the v20 pass found: heading matches / heading not matched / English line not found / no German heading found. |
| Heading above the English line (OCR) | 1,118 | Sohmiieke dich» o Liebe Saele. ./". FVnnoi. [iTo?^ OcmitHimi | German heading the pass found above the English line (raw OCR). |
| Better-matching German text (OCR heading) | 568 | DE-04637 Schmücke dich, o liebe Seele | A German text that matched the OCR heading better than the linked one, if any. |
| Cluster (rows on one heading, page) | 566 | check: 8 rows on this heading and page | Size of the group of rows attached to the same heading on the same page (large = an import error suspected). |
| v20 action | 160 | read in OCR: link kept | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v21 action (2026-11-12) | 64 | cluster fixed (Spitta): → DE-07105 | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v22 action (2026-11-12) | 201 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v23 action (2026-11-12) | 18 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v24 action (2026-11-12) | 197 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v25 action (2026-11-12) | 129 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v26 action (2026-11-12) | 219 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v27 action (2026-11-12) | 163 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |
| v29 action (2026-11-12) | 104 | link confirmed | What that version did: confirmed / relinked to DE-… / new DE text / unlinked (not a translation of German) / TITLE; with Julian's page and the reason. |

### meter_check_2026_11_12.csv (332 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Meter check 2026-11-12'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| No. (1740) | 332 | 1 | 1740 hymn number. |
| Danish first line (1740) | 332 | Kom, hedningers Frelser sand | First line. |
| Zahn tune | 332 | 1174 | Zahn number of the tune printed. |
| Zahn tune URL | 332 | https://archive.org/details/1508283124bsb11304498/page/314/m | Link carried by 'Zahn tune' (as a URL). |
| Tune confidence | 332 | confirmed | Confidence of the hymn's tune link. |
| Syllables per line, stanza 1 (approx.) | 332 | 4.3.4.3.1.7.7 | Approximate syllables per printed line of stanza 1. |
| Stanza 1 syllables | 332 | 29 | Total syllables of stanza 1. |
| Zahn syllable pattern | 323 | 7.7.7.7 | Syllable pattern of the linked Zahn tune. |
| Tune syllables | 323 | 28 | Total syllables of that pattern. |
| Difference | 323 | 1 | Stanza total minus tune total; large = the tune link needs a look. |
| Verdict | 332 | fits | fits / close / fits (tune repeated) / does not fit — total syllables of stanza 1 against the tune's pattern (within 6% / 15%). |
| Recheck 2026-11-12 (Claude) | 49 | counting artefact: the transcribed stanza 1 runs on into lat | For the 46 'does not fit' rows: why the count was off (counting artefact / refrain / Reformation-era Danish) or REAL with the tune correction made; also notes tunes changed later. |

### data_issues.csv (17 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Data issues'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Where | 17 | Comparison index | Source of the Danish text. |
| Issue | 17 | ELHB nos. 230 and 286 appear swapped: ELHB index says 230 =  | A problem found in a source or in our data. |
| Action | 13 | Check the 1918 book; fix the comparison index | What to do about it, or what was done. |

### scandinavian_id_changes.csv (111 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'Scandinavian ID changes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Old ID (v2) | 111 | NO-0003 | ID before the change. |
| New ID (v3) | 111 | DA-0001 | ID now. |
| Why | 111 | Danish translation printed unrevised in Norwegian books | Reason for the suggestion. |

### en_id_changes.csv (26 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'EN ID changes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Old EN ID (v13) | 26 | EN-05077 | EN ID before the merge. |
| New EN ID (v14) | 26 | EN-00475 | EN ID it was merged into. |
| Why | 26 | same English first line, same German source and translator — | Reason for the suggestion. |

### de_id_changes.csv (1 rows)

From: Tunes_and_Texts_DATA_2026-11-23_v95.xlsx, sheet 'DE ID changes'.

| Column | Filled | Example | Meaning |
|---|---|---|---|
| Old ID | 1 | DE-07098 | DE ID before the change. |
| New ID | 1 | DE-05236 | DE ID now. |
| Why | 1 | "Wenn wir in höchsten Nöten sein" (provisional) = Zahn's "Wa | Reason for the change. |



## persons.csv (core, added 2026-11-23)
Authority list: one row per identified author, translator or composer. **Person key** stable ID; **Preferred name** "Surname, Given"; **Name (display)**; **Born / Died** years (German National Library GND where it has the person, otherwise hymnological reference works); **Role**; **GND / GND URL / VIAF** authority-file IDs; **Texts (n) / Tunes (n)** and **Text IDs / Zahn nos.** the texts and tunes credited to the person; **Printed forms** the credits as printed in the sources that were merged into this person. 377 persons, about 83 % of author/composer credits; the rest stay as printed.

## text_guidance.csv (core, added 2026-11-23)
One row per text. **Place in family tree**: original (no original linked above it) or translation; **Original (top of tree)** the text at the top. **Original's own tune(s)**: Zahn tunes of the original that Zahn prints under the original itself (they first appeared with it). **Original's borrowed tune(s)**: tunes the original was sung to that Zahn prints under another text (an original with only "also sung to" tunes counts as borrowed). **Other melodies**: tunes linked to this text that the original does not have. **Copyright status (guidance)**: public domain (printed in a book before 1931, hymnary.org "Public Domain", or every credited person died by 1930) / likely public domain, life + 70 (every credited person died 1931–1955, no printing before 1931 found) / probably in copyright (hymnary.org © notice, or a credited person died 1956 or later or is living) / not known; **Copyright basis** the reason. Guidance from dates, not legal advice.

**First line before spell check (2026-11-23)** (scandinavian_texts, de_texts_added, zahn_texts): the first line before the 2026-11-23 spell/OCR check of German and Danish first lines; empty where nothing changed.
