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
from notification_manager import NotificationManager
from policy_builder import PolicyGraph, IntentVerification
from intent_determination import IntentDetermination
#from elasticsearch_database import ElasticsearchDatabase
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
        notifs = None
        
        if match:
            if match.group("start") == "iro":
                cmd = match.group("command")
                if cmd == "add":
                    info_message, my_form, my_form_script, notifs = self.instruct_add(match.group("intent"))
                elif cmd == "status":
                    info_message = self.instruct_status()
                elif cmd == "reset":
                    info_message = self.instruct_reset()
                elif cmd == "intents":
                    info_message = self.instruct_intents()
                elif cmd == "push":
                    info_message = self.instruct_push()
                if info_message:
                    return info_message, my_form, my_form_script, notifs

            if match.group("start") == "reports":
                info_message = "reports"
                return info_message, my_form, my_form_script, notifs
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
                return info_message, my_form, my_form_script, notifs

        return self.notif.get_instructions(), my_form, my_form_script, notifs

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
        verified = True
        validated = True
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

        # the text is assumed to be verified 
        if plain_text is not None:
            if verified:
                if validated:
                    if plain_text=="wallet_id_attack_detection":
                        #notifs = "Wallet ID Attack Detection Rule"
                        msg = "Please provide details and submit the intent !"
                        my_form, my_form_script = self.notif.get_form("wallet_detection")
                        return msg, my_form, my_form_script, notifs
                    return "ERROR: Non valid intent please enter a valid intent !", my_form, my_form_script, notifs
        return 'ERROR: Please enter an intent\n Maybe you should use quotes ""\nwrite anything to see instructions', my_form, my_form_script, notifs



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
        display_message = self.notif.get_intents()
        return (
            "The list of intents: \n\n"
            + display_message
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
        if is_file_empty("./outputfiles/" + self.json_filename):
            return "Please enter Intents !!"
        self.conflict_solving()
        return "Pushing and resolving conflict !!"


    def create_hspl_from_intent(self,form_data, intent_name):
        # create the json from the form_data
        to_test = {'wallet_id':"wallet id 1", "value": 1, "period": 1, "time":"hour",
        "hspl_object":[{"id":"1", "action":"notify", "object":"supply_chain_operator"}]
        }
        structured_data = self.get_data_from_intent(form_data, intent_name)
        print(structured_data)
        for  val in structured_data['hspl_object']:
            print("it works.........")
        #check the needed xml template
        fpath = "/edc/hspl_new.xml"
        fname = "tmp_register/hspl1.xml"
        with open(fpath, 'w') as f:
            html = render_template(fname, objects=structured_data)
            f.write(html)
        if not os.path.exists(fpath):
            raise Exception("it is not saved :((")
        msg = None
        try:
            with open(fpath) as f_obj:
                msg = f_obj.read()
        except FileNotFoundError:
            msg = "Sorry, the file "+ fpath + "does not exist."

        
        return msg

    def get_data_from_intent(self, form_data, intent_name):
        structured_data = {}
        if intent_name == 'wallet_id_attack_detection':
            structured_data['id'] = "hspl1"
            structured_data['wallet_id'] = form_data['subject']
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
        return structured_data

    def conflict_solving(self):
        """
        |    solve conflicts of the intents registered in the intent register.
        |
        |   Returns:
        |       str: information message to User
        |
        """
        str_name_store = ""
        users = np.array([[None, None]])
        output_file = open("./outputfiles/" + self.json_filename)
        #users = np.append(users, [["user1", PolicyGraph()]], axis=0)
        #users = np.append(users, [["user2", PolicyGraph()]], axis=0)
        with output_file as file:
            lines = file.read()
        lines = ast.literal_eval(lines)
        for line in lines:
            str_name_store = line["users"]
            if self.check_for_user(str_name_store, users):
                self.change_state(line, self.get_graph(str_name_store, users))
                print(self.get_graph(str_name_store, users).print_graph())
            else:
                users = np.append(users, [[str_name_store, PolicyGraph()]], axis=0)
                self.change_state(line, self.get_graph(str_name_store, users))
                print(self.get_graph(str_name_store, users).print_graph())
        for user in users:
            if user[0] is not None:
                print_result_file(self.export_text(user[0], user[1]))
        '''policy_graph = PolicyGraph()
        with output_file as file:
            lines = file.read()
        lines = ast.literal_eval(lines)
        for line in lines:
            str_name_store = line["users"]
            if line["permission"] == "blocked":
                permission = False
            else:
                permission = True
            policy_graph.change_state(line["asset"], permission)
        policy_graph.print_graph()'''

        #message = "allow " + str_name_store + " to access assets in "
        #str_result = "check " + str_name_store + " in database of users" + "\n"
        '''if policy_graph.print_outputnew() == "":
            str_result += message + "" + policy_graph.org_name
        else:
            str_result += (
                message
                + ""
                + policy_graph.org_name
                + " except "
                + policy_graph.print_outputnew()
            )
        str_result += "\n" + "alert admin in " + policy_graph.org_name'''
        #print_result_file(str_result)
        self.instruct_reset()

    def export_text(self, str_name_store, policy_graph):
        """
        |    return final result
        |
        |   Args:
        |       str_name_store(str):
        |       policy_graph(PolicyGraph):
        |   Returns:
        |       str_result(str): information message to User
        |
        """
        message = "allow " + str_name_store + " to access assets in "
        str_result = "check " + str_name_store + " in database of users" + "\n"
        if policy_graph.print_outputnew() == "":
            str_result += message + "" + policy_graph.org_name
        else:
            str_result += (
                message
                + ""
                + policy_graph.org_name
                + " except "
                + policy_graph.print_outputnew()
            )
        str_result += "\n" + "alert admin in " + policy_graph.org_name + "\n \n"
        return str_result

    def change_state(self, line, policy_graph):
        """
        |    change state in User policy graph
        |
        |   Args:
        |       line(str):
        |       policy_graph(PolicyGraph):
        |
        """
        if line["permission"] == "blocked":
            permission = False
        else:
            permission = True
        policy_graph.change_state(line["asset"], permission)

    def check_for_user(self, user, users):
        for my_user in users:
            if my_user[0] == user:
                return True
        return False

    def get_graph(self, user, users):
        for my_user in users:
            if my_user[0] == user:
                return my_user[1]
        return None

    def write_json(self, new_data):
        """
        |    append intents to Intents Document.
        |
        |   Args:
        |       new_data(str):  data to be written in JSON
        """
        with open("./outputfiles/" + self.json_filename, "a") as file:
            if not is_file_empty("./outputfiles/" + self.json_filename):
                file.write(",")
            file.write(json.dumps(new_data, indent=4, sort_keys=True))

    def write_new(self, new_data):
        """
        |    append intents to Intents Document.
        |
        |   Args:
        |       new_data(str):  data to be written in JSON
        """
        my_array = []
        with open("./outputfiles/" + self.json_filename, "a") as file:
            if not is_file_empty("./outputfiles/" + self.json_filename):
                output_file = open("./outputfiles/" + self.json_filename)
                with output_file as my_file:
                    lines = my_file.read()
                my_array = ast.literal_eval(lines)
                my_array.append(new_data)
            else:
                my_array.append(new_data)
            self.instruct_reset()
            file.write(json.dumps(my_array, indent=4, sort_keys=True))
