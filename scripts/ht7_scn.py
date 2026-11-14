"""Analysis 6g: which 5-HT receptor mediates circadian phase resetting in the SCN,
and is 5-HT2A a rival explanation?"""
import requests,time,json
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def eg(p):
    for k in range(6):
        j=requests.get(E+"esearch.fcgi",params=dict(db="pubmed",retmode="json",**p),timeout=60).json()
        if "error" not in j: return j["esearchresult"]
        time.sleep(1.5*(k+1))
qs={
 "5-HT7 + SCN/circadian":'("5-HT7"[tiab] OR "5-HT(7)"[tiab] OR HTR7[tiab]) AND (suprachiasmatic[tiab] OR circadian[tiab])',
 "5-HT2A + SCN/circadian":'("5-HT2A"[tiab] OR "5-HT(2A)"[tiab] OR HTR2A[tiab]) AND (suprachiasmatic[tiab] OR circadian[tiab])',
 "5-HT7 + phase shift":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND ("phase shift"[tiab] OR "phase advance"[tiab] OR "phase resetting"[tiab])',
 "5-HT2A + phase shift":'("5-HT2A"[tiab] OR "5-HT(2A)"[tiab]) AND ("phase shift"[tiab] OR "phase advance"[tiab] OR "phase resetting"[tiab])',
 "5-HT7 + trigeminal":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (trigeminal[tiab] OR dura[tiab] OR meningeal[tiab])',
 "5-HT7 + CGRP":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND (CGRP[tiab] OR "calcitonin gene-related"[tiab])',
 "5-HT7 + migraine":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND migraine[tiab]',
 "5-HT7 + cluster headache":'("5-HT7"[tiab] OR "5-HT(7)"[tiab]) AND ("cluster headache"[tiab])',
}
res={}
for k,q in qs.items():
    r=eg({"term":q,"retmax":8}); res[k]={"n":int(r["count"]),"ids":r["idlist"]}
    print(f'{k:28s} {r["count"]}'); time.sleep(0.7)
json.dump(res,open("data/ht7_scn.json","w"),indent=1)
ids=res["5-HT7 + phase shift"]["ids"]+res["5-HT7 + trigeminal"]["ids"][:4]+res["5-HT7 + CGRP"]["ids"][:3]
print("\nfetching",len(ids))
print(requests.get(E+"esummary.fcgi",params={"db":"pubmed","id":",".join(ids),"retmode":"json"},timeout=90).text[:50])
import collections
s=requests.get(E+"esummary.fcgi",params={"db":"pubmed","id":",".join(ids),"retmode":"json"},timeout=90).json()["result"]
for i in ids:
    if i in s: print(" ",i,s[i]["pubdate"][:4],s[i]["title"][:115])
