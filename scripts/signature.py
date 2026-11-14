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
