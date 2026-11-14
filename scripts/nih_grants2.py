"""Analysis 8b: genuine cluster headache grants - phrase-filtered on title/abstract."""
import requests,json,collections,re
U="https://api.reporter.nih.gov/v2/projects/search"
out=[];off=0
while True:
    body={"criteria":{"advanced_text_search":{"operator":"and","search_field":"projecttitle,abstracttext,terms","search_text":"cluster headache"}},
          "include_fields":["ProjectNum","ProjectTitle","AbstractText","Organization","PrincipalInvestigators",
                            "FiscalYear","AwardAmount","ProjectStartDate","ProjectEndDate","AgencyIcAdmin","ActivityCode"],
          "offset":off,"limit":500}
    r=requests.post(U,json=body,timeout=180); j=r.json()
    out+=j.get("results",[]); tot=j["meta"]["total"]; off+=500
    if off>=tot or not j.get("results"): break
pat=re.compile(r"cluster\s+headache",re.I)
hits=[p for p in out if pat.search((p.get("project_title") or "")+" "+(p.get("abstract_text") or ""))]
print(f"{len(out)} matched loosely -> {len(hits)} actually mention 'cluster headache'")
title=[p for p in hits if pat.search(p.get("project_title") or "")]
print(f"of those, {len(title)} have it in the TITLE (i.e. the grant is about CH)\n")
def row(p):
    o=(p.get("organization") or {}).get("org_name","?")
    pi="; ".join(x.get("full_name","") for x in (p.get("principal_investigators") or []))
    return (p.get("fiscal_year"),o,pi,p.get("project_num"),p.get("award_amount") or 0,
            (p.get("project_title") or "")[:72],(p.get("agency_ic_admin") or {}).get("abbreviation",""))
print("=== grants with CLUSTER HEADACHE IN THE TITLE ===")
for r_ in sorted((row(p) for p in title),reverse=True):
    print(f"  FY{r_[0]}  {r_[1][:40]:42s} {r_[2][:26]:28s} {r_[3]:16s} ${r_[4]:>10,} {r_[6]:6s} {r_[5]}")
print("\n=== institutions, CH-in-title grants only ===")
c=collections.Counter(); m=collections.Counter(); who=collections.defaultdict(set); fy=collections.defaultdict(list)
for p in title:
    o=(p.get("organization") or {}).get("org_name","?"); c[o]+=1; m[o]+=p.get("award_amount") or 0
    for x in (p.get("principal_investigators") or []): who[o].add(x.get("full_name",""))
    fy[o].append(p.get("fiscal_year"))
for o,n in c.most_common():
    y=[x for x in fy[o] if x]
    print(f"  {n:2d} yrs  ${m[o]:>11,}  {o[:42]:44s} {min(y)}-{max(y)}  {'; '.join(sorted(who[o]))[:48]}")
json.dump({"all":hits,"title":title},open("data/nih_ch_grants.json","w"),indent=1)
