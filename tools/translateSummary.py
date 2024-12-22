import pandas as pd
import ragDeployUtils as rag
import json

sumIn = "ksk_summary.json"
sumOut = "ksk_summary_en.json"

df = pd.read_json(sumIn)

en = rag.Llm(lang = "english")

def translate(x):
    return en.translate(x)[0]

def transMeta(x):
    meta = json.loads(x)
    meta["title"] = translate(meta["title"])
    print(meta["title"])
    return json.dumps(meta)


df["meta"] = df.meta.apply(transMeta)
df["text"] = df.text.apply(translate)

df.to_json(sumOut, orient="records",index=False)


