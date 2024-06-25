import os
import json
import pathlib
import sys

base = os.sep.join(str(pathlib.PosixPath(sys.argv[0])).split(os.sep)[:-1])

search = f"{base}/../src/components"

for f in os.walk(search):
    #print(f)
    if len(f[2]) > 2:
        for fl in f[2]:
            if fl == "card.json":
                print(os.sep.join([f[0],fl]))
    
