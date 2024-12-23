import os
import sys
import requests
from ragInstrumentation import measure_execution_time

import private_remote as pr

DEBUG = False


class Embedder:
    def __init__(self, provider: str = "deepinfra"):
        if provider == "deepinfra":
            self.api_key = pr.mdlApiKey
            self.model = pr.embMdl
            self.url = "https://api.deepinfra.com/v1/openai/embeddings"
        else:
            raise ValueError("Invalid provider")

    @measure_execution_time
    def encode(self, input):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {"model": self.model, "input": input, "encoding_format": "float"}
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None


class Llm:
    def __init__(self, provider: str = "deepinfra", lang="german"):
        if provider == "deepinfra":
            self.api_key = pr.mdlApiKey
            self.model = pr.lngMdl
            self.url = "https://api.deepinfra.com/v1/openai/chat/completions"
            self.lang = lang
        else:
            raise ValueError("Invalid provider")

    @staticmethod
    def getDefaultModel():
        return pr.lngMdl

    def getModel(self):
        return self.model
    
    def setModel(self, model):
        self.model = model

    @measure_execution_time
    def query(self, query, size = 100):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        richQuery = f"""
        You are an intelligent assistant.
        The question is:
        {query}
        Respond in {self.lang} language with a limit of {size} {self.lang} words.
        """
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": richQuery, "temperature": 0.4}],
        }
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            return text, tokens
        else:
            return None

    @measure_execution_time
    def summarize(self, text, size=500):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        richQuery = f"""
        You are an intelligent assistant.
        Summarize the following {self.lang} text into {self.lang}:
        {text}
        Respond in {self.lang} language. Limit the summary to {size} {self.lang} words.
        """
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": richQuery, "temperature": 0.4}],
        }
        if DEBUG:
            print(richQuery)
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            return text, tokens
        else:
            return None

    @measure_execution_time
    def translate(self, text, src="english"):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        richQuery = f"""
        You are an intelligent assistant.
        Translate the following {src} text into {self.lang}:
        {text}
        Respond in {self.lang} language, translation only, no comments. Do not add any leading or trailing comments on translation process.
        """
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": richQuery, "temperature": 0.4}],
        }
        if DEBUG:
            print(richQuery)
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            return text, tokens
        else:
            return None
    
    @measure_execution_time
    def queryWithContext(self, context, query, msgHistory=[], size=100):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        richQuery = f"""
        You are an intelligent assistant. Use the following {self.lang} context to answer the question in {self.lang}.
        {context}
        The {self.lang} question is:
        {query}
        Respond in {self.lang} language. Limit your response to {size} {self.lang} words.
        """
        msg = {"role": "user", "content": richQuery}
        msgHistory.append(msg)
        data = {
            "model": self.model,
            "messages": [msg],  # msgHistory,
            "temperature": 0.4,
        }
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            if DEBUG:
                print(data)
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            msgHistory.append(
                {"role": data["choices"][0]["message"]["role"], "content": text}
            )
            return text, tokens
        else:
            print("LLM failed:",response.status_code)
            return None, None

    @measure_execution_time
    def initChat(self, context, query, size=100):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        msgs = []
        msgs.append({
            "role": "system", 
            "content": """
                You are an expert assistant designed to provide detailed and accurate responses 
                based on user queries and retrieved context. 
                If the retrieved context is insufficient or ambiguous, 
                ask for clarification or provide a logical extrapolation."
            """
                })
        msgs.append({
            "role": "system", 
            "content": f"""
                Context in {self.lang}:\n
                {context}
                """
                })
        msgs.append({
            "role": "user", 
            "content": f"""
                The {self.lang} question is:
                {query}
                Respond in {self.lang} language. Limit your response to {size} {self.lang} words.
                Offer assistance for follow-up question.
                """
                })
                
        data = {
            "model": self.model,
            "messages": msgs,  # msgHistory,
            "temperature": 0.4,
        }
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            if DEBUG:
                print(data)
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            return text, tokens, msgs
        else:
            print("LLM failed:",response.status_code)
            return None, None, None

    @measure_execution_time
    def followChat(self, query, msgHistory=[], size=100):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        msgHistory.append({
            "role": "user", 
            "content": f"""
                The {self.lang} question is:\n
                {query}
                
                Respond in {self.lang} language. Limit your response to {size} {self.lang} words. 
                Silently verify the question is related to the context provided. 
                Do not offer assistance if the question is unrelated.
                """
            })
        data = {
            "model": self.model,
            "messages": msgHistory,  # msgHistory,
            "temperature": 0.4,
        }
        response = requests.post(self.url, headers=hdrs, json=data)
        if response.status_code == 200:
            data = response.json()
            if DEBUG:
                print(data)
            text = data["choices"][0]["message"]["content"].strip()
            tokens = data["usage"]["total_tokens"]
            return text, tokens, msgHistory
        else:
            print("LLM failed:",response.status_code)
            return None, None, None



# https://cloud.zilliz.com/orgs/org-vuubdaymoyjvtgcqjczdsp/projects/proj-11d29d1ea430702a07c431/clusters/in03-eb450554ac4fcc5/collections/ksk/playground?collection=ksk&type=QUERY_DATA
class VectorDb:
    """ make sure to check parameter names. rest api is different from python"""
    def __init__(self, provider: str = "zilliz"):
        self.api_key = pr.dbApiKey
        self.collection = pr.dbCollection
        # like
        # https://in03-eb450554ac4fcc5.serverless.gcp-us-west1.cloud.zilliz.com
        self.url = f"https://{pr.dbCluster}.serverless.{pr.dbRegion}.cloud.zilliz.com"
        print(self.url)

    @measure_execution_time
    def describeCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName": collection}
        url = f"{self.url}/v2/vectordb/collections/describe"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def indexCollection(self, collection, field):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName": collection,
            "indexParams": [
                {
                    "metricType": "L2",
                    "fieldName": field,
                    "indexName": field,
                    "indexConfig": {"index_type": "AUTOINDEX"},
                }
            ],
        }
        url = f"{self.url}/v2/vectordb/indexes/create"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def indexDescribeCollection(self, collection, field):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName": collection, "indexName": field}
        url = f"{self.url}/v2/vectordb/indexes/describe"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def indexListCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName": collection}
        url = f"{self.url}/v2/vectordb/indexes/list"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def statCollection(self, collection):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName": collection}
        url = f"{self.url}/v2/vectordb/collections/get_stats"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def upsertItem(self, collection, item):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {"collectionName": collection, "data": [item]}
        url = f"{self.url}/v2/vectordb/entities/upsert"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def searchItem(self, collection, vectors, limit=3, fields=["*"], groupByFile=True):
        """_summary_

        Args:
            collection (_type_): _description_
            vectors (_type_): _description_
            limit (int, optional): _description_. Defaults to 3.
            fields (list, optional): _description_. Defaults to ["*"].
            groupByFile (bool, optional): _description_. Defaults to True.
            L2      Smaller L2 distances indicate higher similarity.
            IP      Larger IP distances indicate higher similarity.
            COSINE  Larger cosine value indicates higher similarity.
        """

        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName": collection,
            "data": [vectors],
            "limit": limit,
            "outputFields": fields,
        }
        if groupByFile:
            data["groupingField"] = "itemCode"
        url = f"{self.url}/v2/vectordb/entities/search"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            if response.json()["code"] == 0:
                return response.json()
            raise ValueError(response.json())
        else:
            print(response.status_code)
            return None

    @measure_execution_time
    def queryText(self, collection, condition, limit=3, fields=["*"]):
        hdrs = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if collection == None:
            collection = self.collection
        data = {
            "collectionName": collection,
            "filter": condition,
            "limit": limit,
            "outputFields": fields,
        }
        url = f"{self.url}/v2/vectordb/entities/query"
        response = requests.post(url, headers=hdrs, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None
