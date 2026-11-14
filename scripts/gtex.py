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
