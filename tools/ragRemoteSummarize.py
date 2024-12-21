""" summarize files into a summary file """
import json
import os
import datetime
import pandas as pd

import ragTextUtils as textUtils
import ragDeployUtils as deployUtils


DEBUG = False

basedir = '../docs/karlsruhe/ksk_extracted'
dbCollection = "ksk" # kskSum using summary, ksk using raw content
summaryFile = dbCollection + "_summary.json"


# read markers
try:
    with open(os.sep.join([basedir,'markers.json']), 'r') as f:
        markers = json.load(f)
except:
    print("Error reading markers")
    markers = []

dbClient = deployUtils.VectorDb()

# text stuff
preprocessor = textUtils.PreProcessor()

# get models
llm = deployUtils.Llm()


def prepare_indexed_data(base, filename):
    file_path = os.sep.join([base, filename])
    if not os.path.exists(file_path):
        raise ValueError(f"File does't exist: {file_path}")

    if DEBUG: print(f"Preparing indexed data from folder: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            document = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file {file_path}: {e}")
            return None
        
        if "body" not in document:
            print(f"No 'content' field in file {file_path}. Skipping.")
            return None
        
        meta = {"filename": filename,"indexdate": datetime.datetime.now().isoformat()}
        # assume source is pdf here
        meta["type"] = "pdf"
        # add title
        meta["title"] = document.get("title", "")
        meta["area"] = document['area']
        meta["bundle"] = document['bundle']
        meta["topic"] = document['idx']

        raw_content = document['body']
        if DEBUG: print(raw_content)
        clean_content,_,__ = preprocessor.clean(raw_content)
        if DEBUG: print("Cleaned:",clean_content)
        summary_content, _ = llm.summarize(clean_content)
        if DEBUG: print("Summarized:",summary_content)
        return summary_content, meta
    

    
if __name__ == "__main__":
    files = os.listdir(basedir)

    df = pd.DataFrame(columns=["filename","text","meta"])
    for f in files:
        if f == 'markers.json':
            continue
        if not f.endswith('.json'):
            continue
        text, meta = prepare_indexed_data(basedir, f)
        if text == None:
            print("No data",f)
            continue
        if DEBUG: print("Prepared:",text,meta)
        df = pd.concat([df,pd.DataFrame({"filename":f,"text":text,"meta":json.dumps(meta)},index=[0])],ignore_index=True)
        print(len(df))

    df.to_json(summaryFile,orient="records", index=False)
