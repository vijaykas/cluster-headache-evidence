"""Analysis 7b: who publishes on CH, and who publishes on 5-HT7 cranial vascular pharmacology?
The overlap (or absence of it) is the targeting insight."""
import requests,time,json,collections
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def eg(p,ep="esearch.fcgi"):
    for k in range(6):
        j=requests.get(E+ep,params=dict(db="pubmed",retmode="json",**p),timeout=90).json()
        if "error" not in j: return j
        time.sleep(1.5*(k+1))
    raise RuntimeError(j)
def authors(term,label,n=200,since="2019"):
    r=eg({"term":f'{term} AND ("{since}"[dp] : "3000"[dp])',"retmax":n})["esearchresult"]
    ids=r["idlist"]; print(f"\n=== {label}: {r['count']} papers since {since} (reading {len(ids)}) ===")
    cnt=collections.Counter(); last=collections.defaultdict(str); aff=collections.defaultdict(str)
    for i in range(0,len(ids),100):
        s=eg({"id":",".join(ids[i:i+100])},"esummary.fcgi")["result"]
        for u in ids[i:i+100]:
            d=s.get(u) or {}
            for a in (d.get("authors") or []):
                nm=a.get("name","")
                if nm: cnt[nm]+=1; last[nm]=max(last[nm],d.get("pubdate","")[:4])
        time.sleep(0.5)
    for nm,c in cnt.most_common(22): print(f"  {c:3d}  {nm:28s} latest {last[nm]}")
    return cnt
ch=authors('"cluster headache"[tiab]',"Cluster headache")
h7=authors('("5-HT7"[tiab] OR "5-HT(7)"[tiab] OR HTR7[tiab]) AND (vascular[tiab] OR cranial[tiab] OR artery[tiab] OR meningeal[tiab] OR CGRP[tiab] OR trigeminal[tiab] OR migraine[tiab])',"5-HT7 cranial / vascular / trigeminal",since="2010")
both=set(ch)&set(h7)
print("\n=== authors in BOTH sets ===")
print("  ", sorted(both) if both else "(none)")
json.dump({"ch":ch.most_common(60),"ht7":h7.most_common(60),"both":sorted(both)},open("data/authors.json","w"),indent=1)
