"""Analysis 8c: broaden the grant search - other TAC terms (NIH), UK (UKRI), EU (OpenAIRE)."""
import requests,json,re,collections
pat=re.compile(r"cluster\s+headach|trigeminal\s+autonomic|SUNCT|paroxysmal\s+hemicrania|hemicrania\s+continua",re.I)

print("########## NIH RePORTER, broader TAC terms ##########")
U="https://api.reporter.nih.gov/v2/projects/search"
seen={}
for term in ["trigeminal autonomic cephalalgia","paroxysmal hemicrania","hemicrania continua","SUNCT","cluster headache"]:
    off=0
    while True:
        b={"criteria":{"advanced_text_search":{"operator":"and","search_field":"projecttitle,abstracttext,terms","search_text":term}},
           "include_fields":["ProjectNum","ProjectTitle","AbstractText","Organization","PrincipalInvestigators","FiscalYear","AwardAmount","AgencyIcAdmin"],
           "offset":off,"limit":500}
        r=requests.post(U,json=b,timeout=180)
        if r.status_code!=200: print(" ",term,"HTTP",r.status_code); break
        j=r.json()
        for p in j.get("results",[]): seen[p["project_num"]]=p
        off+=500
        if off>=j["meta"]["total"] or not j.get("results"): break
    print(f"  '{term}' -> cumulative unique {len(seen)}")
hits=[p for p in seen.values() if pat.search((p.get("project_title") or "")+" "+(p.get("abstract_text") or ""))]
tt=[p for p in hits if pat.search(p.get("project_title") or "")]
print(f"\n  phrase-confirmed: {len(hits)}; with a TAC term in the TITLE: {len(tt)}")
for p in sorted(tt,key=lambda x:-(x.get("fiscal_year") or 0)):
    o=(p.get("organization") or {}).get("org_name","?")
    pi="; ".join(x.get("full_name","") for x in (p.get("principal_investigators") or []))
    print(f"   FY{p.get('fiscal_year')} {o[:34]:36s} {pi[:24]:26s} ${p.get('award_amount') or 0:>9,} {(p.get('project_title') or '')[:54]}")

print("\n########## UKRI Gateway to Research ##########")
try:
    r=requests.get("https://gtr.ukri.org/api/projects",params={"q":'"cluster headache"',"s":100},
                   headers={"Accept":"application/vnd.rcuk.gtr.json-v7"},timeout=120)
    print("  HTTP",r.status_code)
    if r.status_code==200:
        j=r.json(); ps=j.get("project",[])
        print("  total:",j.get("totalSize"))
        for p in ps[:25]:
            t=p.get("title","") or ""
            if pat.search(t+" "+(p.get("abstractText") or "")):
                orgs=[l.get("name") for l in (p.get("leadResearchOrganisation") and [p["leadResearchOrganisation"]] or [])]
                print(f"   {p.get('grantCategory','')[:16]:18s} {','.join(o for o in orgs if o)[:40]:42s} {t[:60]}")
except Exception as e: print("  UKRI failed:",e)

print("\n########## OpenAIRE projects (EU + national) ##########")
try:
    r=requests.get("https://api.openaire.eu/search/projects",params={"keywords":"cluster headache","size":50,"format":"json"},timeout=120)
    print("  HTTP",r.status_code, len(r.text))
    if r.status_code==200:
        j=r.json(); res=j.get("response",{}).get("results",{}).get("result",[]) or []
        print("  returned:",len(res))
        for x in res[:40]:
            try:
                m=x["metadata"]["oaf:entity"]["oaf:project"]
                t=(m.get("title") or {}).get("$","")
                f=(m.get("fundingtree") or {})
                nm=""
                if isinstance(f,dict): nm=((f.get("funder") or {}).get("shortname") or {}).get("$","")
                if pat.search(t): print(f"   {nm[:14]:16s} {t[:88]}")
            except Exception: pass
except Exception as e: print("  OpenAIRE failed:",e)
