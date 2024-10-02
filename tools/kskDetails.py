""" read all text files, extact key section and create json"""
import pandas as pd
import json
import os
import sys


kskdir = "../docs/karlsruhe/ksk_extracted"

files = os.listdir(kskdir)

keys = [
    "\nWas & Warum?\n",
    "\nWie & Wann?\n",
    "\nWas und Wen?\n",
    "\nWer?\n",
    "\nWo noch?\n",
    "\nWas bringt es?\n",
    "\nWieviel?\n",
    "\nRisiken & Herausforderungen?\n",
    "\nWann?\n",
    "\nUmsetzungszeitraum:",
    "\nWirkzeitraum:"
    ]

skip_key = "\nWann?\n"

# with wann:
#Umsetzungszeitraum
#Wirkzeitraum

def separate(txt,base):
    name = base.split(" ")[0]
    print(name)
    lines = []
    for l in txt.split("\n"):
        if not l.startswith(" ".join(["Maßnahme",base])):
            lines.append(l)

    txt = "\n".join(lines)
    sections = {}
    for k in keys:
        if txt.find(k) >= 0:
            sections[k] = txt.index(k)
        else:
            print("no ",k)

    sorted_sections = dict(sorted(sections.items(), key=lambda item: item[1]))
    print(sorted_sections)
    #return sorted_sections
    items = {}
    startPositions = [sorted_sections[x] for x in sorted_sections]
    for i,s in enumerate(startPositions):
        rawKey = list(sorted_sections.keys())[i]
        if rawKey == skip_key:
            continue
        if i < len(startPositions) - 1:
            t = txt[startPositions[i]:startPositions[i+1]]
        else:
            t = txt[startPositions[i]:]
        key = rawKey.strip()
        items[key] = t.split(rawKey)[1]

    return items

for file in files:
    if not file.endswith(".txt"):
        continue
    base = file.split(".txt")[0]
    if base == "":
        continue
    with open (os.sep.join([kskdir,file])) as f:
        txt = f.read()
    sections = separate(txt,base)
    with open (os.sep.join([kskdir,base+".json"]),"w") as f:
        json.dump(sections,f)
        
