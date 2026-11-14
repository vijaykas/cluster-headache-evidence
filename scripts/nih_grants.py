"""Analysis 8: which institutions hold cluster headache research grants? NIH RePORTER API v2."""
import requests,json,collections
U="https://api.reporter.nih.gov/v2/projects/search"
def q(text,years=None):
    out=[];off=0
    while True:
        body={"criteria":{"advanced_text_search":{"operator":"and","search_field":"projecttitle,abstracttext,terms","search_text":text}},
              "include_fields":["ProjectNum","ProjectTitle","Organization","PrincipalInvestigators","FiscalYear",
                                "AwardAmount","ProjectStartDate","ProjectEndDate","AgencyIcAdmin","ActivityCode"],
              "offset":off,"limit":500}
        if years: body["criteria"]["fiscal_years"]=years
        r=requests.post(U,json=body,timeout=120)
        if r.status_code!=200:
            print("HTTP",r.status_code,r.text[:300]); return out
        j=r.json(); out+=j.get("results",[]); tot=j["meta"]["total"]
        off+=500
        if off>=tot or not j.get("results"): break
    return out
res=q("cluster headache")
print("projects matching 'cluster headache':",len(res))
org=collections.Counter(); money=collections.Counter(); pis=collections.defaultdict(set); yrs=collections.defaultdict(list)
for p in res:
    o=(p.get("organization") or {}).get("org_name","?")
    org[o]+=1; money[o]+=(p.get("award_amount") or 0)
    for pi in (p.get("principal_investigators") or []): pis[o].add(pi.get("full_name",""))
    yrs[o].append(p.get("fiscal_year"))
print("\n=== institutions by number of project-years ===")
for o,c in org.most_common(25):
    y=[x for x in yrs[o] if x]
    print(f"  {c:3d}  ${money[o]:>12,}  {o[:46]:48s} {min(y) if y else ''}-{max(y) if y else ''}  {'; '.join(sorted(x for x in pis[o] if x))[:60]}")
json.dump(res,open("data/nih_ch_grants.json","w"),indent=1)
