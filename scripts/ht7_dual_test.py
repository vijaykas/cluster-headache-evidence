"""Analysis 6f: is HTR7's joint artery+hypothalamus specificity unusual?
Same z-score method as Analysis 2, tested against the 524-gene background
and against all GPCR-like drug targets we have pulled."""
import json,numpy as np,pandas as pd
bg=json.load(open("data/gtex_bg.json")); tg=json.load(open("data/gtex_targets.json"))
risk=json.load(open("data/gtex_risk.json"))
allg={**bg,**tg,**risk}
df=pd.DataFrame(allg).T
df=df.drop(columns=[c for c in df.columns if c.startswith("Cells_") or c=="Testis"],errors="ignore").fillna(0)
l=np.log2(df+1); sd=l.std(axis=1).replace(0,np.nan)
Z=l.sub(l.mean(axis=1),axis=0).div(sd,axis=0).dropna()
ART=[c for c in Z.columns if c.startswith("Artery_")]
HYP="Brain_Hypothalamus"
Z["artery_z"]=Z[ART].mean(axis=1); Z["hypo_z"]=Z[HYP]
Z["dual"]=np.minimum(Z.artery_z,Z.hypo_z)          # both must be high
bgset=[g for g in bg if g in Z.index]
print(f"background genes used: {len(bgset)}  tissues: {len(ART)+1} of {Z.shape[1]-3}")
for g in ["HTR7","HTR1B","HTR1D","HTR2A","HTR6","CALCA","KCNJ8","ABCC9","MTNR1A","MTNR1B","CACNA1C","PLCE1","LRP1","FHL5"]:
    if g in Z.index:
        r=Z.loc[g]
        pct=(pd.Series([Z.loc[b,"dual"] for b in bgset])<r["dual"]).mean()*100
        print(f"{g:8s} artery_z={r.artery_z:+.2f}  hypothalamus_z={r.hypo_z:+.2f}  dual={r.dual:+.2f}  >{pct:.1f}% of background")
# empirical p for HTR7 dual score
d=np.array([Z.loc[b,"dual"] for b in bgset]); h=Z.loc["HTR7","dual"]
print(f"\nHTR7 dual score {h:+.3f}; background mean {d.mean():+.3f} sd {d.std():.3f}")
print(f"empirical p (background genes with dual >= HTR7): {(d>=h).sum()}/{len(d)} = {(d>=h).mean():.4f}")
Z[["artery_z","hypo_z","dual"]].sort_values("dual",ascending=False).head(15).round(3).to_csv("data/dual_tissue_top.csv")
print("\ntop 12 genes overall by dual score:")
print(Z[["artery_z","hypo_z","dual"]].sort_values("dual",ascending=False).head(12).round(2).to_string())
