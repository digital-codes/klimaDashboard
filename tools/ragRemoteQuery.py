import json
import os
import sys
import pandas as pd

import ragTextUtils as textUtils
import ragDeployUtils as deployUtils
from ragInstrumentation import measure_execution_time, log_query


DEBUG = False

# maybe basedir needed for source information
basedir = '../docs/karlsruhe/ksk_extracted'
dbCollection = "ksk" # kskSum using summary, ksk using raw content
summaryFile = dbCollection + "_summary.json"

dbClient = deployUtils.VectorDb()
# items to retrieve on search 
dbItems = 5

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
llm = deployUtils.Llm()
embedder = deployUtils.Embedder()

summary = pd.read_json(summaryFile)


@measure_execution_time
def readSummary(id,title):
    item = summary.loc[summary["filename"]==id]
    if item.empty:
        print(f"Summary not found for   {id}")
        return None
    return f"{id.split('_extracted')[0]}:{title}\n{item['text'].values[0]}\n\n"

@log_query
def queryLlm(context, query, history,size=200):
    answer, tokens = llm.queryWithContext(context, query, history,size)
    return answer, tokens

# Step 5: Run the RAG system
if __name__ == "__main__":
    msgHistory = []
    query = input("\nEnter your query: ")
    followUp = False
    while len(query) > 0:
        embedding = embedder.encode(query)
        searchVector = embedding["data"][0]["embedding"]
        searchResult = dbClient.searchItem(dbCollection, searchVector, limit=5, fields=["itemId","title","file","meta","text"])
        if DEBUG: print(searchResult)
        files = [f["file"] for f in searchResult["data"]]
        results = [(f["itemId"],f["title"],f["text"]) for f in searchResult["data"]]
        if DEBUG: print(results)
        
        if not followUp:
            followUp = True
            context = ""
            for r in results:
                context = "\n".join([f"{r[0].split("_chunk")[0]}:{r[1]}",r[2],context])
            if DEBUG: print(context)
        # answer, tokens = llm.queryWithContext(context, query, msgHistory)
        answer, tokens = queryLlm(context, query, msgHistory)
        if answer == None:
            print("No answer found")    
        print("Answer:", answer,files)
        if DEBUG: print("History",msgHistory)
        print("Len History",len(msgHistory))
        if len(msgHistory) > 8:
            # keep 1 and 2, initial context and query
            msgHistory.pop(2)
            msgHistory.pop(2)
        query = input("\nEnter your query: ")

    
    
