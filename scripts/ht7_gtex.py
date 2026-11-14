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
