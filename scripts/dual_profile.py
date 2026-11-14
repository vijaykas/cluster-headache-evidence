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
