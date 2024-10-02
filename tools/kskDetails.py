""" read all text files, extact key section and create json"""
import pandas as pd
import json
import os
import sys


kskdir = "./ksk_extracted"

files = os.listdir(kskdir)

keys = [
    "\nWas & Warum?\n",
    "\nWie & Wann?\n",
    "\nWas und Wen?\n",
    "\nWer?\n",
    "\nWo noch?\n",
    "\nWann?\n",
    "\nUmsetzungszeitraum:",
    "\nWirkzeitraum:"
    ]
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
        print(k)
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
        print("i",i)
        rawKey = list(sorted_sections.keys())[i]
        if rawKey == keys[5]:
            continue
        if i < len(startPositions) - 1:
            t = txt[startPositions[i]:startPositions[i+1]]
        else:
            t = txt[startPositions[i]:]
        key = rawKey.strip()
        items[key] = t.split(rawKey)[1]

    return items
        
           
    for s in sorted_sections:
        print(s)
        start = txt.index(s)
        end = len(txt)
        for key in sorted_sections:
            if sorted_sections[key] > start:
                end = sorted_sections[key]
                break
        print(start,end)
        section = txt[start:end]
        #print(section)
        #with open (os.sep.join([kskdir,base,s.replace("\n","").replace(" ","_")+".txt"]),"w") as f:
        #    f.write(section)

    return sorted_sections    

for file in files:
    base = file.split(".txt")[0]
    if base == "":
        continue
    with open (os.sep.join([kskdir,file])) as f:
        txt = f.read()
    sections = separate(txt,base)
    with open (os.sep.join([kskdir,base+".json"]),"w") as f:
        json.dump(sections,f)
        
