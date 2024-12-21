import json
import os
import datetime
import sys
import pandas as pd

import ragTextUtils as textUtils
import ragDeployUtils as deployUtils


DEBUG = False

basedir = '../docs/karlsruhe/ksk_extracted'
dbCollection = "ksk" # kskSum using summary, ksk using raw content
summaryFile = dbCollection + "_summary.json"


dbClient = deployUtils.VectorDb()

# check collection exists
try:
    collection = dbClient.describeCollection(dbCollection)
    if DEBUG: print(collection)
    if collection["code"] != 0:
        print(collection)
        raise ValueError
    print("Collection exists:",collection["data"]["collectionName"])
except Exception as e:
    print("Collection failed",e)
    sys.exit()

# text stuff
preprocessor = textUtils.PreProcessor()

# get models
embedder = deployUtils.Embedder()

    
if __name__ == "__main__":

    # try to get summary file first
    try:
        summary = pd.read_json(summaryFile)
    except:
        print("Error reading summary file")
        sys.exit()
    

    for item in summary.itertuples(index=False):
        meta = json.loads(item.meta)
        text = item.text
        chunks = preprocessor.chunk(text)
        for i, chunk in enumerate(chunks):
            # create item
            itemId = f"{meta['area']}_{meta['bundle']}_{meta['topic']}_chunk_{i}"
            if DEBUG: print(itemId)
            embedding = embedder.encode(chunk)
            vectors = embedding["data"][0]["embedding"]
            if DEBUG: print(itemId,embedding["usage"],vectors)
            dbitem = { 
                "primary_key": itemId, 
                "vector": vectors,
                "chunk": i,
                "area": ord(meta['area']),
                "bundle": int(meta['bundle']),
                "topic": int(meta['topic']),
                "title": meta['title'],
                "text": chunk,
                "file": meta['filename'],
                "meta": json.dumps(meta)
              }
            if DEBUG: print("Item:",dbitem)
            try:
                print(item.filename)
                result = dbClient.upsertItem(dbCollection,dbitem)
                if DEBUG: print(result)
            except :
                print("Error in adding document")
                break
                continue

