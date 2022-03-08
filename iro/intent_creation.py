"""
|
|   file:       intent_creation.py
|
|   brief:
|   author:     Mounir Bensalem
|   email:      mounir.bensalem@tu-bs.de
|   copyright:  © IDA - All rights reserved
"""
import string
import numpy as np


class IntentCreation:
    """
    |   IntentCreation Class
    """
    def __init__(self):
        self.list_of_intents = []
        self.intent_setup = None
        self.define_intent()
        self.define_intents()


    def define_intents(self):
        """
        |    define intents requirements and options
        | TODO: read predefined intents from a YAML file or from elasticsearch
        """
        tmp = IntentSetup(intent_name="Attacker_detection")\
            .requirement("condition")\
            .requirement("subject")\
            .requirement("occurence")\
            .requirement("time")\
            .requirement("reaction")\
            .requirement("action")\
            .requirement("object")
        self.list_of_intents.append(tmp)
        """
        # TODO: to add in the future
        tmp = IntentSetup(intent_name="Attacker_DID_detection")\
            .requirement("if")\
            .requirement("did")\
            .requirement("occurence")\
            .requirement("time")\
            .requirement("then")\
            .requirement("action")\
            .requirement("object")
        self.list_of_intents.append(tmp)

        tmp = IntentSetup(intent_name="Attacker_IP_detection")\
            .requirement("if")\
            .requirement("ip_address")\
            .requirement("occurence")\
            .requirement("time")\
            .requirement("then")\
            .requirement("action")\
            .requirement("object")
        self.list_of_intents.append(tmp)
        """
    
    def get_options_per_intent(self, intent_name):
        """
        |    get intent options per intent
        |
        |   Args:
        |       intent.get_options(list):  options list
        """
        for intent in self.list_of_intents:
            if intent.intent_name == intent_name:
                return intent.get_options()
        return False

    def get_requirements_per_intent(self, intent_name):
        """
        |    get intent requirements per intent
        |
        |   Args:
        |       intent.get_requirements(list): all requirements list
        """
        for intent in self.list_of_intents:
            if intent.intent_name == intent_name:
                return intent.get_requirements()
        return False

    def get_all_options(self):
        """
        |    get all intent options
        |
        |   Args:
        |       all_options:  all options list
        """
        all_options = [i.get_options() for i in self.list_of_intents]
        return all_options

    def get_all_requirements(self):
        """
        |    get all intent requirements
        |
        |   Args:
        |       all_requirements:  all requirements list
        """
        all_requirements = [i.get_requirements() for i in self.list_of_intents]
        return all_requirements
        
    
    # for test example
    def define_intent(self):
        """
        |    define intent requirements and options
        |
        """
        self.intent_setup = IntentSetup() \
            .requirement("users") \
            .requirement("permission") \
            .requirement("asset") \
            .option("timeframes", "Nachtschicht") \
            .option("spot", "Spot1")

    def get_options(self):
        """
        |    get intent options
        |
        |   Args:
        |       self.intent_setup.get_options(list):  options list
        """
        return self.intent_setup.get_options()
        

    

    def get_requirements(self):
        """
        |    get intent requirements
        |
        |   Args:
        |       self.intent_setup.get_requirements(list):  requirements list
        """
        return self.intent_setup.get_requirements()


class IntentSetup:
    """
    |   IntentSetup Class
    """
    def __init__(self, intent_name=""):
        self.intent_name: string = intent_name
        self.requirements = []
        self.options = np.empty(shape=[0, 2])

    def requirement(self, vocabulary_name=None):
        """
        |    set intent requirement
        |
        """
        self.requirements.append(vocabulary_name)
        return self

    def option(self, vocabulary_name, standard_value):
        """
        |    set intent options
        |
        """
        self.options = np.append(self.options, [[vocabulary_name, standard_value]], axis=0)
        return self

    def get_options(self):
        """
        |    get intent options
        |
        """
        return self.options

    def get_requirements(self):
        """
        |    get intent requirements
        |
        """
        return self.requirements
# tmp = IntentCreation()
# print(tmp.get_options())