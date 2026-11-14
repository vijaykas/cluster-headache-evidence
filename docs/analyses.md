# Analyses: methods, code and results

Eight computational analyses run against public data. Each section gives the
method, the result and the limitation. All code is in `scripts/`.

Results and their interpretation are the record; the claims they feed are kept
separately in `hypotheses.md`.

---

# Cluster headache analyses — code (2026-11-11)

# Cluster headache computational analyses (2026-11-11)

Re-run in order (Python 3, requests, pandas, numpy). All data is pulled from public APIs.

1. scripts/fetch_trials.py      -> data/trials.json (ClinicalTrials.gov API v2, query "cluster headache")
   scripts/classify_trials.py   -> data/trials_classified.csv (approach categories + gap search)
2. scripts/gtex.py GENES out    -> GTEx v8 median TPM for the 16 risk genes (Winsvold 2023 Table 2)
   scripts/gtex_bg.py           -> 524 random protein-coding background genes (seed 42)
   scripts/tissue_enrich.py     -> data/tissue_enrichment.csv (z-score specificity, 10,000 permutations, seed 1)
   scripts/opentargets.py       -> data/opentargets_genes.json (drugs + tractability per gene)
3. scripts/chembl_profiles.py   -> data/chembl_profiles.json (human pChEMBL per target)
   scripts/signature.py         -> data/receptor_matrix.csv, data/receptor_signature.csv
   scripts/screen_5ht7.py       -> data/approved_5ht7_screen.json (approved drugs with pChEMBL>=7 at 5-HT7)
   scripts/pubmed_counts.py     -> data/pubmed_counts.json (title/abstract co-mentions with cluster headache)

## scripts/chembl_profiles.py
```python
import requests,json,collections
B="https://www.ebi.ac.uk/chembl/api/data"
names={"sumatriptan":"SUMATRIPTAN","zolmitriptan":"ZOLMITRIPTAN","ergotamine":"ERGOTAMINE","dihydroergotamine":"DIHYDROERGOTAMINE",
"methysergide":"METHYSERGIDE","psilocin":"PSILOCIN","LSD":"LYSERGIDE",}
ids={}
for k,n in names.items():
    r=requests.get(f"{B}/molecule/search.json",params={"q":n,"limit":5},timeout=60).json()["molecules"]
    m=[x for x in r if (x["pref_name"] or "").upper()==n] or r
    ids[k]=m[0]["molecule_chembl_id"] if m else None
    print(k,ids[k],m[0]["pref_name"] if m else None)
ids["BOL-148"]="CHEMBL274384"
prof={}
for k,cid in ids.items():
    acts=[];url=f"{B}/activity.json";p={"molecule_chembl_id":cid,"pchembl_value__isnull":"false","target_organism":"Homo sapiens","limit":1000}
    while url:
        d=requests.get(url,params=p,timeout=120).json(); acts+=d["activities"]
        nxt=d["page_meta"]["next"]; url=("https://www.ebi.ac.uk"+nxt) if nxt else None; p=None
    best=collections.defaultdict(float)
    for a in acts:
        v=float(a["pchembl_value"]); t=a["target_pref_name"]
        best[t]=max(best[t],v)
    prof[k]=dict(best); print(k,len(acts),"targets",len(best))
json.dump({"ids":ids,"profiles":prof},open("data/chembl_profiles.json","w"),indent=1)
```

## scripts/classify_trials.py
```python
import json,re,collections,csv
R=json.load(open("data/trials_flat.json"))
I=[r for r in R if r["type"]=="INTERVENTIONAL"]
cats=[
 ("CGRP/PACAP pathway (antibodies, gepants)",r"galcanezumab|fremanezumab|eptinezumab|erenumab|rimegepant|zavegepant|gepant"),
 ("Neuromodulation / devices",r"stimulat|gammacore|neurostim|tdcs|rtms|transcranial|primus|bion|ati |vagus|electrode|cooling|rhinochill|onss|occipital nerve stim"),
 ("Psychedelics",r"psilocybin|lysergic|lsd"),
 ("Oxygen / gases",r"oxygen|carbon dioxide|mask"),
 ("Triptans",r"triptan"),
 ("Steroids / nerve blocks / injections",r"methylprednisolone|cortivazol|dexamethasone|greater occipital|nerve block|bupivacaine|exparel|pulsed radiofreq|\bprf\b|\bnb\b|botulinum"),
 ("Other drugs",r"candesartan|verapamil|topiramate|depak|depacon|valpro|oxybate|ketamine|magnesium|som230|pasireotide|civamide|capsaicin|acetium|droperidol|metoclopramide|ketorolac|c213|levcromakalim|vitamin|multivitamin"),
 ("Mechanism / provocation studies",r"calcitonin-gene|pacap38|levcromakalim|pet|tomography|blood sample|actigraphy"),
 ("Lifestyle / behavioral / other",r"diet|physio|exercise|yoga|breathing|osteopath|water|telephone|commitment|pbt|wearable|sensor|light"),
]
assign={}
for r in I:
    t=(r["interventions"]+" "+r["title"]).lower()
    c="Unclassified"
    for name,pat in cats:
        if re.search(pat,t): c=name; break
    assign[r["nct"]]=c
cnt=collections.Counter(assign.values())
for k,v in cnt.most_common(): print(v,k)
# targeted searches for gaps
def has(pat): return [r["nct"] for r in I if re.search(pat,(r["interventions"]+" "+r["title"]+" "+r["elig"]).lower())]
gaps={"melatonin/ramelteon/tasimelteon":has(r"melatonin|ramelteon|tasimelteon|agomelatine"),
 "light therapy":has(r"light therapy|luminette|bright light"),
 "lithium":has(r"lithium"),
 "clomiphene/hormonal":has(r"clomiphene|testosterone|estrogen"),
 "pre-bout / pre-cluster start":has(r"pre-cluster|precluster|before (the )?(onset of|start of) (the )?(cluster|bout)|pre-emptive|preemptive"),
 "pharmacogenetic":has(r"pharmacogen|genotype"),
 "anti-PACAP":has(r"anti-pacap|lu ag09222|pacap antibody"),
 "chronotherapy / timed dosing":has(r"chronotherap|bedtime dosing|timed dosing|circadian"),
}
for k,v in gaps.items(): print(f"{k}: {len(v)} {v}")
with open("data/trials_classified.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["nct","start","phase","n","category","interventions","title"])
    for r in I: w.writerow([r["nct"],r["start"][:4],r["phase"],r["n"],assign[r["nct"]],r["interventions"],r["title"]])
# enrollment by category
tot=collections.defaultdict(int)
for r in I: tot[assign[r["nct"]]]+=r["n"] or 0
print(dict(tot))
```

## scripts/fetch_trials.py
```python
import requests, json
url="https://clinicaltrials.gov/api/v2/studies"
params={"query.cond":"cluster headache","pageSize":1000,"format":"json"}
out=[]; tok=None
while True:
    p=dict(params)
    if tok: p["pageToken"]=tok
    r=requests.get(url,params=p,timeout=60); r.raise_for_status(); d=r.json()
    out+=d["studies"]; tok=d.get("nextPageToken")
    if not tok: break
json.dump(out,open("data/trials.json","w"))
print(len(out))
```

## scripts/gtex.py
```python
import requests,json,time,sys
B="https://gtexportal.org/api/v2"
genes=sys.argv[1].split(",")
out={}
ids={}
for g in genes:
    r=requests.get(f"{B}/reference/gene",params={"geneId":g,"gencodeVersion":"v26","genomeBuild":"GRCh38/hg38"},timeout=60).json()
    d=[x for x in r.get("data",[]) if x["geneSymbol"]==g]
    if d: ids[g]=d[0]["gencodeId"]
print(ids)
for g,gid in ids.items():
    r=requests.get(f"{B}/expression/medianGeneExpression",params={"gencodeId":gid,"datasetId":"gtex_v8"},timeout=60).json()
    out[g]={x["tissueSiteDetailId"]:x["median"] for x in r.get("data",[])}
json.dump(out,open(sys.argv[2],"w"))
print(len(out), list(out.values())[0] if out else None)
```

## scripts/gtex_bg.py
```python
import requests,json,random
B="https://gtexportal.org/api/v2"
g=[l.strip() for l in open("data/human_genes.tsv").read().splitlines()[1:] if l.strip() and " " not in l.strip()]
random.seed(42); samp=random.sample(g,600)
ids={}
for i in range(0,len(samp),50):
    p=[("geneId",x) for x in samp[i:i+50]]+[("gencodeVersion","v26"),("genomeBuild","GRCh38/hg38"),("itemsPerPage","250")]
    for x in requests.get(f"{B}/reference/gene",params=p,timeout=120).json().get("data",[]):
        if x["geneSymbol"] in samp and x.get("geneType")=="protein coding": ids.setdefault(x["geneSymbol"],x["gencodeId"])
print("ids",len(ids))
out={}; items=list(ids.items())
for i in range(0,len(items),4):
    chunk=items[i:i+4]
    p=[("gencodeId",gid) for _,gid in chunk]+[("datasetId","gtex_v8"),("itemsPerPage","250")]
    for x in requests.get(f"{B}/expression/medianGeneExpression",params=p,timeout=120).json().get("data",[]):
        out.setdefault(x["geneSymbol"],{})[x["tissueSiteDetailId"]]=x["median"]
json.dump(out,open("data/gtex_bg.json","w")); print("bg genes",len(out))
```

## scripts/opentargets.py
```python
import requests,json
U="https://api.platform.opentargets.org/api/v4/graphql"
def q(query,var=None):
    r=requests.post(U,json={"query":query,"variables":var or {}},timeout=90)
    if r.status_code!=200: print(r.text[:400]); r.raise_for_status()
    return r.json()
genes="DUSP10 MERTK TMEM87B FBLN7 SLC20A1 SATB2 UFL1 FHL5 KLHL32 NDUFAF4 CFTR CAPZA2 ST7 PLCE1 LRP1 CAPN2".split()
res={}
for g in genes:
    s=q('query($q:String!){search(queryString:$q,entityNames:["target"],page:{index:0,size:3}){hits{id name}}}',{"q":g})
    hit=[h for h in s["data"]["search"]["hits"] if h["name"]==g] or s["data"]["search"]["hits"]
    tid=hit[0]["id"]
    d=q('query($id:String!){target(ensemblId:$id){approvedSymbol tractability{label modality value} drugAndClinicalCandidates{count rows{maxClinicalStage drug{name mechanismsOfAction{rows{mechanismOfAction}}}}}}}',{"id":tid})["data"]["target"]
    tr=[f'{x["modality"]}:{x["label"]}' for x in d["tractability"] if x["value"]]
    drugs=[(r["drug"]["name"] if r["drug"] else r.get("id"),r["maxClinicalStage"]) for r in d["drugAndClinicalCandidates"]["rows"]]
    res[g]={"id":tid,"tractable":tr,"drugs":drugs}
    print(g,"| n_drugs",len(drugs),drugs[:8],"| tract:",tr[:5])
json.dump(res,open("data/opentargets_genes.json","w"),indent=1)
```

## scripts/pubmed_counts.py
```python
import requests,time,json
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
drugs="frovatriptan olanzapine chlorpromazine quetiapine risperidone aripiprazole clozapine lurasidone vortioxetine mianserin cyproheptadine amisulpride brexpiprazole ziprasidone methysergide dihydroergotamine tasimelteon ramelteon agomelatine melatonin clomiphene lithium verapamil".split()
out={}
for d in drugs:
    q=f'"{d}"[tiab] AND ("cluster headache"[tiab] OR "cluster headaches"[tiab])'
    r=requests.get(E,params={"db":"pubmed","term":q,"retmode":"json","retmax":20},timeout=60).json()["esearchresult"]
    out[d]={"count":int(r["count"]),"pmids":r["idlist"]}; print(d,r["count"]); time.sleep(0.4)
json.dump(out,open("data/pubmed_counts.json","w"),indent=1)
```

## scripts/screen_5ht7.py
```python
import requests,json,collections,os
B="https://www.ebi.ac.uk/chembl/api/data"
def get_all(url,params,key):
    out=[]
    while url:
        d=requests.get(url,params=params,timeout=180).json(); out+=d[key]
        nxt=d["page_meta"]["next"]; url=("https://www.ebi.ac.uk"+nxt) if nxt else None; params=None
    return out
if not os.path.exists("data/approved.json"):
    ap=get_all(f"{B}/molecule.json",{"max_phase":4,"limit":1000,"only":"molecule_chembl_id,pref_name"},"molecules")
    json.dump({x["molecule_chembl_id"]:x["pref_name"] for x in ap},open("data/approved.json","w"))
approved=json.load(open("data/approved.json")); print("approved drugs",len(approved))
tg={"5-HT7":"CHEMBL3155","5-HT6":"CHEMBL3371","5-HT2A":"CHEMBL224","5-HT1A":"CHEMBL214"}
best=collections.defaultdict(dict)
for name,tid in tg.items():
    f=f"data/acts_{name}.json"
    if not os.path.exists(f):
        json.dump(get_all(f"{B}/activity.json",{"target_chembl_id":tid,"pchembl_value__gte":7,"limit":1000,"only":"molecule_chembl_id,pchembl_value"},"activities"),open(f,"w"))
    for a in json.load(open(f)):
        m=a["molecule_chembl_id"]
        if m in approved: best[m][name]=max(best[m].get(name,0),float(a["pchembl_value"]))
mech=collections.defaultdict(dict)
for name,tid in tg.items():
    for m in get_all(f"{B}/mechanism.json",{"target_chembl_id":tid,"limit":1000},"mechanisms"):
        mech[m["molecule_chembl_id"]][name]=m["action_type"]
rows=[{"chembl":m,"drug":approved[m],**v,"mech":mech.get(m,{})} for m,v in best.items() if "5-HT7" in v]
rows.sort(key=lambda r:-r["5-HT7"])
json.dump(rows,open("data/approved_5ht7_screen.json","w"),indent=1)
print(len(rows))
for r in rows: print(r)
```

## scripts/signature.py
```python
import json,pandas as pd
d=json.load(open("data/chembl_profiles.json"))["profiles"]
# BOL-148: ChEMBL has only 5-HT6/5-HT7 values; add published functional data (Lewis et al. 2023): potent agonism at all five 5-HT1 subtypes, 5-HT2A partial agonism (EC50 0.81 nM), 5-HT6 partial agonism (EC50 0.35 nM)
lit={"5-hydroxytryptamine receptor 1A":8,"5-hydroxytryptamine receptor 1B":8,"5-hydroxytryptamine receptor 1D":8,"5-hydroxytryptamine receptor 1E":8,"5-hydroxytryptamine receptor 1F":8,"5-hydroxytryptamine receptor 2A":9.1,"5-hydroxytryptamine receptor 6":9.4}
for k,v in lit.items(): d["BOL-148"][k]=max(d["BOL-148"].get(k,0),v)
df=pd.DataFrame(d).fillna(0)
pot=(df>=7).astype(int)
lasting=["methysergide","psilocin","LSD","BOL-148"]       # reported to end bouts / lasting preventive effect
acute=["sumatriptan","zolmitriptan"]                      # abort attacks, no lasting effect
erg=["ergotamine","dihydroergotamine"]
out=pd.DataFrame({"lasting_hits":pot[lasting].sum(axis=1),"triptan_hits":pot[acute].sum(axis=1),"ergot_hits":pot[erg].sum(axis=1)})
out=out[(out.lasting_hits>=3)].sort_values(["lasting_hits","triptan_hits"],ascending=[False,True])
print(out)
pot.to_csv("data/receptor_matrix.csv"); out.to_csv("data/receptor_signature.csv")
```

## scripts/tissue_enrich.py
```python
import json,numpy as np,pandas as pd
risk=json.load(open("data/gtex_risk.json")); bg=json.load(open("data/gtex_bg.json"))
def frame(d):
    df=pd.DataFrame(d).T.fillna(0)
    df=df.drop(columns=[c for c in df.columns if c.startswith("Cells_")],errors="ignore")
    l=np.log2(df+1); sd=l.std(axis=1).replace(0,np.nan)
    return l.sub(l.mean(axis=1),axis=0).div(sd,axis=0).dropna()
R=frame(risk); G=frame(bg)[R.columns]
G=G[G.index.map(lambda x: x not in R.index)]
obs=R.mean()
rng=np.random.default_rng(1); n=len(R); P=10000
null=np.stack([G.iloc[rng.choice(len(G),n,replace=False)].mean().values for _ in range(P)])
p=(null>=obs.values).sum(0)/P
res=pd.DataFrame({"mean_z":obs.values,"p_perm":p,"null_mean":null.mean(0)},index=obs.index).sort_values("mean_z",ascending=False)
res["fdr"]=np.minimum(1,res.p_perm*len(res)/ (res.p_perm.rank()))
res.to_csv("data/tissue_enrichment.csv")
print(res.head(12).round(3)); print(res.tail(5).round(3))
# per-gene top tissues
top={g:list(R.loc[g].sort_values(ascending=False).index[:3]) for g in R.index}
for g,t in top.items(): print(g,t)
hyp=R["Brain_Hypothalamus"].sort_values(ascending=False); print("hypothalamus z:",hyp.round(2).to_dict())
```

## Key result tables
```csv
,mean_z,p_perm,null_mean,fdr,fdr_bh
Artery_Tibial,1.143518608980327,0.0,0.1732187275960849,0.0,0.005200000000000001
Artery_Aorta,0.8771293427032785,0.0012,0.2584135154760432,0.0208,0.0208
Artery_Coronary,0.8417731432340974,0.0003,0.236967115489155,0.0078,0.0078
Lung,0.7423577438843221,0.0385,0.4050636213693392,0.286,0.286
Fallopian_Tube,0.6682647232522843,0.0704,0.4376668626141715,0.4576,0.4576
Nerve_Tibial,0.6518153604213816,0.3079,0.5542194542023074,0.80054,0.7381636363636365
Thyroid,0.6385828152596122,0.312,0.5467187115897281,0.7725714285714286,0.7381636363636365
Cervix_Ectocervix,0.6179362006454869,0.1127,0.4054086440544117,0.5327636363636363,0.5300285714285714
Uterus,0.5948552905169737,0.1817,0.4322222154634706,0.590525,0.590525
Cervix_Endocervix,0.588129254419942,0.3123,0.503905426899151,0.7381636363636365,0.7381636363636365
Adipose_Subcutaneous,0.5749110490491436,0.0102,0.174746394731574,0.10608,0.10608
Colon_Transverse,0.5349241668575652,0.0018,-0.0180328106795729,0.0234,0.0234
Bladder,0.4257422006970091,0.1427,0.264935091281112,0.5300285714285714,0.5300285714285714
Adipose_Visceral_Omentum,0.4245224908134209,0.0216,0.0795944326399281,0.1872,0.1872
Breast_Mammary_Tissue,0.4178539710786274,0.0793,0.2187262866067485,0.4581777777777777,0.45817777777777774
Vagina,0.4095585792508734,0.3672,0.3545234467746926,0.8301913043478261,0.8301913043478261
Small_Intestine_Terminal_Ileum,0.3640478285033571,0.0975,0.1126065271979165,0.507,0.507
Colon_Sigmoid,0.3122447731381663,0.1326,0.1470389584101141,0.5746,0.5300285714285714
Esophagus_Gastroesophageal_Junction,0.2686710909659334,0.1397,0.1140681954276659,0.5588,0.5300285714285714
Esophagus_Muscularis,0.2482682010316654,0.1629,0.1015358695745929,0.5647199999999999,0.5647199999999999
Brain_Cerebellum,0.2379877034875522,0.6607,0.360777801699163,1.0,0.9855
Brain_Cerebellar_Hemisphere,0.2284289057395898,0.6694,0.3607561107425737,1.0,0.9855
Testis,0.2007074600798625,0.9695,1.1106559984050586,1.0,0.9855
Prostate,0.1950374607822858,0.7995,0.324991347952382,1.0,0.9855
Ovary,0.1871141399457812,0.8293,0.3899697233381354,1.0,0.9855
Minor_Salivary_Gland,0.1030566517553214,0.4261,0.0921617614061186,0.886288,0.886288
Spleen,0.0954545641315898,0.7172,0.237348454045514,1.0,0.9855
Brain_Frontal_Cortex_BA9,0.071913570828018,0.23,-0.0985429173375523,0.6644444444444445,0.6644444444444445
Adrenal_Gland,0.0506328307131871,0.2579,-0.0554059104309309,0.7058315789473685,0.7058315789473685
Pituitary,0.0060500597372037,0.9855,0.4198309211169296,0.9855,0.9855
Skin_Sun_Exposed_Lower_leg,-0.1213841795528967,0.959,0.2441405048466047,1.0,0.9855
Brain_Cortex,-0.1820468116549818,0.4764,-0.1865085011941621,0.9175111111111112,0.9175111111111112
Skin_Not_Sun_Exposed_Suprapubic,-0.2090950504989941,0.9739,0.186264945322265,1.0,0.9855
Brain_Spinal_cord_cervical_c-1,-0.2574211081757396,0.5653,-0.215816885157161,1.0,0.9855
Stomach,-0.2866409324590682,0.6388,-0.2184549889694219,1.0,0.9855
Esophagus_Mucosa,-0.3687435608283153,0.9809,0.0910593768860539,1.0,0.9855
Brain_Anterior_cingulate_cortex_BA24,-0.3753696825706244,0.4671,-0.3839511765337743,0.9342,0.9175111111111112
Kidney_Medulla,-0.3855057359263186,0.9547,-0.0859872069716761,1.0,0.9855
Brain_Caudate_basal_ganglia,-0.4952641671247767,0.6548,-0.4069658010775537,1.0,0.9855
Heart_Atrial_Appendage,-0.5033608947382184,0.3872,-0.5452359014569866,0.8389333333333333,0.8389333333333333
Brain_Hypothalamus,-0.5218529504932901,0.9066,-0.2586086527209008,1.0,0.9855
Brain_Substantia_nigra,-0.6066449646163758,0.7233,-0.4855693733705308,1.0,0.9855
Pancreas,-0.6194245482139852,0.227,-0.7955663012604175,0.6943529411764706,0.6644444444444445
Brain_Nucleus_accumbens_basal_ganglia,-0.6298551586053895,0.9297,-0.3413883885300233,1.0,0.9855
Brain_Hippocampus,-0.6751356287316368,0.7092,-0.5628829846346367,1.0,0.9855
Liver,-0.7317547930877586,0.5195,-0.6788931492377381,0.9647857142857142,0.9647857142857142
Kidney_Cortex,-0.7352141729264287,0.9406,-0.4584142906600346,1.0,0.9855
Brain_Putamen_basal_ganglia,-0.7379091242257424,0.7372,-0.6001409996040401,1.0,0.9855
Brain_Amygdala,-0.7426952610910423,0.8092,-0.5661891770182509,1.0,0.9855
Muscle_Skeletal,-0.7766968309431428,0.7573,-0.5658174608189748,1.0,0.9855
Heart_Left_Ventricle,-1.0578530260839836,0.8019,-0.86937441987472,1.0,0.9855
Whole_Blood,-1.7016215993551491,0.9805,-0.9417891456199524,1.0,0.9855
```
```csv
,lasting_hits,triptan_hits,ergot_hits
5-hydroxytryptamine receptor 2A,4,0,2
5-hydroxytryptamine receptor 7,4,0,0
5-hydroxytryptamine receptor 6,4,0,2
5-hydroxytryptamine receptor 1E,3,0,0
5-hydroxytryptamine receptor 2B,3,0,2
D(3) dopamine receptor,3,0,2
5-hydroxytryptamine receptor 1A,3,1,1
5-hydroxytryptamine receptor 2C,3,1,2
5-hydroxytryptamine receptor 1D,3,2,1
```

---

 
 Headline result of Analysis 6, in one line: the drugs reported to end a cluster bout are 5-HT7
 **antagonists**, frovatriptan is a full **agonist**, and that reverses the frovatriptan lead from Analysis 3.
 
 ---
 
 ### `scripts/eqtl_lookup.py`
 
 Analysis 5 — eQTL direction for the 13 lead variants, re-oriented to the risk allele.
 
 ```python
 import requests,json,time
 B="https://gtexportal.org/api/v2"
 # lead variants: (rsid, risk allele, locus, source)  from Winsvold 2023 Tables 2 (EUR) and 3 (trans-ancestry); EA = risk allele
 V=[("rs17011182","G","DUSP10","EUR"),("rs13399108","G","MERTK","EUR"),("rs6714578","A","FTCDNL1","EUR"),
    ("rs9486725","T","FHL5","EUR"),("rs2402176","C","WNT2","EUR"),("rs57866767","T","PLCE1","EUR"),("rs11172113","T","LRP1","EUR+TA"),
    ("rs12129860","G","DUSP10","TA"),("rs10916600","T","CAPN2","TA"),("rs10188642","A","MERTK","TA"),("rs4673382","G","FTCDNL1","TA"),
    ("rs11153085","T","FHL5","TA"),("rs2274224","G","PLCE1","TA")]
 rows=[]
 for rs,risk,locus,src in V:
     v=requests.get(f"{B}/dataset/variant",params={"snpId":rs,"datasetId":"gtex_v8"},timeout=60).json()["data"]
     if not v: print(rs,"not in GTEx"); continue
     v=v[0]; ref,alt=v["ref"],v["alt"]
     if risk==alt: sign=1
     elif risk==ref: sign=-1
     else: print(rs,"allele mismatch",risk,ref,alt); continue
     e=requests.get(f"{B}/association/singleTissueEqtl",params={"variantId":v["variantId"],"datasetId":"gtex_v8","itemsPerPage":250},timeout=120).json().get("data",[])
     print(rs,locus,src,v["variantId"],"risk=",risk,"(alt)" if sign==1 else "(ref)","eQTLs:",len(e))
     for x in e:
         rows.append(dict(rsid=rs,locus=locus,source=src,variant=v["variantId"],risk=risk,gene=x["geneSymbol"],tissue=x["tissueSiteDetailId"],
                          nes_risk=sign*x["nes"],p=x["pValue"]))
     time.sleep(0.3)
 json.dump(rows,open("data/eqtl_hits.json","w"),indent=1)
 print("total eQTL rows",len(rows))
 ```
 
 ### `scripts/ht7_pubchem.py`
 
 Analysis 6 — locate the IUPHAR/GtoPdb-deposited 5-HT7 assays in PubChem and pull their ligand tables.
 
 ```python
 import requests,json,time
 P="https://pubchem.ncbi.nlm.nih.gov/rest/pug"
 names={"psilocin":"psilocin","LSD":"lysergide","BOL-148":"2-bromolysergic acid diethylamide","methysergide":"methysergide","dihydroergotamine":"dihydroergotamine","ergotamine":"ergotamine","frovatriptan":"frovatriptan","sumatriptan":"sumatriptan","5-CT":"5-carboxamidotryptamine","serotonin":"serotonin"}
 out=[]
 for k,n in names.items():
     cid=requests.get(f"{P}/compound/name/{requests.utils.quote(n)}/cids/JSON",timeout=60).json()["IdentifierList"]["CID"][0]
     r=requests.get(f"{P}/compound/cid/{cid}/assaysummary/JSON",timeout=180).json()
     cols=r["Table"]["Columns"]["Column"]; rows=r["Table"]["Row"]
     ix={c:i for i,c in enumerate(cols)}
     n7=0
     for row in rows:
         c=row["Cell"]
         tgt=(c[ix.get("Target GeneID")] if "Target GeneID" in ix else "")
         name=c[ix["Assay Name"]] if "Assay Name" in ix else ""
         if str(tgt) in ("3363","15566","65032") or "5-HT7" in name or "5-hydroxytryptamine receptor 7" in name.lower() or "5-HT 7" in name:
             n7+=1
             out.append(dict(drug=k,cid=cid,aid=c[ix["AID"]],outcome=c[ix["Activity Outcome"]],act_name=c[ix.get("Activity Name","AID")] if "Activity Name" in ix else "",value=c[ix["Activity Value [uM]"]] if "Activity Value [uM]" in ix else "",gene=tgt,assay=name))
     print(k,cid,"rows",len(rows),"5-HT7",n7); time.sleep(0.5)
 print(cols)
 json.dump(out,open("data/ht7_pubchem.json","w"),indent=1)
 ```
 
 ### `scripts/ht7_antag_pubmed.py`
 
 Analysis 6 — for each curated 5-HT7 blocker that is an approved drug, count and list PubMed papers pairing it with cluster headache.
 
 ```python
 """Analysis 6b: for every curated 5-HT7 antagonist/inverse agonist that is an approved drug,
 count PubMed papers pairing it with cluster headache, and list titles."""
 import requests,time,json
 def get(url,params):
     for k in range(6):
         j=requests.get(url,params=params,timeout=60).json()
         if "error" not in j: return j
         time.sleep(1.5*(k+1))
     raise RuntimeError(j)
 E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
 drugs=["lurasidone","risperidone","ziprasidone","zotepine","metergoline","dihydroergotamine","fluphenazine",
 "methysergide","clozapine","mianserin","chlorpromazine","ritanserin","perphenazine","cyamemazine","thioridazine",
 "iloperidone","cyproheptadine","haloperidol","olanzapine","ketanserin","vortioxetine","amisulpride","pizotifen","ergotamine"]
 out=[]
 for d in drugs:
     q=f'"{d}"[tiab] AND ("cluster headache"[tiab] OR "cluster headaches"[tiab])'
     r=get(E+"esearch.fcgi",{"db":"pubmed","term":q,"retmode":"json","retmax":20})["esearchresult"]
     ids=r["idlist"]; titles=[]
     if ids:
         time.sleep(0.8)
         s=get(E+"esummary.fcgi",{"db":"pubmed","id":",".join(ids),"retmode":"json"})["result"]
         titles=[(i,s[i]["pubdate"][:4],s[i]["title"]) for i in ids]
     out.append({"drug":d,"n":int(r["count"]),"titles":titles}); time.sleep(0.8)
 json.dump(out,open("data/ht7_antag_pubmed.json","w"),indent=1)
 for o in out:
     print(f'{o["drug"]:18s} {o["n"]}')
     if o["drug"] not in ("dihydroergotamine","methysergide","ergotamine"):
         for t in o["titles"][:6]: print("     ",t)
 ```
 
 ### `scripts/ht7_specificity.py`
 
 Analysis 6 — the confound check: 5-HT7 vs 5-HT2A vs D2 affinity for every drug with any CH report.
 
 ```python
 """Analysis 6c: is 5-HT7 blockade the common thread among drugs reported to help CH,
 or is it confounded by 5-HT2A / D2 blockade?  Uses GtoPdb curated tables via PubChem."""
 import pandas as pd,requests
 P="https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
 def load(aid,label):
     d=pd.read_csv(f"data/aid_{aid}.csv"); d=d[pd.to_numeric(d.PUBCHEM_CID,errors="coerce").notna()].copy()
     d["CID"]=d.PUBCHEM_CID.astype(float).astype(int)
     for c in ["pKi_max","pKi_min","pKd_max","pIC50_max","pKB_max"]:
         if c not in d: d[c]=None
     num=lambda c:pd.to_numeric(d[c],errors="coerce")
     d["p"]=num("pKi_max").fillna(num("pKd_max")).fillna(num("pIC50_max")).fillna(num("pKB_max"))
     d=d.sort_values("p",ascending=False).drop_duplicates("CID")
     return d.set_index("CID")[["p","Type","Action"]].add_prefix(label+"_")
 t=load(1345291,"HT7").join(load(1259419,"HT2A"),how="outer").join(load(1345788,"D2"),how="outer")
 names=requests.post(P+"compound/cid/property/Title/JSON",data={"cid":",".join(map(str,t.index))},timeout=120).json()["PropertyTable"]["Properties"]
 t["name"]=pd.Series({p["CID"]:p.get("Title","").lower() for p in names})
 # CH clinical evidence label (from literature counts in Analyses 3/6b; open = open-label/case series)
 ch={"methysergide":"prophylaxis: effective (decades of use)","dihydroergotamine":"IV DHE breaks bouts (open series)",
 "bromolysergide":"BOL-148 pilot: lasting remission (open, n=5)","chlorpromazine":"open series: 12/13 relieved (1980)",
 "olanzapine":"abortive: 4/5 >=80% relief (open, n=5)","clozapine":"single case report","cyproheptadine":"older reports, weak",
 "sumatriptan":"acute: effective (RCT) - acts via 5-HT1B/1D","haloperidol":"no CH reports","risperidone":"no CH reports",
 "lurasidone":"no CH reports","ziprasidone":"no CH reports","vortioxetine":"no CH reports","ketanserin":"no CH reports",
 "ritanserin":"no CH reports","metergoline":"no CH reports","mianserin":"no CH reports","fluphenazine":"no CH reports",
 "iloperidone":"no CH reports","zotepine":"no CH reports","thioridazine":"no CH reports","perphenazine":"no CH reports",
 "spiperone":"no CH reports (research tool)","amisulpride":"no CH reports","ergotamine":"effective (classic)"}
 out=t[t.name.isin(ch)].copy(); out["CH_evidence"]=out.name.map(ch)
 cols=["name","HT7_p","HT7_Action","HT2A_p","HT2A_Action","D2_p","D2_Action","CH_evidence"]
 out=out[cols].sort_values("HT7_p",ascending=False)
 pd.set_option("display.width",250); print(out.to_string(index=False))
 out.to_csv("data/ht7_specificity.csv",index=False)
 ```
 
 ### `scripts/ht7_clinical.py`
 
 Analysis 6 — has any selective 5-HT7 antagonist reached human trials? ClinicalTrials.gov v2 + PubMed over 15 named compounds.
 
 ```python
 """Analysis 6d: has any SELECTIVE 5-HT7 antagonist ever reached human trials?
 Search ClinicalTrials.gov v2 + PubMed for the known selective 5-HT7 ligands."""
 import requests,time,json
 CT="https://clinicaltrials.gov/api/v2/studies"
 E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
 def eget(u,p):
     for k in range(6):
         j=requests.get(u,params=p,timeout=60).json()
         if "error" not in j: return j
         time.sleep(1.5*(k+1))
     raise RuntimeError(j)
 
 cands=["JNJ-18038683","JNJ 18038683","SB-269970","SB269970","LP-211","DR-4004",
        "lurasidone","vortioxetine","amisulpride","intepirdine","idalopirdine",
        "SB-258719","SB-656104","PZ-1444"]
 out={}
 for c in cands:
     r=requests.get(CT,params={"query.term":c,"pageSize":50,
         "fields":"NCTId,BriefTitle,Phase,OverallStatus,Condition,InterventionName,StartDate"},timeout=90).json()
     st=r.get("studies",[])
     rows=[]
     for s in st:
         p=s["protocolSection"]
         rows.append({"nct":p["identificationModule"]["nctId"],
                      "title":p["identificationModule"]["briefTitle"][:95],
                      "phase":",".join(p.get("designModule",{}).get("phases",[])),
                      "status":p["statusModule"]["overallStatus"],
                      "cond":";".join(p.get("conditionsModule",{}).get("conditions",[]))[:70]})
     q=f'"{c}"[tiab]'
     n=int(eget(E+"esearch.fcgi",{"db":"pubmed","term":q,"retmode":"json","retmax":0})["esearchresult"]["count"])
     nh=int(eget(E+"esearch.fcgi",{"db":"pubmed","term":q+' AND (human[tiab] OR patients[tiab] OR "clinical trial"[pt])',
         "retmode":"json","retmax":0})["esearchresult"]["count"])
     out[c]={"trials":rows,"pubmed_all":n,"pubmed_human":nh}
     print(f'{c:16s} trials={len(rows):3d}  pubmed={n:5d}  human/clinical={nh:4d}')
     for r_ in rows[:4]: print("    ",r_["nct"],r_["phase"],r_["status"],"|",r_["cond"],"|",r_["title"][:60])
     time.sleep(0.7)
 json.dump(out,open("data/ht7_clinical.json","w"),indent=1)
 ```
 
 ### `scripts/ht7_scn.py`
 
 Analysis 6 — 5-HT7 vs 5-HT2A in the circadian and trigeminal literature.
 
 ```python
 """Analysis 6g: which 5-HT receptor mediates circadian phase resetting in the SCN,
 and is 5-HT2A a rival explanation?"""
 import requests,time,json
 E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
 def eg(p):
     for k in range(6):
         j=requests.get(E+"esearch.fcgi",params=dict(db="pubmed",retmode="json",**p),timeout=60).json()
         if "error" not in j: return j["esearchresult"]
         time.sleep(1.5*(k+1))
 qs={
  "5-HT7 + SCN/circadian":'("5-HT7"[tiab] OR "5-HT(7)"[tiab] OR HTR7[tiab]) AND (suprachiasmatic[tiab] OR circadian[tiab])',
  "5-HT2A + SCN/circadian":'("5-HT2A"[tiab] OR "5-HT(2A)"[tiab] OR HTR2A[tiab]) AND (suprachiasmatic[tiab] OR circadian[tiab])',
  "5-HT7 + phase shift":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND ("phase shift"[tiab] OR "phase advance"[tiab] OR "phase resetting"[tiab])',
  "5-HT2A + phase shift":'("5-HT2A"[tiab] OR "5-HT(2A)"[tiab]) AND ("phase shift"[tiab] OR "phase advance"[tiab] OR "phase resetting"[tiab])',
  "5-HT7 + trigeminal":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (trigeminal[tiab] OR dura[tiab] OR meningeal[tiab])',
  "5-HT7 + CGRP":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (CGRP[tiab] OR "calcitonin gene-related"[tiab])',
  "5-HT7 + migraine":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND migraine[tiab]',
  "5-HT7 + cluster headache":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND ("cluster headache"[tiab])',
 }
 res={}
 for k,q in qs.items():
     r=eg({"term":q,"retmax":8}); res[k]={"n":int(r["count"]),"ids":r["idlist"]}
     print(f'{k:28s} {r["count"]}'); time.sleep(0.7)
 json.dump(res,open("data/ht7_scn.json","w"),indent=1)
 ids=res["5-HT7 + phase shift"]["ids"]+res["5-HT7 + trigeminal"]["ids"][:4]+res["5-HT7 + CGRP"]["ids"][:3]
 print("\nfetching",len(ids))
 print(requests.get(E+"esummary.fcgi",params={"db":"pubmed","id":",".join(ids),"retmode":"json"},timeout=90).text[:50])
 import collections
 s=requests.get(E+"esummary.fcgi",params={"db":"pubmed","id":",".join(ids),"retmode":"json"},timeout=90).json()["result"]
 for i in ids:
     if i in s: print(" ",i,s[i]["pubdate"][:4],s[i]["title"][:115])
 ```
 
 ### `scripts/ht7_gtex.py`
 
 Analysis 6 — HTR7 position and tissue expression.
 
 ```python
 """Analysis 6e: where is HTR7 expressed, and is it near a CH risk locus?"""
 import requests,json,pandas as pd
 G="https://gtexportal.org/api/v2/"
 r=requests.get(G+"reference/gene",params={"geneId":"HTR7","gencodeVersion":"v26","genomeBuild":"GRCh38/hg38"},timeout=90).json()["data"]
 g=[x for x in r if x["geneSymbol"]=="HTR7"][0]
 print("HTR7:",g["chromosome"],g["start"],g["end"],g["gencodeId"])
 ex=requests.get(G+"expression/medianGeneExpression",params={"gencodeId":g["gencodeId"],"itemsPerPage":100},timeout=90).json()["data"]
 d=pd.DataFrame(ex).sort_values("median",ascending=False)[["tissueSiteDetailId","median"]]
 print(d.head(18).to_string(index=False))
 print("\nhypothalamus/artery rows:")
 print(d[d.tissueSiteDetailId.str.contains("Hypothal|Artery|Nerve|Brain_Hypo",case=False)].to_string(index=False))
 json.dump({"gene":g,"expr":ex},open("data/htr7_gtex.json","w"))
 ```
 
 ### `scripts/ht7_dual_test.py`
 
 Analysis 6 — joint artery+hypothalamus specificity of HTR7 against the 514-gene background.
 
 ```python
 """Analysis 6f: is HTR7's joint artery+hypothalamus specificity unusual?
 Same z-score method as Analysis 2, tested against the 524-gene background
 and against all GPCR-like drug targets we have pulled."""
 import json,numpy as np,pandas as pd
 bg=json.load(open("data/gtex_bg.json")); tg=json.load(open("data/gtex_targets.json"))
 risk=json.load(open("data/gtex_risk.json"))
 allg={**bg,**tg,**risk}
 df=pd.DataFrame(allg).T
 df=df.drop(columns=[c for c in df.columns if c.startswith("Cells_") or c=="Testis"],errors="ignore").fillna(0)
 l=np.log2(df+1); sd=l.std(axis=1).replace(0,np.nan)
 Z=l.sub(l.mean(axis=1),axis=0).div(sd,axis=0).dropna()
 ART=[c for c in Z.columns if c.startswith("Artery_")]
 HYP="Brain_Hypothalamus"
 Z["artery_z"]=Z[ART].mean(axis=1); Z["hypo_z"]=Z[HYP]
 Z["dual"]=np.minimum(Z.artery_z,Z.hypo_z)          # both must be high
 bgset=[g for g in bg if g in Z.index]
 print(f"background genes used: {len(bgset)}  tissues: {len(ART)+1} of {Z.shape[1]-3}")
 for g in ["HTR7","HTR1B","HTR1D","HTR2A","HTR6","CALCA","KCNJ8","ABCC9","MTNR1A","MTNR1B","CACNA1C","PLCE1","LRP1","FHL5"]:
     if g in Z.index:
         r=Z.loc[g]
         pct=(pd.Series([Z.loc[b,"dual"] for b in bgset])<r["dual"]).mean()*100
         print(f"{g:8s} artery_z={r.artery_z:+.2f}  hypothalamus_z={r.hypo_z:+.2f}  dual={r.dual:+.2f}  >{pct:.1f}% of background")
 # empirical p for HTR7 dual score
 d=np.array([Z.loc[b,"dual"] for b in bgset]); h=Z.loc["HTR7","dual"]
 print(f"\nHTR7 dual score {h:+.3f}; background mean {d.mean():+.3f} sd {d.std():.3f}")
 print(f"empirical p (background genes with dual >= HTR7): {(d>=h).sum()}/{len(d)} = {(d>=h).mean():.4f}")
 Z[["artery_z","hypo_z","dual"]].sort_values("dual",ascending=False).head(15).round(3).to_csv("data/dual_tissue_top.csv")
 print("\ntop 12 genes overall by dual score:")
 print(Z[["artery_z","hypo_z","dual"]].sort_values("dual",ascending=False).head(12).round(2).to_string())
 ```
 
 ### `scripts/dual_profile.py`
 
 Analysis 6 — the decisive test: does 5-HT7 potency separate bout-ending drugs from acute-only triptans? Exact permutation over all 15 splits.
 
 ```python
 """Analysis 6h: the decisive test.
 Hypothesis: drugs with LASTING effects in CH combine
    (a) 5-HT1B/1D/1F AGONISM  -> prejunctional brake on CGRP release
    (b) 5-HT7  ANTAGONISM     -> blocks cranial vasodilation + circadian phase shifting
 whereas acute-only drugs (triptans) have (a) but only weak (b).
 Affinities from IUPHAR/GtoPdb curated tables via PubChem; direction from the Action column."""
 import pandas as pd,requests,numpy as np
 P="https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
 # GtoPdb-deposited PubChem AIDs for the human receptors of interest
 AID={"5HT7":1345291}
 def load(aid):
     d=pd.read_csv(f"data/aid_{aid}.csv"); d=d[pd.to_numeric(d.PUBCHEM_CID,errors="coerce").notna()].copy()
     d["CID"]=d.PUBCHEM_CID.astype(float).astype(int)
     num=lambda c: pd.to_numeric(d[c],errors="coerce") if c in d else pd.Series(np.nan,index=d.index)
     d["p"]=num("pKi_max").fillna(num("pKd_max")).fillna(num("pIC50_max")).fillna(num("pKB_max"))
     return d.sort_values("p",ascending=False).drop_duplicates("CID").set_index("CID")[["p","Type","Action"]]
 h7=load(1345291)
 nm=requests.post(P+"compound/cid/property/Title/JSON",data={"cid":",".join(map(str,h7.index))},timeout=120).json()["PropertyTable"]["Properties"]
 h7["name"]=pd.Series({x["CID"]:x.get("Title","").lower() for x in nm})
 
 # published 5-HT1B/1D/1F potency (pKi/pEC50) and CH clinical class, from the papers already read in Analyses 3 & 6
 rows=[
  # drug,            5-HT1B/1D/1F agonist potency (approx pKi, literature), CH clinical class
  ("sumatriptan",      8.5, "acute abortive only (RCT)"),
  ("zolmitriptan",     8.8, "acute abortive only (RCT)"),
  ("frovatriptan",     8.6, "acute/short prophylaxis (migraine)"),
  ("dihydroergotamine",9.0, "LASTING: IV breaks the bout"),
  ("ergotamine",       8.8, "LASTING: classic prophylaxis"),
  ("methysergide",     8.0, "LASTING: prophylaxis, ends bouts"),
  ("bromolysergide",   9.1, "LASTING: remission months (BOL-148 pilot)"),
  ("lurasidone",       None,"never tested in CH"),
  ("vortioxetine",     None,"never tested in CH"),
  ("olanzapine",       None,"abortive only (open, n=5)"),
  ("chlorpromazine",   None,"relief in open series (1980)"),
 ]
 t=pd.DataFrame(rows,columns=["drug","p_5HT1BDF_agonist","CH_class"])
 m=h7.reset_index().set_index("name")
 t["p_5HT7"]=t.drug.map(m["p"]); t["HT7_action"]=t.drug.map(m["Action"])
 # frovatriptan: GtoPdb human table has no entry; Comer 2002 reports full agonist, pEC50 ~7.3
 t.loc[t.drug=="frovatriptan",["p_5HT7","HT7_action"]]=[7.3,"FULL AGONIST (Comer 2002)"]
 t.loc[t.drug=="ergotamine",["p_5HT7","HT7_action"]]=[7.4,"Antagonist (mouse AID 1345215)"]
 t["lasting"]=t.CH_class.str.startswith("LASTING")
 pd.set_option("display.width",220)
 print(t[["drug","p_5HT1BDF_agonist","p_5HT7","HT7_action","CH_class"]].to_string(index=False))
 a=t[t.lasting].p_5HT7.dropna(); b=t[(~t.lasting)&t.drug.isin(["sumatriptan","zolmitriptan","frovatriptan"])].p_5HT7.dropna()
 print(f"\n5-HT7 potency, LASTING-effect drugs  n={len(a)} mean pKi={a.mean():.2f}  range {a.min():.1f}-{a.max():.1f}")
 print(f"5-HT7 potency, acute-only triptans   n={len(b)} mean   ={b.mean():.2f}  range {b.min():.1f}-{b.max():.1f}")
 print(f"difference = {a.mean()-b.mean():+.2f} log units  (~{10**(a.mean()-b.mean()):.0f}-fold)")
 from itertools import product
 # exact permutation test on 6 observations (rank-based), tiny n so report exactly
 obs=a.mean()-b.mean(); pool=np.concatenate([a.values,b.values]); na=len(a)
 from itertools import combinations
 cnt=0; tot=0
 for idx in combinations(range(len(pool)),na):
     o=np.array(idx); r=np.setdiff1d(np.arange(len(pool)),o)
     tot+=1; cnt+= (pool[o].mean()-pool[r].mean())>=obs
 print(f"exact permutation p = {cnt}/{tot} = {cnt/tot:.3f}   (direction: lasting > acute)")
 t.to_csv("data/dual_profile.csv",index=False)
 ```

---

## Analyses 7-8: who researches and who funds cluster headache

Not mechanism work. These map the field, because a finding is only useful if it
reaches someone able to act on it.

### `who_runs_trials.py` — who runs the trials

Every investigator, sponsor and site named on the 129 cluster headache studies in
ClinicalTrials.gov, filtered to the 69 that began in 2018 or later or are still
active.

Result: the trial world is small and concentrated. UTHealth Houston leads five
studies, Leiden UMC five; after that it is a long tail of single trials. The
most-used sites are UTHealth Houston, the Danish Headache Center, Hopital
Lariboisiere, Kopfschmerzzentrum Frankfurt, Ghent and Leiden.

### `who_publishes.py` — who publishes, and the gap between two literatures

Author counts across 980 cluster headache papers since 2019 and 71 papers since
2010 on 5-HT7 in cranial, vascular or trigeminal contexts.

Result: the two literatures barely overlap. Fourteen author names appear in both.
The overlap matters more than either list: it identifies the small number of
people positioned to evaluate a 5-HT7 claim in a headache context, rather than
one or the other.

Limitation: author-name matching is naive and does not disambiguate common names.

### `nih_grants.py`, `nih_grants2.py`, `grants_wide.py` — US federal funding

NIH RePORTER API v2, searched for "cluster headache" and then phrase-filtered on
title and abstract, since a loose two-word search returns concussion, IBS and
orofacial-pain projects.

Result: 173 projects match loosely, 39 genuinely mention cluster headache, and
six have it in the title. Five of those six are a single Michigan sleep-apnea
project from 1997-2000. One is current: a NINDS R61 at UTHealth Houston
(Burish and Yoo) for a multi-modal mouse model, alongside a related trigeminal
ganglion award.

Broadening to "trigeminal autonomic cephalalgia", "paroxysmal hemicrania",
"hemicrania continua" and "SUNCT" added no further projects.

Limitations: NIH only. Excludes private foundations, industry, and non-US
funders. A text search misses grants that never use the phrase. An OpenAIRE
query found three European projects (Aarhus/Novo Nordisk Foundation, Capital
Region of Denmark/Lundbeck Foundation, and an EU grant to a Dutch device
company), but OpenAIRE's coverage of national funders is patchy. A UKRI Gateway
to Research query failed to filter and returned unrelated projects, so UK
funding is unmeasured rather than absent.

### `industry.py` — commercial activity

Sponsors of the 129 registered studies, split into academic and non-academic.

Result: 50 studies have non-academic sponsors across 28 organisations, and the
pattern is a withdrawal. Large pharmaceutical companies ran CGRP trials and
stopped: Lilly's galcanezumab studies ended in 2016, Teva terminated all three
fremanezumab trials in 2017, Lundbeck finished eptinezumab in 2021, Novartis
terminated its pasireotide study in 2016. What remains active is almost entirely
neurostimulation devices.

Implication for drug repurposing: there is no commercial sponsor for an
off-patent hypothesis in this disease, and there will not be one. Any such test
has to come through academic or foundation funding.
