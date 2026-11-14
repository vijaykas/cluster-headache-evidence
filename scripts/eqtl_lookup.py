import requests,json,time
B="https://gtexportal.org/api/v2"
# lead variants: (rsid, risk allele, locus, source)  from Winsvold 2023 Tables 2 (EUR) and 3 (trans-ancestry); EA = risk allele
V=[("rs17011182","G","DUSP10","EUR"),("rs13399108","G","MERTK","EUR"),("rs6714578","A","FTCDNL1","EUR"),
   ("rs9486725","T","FHL5","EUR"),("rs2402176","C","WNT2","EUR"),("rs57866767","T","PLCE1","EUR"),("rs11172113","T","LRP1","EUR+TA"),
   ("rs12129860","G","DUSP10","TA"),("rs10916600","T","CAPN2","TA"),("rs10188642","A","MERTK","TA"),("rs4673382","G","FTCDNL1","TA"),
   ("rs11153085","T","FHL5","TA"),("rs2274224","G","PLCE1","TA")]
rows=[]
for rs,risk,locus,src in V:
    v=requests.get(f"{B}/dataset/variant",params={"snpId":rs,"datasetId":"gtex_v8"},timeout=60).json()["data"]
    if not v: print(rs,"not in GTEx"); continue
    v=v[0]; ref,alt=v["ref"],v["alt"]
    if risk==alt: sign=1
    elif risk==ref: sign=-1
    else: print(rs,"allele mismatch",risk,ref,alt); continue
    e=requests.get(f"{B}/association/singleTissueEqtl",params={"variantId":v["variantId"],"datasetId":"gtex_v8","itemsPerPage":250},timeout=120).json().get("data",[])
    print(rs,locus,src,v["variantId"],"risk=",risk,"(alt)" if sign==1 else "(ref)","eQTLs:",len(e))
    for x in e:
        rows.append(dict(rsid=rs,locus=locus,source=src,variant=v["variantId"],risk=risk,gene=x["geneSymbol"],tissue=x["tissueSiteDetailId"],
                         nes_risk=sign*x["nes"],p=x["pValue"]))
    time.sleep(0.3)
json.dump(rows,open("data/eqtl_hits.json","w"),indent=1)
print("total eQTL rows",len(rows))
