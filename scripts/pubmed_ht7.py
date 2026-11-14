import requests,time,json
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
Q={"lsd_5ht7_function":'(LSD[tiab] OR lysergic[tiab]) AND ("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (agonist[tiab] OR cAMP[tiab] OR adenylyl[tiab] OR adenylate[tiab])',
"psilocin_5ht7":'(psilocin[tiab] OR psilocybin[tiab]) AND ("5-HT7"[tiab] OR "5-HT(7)"[tiab])',
"frova_5ht7":'frovatriptan[tiab] AND ("5-HT7"[tiab] OR "5-HT(7)"[tiab])',
"ht7_vasodilation":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (vasodilat*[tiab] OR relaxation[tiab]) AND (cranial[tiab] OR meningeal[tiab] OR cerebral[tiab] OR carotid[tiab])',
"ht7_migraine":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (migraine[tiab] OR headache[tiab]) AND antagonist*[tiab]',
"ht7_cluster":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND "cluster headache"[tiab]',
"ht7_scn":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (suprachiasmatic[tiab] OR circadian[tiab])'}
out={}
for k,q in Q.items():
    r=requests.get(E+"esearch.fcgi",params={"db":"pubmed","term":q,"retmode":"json","retmax":8,"sort":"relevance"},timeout=60).json()["esearchresult"]
    ids=r["idlist"]; out[k]={"count":int(r["count"]),"ids":ids}
    if ids:
        s=requests.get(E+"esummary.fcgi",params={"db":"pubmed","id":",".join(ids),"retmode":"json"},timeout=60).json()["result"]
        out[k]["titles"]=[(i,s[i]["pubdate"][:4],s[i]["title"]) for i in ids]
    print("\n##",k,r["count"])
    for t in out[k].get("titles",[]): print(" ",t[0],t[1],t[2][:140])
    time.sleep(0.5)
json.dump(out,open("data/pubmed_ht7.json","w"),indent=1)
