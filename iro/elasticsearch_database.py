"""
|
|   file:       elasticsearch_database.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""
from elasticsearch import Elasticsearch
from intent_store import Database
import numpy as np
import os
import time


es_url="127.0.0.1"
es_port="9200"
es_retry_time = 5
es = None
try:
    es_url = os.environ["ES_HOST"]
    es_port = os.environ["ES_PORT"]
except:
    print("ES_HOST:ES_PORT environment variables do not exist!!, trying with localhost...")

while True:
    try:
        es = Elasticsearch(
            [{"host": es_url, "port": es_port}],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            sniffer_timeout=60,
            sniff_timeout=10,
            timeout=30,
        )
    except:
        print("Connection to Elasticsearch [" + es_url + ":" + es_port + "] failed!, retrying in " + str(es_retry_time) + " seconds...")
        time.sleep(es_retry_time)
    if es != None:
        print("Connection to Elasticsearch [" + es_url + ":" + es_port + "] has been established")
        break
    
if es.indices.exists(index="database"):
    es.indices.delete(index="database")
res = es.index(index="database", id=5, body=Database)


class ElasticsearchDatabase:
    def __init__(self):
        self.client = es

    def query_elasticsearch(self, word):
        query = {"query": {"query_string": {"query": word}}}
        return query

    def get_intent_name(self, word, query):

        for index in self.client.indices.get("*"):
            search_result = self.client.search(index=index, body=query)
            for hit in search_result["hits"]["hits"]:
                for key in hit["_source"]:
                    for val in hit["_source"][key]:
                        for va in hit["_source"][key][val]["vocabulary"]:
                            if va == word:
                                return np.array([key, val])
        return np.array(["key", "val"])

    def get_specific_vocab(self, index, name):
        vocabularies = []
        store = self.client.get(index=index, id=5)
        for va in store["_source"][name]:
            for v in store["_source"][name][va]["vocabulary"]:
                vocabularies.append(v)
        return vocabularies

    def get_all_vocabulary(self, index):
        vocabularies = []
        store = self.client.get(index=index, id=5)
        for val in store["_source"]:
            for va in store["_source"][val]:
                for v in store["_source"][val][va]["vocabulary"]:
                    vocabularies.append(v)
        return vocabularies
