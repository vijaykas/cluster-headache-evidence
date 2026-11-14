import requests, json
url="https://clinicaltrials.gov/api/v2/studies"
params={"query.cond":"cluster headache","pageSize":1000,"format":"json"}
out=[]; tok=None
while True:
    p=dict(params)
    if tok: p["pageToken"]=tok
    r=requests.get(url,params=p,timeout=60); r.raise_for_status(); d=r.json()
    out+=d["studies"]; tok=d.get("nextPageToken")
    if not tok: break
json.dump(out,open("data/trials.json","w"))
print(len(out))
