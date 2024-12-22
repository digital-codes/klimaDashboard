import json
import os
import sys
import pandas as pd

import ragTextUtils as textUtils
import ragDeployUtils as deployUtils
from ragInstrumentation import measure_execution_time, log_query


DEBUG = False

if len(sys.argv) > 1:
    lang = sys.argv[1]
else:
    lang = "de"


# maybe basedir needed for source information
basedir = '../docs/karlsruhe/ksk_extracted'
if lang == "de":
    dbCollection = "ksk" # kskSum using summary, ksk using raw content
elif lang == "en":
    dbCollection = "ksk_en"

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
if lang == "de":
    llm = deployUtils.Llm(lang="german")
elif lang == "en":
    llm = deployUtils.Llm(lang="english")

embedder = deployUtils.Embedder()


@log_query
def queryLlm(context, query, history,size=200):
    answer, tokens = llm.queryWithContext(context, query, history,size)
    return answer, tokens

@log_query
def initQuery(context, query, size=200):
    answer, tokens, msgs  = llm.initChat(context, query, size)
    return answer, tokens, msgs

@log_query
def followQuery(query, history, size=200):
    answer, tokens, msgs  = llm.followChat(query, history, size)
    return answer, tokens, msgs

# Step 5: Run the RAG system
if __name__ == "__main__":
    msgHistory = []
    query = input("\nEnter your query: ")
    followUp = False
    while len(query) > 0:
        if not followUp:
            embedding = embedder.encode(query)
            searchVector = embedding["data"][0]["embedding"]
            searchResult = dbClient.searchItem(dbCollection, searchVector, limit=5, fields=["itemId","title","file","meta","text"])
            if DEBUG: print(searchResult)
            files = [f["file"] for f in searchResult["data"]]
            results = [(f["itemId"], f["title"], f["text"]) for f in searchResult["data"] if f["distance"] >= .35]
            if DEBUG: print(files)
            if len(results) == 0:
                print("No relevant documents found")
                query = input("\nEnter your query: ")
                continue
            context = ""
            followUp = True
            for r in results:
                context = "\n".join([f"{r[0].split("_chunk")[0]}:{r[1]}",r[2],context])
            if DEBUG: print(context)
            answer, tokens, msgs = initQuery(context, query)
        else:
            # add assistant answer to msgs
            msgs.append({"role":"assistant","content":answer})
            answer, tokens, msgs = followQuery(query,msgs)
            
        if answer == None:
            print("No answer found")    
        print("Answer:", answer,tokens, files)
        if DEBUG: print("History",msgs)
        print("Len History",len(msgs))
        query = input("\nEnter your query: ")

    
    
