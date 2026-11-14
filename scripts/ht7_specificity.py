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
