"""
|
|   file:       intent_creation.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""
import numpy as np


class IntentCreation:
    """
    |   IntentCreation Class
    """
    def __init__(self):
        self.intent_setup = None
        self.define_intent()

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
    def __init__(self):
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
