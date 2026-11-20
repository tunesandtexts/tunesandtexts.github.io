# Tunes and Texts: Lutheran Hymns in German, Scandinavian and English

**Release 0.9 — provisional, under review (2026-11-20), built from the working database DATA v90, Zahn master v16 and Zahn texts and links v9, after two quality-control passes: QC #2 (2026-11-14 → 2026-11-19: seeded random samples in 16 batches by how the data were made; a batch passes at ≤1 serious error in 60+ rows, and every error found was fixed and swept for wherever else it occurred) and a final QC #3 (2026-11-20: an automated check of every row, a full read of the latest changes, and a 500-row random sample — 1 serious error, so the serious-error rate is at most about 1 % at 95 % confidence; the error and the 25 mislabelled rows found by the sweep were fixed), followed by a full read of the last additions (DATA v89: Finnish melodies re-read from the hymnal's printed music, Czech links checked against the Evangelický zpěvník 2021; 2 serious errors found and fixed in DATA v90).** This is a review version: links marked *probable* or *check* may still change. The sources it draws on are being invited to look it over and send corrections or objections. Release 1.0, with a DOI, will follow the review.

Compiled by John Hutchins.

## What this is
A linked index of Lutheran hymn **tunes** and **texts**:
- **9,538 tunes** — every melody in Johannes Zahn, *Die Melodien der deutschen evangelischen Kirchenlieder* (6 vols., 1889–1893), with its Zahn number, source, meter and opening notes, and a link to the scan of the tune.
- **German texts** — 5,897 from Zahn's text register (DE-00001…DE-05897) and 2,076 added by this project (DE-05898…DE-07977; 33 of them are marked DUPLICATE of a Zahn text and kept only for the record), each with the tunes it is sung to (11,789 text–tune links from Zahn).
- **7,389 English texts** (first lines), 6,228 linked to the German (or Latin) text they translate, and to Zahn tunes (3,914 English–tune links).
- **1,106 Danish, Norwegian and Swedish texts**, linked to their German originals and to Zahn tunes (1,003 links), including the whole of Pontoppidan's *Den nye Psalme-Bog* (1740) checked against Breitendich's melody book (1764).
- **475 Finnish, Czech, Slovak, Polish and Spanish texts**: Finnish translations from the Finnish hymnal of 1986 (FI-, 169), biblical-Czech translations of the Tranoscius tradition from the Cithara Sanctorum (CS-, 236) and their modern Slovak forms from the Evanjelický spevník (SK-, 58), and a few Polish (PL-, 10) and Spanish (ES-, 2) translations found among hymnary.org's records of German hymns, with 361 links to Zahn tunes — 63 of them the melody Finland sang, chosen with Zahn's citations of the Finnish chorale book (Helsingfors 1888) and the hymnal's melody notes.

The question it answers: *which tune goes with this text, where does the text come from, and is there already a translation?*

**No hymn texts are included** — only first lines, authors/translators and sources, as in Julian's *Dictionary of Hymnology* and hymnary.org.

## Website
**https://tunesandtexts.github.io/** (live once this repository is public) — search any first line, follow a hymn's family of translations from the German original, see each Zahn tune's opening notes with a link to the scan, search by melody, and compare two hymnals. A *Scholar view* switch shows the sources, evidence tags and reasoning on every line.

The site is static (no server): `index.html`, `assets/` and `site-data/`, which is built from `data/core/` by `build/build_site_data.py`. To rebuild after a data change:

```
python3 build/build_site_data.py . site-data
python3 build/build_repo.py <release folder> .   # only when a new release export replaces data/
```

To try it locally: `python3 -m http.server` in this folder, then open http://localhost:8000/.

## Folders
- `data/core/` — the database proper.
- `downloads/` — every table in one Excel workbook.
- `index.html`, `assets/`, `site-data/` — the website; `build/` — the scripts that build it.
- `data/sources/` — one table per source that was read (melody books, registers, handbooks, Julian). These are the evidence behind the core links.
- `data/work/` — check logs and ID changes.
- `DATA_DICTIONARY.md` — every file and column, with fill counts, an example and the meaning.
- `CHANGELOG.md` — what changed in each version of the working database.
- `manifest.json` — file list with row and column counts.
- `SOURCES.md` — every source, what was taken from it, its terms and the credit line; required notices (hymnary.org, the MIT-licensed salmer dataset, Matthew Carver).
- `SOURCE_AUDIT.csv` — the same as a table, with the risk and the action taken for each source (all settled 2026-11-19).
- `TRIMS.csv` — columns left out of this export because they were copied whole from a compilation.

All files are UTF-8 CSV. A column ending in **URL** holds the link that the spreadsheet cell to its left carried (Zahn scan, hymnary.org page, Julian page).

| File | Rows | From sheet |
|---|---|---|
| `data/core/en_texts.csv` | 7,389 | EN Texts |
| `data/core/en_tune_links.csv` | 3,914 | EN-Tune links |
| `data/core/scandinavian_texts.csv` | 1,106 | Scandinavian texts |
| `data/core/scandinavian_tune_links.csv` | 1,003 | Scandinavian–Tune links |
| `data/core/scandinavian_english_links.csv` | 38 | Scandinavian–English links |
| `data/core/de_texts_added.csv` | 2,076 | New DE texts |
| `data/core/becker_psalter_schuetz.csv` | 159 | Becker Psalter (Schütz) |
| `data/core/translators.csv` | 29 | Translators |
| `data/core/hymnal_appearances.csv` | 7,906 | Hymnal appearances |
| `data/core/scandinavian_appearances.csv` | 1,760 | Scandinavian appearances |
| `data/core/other_language_texts.csv` | 475 | Other-language texts |
| `data/core/other_language_tune_links.csv` | 361 | Other-language–Tune links |
| `data/core/other_language_appearances.csv` | 494 | Other-language appearances |
| `data/core/tune_names_to_zahn.csv` | 1,783 | Tune names → Zahn |
| `data/core/tune_evidence.csv` | 531 | Tune evidence |
| `data/sources/breitendich_1764_melodies.csv` | 194 | Breitendich 1764 melodies |
| `data/sources/breitendich_cross_references.csv` | 280 | Breitendich cross-references |
| `data/sources/foltmar_1785_melodies.csv` | 93 | Foltmar 1785 melodies |
| `data/sources/foltmar_1785_register.csv` | 301 | Foltmar 1785 register |
| `data/sources/lindeman_1873_older_melodies.csv` | 77 | Lindeman 1873 older melodies |
| `data/sources/belsheim_1876.csv` | 156 | Belsheim 1876 |
| `data/sources/belsheim_1876_tunes.csv` | 94 | Belsheim 1876 – tunes |
| `data/sources/berggreen_origins.csv` | 143 | Berggreen origins |
| `data/sources/kingo_hymnal_melody_lines.csv` | 59 | Kingo hymnal melody lines |
| `data/sources/guldberg_1779_melody_lines.csv` | 159 | Guldberg 1779 melody lines |
| `data/sources/pontoppidan_1740_check.csv` | 549 | Pontoppidan 1740 check |
| `data/sources/pontoppidan_1740_breitendich.csv` | 189 | Pontoppidan – Breitendich |
| `data/sources/neuendorf_translations.csv` | 70 | Neuendorf translations |
| `data/sources/hm_2004_register.csv` | 432 | HM 2004 register |
| `data/sources/chorale_book_1863.csv` | 190 | Chorale Book 1863 |
| `data/sources/elh_handbook.csv` | 646 | ELH Handbook |
| `data/sources/elh_handbook_tunes.csv` | 413 | ELH Handbook tunes |
| `data/sources/elhb_1911_tunes.csv` | 601 | ELHB 1911 tunes |
| `data/sources/julian_article_rows.csv` | 2,936 | Julian article rows |
| `data/sources/hymnoglypt_left_out.csv` | 72 | Hymnoglypt left out |
| `data/sources/norsk_salmebok_1985.csv` | 106 | Norsk salmebok 1985 |
| `data/sources/n13_versemaal_haavik.csv` | 120 | N13 versemål (Haavik) |
| `data/sources/n13_german_authors_km_2012.csv` | 83 | N13 German authors (KM 2012) |
| `data/sources/troens_rare_klenodie_1894.csv` | 355 | Troens rare Klenodie 1894 |
| `data/work/julian_ocr_check_2026_11_11.csv` | 1,688 | Julian OCR check 2026-11-11 |
| `data/work/meter_check_2026_11_12.csv` | 332 | Meter check 2026-11-12 |
| `data/work/data_issues.csv` | 17 | Data issues |
| `data/work/scandinavian_id_changes.csv` | 111 | Scandinavian ID changes |
| `data/work/en_id_changes.csv` | 26 | EN ID changes |
| `data/work/de_id_changes.csv` | 1 | DE ID changes |
| `data/core/zahn_tunes.csv` | 9,538 | Sheet1 |
| `data/core/zahn_texts.csv` | 5,897 | Texts |
| `data/core/zahn_text_tune_links.csv` | 11,789 | Text-Tune |

## IDs
- **Tunes:** Zahn number, with Zahn's variant letter (e.g. 4429a).
- **Texts:** DE- (German), DA- (Danish), NO- (Norwegian), SV- (Swedish), FI- (Finnish), CS- (Czech: the biblical Czech of the Tranoscius hymnals, which Slovak Lutherans sang into the 20th century), SK- (modern Slovak), PL- (Polish), ES- (Spanish) + number; DE-00001…05897 are Zahn's register; higher numbers were added by this project.
- **English:** EN- + number.

## How sure is each link?
Every link carries a status and the evidence it rests on:
- **confirmed** — checked against the source itself (e.g. the printed page or the notes on the page), or two independent sources agree.
- **probable** — one source, or a reading that is very likely but not certain. Shown on purpose, with its evidence.
- **check** — needs a look.
- **structural** — implied by another link.
- **REJECTED** — a link once made and later disproved; kept with the reason and the old value (`REJECTED (who, date: why) | was: …`).

Evidence tags for links taken from Julian: **PR** printed page (certain), **SC/JV** Julian's scanned text (probable), **KN** compiler's/Claude's judgement only (probable). Decisions by the compiler are marked "owner" with a date.

## Method
Data were extracted, read and matched with Claude (an AI model by Anthropic): OCR of registers and melody books, reading of opening notes on scanned pages, matching first lines across languages. Every value records its source; uncertain values are labelled; the compiler reviewed the open questions and decided them (columns "Owner's decision" / "Owner's review …"). Scans are linked, not copied.

## Main sources
Zahn I–VI (1889–1893); Julian, *A Dictionary of Hymnology* (1892; 2nd ed. 1907); Pontoppidan, *Den nye Psalme-Bog* (1740); Breitendich, *Fuldstændig Choral-Bog* (1764); Foltmar (1785); Kingo's hymnal (1833 printing); Guldberg (1779); Berggreen; Lindeman (1873); Belsheim (1876); hymnary.org; the Danish hymnal dataset (lassehjorthmadsen/salmer, MIT License); Hymnologiske Meddelelser (2004) register; Norsk salmebok 1985/2013 and the Kirkemøtet 2012 registers; GGG indexes; Matthew Carver's Hymnoglypt translations; the ELH Handbook; the Chorale Book for England (1863); the Free Lutheran Chorale-Book (Neuendorf); the Finnish hymnal of 1986 with the virsikirja.fi notes on its originals (Väinölä); the Cithara Sanctorum (1952 edition, via hymnary.org); the Evanjelický spevník; the Czech Evangelický zpěvník (2021). Full list with terms and credit lines: `SOURCES.md`.

## License
**CC0 1.0** for this project's own contributions: IDs, links, decisions, corrections and readings. Values drawn from the listed sources (first lines, register entries, attributions) remain subject to those sources' terms; see `SOURCES.md`. Please credit the sources you use.

## Quality notes
Rows whose 'First-line QC (2026-11-13)' starts with NOT … are kept for the record but are not hymn first lines; leave them out of first-line searches. In `zahn_tunes.csv`, 'Zahn no.' is Zahn's number (the ID) and 'Sort key' is only for ordering. In `zahn_text_tune_links.csv` the corrected composer and year come from Zahn master v16 (after the QC re-reading of the composer fills). German texts marked DUPLICATE in `de_texts_added.csv` name the Zahn text that replaces them; no link uses them. For the Czech texts the German original is usually the compiler's identification from the Czech first line and the author credit (marked probable), because the Czech and Slovak hymnals do not name the originals.

## How to cite
Hutchins, John (comp.). *Tunes and Texts: Lutheran Hymns in German, Scandinavian and English*, release 0.9 (provisional, 2026-11-20). Please cite the release number; a DOI will be given with release 1.0.

## Corrections
Corrections and objections are welcome, especially from the sources listed in `SOURCES.md`: use **Suggest a correction** on any page of the site, open an issue on this repository, or write to intuitufidei@gmail.com.
