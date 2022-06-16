"""
|
|   file:       intent_manager.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""
#from msilib.schema import Error
import re
import numpy as np
import ast
import json
import os
from flask import render_template
from learningAndReasoning.notifications.notification_manager import NotificationManager
from policy_builder import PolicyGraph, IntentVerification
from intent_determination import IntentDetermination
#from elasticsearch_database import ElasticsearchDatabase
from knowledgeBase.intentStore import intentStoreManager as ism
from attack_intent_store import Attack_Data
from intent_creation import IntentCreation


def print_result_file(str_result):
    """
    |    prints result in export text file.
    |
    |   Args:
    |       str_result(str):  final string
    """
    if not os.path.exists("./outputfiles"):
        os.makedirs("./outputfiles")
    
    with open("./outputfiles/export.txt", "a") as file:
        file.write(str_result)


def is_file_empty(file):
    """
    |    check if the file contains anything.
    |
    |   Args:
    |       file(str):  data to be written in JSON
    |
    |   Returns:
    |       bool: return if the file is empty or not
    """
    with open(file, "r") as r_file:
        file_content = r_file.read()
    if re.search(r"^\s*$", file_content):
        return True
    return False


class IntentManager:
    """
    |   IntentManager Class
    """
    def __init__(self, notif=NotificationManager):
        """
        |    Create Intent Manager
        | TODO: - update IntentCreation to consider new intent structure (eg. 
        | "If (Attacker wallet ID appears more than 5 times in two hours) then 
        | notifies/alerts F2F supply chain operator..")
        |       - add intent structure to intent_strore
        |       - update instruct_add() method
        """
        self.json_filename = "register.json"  # intent input history (intent_log)
        # TODO: update intent store to match hspl policies
        self.intent_store = ism.IntentStoreManager()
        self.hspl_id_counter = 0
        self.attack_info_id_counter = 0
        #self.intent_store = ElasticsearchDatabase()
        # TODO: make intent_structure a list which contains all structures, 
        # and update all the other methods using it
        self.intent_structure = IntentCreation()
        self.notif = notif

    def reading_command(self, intent_text):
        """
        |    reading commands method
        |
        |   Args:
        |       intent_text(str):  message sent from dashboard
        |
        |   Returns:
        |       str: information message to User
        |
        """
        '''
        TODO: add more regex and matches for CLI commands
        '''
        reading_regex = r"^(?P<start>\w+) (?P<command>\w+)? ?(?:\"(?P<intent>.*?)\")?"
        pattern = re.compile(reading_regex, re.I)
        match = pattern.search(intent_text)
        info_message = ""
        my_form = None
        my_form_script = None
        HTMLtemplate = None
        JStemplate = None
        notifs = None
        
        if match:
            if match.group("start") == "iro":
                cmd = match.group("command")
                if cmd == "add":
                    info_message, my_form, my_form_script,HTMLtemplate,JStemplate, notifs = self.instruct_add(match.group("intent"))
                elif cmd == "status":
                    info_message = self.instruct_status()
                elif cmd == "reset":
                    info_message = self.instruct_reset()
                elif cmd == "intents":
                    info_message = self.instruct_intents()
                elif cmd == "push":
                    info_message = self.instruct_push()
                if info_message:
                    return info_message, my_form, my_form_script, HTMLtemplate, JStemplate, notifs

            if match.group("start") == "reports":
                info_message = "reports"
                return info_message, my_form, my_form_script,HTMLtemplate,JStemplate, notifs
            '''return (
                "usage : iro <command> <args> \n"
                "\n"
                'add "intent"        read intents\n'
                "format              show the intent Requirements\n"
                "status              show intent register status\n"
                "push                solve conflict and send to controller\n"
                "reset               reset intent register\n"
            )
            '''
        else:
            if intent_text == "reports":
                info_message = "reports..."
                print("yes....")
                return info_message, my_form, my_form_script,HTMLtemplate, notifs

        return self.notif.get_instructions(), my_form, my_form_script, HTMLtemplate, notifs

    def instruct_add(self, plain_text):
        """
        |    read/add intents to intent register.
        |
        |   Args:
        |       plain_text(str):  extracted intent text
        |
        |   Returns:
        |       str: information message to User
        |
        """
        my_form = None
        my_form_script = None
        notifs = None
        '''
        # TODO: re-create those methods 
        intent_verification = IntentVerification(
            self.intent_structure, plain_text, self.intent_store
        )
        if plain_text is not None:
            if intent_verification.check_validation():
                intent_determine = IntentDetermination(
                    self.intent_store, self.intent_structure, intent_verification
                )
                #self.write_json(intent_determine.json_text)
                self.write_new(intent_determine.json_text)
                return "The intent has been successfully saved !"
            return "ERROR: Non valid intent please enter a valid intent !"
        return "ERROR: Please enter an intent "
        '''
        

        # the text is assumed to be verified TODO: consider intentStore here !!
        if plain_text is not None:
            if self.is_intent_exist(plain_text):
                intent_json = self.get_intent_info(plain_text)
                intent_json = intent_json['_source']
                msg = "Please provide details and submit the intent !"
                if intent_json['use_template']:
                    my_form, my_form_script, HTMLtemplate, JStemplate = self.notif.get_form(intent_json)
                return msg, my_form, my_form_script, HTMLtemplate,JStemplate, notifs
            return "ERROR: Non valid intent please enter a valid intent !", my_form, my_form_script,HTMLtemplate,JStemplate, notifs
        return 'ERROR: Please enter an intent\n Maybe you should use quotes ""\nwrite anything to see instructions', my_form, my_form_script,HTMLtemplate,JStemplate, notifs



    def instruct_status(self):
        """
        |    return status of the intent register.
        |
        |   Returns:
        |       str: information message to User
        |
        """
        if not os.path.exists("./outputfiles/" + self.json_filename):
            os.mknod("./outputfiles/" + self.json_filename)
        output_file = open("./outputfiles/" + self.json_filename)
        with output_file as file:
            lines = file.read()
        count = lines.count("{")
        return (
            str(count) + " intents to be pushed:\n"
            '   (use "iro push" to push your saved intents)'
        )

    def instruct_reset(self):
        """
        |    reset the intent register
        |
        |   Returns:
        |       str: information message to User
        |
        """
        with open("./outputfiles/" + self.json_filename, "w") as file:
            file.write("")
        return "reset successful !!"

    def instruct_intents(self):
        """
        |    return list of the intents
        |
        |   Returns:
        |       str: information message to User
        |
        """
        list_of_intents = self.notif.get_intents()
        return (
             list_of_intents
        )

        '''
        for i in self.intent_structure.get_requirements():
            display_message += "√ " + i + "\n"
        return (
            "The following information should be included in the intent: \n\n"
            + display_message
        )'''

    def instruct_push(self):
        """
        |    check if intents are ready to be solved.
        |
        |   Returns:
        |       str: information message to User
        |
        """
        # push to central repo 
        # TODO: push to elasticsearch index HSPL and Attack_info
        fpath = "edc/hspl_new.xml"
        fname = "tmp_register/hspl1.xml"
        with open(fpath, 'r') as f:
            hspl_info = f.read()
            
        if not os.path.exists(fpath):
            raise Exception("it is not saved :((")

        fpatha = "edc/attacker_new.txt"
        fnamea = "tmp_register/attack_id1.txt"
        with open(fpatha, 'r') as f:
            attacker_info = f.read()
            
        if not os.path.exists(fpatha):
            raise Exception("it is not saved :((")

        msg = None
        try:
            self.hspl_id_counter += 1
            hspl_info = {"id": self.hspl_id_counter, "XML": hspl_info}
            self.attack_info_id_counter += 1
            attacker_info = {"id": self.attack_info_id_counter, "JSON": attacker_info}
            self.intent_store.client.index(index="hspl", id=self.hspl_id_counter, document=hspl_info)
            self.intent_store.client.index(index="attacksinfo", id=self.hspl_id_counter, document=attacker_info)

            #self.conflict_solving()
            msg = "Policies saved successfully!\n\n" 
        except FileNotFoundError:
            msg = "Sorry, the file "+ fpath + "does not exist."

        return msg
    
    def is_intent_exist(self, intent_text):
        tmp = self.intent_store.query_intentname(intent_text)
        print(tmp)
        if tmp['hits']['hits'] != []:
            return True
        return False

    def get_intent_info(self, intent_text):
        tmp = self.intent_store.query_intentname(intent_text)
        return tmp['hits']['hits'][0]


    def create_hspl_from_intent(self,form_data, intent_name):
        # create the json from the form_data
        to_test = {'wallet_id':"wallet id 1", "value": 1, "period": 1, "time":"hour",
        "hspl_object":[{"id":"1", "action":"notify", "object":"supply_chain_operator"}]
        }
        structured_data_hspl, structured_data_attacker = self.get_data_from_intent(form_data, intent_name)
         
        print(structured_data_hspl)
        for  val in structured_data_hspl['hspl_object']:
            print("it works.........")
        #check the needed xml template
        fpath = "edc/hspl_new.xml"
        fname = "tmp_register/hspl1.xml"
        with open(fpath, 'w') as f:
            html = render_template(fname, objects=structured_data_hspl)
            f.write(html)
        if not os.path.exists(fpath):
            raise Exception("it is not saved :((")

        fpatha = "edc/attacker_new.txt"
        fnamea = "tmp_register/attack_id1.txt"
        with open(fpatha, 'w') as f:
            html = render_template(fnamea, attacker=structured_data_attacker)
            f.write(html)
        if not os.path.exists(fpatha):
            raise Exception("it is not saved :((")

        msg = None
        try:
            with open(fpath) as f_obj:
                tmp1 = f_obj.read()
            with open(fpatha) as f_obja:
                tmp2 = f_obja.read()
            msg = "Policies generated successfully!\n\n" + tmp1 + "\n" + tmp2
        except FileNotFoundError:
            msg = "Sorry, the file "+ fpath + "does not exist."

        
        return msg

    def get_data_from_intent(self, form_data, intent_name):
        structured_data = {}
        structured_data_attacker = {}
        if intent_name == 'wallet_id_attack_detection':
            structured_data['id'] = "hspl1"
            structured_data['wallet_id'] = Attack_Data[form_data['subject']]
            # should be read from policy store
            structured_data_attacker['name'] = Attack_Data[form_data['subject']]
            structured_data_attacker['type'] = 'WID'
            structured_data_attacker['id'] = form_data['subject']
            structured_data['value'] = form_data['value']
            structured_data['period'] = form_data['period']
            structured_data['time'] = form_data['time']
            structured_data['hspl_object'] = []
            try:
                k = 0
                while form_data['action_'+str(k)]:
                    structured_data['hspl_object'].append({})
                    structured_data['hspl_object'][k]['id'] = "hspl"+str(k)
                    structured_data['hspl_object'][k]['action'] = form_data['action_'+str(k)]
                    structured_data['hspl_object'][k]['object'] = form_data['object_'+str(k)]
                    k += 1
            except:
                pass

        else:
            print(intent_name)
        return structured_data, structured_data_attacker

    def conflict_solving(self):
        """
        |    solve conflicts of the intents registered in the intent register.
        |
        |   Returns:
        |       str: information message to User
        |
        """
        self.instruct_reset()