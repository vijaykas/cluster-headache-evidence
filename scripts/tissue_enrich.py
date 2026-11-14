import json,numpy as np,pandas as pd
risk=json.load(open("data/gtex_risk.json")); bg=json.load(open("data/gtex_bg.json"))
def frame(d):
    df=pd.DataFrame(d).T.fillna(0)
    df=df.drop(columns=[c for c in df.columns if c.startswith("Cells_")],errors="ignore")
    l=np.log2(df+1); sd=l.std(axis=1).replace(0,np.nan)
    return l.sub(l.mean(axis=1),axis=0).div(sd,axis=0).dropna()
R=frame(risk); G=frame(bg)[R.columns]
G=G[G.index.map(lambda x: x not in R.index)]
obs=R.mean()
rng=np.random.default_rng(1); n=len(R); P=10000
null=np.stack([G.iloc[rng.choice(len(G),n,replace=False)].mean().values for _ in range(P)])
p=(null>=obs.values).sum(0)/P
res=pd.DataFrame({"mean_z":obs.values,"p_perm":p,"null_mean":null.mean(0)},index=obs.index).sort_values("mean_z",ascending=False)
res["fdr"]=np.minimum(1,res.p_perm*len(res)/ (res.p_perm.rank()))
res.to_csv("data/tissue_enrichment.csv")
print(res.head(12).round(3)); print(res.tail(5).round(3))
# per-gene top tissues
top={g:list(R.loc[g].sort_values(ascending=False).index[:3]) for g in R.index}
for g,t in top.items(): print(g,t)
hyp=R["Brain_Hypothalamus"].sort_values(ascending=False); print("hypothalamus z:",hyp.round(2).to_dict())
