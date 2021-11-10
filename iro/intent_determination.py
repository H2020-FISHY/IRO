"""
|
|   file:       intent_determination.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""


def my_function(my_list):
    """
    |    change format
    |
    |   Args:
    |       my_list(list): vector list
    |
    |   Returns:
    |       list:  new format
    """
    return list(dict.fromkeys(my_list))


def create_json(tmp_intent_list):
    """
    |    create json document
    |
    |   Args:
    |       tmp_intent_list(list): list of intents
    |
    |   Returns:
    |       new_intent(dict):  json dict
    """
    outputs = {}
    new_intent = {}
    for lines in tmp_intent_list:
        for line in lines[0:]:
            if "set" in line:
                _, name, _, val = line.split()
                new_intent[name] = val
        outputs["item"] = new_intent
    return new_intent


class IntentDetermination:
    """
    |   IntentDetermination Class
    """

    def __init__(self, intent_store, intent_structure, intent_verification):
        self.intent_store = intent_store
        self.json_text = None
        self.intent_structure = intent_structure
        self.intent_content_list = intent_verification.content_list
        self.intent_options_list = intent_verification.option_list
        self.start_translation()

    def start_translation(self):
        """
        |    get intent options
        |
        |   Args:
        |       self.intent_setup.get_options(list):  options list
        """
        tmp_intent_list = self.translate_grammar_to_list()
        self.json_text = create_json(tmp_intent_list)

    def translate_to_grammar(self):
        """
        |    translate requirements and options to string
        |
        |   Returns:
        |       grammar_text(str):  intent text
        """
        grammar_text = ""
        grammar_text += self.translate_requirements()
        grammar_text += self.translate_options()
        return grammar_text

    def translate_requirements(self):
        """
        |    translate requirements to string
        |
        |   Returns:
        |       grammar_text(str):  requirements text
        """
        grammar_text = ""
        for vocab in my_function(self.intent_content_list):
            vector = self.intent_store.get_intent_name(
                vocab, self.intent_store.query_elasticsearch(vocab)
            )
            grammar_text += "set %s equal %s \n" % (vector[0], vector[1])
        return grammar_text

    def translate_options(self):
        """
        |    translate options to string
        |
        |   Returns:
        |       grammar_text(str):  options text
        """
        grammar_text = ""
        for vector in self.intent_options_list:
            grammar_text += "set %s equal %s \n" % (vector[0], vector[1])
        return grammar_text

    def translate_grammar_to_list(self):
        """
        |    translate grammar to list
        |
        |   Returns:
        |       self.intent_setup.get_options(list):  options list
        """
        tmp_intents = []
        new_intent = []
        intent_lines = self.translate_to_grammar().split("\n")
        for line in intent_lines:
            if line and line != "\r":
                new_intent.append(line)
            else:
                tmp_intents.append(new_intent)
        return tmp_intents
