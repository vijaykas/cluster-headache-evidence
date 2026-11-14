import requests,json,time
P="https://pubchem.ncbi.nlm.nih.gov/rest/pug"
names={"psilocin":"psilocin","LSD":"lysergide","BOL-148":"2-bromolysergic acid diethylamide","methysergide":"methysergide","dihydroergotamine":"dihydroergotamine","ergotamine":"ergotamine","frovatriptan":"frovatriptan","sumatriptan":"sumatriptan","5-CT":"5-carboxamidotryptamine","serotonin":"serotonin"}
out=[]
for k,n in names.items():
    cid=requests.get(f"{P}/compound/name/{requests.utils.quote(n)}/cids/JSON",timeout=60).json()["IdentifierList"]["CID"][0]
    r=requests.get(f"{P}/compound/cid/{cid}/assaysummary/JSON",timeout=180).json()
    cols=r["Table"]["Columns"]["Column"]; rows=r["Table"]["Row"]
    ix={c:i for i,c in enumerate(cols)}
    n7=0
    for row in rows:
        c=row["Cell"]
        tgt=(c[ix.get("Target GeneID")] if "Target GeneID" in ix else "")
        name=c[ix["Assay Name"]] if "Assay Name" in ix else ""
        if str(tgt) in ("3363","15566","65032") or "5-HT7" in name or "5-hydroxytryptamine receptor 7" in name.lower() or "5-HT 7" in name:
            n7+=1
            out.append(dict(drug=k,cid=cid,aid=c[ix["AID"]],outcome=c[ix["Activity Outcome"]],act_name=c[ix.get("Activity Name","AID")] if "Activity Name" in ix else "",value=c[ix["Activity Value [uM]"]] if "Activity Value [uM]" in ix else "",gene=tgt,assay=name))
    print(k,cid,"rows",len(rows),"5-HT7",n7); time.sleep(0.5)
print(cols)
json.dump(out,open("data/ht7_pubchem.json","w"),indent=1)
