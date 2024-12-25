"""This script provides tools for querying a remote database using a Retrieval-Augmented Generation (RAG) system. 
It includes functions for initializing the system, checking the database, and querying a language model (LLM).
Modules:
    - json
    - os
    - sys
    - pandas as pd
    - argparse
    - ragTextUtils as textUtils
    - ragDeployUtils as deployUtils
    - measure_execution_time, log_query from ragInstrumentation
Functions:
    - initialize(): Initializes the configuration for the application, setting up the database client, preprocessor, embedder, and language model.
    - checkDb(): Checks if the specified database collection exists and is accessible.
    - queryLlm(context, query, history, size=200): Queries the language model (LLM) with the given context, query, and history.
    - initQuery(context, query, size=200): Initializes a query using the provided context and query parameters.
    - followQuery(query, history, size=200): Executes a follow-up query using the provided LLM configuration.
Main Execution:
    - Parses command-line arguments for items, language, and collection.
    - Initializes the configuration and database.
    - Continuously prompts the user for queries, processes them, and prints the answers.
"""
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
    "dbCollection": "ksk_de" , # dbCollection = "ksk_en"
    "dbItems" : 5,
    "dbClient" : None,
    "preprocessor" : None,
    "embedder" : None,
    "llm" : None,
    "embProvider":None,
    "llmProvider":None,
    "dbProvider":"zilliz"
}

def initialize():
    """
    Initializes the configuration for the application.

    This function sets up the following components:
    - Database client using `deployUtils.VectorDb()`.
    - Preprocessor for text processing using `textUtils.PreProcessor` with the specified language.
    - Embedder model using `deployUtils.Embedder()`.
    - Language model (LLM) using `deployUtils.Llm` with the specified language.

    The function also calls `checkDb()` to ensure the database is properly set up.
    """
    config["dbClient"] = deployUtils.VectorDb(provider=config["dbProvider"])
    checkDb()
    # text stuff
    config["preprocessor"] = textUtils.PreProcessor(config["lang"])
    # models
    config["embedder"] = deployUtils.Embedder(provider=config["embProvider"])
    # llm
    config["llm"] = deployUtils.Llm(lang=config["lang"],provider=config["llmProvider"])


def checkDb():
    """
    Checks if the specified database collection exists and is accessible.

    This function attempts to describe the collection specified in the configuration.
    If the collection does not exist or an error occurs, it raises a ValueError.

    Raises:
        ValueError: If the collection does not exist or an error occurs during the check.

    Prints:
        Collection details if DEBUG is enabled.
        Error message if the collection check fails.
    """
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
    def queryLlm(context, query, history, size=200):
        """
        Queries the language model (LLM) with the given context, query, and history.

        Args:
            context (str): The context to provide to the LLM.
            query (str): The query to ask the LLM.
            history (list): The history of previous interactions with the LLM.
            size (int, optional): The maximum number of tokens for the response. Defaults to 200.

        Returns:
            tuple: A tuple containing the answer from the LLM and the number of tokens used.
        """
    answer, tokens = config["llm"].queryWithContext(context, query, history,size)
    return answer, tokens

@log_query
def initQuery(context, query, size=200):
    """
    Initializes a query using the provided context and query parameters.

    Args:
        context (str): The context in which the query is being made.
        query (str): The query string to be processed.
        size (int, optional): The size parameter for the query. Defaults to 200.

    Returns:
        tuple: A tuple containing the answer, tokens, and messages from the query.
    """
    answer, tokens, msgs  = config["llm"].initChat(context, query, size)
    return answer, tokens, msgs

@log_query
def followQuery(query, history, size=200):
    """
    Executes a follow-up query using the provided LLM configuration.

    Args:
        query (str): The query string to be followed.
        history (list): The history of previous interactions or messages.
        size (int, optional): The size parameter for the LLM follow-up chat. Defaults to 200.

    Returns:
        tuple: A tuple containing the answer, tokens, and messages from the LLM follow-up chat.
    """
    answer, tokens, msgs  = config["llm"].followChat(query, history, size)
    return answer, tokens, msgs

# Step 5: Run the RAG system
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--items', default = 5)      # option that takes a value
    parser.add_argument('-l', '--lang',default = "de")      # option that takes a value
    parser.add_argument('-c', '--collection',default = "ksk")      # option that takes a value
    parser.add_argument('-e', '--embProvider',default = "deepinfra")      # option that takes a value
    parser.add_argument('-m', '--llmProvider',default = "deepinfra")      # option that takes a value
    args = parser.parse_args()
    print(args.items, args.lang, args.collection) 

    config["lang"] = args.lang
    config["dbCollection"] = f"{args.collection}_{args.lang}"
    config["dbItems"] = int(args.items)
    config["embProvider"] = args.embProvider
    config["llmProvider"] = args.llmProvider
    if DEBUG: print(config)
    initialize()
    print(config["llm"].getModel())
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

    
    
