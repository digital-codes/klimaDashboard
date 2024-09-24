import json
import sys

file = sys.argv[1]
dirty = False
with open(file,"r") as f:
    j = json.load(f)
    if j["de"].get("more") == None:
        j["de"]["more"] = "Mehr"
        dirty = True
    if j["en"].get("more") == None:
        j["en"]["more"] = "More"
        dirty = True


if dirty:
    with open(file,"w") as f:
        json.dump(j,f)

        
