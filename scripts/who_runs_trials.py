"""Analysis 7: who actually runs cluster headache trials?
Builds a targeted outreach list from ClinicalTrials.gov rather than guessing."""
import requests,json,collections,time
CT="https://clinicaltrials.gov/api/v2/studies"
F=("NCTId,BriefTitle,OverallStatus,StartDate,CompletionDate,Phase,EnrollmentCount,"
   "LeadSponsorName,CollaboratorName,OverallOfficialName,OverallOfficialAffiliation,"
   "LocationFacility,LocationCity,LocationCountry,CentralContactName,StudyType,Condition,InterventionName")
studies=[];tok=None
while True:
    p={"query.cond":"cluster headache","pageSize":100,"fields":F}
    if tok: p["pageToken"]=tok
    r=requests.get(CT,params=p,timeout=120).json()
    studies+=r.get("studies",[]); tok=r.get("nextPageToken")
    if not tok: break
    time.sleep(0.3)
print("studies:",len(studies))
rows=[]
for s in studies:
    ps=s["protocolSection"]; idm=ps["identificationModule"]; st=ps["statusModule"]
    sp=ps.get("sponsorCollaboratorsModule",{}); cm=ps.get("contactsLocationsModule",{})
    offs=cm.get("overallOfficials",[]) or []
    locs=cm.get("locations",[]) or []
    rows.append(dict(
        nct=idm["nctId"], title=idm["briefTitle"],
        status=st["overallStatus"],
        start=(st.get("startDateStruct") or {}).get("date",""),
        done=(st.get("completionDateStruct") or {}).get("date",""),
        phase=",".join(ps.get("designModule",{}).get("phases",[])),
        n=(ps.get("designModule",{}).get("enrollmentInfo") or {}).get("count"),
        sponsor=(sp.get("leadSponsor") or {}).get("name",""),
        collabs=[c.get("name") for c in (sp.get("collaborators") or [])],
        pis=[(o.get("name"),o.get("affiliation","")) for o in offs],
        sites=[(l.get("facility",""),l.get("city",""),l.get("country","")) for l in locs],
        interv=[i.get("name") for i in ps.get("armsInterventionsModule",{}).get("interventions",[])] ))
json.dump(rows,open("data/trial_people.json","w"),indent=1)

def yr(d): 
    try: return int(d[:4])
    except: return 0
recent=[r for r in rows if yr(r["start"])>=2018 or r["status"] in ("RECRUITING","NOT_YET_RECRUITING","ACTIVE_NOT_RECRUITING","ENROLLING_BY_INVITATION")]
print("recent/active:",len(recent))
pi=collections.Counter(); aff=collections.defaultdict(set); spon=collections.Counter(); site=collections.Counter()
for r in recent:
    for n,a in r["pis"]:
        if n: pi[n]+=1; aff[n].add(a)
    spon[r["sponsor"]]+=1
    for f,c,co in r["sites"]:
        if f: site[(f,c,co)]+=1
print("\n=== investigators named on 2018+ / active CH trials ===")
for n,c in pi.most_common(30): print(f"  {c}  {n:34s} {' | '.join(x for x in aff[n] if x)[:70]}")
print("\n=== lead sponsors ===")
for n,c in spon.most_common(18): print(f"  {c}  {n}")
print("\n=== sites running the most ===")
for (f,c,co),k in site.most_common(18): print(f"  {k}  {f[:48]:50s} {c}, {co}")
