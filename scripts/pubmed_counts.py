import requests,time,json
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
drugs="frovatriptan olanzapine chlorpromazine quetiapine risperidone aripiprazole clozapine lurasidone vortioxetine mianserin cyproheptadine amisulpride brexpiprazole ziprasidone methysergide dihydroergotamine tasimelteon ramelteon agomelatine melatonin clomiphene lithium verapamil".split()
out={}
for d in drugs:
    q=f'"{d}"[tiab] AND ("cluster headache"[tiab] OR "cluster headaches"[tiab])'
    r=requests.get(E,params={"db":"pubmed","term":q,"retmode":"json","retmax":20},timeout=60).json()["esearchresult"]
    out[d]={"count":int(r["count"]),"pmids":r["idlist"]}; print(d,r["count"]); time.sleep(0.4)
json.dump(out,open("data/pubmed_counts.json","w"),indent=1)
