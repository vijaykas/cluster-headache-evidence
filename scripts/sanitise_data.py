"""Strip personal contact details from fetched registry data before publication.

ClinicalTrials.gov publishes investigator emails and phone numbers. They are
public at source, but republishing them as a bulk file in a repository turns
them into a harvestable list, which is a different thing. The analyses never
use these fields. This removes them.

Run after any fetch that touches ClinicalTrials.gov. Idempotent.
"""
import json, re, sys, pathlib
DROP = {"email", "phone", "phoneExt", "centralContacts", "contacts"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items() if k not in DROP}
    if isinstance(o, list):
        return [clean(x) for x in o]
    if isinstance(o, str):
        return EMAIL.sub("[contact removed]", o)
    return o

for p in sys.argv[1:] or [str(x) for x in pathlib.Path("data").glob("*.json")]:
    try:
        d = json.load(open(p))
    except Exception:
        continue
    c = clean(d)
    if c != d:
        json.dump(c, open(p, "w"), indent=1)
        print("cleaned", p)
