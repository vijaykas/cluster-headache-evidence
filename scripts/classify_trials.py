import json,re,collections,csv
R=json.load(open("data/trials_flat.json"))
I=[r for r in R if r["type"]=="INTERVENTIONAL"]
cats=[
 ("CGRP/PACAP pathway (antibodies, gepants)",r"galcanezumab|fremanezumab|eptinezumab|erenumab|rimegepant|zavegepant|gepant"),
 ("Neuromodulation / devices",r"stimulat|gammacore|neurostim|tdcs|rtms|transcranial|primus|bion|ati |vagus|electrode|cooling|rhinochill|onss|occipital nerve stim"),
 ("Psychedelics",r"psilocybin|lysergic|lsd"),
 ("Oxygen / gases",r"oxygen|carbon dioxide|mask"),
 ("Triptans",r"triptan"),
 ("Steroids / nerve blocks / injections",r"methylprednisolone|cortivazol|dexamethasone|greater occipital|nerve block|bupivacaine|exparel|pulsed radiofreq|\bprf\b|\bnb\b|botulinum"),
 ("Other drugs",r"candesartan|verapamil|topiramate|depak|depacon|valpro|oxybate|ketamine|magnesium|som230|pasireotide|civamide|capsaicin|acetium|droperidol|metoclopramide|ketorolac|c213|levcromakalim|vitamin|multivitamin"),
 ("Mechanism / provocation studies",r"calcitonin-gene|pacap38|levcromakalim|pet|tomography|blood sample|actigraphy"),
 ("Lifestyle / behavioral / other",r"diet|physio|exercise|yoga|breathing|osteopath|water|telephone|commitment|pbt|wearable|sensor|light"),
]
assign={}
for r in I:
    t=(r["interventions"]+" "+r["title"]).lower()
    c="Unclassified"
    for name,pat in cats:
        if re.search(pat,t): c=name; break
    assign[r["nct"]]=c
cnt=collections.Counter(assign.values())
for k,v in cnt.most_common(): print(v,k)
# targeted searches for gaps
def has(pat): return [r["nct"] for r in I if re.search(pat,(r["interventions"]+" "+r["title"]+" "+r["elig"]).lower())]
gaps={"melatonin/ramelteon/tasimelteon":has(r"melatonin|ramelteon|tasimelteon|agomelatine"),
 "light therapy":has(r"light therapy|luminette|bright light"),
 "lithium":has(r"lithium"),
 "clomiphene/hormonal":has(r"clomiphene|testosterone|estrogen"),
 "pre-bout / pre-cluster start":has(r"pre-cluster|precluster|before (the )?(onset of|start of) (the )?(cluster|bout)|pre-emptive|preemptive"),
 "pharmacogenetic":has(r"pharmacogen|genotype"),
 "anti-PACAP":has(r"anti-pacap|lu ag09222|pacap antibody"),
 "chronotherapy / timed dosing":has(r"chronotherap|bedtime dosing|timed dosing|circadian"),
}
for k,v in gaps.items(): print(f"{k}: {len(v)} {v}")
with open("data/trials_classified.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["nct","start","phase","n","category","interventions","title"])
    for r in I: w.writerow([r["nct"],r["start"][:4],r["phase"],r["n"],assign[r["nct"]],r["interventions"],r["title"]])
# enrollment by category
tot=collections.defaultdict(int)
for r in I: tot[assign[r["nct"]]]+=r["n"] or 0
print(dict(tot))
