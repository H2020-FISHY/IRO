import sys
import os
_cwd = os.getcwd()
sys.path.append(_cwd+ '/knowledgeBase/policyStore')

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
#import intentQueries as iq
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
#
with open(_cwd + "/knowledgeBase/policyStore/policyConfig.json") as f:
    configurations = json.load(f)
    print(configurations)
if es_index_client.exists(index="policy"):
    es_index_client.delete(index="policy", ignore=404)
    es_index_client.delete(index="test", ignore=404)

es_index_client.create(index="policy", body=configurations)

class PolicyStoreManager:
    def __init__(self) -> None:
        self.client = es
        # this method can be used later to add more policies from the admin (intent configuration)
        self.add_policy_from_JSON(1, "policy_1.json")
        
    def getPolicyFormAndScript(self, intent_id):
        # get data from policy store
        form, script = {}, {}
        try:

            with open(_cwd + "/knowledgeBase/policyStore/forms/policy_"+ str(intent_id) +".json") as f:
                form = json.load(f)
            with open(_cwd + "/knowledgeBase/policyStore/scripts/policyScript_"+ str(intent_id) +".json") as f:
                script = json.load(f)
            form = self.format_policy_json(form)
            script = self.format_policy_json(script)

            form_list, script_list = [], []
            form_list.append(form)
            script_list.append(script)
        except:
            #  no error handling at the moment
            pass

        return form_list, script_list

    def format_policy_json(self, _json):
        _data = {}
        for el in _json['attributes']:
            val_list = []
            for val in el['attribute_values']:
                val_list.append(val['attribute_value'])
            _data[el['attribute_name']] = val_list
        return _data

    def get_policyStore_config(self):
        return 0

    def add_policy_from_JSON(self, id, filename):
        with open(_cwd + "/knowledgeBase/policyStore/forms/" + filename) as f:
            _policy = json.load(f)
        self.client.index(index="policy", id=id, document=_policy)
    
    def get_intent_with_id(self, id):
        _policy = self.client.get(index="policy", id=id)
        return _policy

