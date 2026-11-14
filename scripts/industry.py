"""Analysis 8d: non-university actors in cluster headache - companies running trials."""
import json,collections,re
rows=json.load(open("data/trial_people.json"))
ACA=re.compile(r"univ|hospital|hopital|hôpital|clinic$|medical cent|college|institut(?!e for)|karolinska|charit|"
               r"erasmus|rigshospitalet|assistance publique|hospices|nhs|school of|academ|foundation trust|"
               r"centre hospitalier|irccs|region|county|health system|children",re.I)
def yr(d):
    try: return int(d[:4])
    except: return 0
ind=collections.defaultdict(list)
for r in rows:
    s=r["sponsor"] or "?"
    if not ACA.search(s):
        ind[s].append(r)
print(f"{len(rows)} CH studies; {sum(len(v) for v in ind.values())} led by non-academic sponsors ({len(ind)} organisations)\n")
def key(kv): 
    return (-max((yr(x['start']) for x in kv[1]),default=0), -len(kv[1]))
for s,v in sorted(ind.items(),key=key):
    ys=[yr(x["start"]) for x in v if yr(x["start"])]
    act=[x for x in v if x["status"] in ("RECRUITING","NOT_YET_RECRUITING","ACTIVE_NOT_RECRUITING","ENROLLING_BY_INVITATION")]
    print(f"  {s[:42]:44s} {len(v)} trial(s)  {min(ys) if ys else '?'}-{max(ys) if ys else '?'}  {'ACTIVE: '+str(len(act)) if act else ''}")
    for x in sorted(v,key=lambda z:-yr(z['start']))[:3]:
        iv="; ".join(x["interv"])[:40]
        print(f"      {x['nct']} {x['status'][:14]:16s} {x['start'][:7]:8s} {iv:42s} {x['title'][:46]}")
