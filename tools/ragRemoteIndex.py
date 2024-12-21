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
        filename = item.filename
        chunks = preprocessor.chunk(text)
        for i, chunk in enumerate(chunks):
            # create item
            itemId = f"{meta['area']}_{meta['bundle']}_{meta['topic']}_chunk_{i}"
            itemCode = (ord(meta['area']) << 16 ) | (int(meta['bundle']) << 8) | (int(meta['topic']))
            if DEBUG: print(itemId,itemCode)
            embedding = embedder.encode(chunk)
            vectors = embedding["data"][0]["embedding"]
            if DEBUG: print(itemId,embedding["usage"],vectors)
            dbitem = { 
                "itemId": itemId, 
                "vector": vectors,
                "file": filename,
                "title": meta['title'],
                "text": text, # full text
                "itemCode": itemCode,
                "meta": json.dumps(meta)
              }
            if DEBUG: print("Item:",dbitem)
            try:
                print(filename)
                result = dbClient.upsertItem(dbCollection,dbitem)
                if DEBUG: print(result)
            except :
                print("Error in adding document")
                break
                continue

