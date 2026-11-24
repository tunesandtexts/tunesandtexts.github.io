# 2026-11-23 (v6): rows labelled "NOT DATA (owner …)" are also left out (owner 2026-11-23).
# 2026-11-20 (v4): unchanged from export_v3; used for the 0.9 rebuild from DATA v90 + Master v16 + texts v9.
# 2026-11-20 (v3): + row filter — rows labelled "MOVED (QC3 …)" (kept in DATA for the record; the text now lives under its new ID) and "NOT DATA (QC3 …)" (junk) are left out of the release (owner 2026-11-20).
# 2026-11-19: + Other-language sheets (FI/CS/SK). 2026-11-13: release export (0.9 provisional; trims from the source audit SOURCE_AUDIT.csv applied) — one CSV per table from DATA v41 + the Zahn tune master v7
# + Zahn texts/links v3. Hyperlinked columns get a '<column> URL' column next to them. Personal column names neutralised
# ('Your decision' → "Owner's decision"). Folders: core/ (the database proper), sources/ (per-source readings), work/ (check logs, ID changes).
import openpyxl,csv,os,re,sys,json,datetime
OUT=sys.argv[1]; DATA=sys.argv[2]; MASTER=sys.argv[3]; ZT=sys.argv[4]
def slug(s): return re.sub(r'_+','_',re.sub(r'[^a-z0-9]+','_',s.lower().replace('–','-').replace('→','to').replace('ø','o').replace('å','aa').replace('ü','u'))).strip('_')
PLAN={'core':['EN Texts','EN-Tune links','Scandinavian texts','Scandinavian–Tune links','Scandinavian–English links','New DE texts','Becker Psalter (Schütz)','Translators','Hymnal appearances','Scandinavian appearances','Other-language texts','Other-language–Tune links','Other-language appearances','Tune names → Zahn','Tune evidence'],
 'sources':['Breitendich 1764 melodies','Breitendich cross-references','Foltmar 1785 melodies','Foltmar 1785 register','Lindeman 1873 older melodies','Belsheim 1876','Belsheim 1876 – tunes','Berggreen origins','Kingo hymnal melody lines','Guldberg 1779 melody lines','Pontoppidan 1740 check','Pontoppidan – Breitendich','Neuendorf translations','HM 2004 register','Chorale Book 1863','ELH Handbook','ELH Handbook tunes','ELHB 1911 tunes','Julian article rows','Hymnoglypt left out','Norsk salmebok 1985','N13 versemål (Haavik)','N13 German authors (KM 2012)','Troens rare Klenodie 1894'],
 'work':['Julian OCR check 2026-11-11','Meter check 2026-11-12','Data issues','Scandinavian ID changes','EN ID changes','DE ID changes']}
NAMES={'New DE texts':'de_texts_added','Scandinavian–Tune links':'scandinavian_tune_links','Scandinavian–English links':'scandinavian_english_links','Tune names → Zahn':'tune_names_to_zahn','Belsheim 1876 – tunes':'belsheim_1876_tunes','Pontoppidan – Breitendich':'pontoppidan_1740_breitendich','Becker Psalter (Schütz)':'becker_psalter_schuetz','N13 versemål (Haavik)':'n13_versemaal_haavik','EN-Tune links':'en_tune_links','Other-language texts':'other_language_texts','Other-language–Tune links':'other_language_tune_links','Other-language appearances':'other_language_appearances'}
REN={'Your decision':"Owner's decision",'Your note':"Owner's note"}
# Trims from the source audit (2026-11-13): columns copied whole from compilations that the links do not need.
DROP={'HM 2004 register':['Notes','Occurrences in table'],
 'Norsk salmebok 1985':['Dates'],
 'N13 German authors (KM 2012)':['KM 2012 source','Melody (composer register)'],
 'N13 versemål (Haavik)':['Code','Lines','Foot','Syllables (as printed)','Alternative description (►)','Comment'],
 'ELH Handbook tunes':['Article (start)'],
 'Hymnal appearances':['Stanzas']}
# Row-level: ELH Handbook article sentences in Tune evidence are replaced by the citation.
BLANK={'Tune evidence':('Source of evidence','ELH Handbook tune article','Evidence (as printed)','(article text not included — see ELH Handbook, tune article for this ELH number)')}
trimlog=[]
# Row filter (decided 2026-11-19): from the N13 meter list keep only the hymns that link to texts in this database.
ROWKEEP={}
def _n13_used(wb):
    s=wb['Scandinavian texts']; H=[c.value for c in s[1]]; i=H.index('N13 no. (Norsk salmebok 2013)'); used=set()
    for r in s.iter_rows(min_row=2,values_only=True):
        if r[i] is not None: used|={x.strip() for x in re.split(r'[;, ]+',str(r[i])) if x.strip()}
    g=wb['N13 German authors (KM 2012)']; H=[c.value for c in g[1]]; i=H.index('N13 no.')
    used|={str(r[i]).strip() for r in g.iter_rows(min_row=2,values_only=True) if r[i] is not None}
    v=wb['N13 versemål (Haavik)']; H=[c.value for c in v[1]]; a=H.index('N13 no.'); b=H.index('Our text ID(s)')
    ROWKEEP['N13 versemål (Haavik)']=lambda r: str(r[a].value).strip() in used or (r[b].value not in (None,''))
QC3_OUT=re.compile(r'^(MOVED|NOT DATA) \((QC3|owner)')
def _qc3(wb):
    for sh,col in [('EN Texts','DE link basis'),('New DE texts','Status'),('Scandinavian texts','Link status')]:
        H=[c.value for c in wb[sh][1]]; i=H.index(col)
        ROWKEEP[sh]=(lambda i: lambda r: not QC3_OUT.match(str(r[i].value or '')))(i)
BAD=re.compile(r'\bJim\b|Hutchins',re.I)
manifest=[]; flags=[]
def dump(ws,folder,name,src):
    rows=list(ws.iter_rows())
    if not rows: return
    H=[c.value for c in rows[0]]
    if H and all(h is None or str(h).startswith('Unnamed') for h in H) and len(rows)>1:
        rows=rows[1:]; H=[c.value for c in rows[0]]  # real header sits in the first data row (DE ID changes)
    keep=[j for j,h in enumerate(H) if h is not None and not str(h).startswith('Unnamed')] or list(range(len(H)))
    dr=DROP.get(ws.title,[]); miss=[d for d in dr if d not in H]
    if miss: raise SystemExit(f'DROP columns not found in {ws.title}: {miss}')
    keep=[j for j in keep if H[j] not in dr]
    if dr: trimlog.append((ws.title,'dropped columns',', '.join(dr)))
    bl=BLANK.get(ws.title); nb=0; nkeep_drop=[0]
    linkcols={j for j in keep for r in rows[1:] if j<len(r) and r[j].hyperlink}
    hdr=[]
    for j in keep:
        h=REN.get(str(H[j]),str(H[j]) if H[j] is not None else f'col{j+1}'); hdr.append(h)
        if j in linkcols: hdr.append(h+' URL')
    os.makedirs(f'{OUT}/data/{folder}',exist_ok=True); path=f'{OUT}/data/{folder}/{name}.csv'; n=0
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(hdr)
        for r in rows[1:]:
            if ws.title in ROWKEEP and not ROWKEEP[ws.title](r): nkeep_drop[0]+=1; continue
            if bl and r[H.index(bl[0])].value==bl[1]: r=list(r); idx=H.index(bl[2]); nb+=1
            else: idx=None
            vals=[]
            for j in keep:
                c=r[j] if j<len(r) else None; v=c.value if c is not None else None
                if isinstance(v,(datetime.date,datetime.datetime)): v=v.isoformat()[:10]
                if idx is not None and j==idx and v: v=bl[3]
                vals.append('' if v is None else v)
                if j in linkcols: vals.append(c.hyperlink.target if c is not None and c.hyperlink else '')
            if not any(str(x).strip() for x in vals): continue
            for x in vals:
                if isinstance(x,str) and BAD.search(x): flags.append((name,x[:80]))
            w.writerow(vals); n+=1
    if bl: trimlog.append((ws.title,f'{bl[2]} replaced by citation',f'{nb} rows where {bl[0]} = {bl[1]}'))
    if ws.title in ROWKEEP: trimlog.append((ws.title,'rows kept only for hymns linked to this database' if ws.title.startswith('N13') else 'rows labelled MOVED / NOT DATA (QC3) left out',f'{n} kept, {nkeep_drop[0]} left out'))
    manifest.append(dict(file=f'data/{folder}/{name}.csv',sheet=ws.title,source_file=src,rows=n,columns=len(hdr)))
wb=openpyxl.load_workbook(DATA)
_n13_used(wb)
_qc3(wb)
for folder,sheets in PLAN.items():
    for s in sheets: dump(wb[s],folder,NAMES.get(s,slug(s)),os.path.basename(DATA))
done={s for v in PLAN.values() for s in v}|{'Start here'}
missing=[ws.title for ws in wb.worksheets if ws.title not in done]
mw=openpyxl.load_workbook(MASTER); dump(mw.worksheets[0],'core','zahn_tunes',os.path.basename(MASTER))
zw=openpyxl.load_workbook(ZT); dump(zw['Texts'],'core','zahn_texts',os.path.basename(ZT)); dump(zw['Text-Tune'],'core','zahn_text_tune_links',os.path.basename(ZT))
# changelog from 'Start here' version rows
sh=wb['Start here']; log=[]
for r in sh.iter_rows(values_only=True):
    if r[0] and re.match(r'v\d+',str(r[0])) and r[1]: log.append(f'- **{r[0]}** — {r[1]}')
open(f'{OUT}/CHANGELOG.md','w').write('# Changelog (DATA versions)\n\nFrom the "Start here" sheet of the working database.\n\n'+'\n'.join(log)+'\n')
json.dump(manifest,open(f'{OUT}/manifest.json','w'),indent=1,ensure_ascii=False)
with open(f'{OUT}/TRIMS.csv','w',newline='') as f: csv.writer(f).writerows([('Table','Trim','Detail')]+trimlog)
print('trims',trimlog)
print('files',len(manifest),'missing sheets',missing,'flags',len(flags)); [print(' ',f) for f in flags[:15]]
