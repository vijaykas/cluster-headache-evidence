import requests,json
B="https://www.ebi.ac.uk/chembl/api/data"
def get_all(url,params,key):
    out=[]
    while url:
        d=requests.get(url,params=params,timeout=180).json(); out+=d[key]
        nxt=d["page_meta"]["next"]; url=("https://www.ebi.ac.uk"+nxt) if nxt else None; params=None
    return out
# all 5-HT7 targets (any species)
tg=get_all(f"{B}/target.json",{"pref_name__icontains":"5-hydroxytryptamine receptor 7","limit":100},"targets")
tg+=get_all(f"{B}/target.json",{"pref_name__icontains":"serotonin 7","limit":100},"targets")
tids={t["target_chembl_id"]:(t["pref_name"],t["organism"]) for t in tg}
print(tids)
parents={"psilocin":"CHEMBL65547","LSD":"CHEMBL263881","BOL-148":"CHEMBL274384","methysergide":"CHEMBL1065","dihydroergotamine":"CHEMBL1732","ergotamine":"CHEMBL442","frovatriptan":"CHEMBL1279","sumatriptan":"CHEMBL128","5-CT (reference agonist)":"CHEMBL280074"}
# verify names and collect salt forms
res=[]
for name,pid in parents.items():
    m=requests.get(f"{B}/molecule/{pid}.json",timeout=60).json()
    forms=[f["molecule_chembl_id"] for f in requests.get(f"{B}/molecule_form/{pid}.json",timeout=60).json().get("molecule_forms",[])] or [pid]
    print(name,pid,m.get("pref_name"),"forms",forms)
    for f in set(forms+[pid]):
        for tid in tids:
            for a in get_all(f"{B}/activity.json",{"molecule_chembl_id":f,"target_chembl_id":tid,"limit":1000},"activities"):
                res.append(dict(drug=name,mol=f,target=tids[tid][0],species=tids[tid][1],type=a["standard_type"],rel=a["standard_relation"],value=a["standard_value"],units=a["standard_units"],pchembl=a["pchembl_value"],assay_type=a["assay_type"],assay=a["assay_description"],doc=a["document_chembl_id"]))
json.dump(res,open("data/ht7_activities.json","w"),indent=1)
print(len(res))
