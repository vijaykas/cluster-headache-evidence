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
