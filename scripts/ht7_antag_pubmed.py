"""Analysis 6b: for every curated 5-HT7 antagonist/inverse agonist that is an approved drug,
count PubMed papers pairing it with cluster headache, and list titles."""
import requests,time,json
def get(url,params):
    for k in range(6):
        j=requests.get(url,params=params,timeout=60).json()
        if "error" not in j: return j
        time.sleep(1.5*(k+1))
    raise RuntimeError(j)
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
drugs=["lurasidone","risperidone","ziprasidone","zotepine","metergoline","dihydroergotamine","fluphenazine",
"methysergide","clozapine","mianserin","chlorpromazine","ritanserin","perphenazine","cyamemazine","thioridazine",
"iloperidone","cyproheptadine","haloperidol","olanzapine","ketanserin","vortioxetine","amisulpride","pizotifen","ergotamine"]
out=[]
for d in drugs:
    q=f'"{d}"[tiab] AND ("cluster headache"[tiab] OR "cluster headaches"[tiab])'
    r=get(E+"esearch.fcgi",{"db":"pubmed","term":q,"retmode":"json","retmax":20})["esearchresult"]
    ids=r["idlist"]; titles=[]
    if ids:
        time.sleep(0.8)
        s=get(E+"esummary.fcgi",{"db":"pubmed","id":",".join(ids),"retmode":"json"})["result"]
        titles=[(i,s[i]["pubdate"][:4],s[i]["title"]) for i in ids]
    out.append({"drug":d,"n":int(r["count"]),"titles":titles}); time.sleep(0.8)
json.dump(out,open("data/ht7_antag_pubmed.json","w"),indent=1)
for o in out:
    print(f'{o["drug"]:18s} {o["n"]}')
    if o["drug"] not in ("dihydroergotamine","methysergide","ergotamine"):
        for t in o["titles"][:6]: print("     ",t)
