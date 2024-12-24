import json
import os
import sys
import pandas as pd
import argparse 

import ragTextUtils as textUtils
import ragDeployUtils as deployUtils
from ragInstrumentation import measure_execution_time, log_query


DEBUG = False


config = {
    # maybe basedir needed for source information
    "basedir":'../docs/karlsruhe/ksk_extracted',
    "lang": "de",
    "dbCollection": "ksk" , # dbCollection = "ksk_en"
    "dbItems" : 5,
    "dbClient" : None,
    "preprocessor" : None,
    "embedder" : None,
    "llm" : None
}

def initialize():
    config["dbClient"] = deployUtils.VectorDb()
    checkDb()
    # text stuff
    config["preprocessor"] = textUtils.PreProcessor()
    # models
    config["embedder"] = deployUtils.Embedder()
    # llm
    if config["lang"] == "de":
        config["llm"] = deployUtils.Llm(lang="german")
    elif config["lang"] == "en":
        config["llm"] = deployUtils.Llm(lang="english")
    else:
        raise ValueError("Language not supported")


def checkDb():
    # check collection exists
    try:
        collection = config["dbClient"].describeCollection(config["dbCollection"])
        if DEBUG: print(collection)
        if collection["code"] != 0:
            print(f"Error on {collection}: {collection['code']}")
            raise ValueError
        if DEBUG: print("Collection OK:",collection["data"]["collectionName"])
    except Exception as e:
        print("Collection failed",e)
        raise ValueError


@log_query
def queryLlm(context, query, history,size=200):
    answer, tokens = config["llm"].queryWithContext(context, query, history,size)
    return answer, tokens

@log_query
def initQuery(context, query, size=200):
    answer, tokens, msgs  = config["llm"].initChat(context, query, size)
    return answer, tokens, msgs

@log_query
def followQuery(query, history, size=200):
    answer, tokens, msgs  = config["llm"].followChat(query, history, size)
    return answer, tokens, msgs

# Step 5: Run the RAG system
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', default = 5)      # option that takes a value
    parser.add_argument('-l', '--lang',default = "de")      # option that takes a value
    args = parser.parse_args()
    print(args.count, args.lang) 

    config["lang"] = args.lang
    config["dbItems"] = int(args.count)
    
    initialize()
    
    msgHistory = []
    query = input("\nEnter your query: ")
    followUp = False
    while len(query) > 0:
        if not followUp:
            embedding = config["embedder"].encode(query)
            searchVector = embedding["data"][0]["embedding"]
            searchResult = config["dbClient"].searchItem(config["dbCollection"], searchVector, limit=config["dbItems"], fields=["itemId","title","file","meta","text"])
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

    
    
