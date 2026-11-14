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
