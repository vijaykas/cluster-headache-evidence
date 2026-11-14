"""Analysis 6d: has any SELECTIVE 5-HT7 antagonist ever reached human trials?
Search ClinicalTrials.gov v2 + PubMed for the known selective 5-HT7 ligands."""
import requests,time,json
CT="https://clinicaltrials.gov/api/v2/studies"
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def eget(u,p):
    for k in range(6):
        j=requests.get(u,params=p,timeout=60).json()
        if "error" not in j: return j
        time.sleep(1.5*(k+1))
    raise RuntimeError(j)

cands=["JNJ-18038683","JNJ 18038683","SB-269970","SB269970","LP-211","DR-4004",
       "lurasidone","vortioxetine","amisulpride","intepirdine","idalopirdine",
       "SB-258719","SB-656104","PZ-1444"]
out={}
for c in cands:
    r=requests.get(CT,params={"query.term":c,"pageSize":50,
        "fields":"NCTId,BriefTitle,Phase,OverallStatus,Condition,InterventionName,StartDate"},timeout=90).json()
    st=r.get("studies",[])
    rows=[]
    for s in st:
        p=s["protocolSection"]
        rows.append({"nct":p["identificationModule"]["nctId"],
                     "title":p["identificationModule"]["briefTitle"][:95],
                     "phase":",".join(p.get("designModule",{}).get("phases",[])),
                     "status":p["statusModule"]["overallStatus"],
                     "cond":";".join(p.get("conditionsModule",{}).get("conditions",[]))[:70]})
    q=f'"{c}"[tiab]'
    n=int(eget(E+"esearch.fcgi",{"db":"pubmed","term":q,"retmode":"json","retmax":0})["esearchresult"]["count"])
    nh=int(eget(E+"esearch.fcgi",{"db":"pubmed","term":q+' AND (human[tiab] OR patients[tiab] OR "clinical trial"[pt])',
        "retmode":"json","retmax":0})["esearchresult"]["count"])
    out[c]={"trials":rows,"pubmed_all":n,"pubmed_human":nh}
    print(f'{c:16s} trials={len(rows):3d}  pubmed={n:5d}  human/clinical={nh:4d}')
    for r_ in rows[:4]: print("    ",r_["nct"],r_["phase"],r_["status"],"|",r_["cond"],"|",r_["title"][:60])
    time.sleep(0.7)
json.dump(out,open("data/ht7_clinical.json","w"),indent=1)
