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
