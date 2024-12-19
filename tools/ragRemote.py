import os
import sys
import requests
import re
import nltk

import private_remote as pr

debug = False

class PreProcessor():
    def __init__(self,lang="german"):
        nltk.download('punkt_tab')
        #nltk.download('words')
        if lang not in ["german","english"]:
            raise ValueError("Invalid language")
        self.lang = lang

    def clean(self, text):
        sents_raw = nltk.sent_tokenize(text,language=self.lang)
        sents = []
        wordcount = 0
        for s in sents_raw:
            words = nltk.wordpunct_tokenize(s)
            wordcount += len(words)
            sents.append(" ".join(words).strip())
            
        text_cleaned = ".".join(sents)
        return text_cleaned


    def chunk(self, text, size=200, overlap=30):
        """
        Split the text into smaller chunks of a fixed size with an overlap.
        
        Args:
            text (str): The text to split.
            chunk_size (int): The size of each chunk (in tokens, not characters).
            overlap (int): The number of tokens to overlap between chunks.
        
        Returns:
            list: A list of text chunks.
        """
        overlap = size // 2 if overlap >= size else overlap
        words = text.split()  # Split text into words
        chunks = []
        for i in range(0, len(words), size - overlap):
            chunk = ' '.join(words[i:i + size])
            chunks.append(chunk)
        return chunks


class Embedder():
    def __init__(self, provider: str = "deepinfra"):
        if provider == "deepinfra":
            self.api_key = pr.mdlApiKey
            self.model = pr.embMdl
            self.url = "https://api.deepinfra.com/v1/openai/embeddings"
        else:
            raise ValueError("Invalid provider")

    def embed(self, input):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "input": input,
            "encoding_format": "float"
        }
        response = requests.post(self.url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            return None


class Llm():
    def __init__(self, provider: str = "deepinfra", lang = "german"):
        if provider == "deepinfra":
            self.api_key = pr.mdlApiKey
            self.model = pr.lngMdl
            self.url = "https://api.deepinfra.com/v1/openai/chat/completions"
            self.lang = lang
        else:
            raise ValueError("Invalid provider")

    def query(self, query):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        richQuery = f"""
        You are an intelligent assistant.
        The question is:
        {query}
        Respond in {self.lang} language with a limit of 100 {self.lang} words.
        """
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": richQuery
                }
            ]
        }
        response = requests.post(self.url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def summarize(self, text, size=500):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        richQuery = f"""
        You are an intelligent assistant.
        Summarize the following {self.lang} text into {self.lang}:
        {text}
        Respond in {self.lang} language. Keep the summary to {size} {self.lang} words.
        """
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": richQuery
                }
            ]
        }
        if debug: print(richQuery)
        response = requests.post(self.url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def queryWithContext(self, context, query, size=500):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        richQuery = f"""
        You are an intelligent assistant. Use the following {self.lang} context to answer the question in {self.lang}.
        {context}
        The {self.lang} question is:
        {query}
        Respond in {self.lang} language. Keep the summary to {size} {self.lang} words.
        """
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": richQuery
                }
            ]
        }
        response = requests.post(self.url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            return None

# https://cloud.zilliz.com/orgs/org-vuubdaymoyjvtgcqjczdsp/projects/proj-11d29d1ea430702a07c431/clusters/in03-eb450554ac4fcc5/collections/ksk/playground?collection=ksk&type=QUERY_DATA
class VectorDb():    
    def __init__(self, provider: str = "zilliz"):
        self.api_key = pr.dbApiKey
        self.collection = pr.dbCollection
        # like
        # https://in03-eb450554ac4fcc5.serverless.gcp-us-west1.cloud.zilliz.com
        self.url = f"https://{pr.dbCluster}.serverless.{pr.dbRegion}.cloud.zilliz.com"
        print(self.url)


    def describeCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName":collection}
        url = f"{self.url}/v2/vectordb/collections/describe"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def indexCollection(self, collection,field):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName":collection,
            "indexParams": [
                    {
                        "metricType": "L2",
                        "fieldName": field,
                        "indexName": field,
                        "indexConfig": {
                            "index_type": "AUTOINDEX"
                        }
                    }
                ]            
            }
        url = f"{self.url}/v2/vectordb/indexes/create"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def indexDescribeCollection(self, collection,field):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName":collection,
            "indexName": field
            }
        url = f"{self.url}/v2/vectordb/indexes/describe"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def indexListCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName":collection
                }
        url = f"{self.url}/v2/vectordb/indexes/list"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def statCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName":collection}
        url = f"{self.url}/v2/vectordb/collections/get_stats"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def upsertItem(self,collection,item):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName":collection,
                "data":[item]
            }
        url = f"{self.url}/v2/vectordb/entities/upsert"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    def searchItem(self,collection, item, limit=3, fields=["*"]):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName":collection,
            "data":[item],
            "limit":limit,
            "outputFields":fields
        }
        url = f"{self.url}/v2/vectordb/entities/search"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None


    def queryText(self,collection, condition):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName":collection,
            "filter":condition,
            "limit":limit,
            "outputFields":fields
        }
        url = f"{self.url}/v2/vectordb/entities/query"
        response = requests.post(url, headers=hdrs, json=data) 
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None
        
        
