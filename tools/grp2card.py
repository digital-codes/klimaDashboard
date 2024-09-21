import json
import os
import re

target = "../src/components/tiles/protect/actions"

template = {
  "chart": {
    "updating": False
  },
  "progress": 0,
  "controls": {
    "range": {
      "axis":"x",
      "present": False
    },
    "type": {
      "present": True,
      "options": [
        "line","bar"
      ]
    },
    "stacked": {
      "present": True
    },
    "dataswitch": {
      "present": True
    },
    "animate": {
      "present": False
    }
  }
}

# goes into data section of template
dtemplate = {
      "url": "data/karlsruhe/Kennzahlenwerte_zu_Maßnahme_mit.csv",
      "license": "CC-BY-4.0",
      "format": "csv",
      "xaxis": "Jahr",
      "xlabel": "Jahr",
      "ylabel": "Anzahl",
      "columns": ["Wert"],
      "classes": ["Kennzahl",
      ]
    }

ltemplate = {
    "en": {
        "yes": "Yes",
        "no": "No",
        "title": "A2.1",
        "source": "Source",
        "aria": "Chart",
        "license": "License",
        "chart": "Chart EN",
        "type": "Type",
        "typeleft": "Line",
        "typeright": "Bar",
        "stacked": "Stacked",
        "download": "Download Data",
        "downimage": "Get Image",
        "rangetitle": "X Range",
        "dsname": [
        ],
        "dsleft": "First",
        "dsright": "Second",
        "animation": "Animation",
        "anistart": "Start",
        "anistop": "Stop",
        "more": "More"
    },
    "de": {
        "yes": "Ja",
        "no": "Nein",
        "title": "A2.1",
        "source": "Quelle",
        "aria": "Diagramm",
        "license": "Lizenz",
        "chart": "Chart DE",
        "type": "Typ",
        "typeleft": "Linie",
        "typeright": "Balken",
        "stacked": "Gestapelt",
        "download": "Daten herunterladen",
        "downimage": "Als Bild laden",
        "rangetitle": "X Bereich",
        "dsname": [
        ],
        "dsleft": "Eins",
        "dsright": "Zwei",
        "animation": "Animation DE",
        "anistart": "Start",
        "anistop": "Stop",
        "more": "Mehr"
    }
}

files_ = os.listdir(".")
files = [x for x in files_ if x.startswith("group_") and x.endswith(".json")]

for fl in files:
    with open(fl) as f:
        grp = json.load(f)
        if len(grp) > 2:
            print("too many items:",fl,len(grp))
            continue
        dsets = []
        for elem in grp:
            item = json.loads(json.dumps(dtemplate))
            item["ylabel"] = elem["Ma\u00dfeinheit"].strip()
            for k in elem["unique_l2_values"]:
                item["classes"].append(k) 
            name = f'{elem["Ma\u00dfnahmen_ID"]}_{item["ylabel"]}'
            name = re.sub(r'[^\w\-_.]', '', name)
            print(name,item)
            dsets.append(item)
        try:
            os.makedirs(os.sep.join([target,name]))
        except:
            pass
        fname = os.sep.join([target,name,"card.json"])
        with open(fname,"w") as fo:
            template["data"] = dsets
            json.dump(template,fo)
        lng = json.loads(json.dumps(ltemplate))
        lng["en"]["title"] = grp[0]["Ma\u00dfnahmen_ID"]
        lng["de"]["title"] = grp[0]["Ma\u00dfnahmen_ID"]
        for elem in grp:
            lng["de"]["dsname"].append(elem["Ma\u00dfeinheit"].strip())
            lng["en"]["dsname"].append(elem["Ma\u00dfeinheit"].strip())
        fname = os.sep.join([target,name,"lang.json"])
        with open(fname,"w") as fo:
            json.dump(lng,fo)


            
        
