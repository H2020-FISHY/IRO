"""
|
|   file:       intentStore.py
|
|   brief:
|   author:   Mounir Bensalem  
|   email:    mounir.bensalem@tu-bs.de
|   copyright:  © IDA - All rights reserved
"""
import sys
import os
_cwd = os.getcwd()
sys.path.append(_cwd+ '/knowledgeBase/intentStore')

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import intentQueries as iq
import numpy as np
import os
import time
import json

es_url="127.0.0.1"
es_port="9200"
es_retry_time = 5
es_conn_attempts = 3
es = None
try:
    es_url = os.environ["ES_HOST"]
    es_port = os.environ["ES_PORT"]
except:
    print("ES_HOST:ES_PORT environment variables do not exist!!, trying with localhost...")

for attempt in range(3):
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
        es_conn_attempts -= 1
        if es_conn_attempts == 0:
            print("Connection to Elasticsearch could not be established, exiting...")
            #exit(1)
    if es != None:
        print("Connection to Elasticsearch [" + es_url + ":" + es_port + "] has been established")
        break
    

es_index_client = IndicesClient(es)
# creation of intent store in elasticsearch
with open(_cwd + "/knowledgeBase/intentStore/intentConfig.json") as f:
    configurations = json.load(f)
    #print(configurations)
if es_index_client.exists(index="intent"):
    es_index_client.delete(index="intent", ignore=404)
    es_index_client.delete(index="test", ignore=404)

es_index_client.create(index="intent", body=configurations)

# creation of index for generated policy for EDC
with open(_cwd + "/knowledgeBase/intentStore/HSPLConfig.json") as f:
    configurations = json.load(f)
    #print(configurations)
if es_index_client.exists(index="hspl"):
    es_index_client.delete(index="hspl", ignore=404)

es_index_client.create(index="hspl", body=configurations)

with open(_cwd + "/knowledgeBase/intentStore/AttacksConfig.json") as f:
    configurations = json.load(f)
    #print(configurations)
if es_index_client.exists(index="attacksinfo"):
    es_index_client.delete(index="attacksinfo", ignore=404)

es_index_client.create(index="attacksinfo", body=configurations)

class IntentStoreManager:
    def __init__(self):
        self.client = es
        self.add_intent_from_JSON(1, "intent_1.json")
        self.add_intent_from_JSON(2, "intent_2.json")
        self.add_intent_from_JSON(4, "intent_4.json")

    def query_single_vocab(self, word):
        res = self.client.search(index="intent", body=iq.query_single_vocab(word))
        return res

    def query_two_vocab(self, word1, word2):
        res = self.client.search(index="intent", body=iq.query_two_vocab(word1, word2))
        return res
        
    def query_intentname(self, word):
        res = self.client.search(index="intent", body=iq.query_intentname(word))
        return res
    
    def add_intent_from_JSON(self, id, filename):
        with open(_cwd + "/knowledgeBase/intentStore/" + filename) as f:
            _intent_1 = json.load(f)
        self.client.index(index="intent", id=id, document=_intent_1)
    
    def get_intent_with_id(self, id):
        _intent = self.client.get(index="intent", id=id)
        return _intent
    
    def get_all_intents(self):
        _intent = self.client.search(index="intent", body=iq.query_all())['hits']['hits']
        intent_names = []
        for el in _intent:
            intent_names.append(el['_source']['intentname'])

        return intent_names

    def get_all_generated_policies(self):
        res1 = self.client.search(index="hspl", body=iq.query_all())['hits']['hits']
        res2 = self.client.search(index="attacksinfo", body=iq.query_all())['hits']['hits']
        list_of_policies= {}
        for el in res1:
            list_of_policies["hspl_"+str(el['_source']["id"])] = el['_source']
        
        for el in res2:
            list_of_policies["attack_info_"+str(el['_source']["id"])] = el['_source']
        return list_of_policies

    def get_all_generated_attacks_info(self):
        res = self.client.search(index="attacksinfo", body=iq.query_all())['hits']['hits']['_source']
        return res

#eld = IntentStoreManager()
#print(eld.query_intentname("wallet"))


'''
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json

es_client = Elasticsearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=["elastic", "changeme"],
)

es_index_client = IndicesClient(es_client)
#
with open("intentConfig.json") as f:
    configurations = json.load(f)
    print(configurations)
if es_index_client.exists(index="intent"):
    es_index_client.delete(index="intent", ignore=404)
    es_index_client.delete(index="test", ignore=404)

es_index_client.create(index="intent", body=configurations)
# to delete the index

doc = {
    "id": 1,
    "intentname": "wallet_id_detection",
    "use_template": "True",
    "HTMLtemplate": "form_threat_detection.html",
    "JStemplate": "script_form_th_d.html",
    "attributes": [
        {"attribute_name": "wallet_id", "attribute_type": "string"},
        {"attribute_name": "value", "attribute_type": "integer"},
        {"attribute_name": "period", "attribute_type": "integer"},
        {"attribute_name": "time", "attribute_value": "integer"},
    ],

    "vocabularies": [
        {"vocab_name": "wallet id", "vocab_values": [
            {"vocab_value": "Wallet ID"},
            {"vocab_value": "wallet id"},
            {"vocab_value": "Wallet id"},
            {"vocab_value": "id of wallet"},
            {"vocab_value": "detection"}
            ]
        },
        {"vocab_name": "detection", "vocab_values": [
            {"vocab_value": "detection"},
            {"vocab_value": "detection"},
            {"vocab_value": "detect"}
            ]
        },
    ],
}

es_client.index(index="intent", id=1, document=doc)
print(es_client.get(index="intent", id=1))


doc2 = {
    "id": 2,
    "intentname": "ddos_attack",
    "use_template": "True",
    "HTMLtemplate": "form_threat_detection.html",
    "JStemplate": "script_form_th_d.html",
    "vocabularies": [
        {"vocab_name": "ddos", "vocab_values": [
            {"vocab_value": "ddos attack"},
            {"vocab_value": "ddos"},
            {"vocab_value": "DDOS"},
            {"vocab_value": "DDoS"}
            ]
        },
    ],    
}

es_client.index(index="intent", id=2, document=doc2)
print(es_client.get(index="intent", id=2))

import csv
import json

colums = ["id", "name", "price", "brand", "cpu", "memory", "storage"]
index_name = "intent"

with open("intent.csv", "r") as fi:
    reader = csv.DictReader(
        fi, fieldnames=colums, delimiter=",", quotechar='"'
    )

    # This skips the first row which is the header of the CSV file.
    next(reader)

    actions = []
    for row in reader:
        action = {"index": {"_index": index_name, "_id": int(row["id"])}}
        doc = {
            "id": int(row["id"]),
            "name": row["name"],
            "price": float(row["price"]),
            "brand": row["brand"],
            "attributes": [
                {"attribute_name": "cpu", "attribute_value": row["cpu"]},
                {"attribute_name": "memory", "attribute_value": row["memory"]},
                {
                    "attribute_name": "storage",
                    "attribute_value": row["storage"],
                },
            ],
        }
        actions.append(json.dumps(action))
        actions.append(json.dumps(doc))

    with open("intent.json", "w") as fo:
        fo.write("\n".join(actions))

    es_client.bulk(body="\n".join(actions))

search_query = {
    "query": {
        "match": {
        "name": "Apple"
        }
    }
}


print(es_client.search(index="intent", body=search_query))

print("done!")
'''