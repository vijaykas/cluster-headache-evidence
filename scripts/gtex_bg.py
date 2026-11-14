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
