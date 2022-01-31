"""
|
|   file:       policy_builder.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""
from anytree import Node, RenderTree
import numpy as np



class PolicyReader:
    """
    |   PolicyReader class: it reads the hspl model templates
    |   TODO: define the needed attributes & develop all the needed methods
    """
    def __init__(self) -> None:
        pass

class IntentPolicyMatching:
    """
    |   IntentPolicyMatching class: it matches and validate an intent with policies
    |   TODO: define the needed attributes & develop all the needed methods
    """
    def __init__(self) -> None:
        pass


# a static example for testing
class PolicyGraph:
    """
    |   PolicyGraph Class
    """
    def __init__(self):
        self.org = None
        self.org_name = ""
        self.hash_table = HashTable(2)
        self.setup_graph()

    def setup_graph(self):
        """
        |    create policy graph
        |
        """
        self.org = Node("Organization1")
        self.hash_table.set_val(self.org, False)
        realm_1 = Node("realm1", parent=self.org)
        self.hash_table.set_val(realm_1, False)
        realm_2 = Node("realm2", parent=self.org)
        self.hash_table.set_val(realm_2, False)
        domain_1 = Node("Domain11", parent=realm_1)
        self.hash_table.set_val(domain_1, False)
        domain_2 = Node("Domain12", parent=realm_1)
        self.hash_table.set_val(domain_2, False)
        domain_3 = Node("Domain13", parent=realm_1)
        self.hash_table.set_val(domain_3, False)

        domain_21 = Node("Domain21", parent=realm_2)
        self.hash_table.set_val(domain_21, False)
        domain_22 = Node("Domain22", parent=realm_2)
        self.hash_table.set_val(domain_22, False)

    def change_state(self, str_name, permission):
        """
        |    change Node state
        |
        |   Args:
        |       str_name(str):
        |       permission(bool):
        """
        for pre, fill, node in RenderTree(self.org):
            if node.name == str_name:
                if permission:
                    while_node = node
                    while not while_node.is_root:
                        self.hash_table.set_val(while_node.parent, True)
                        while_node = while_node.parent

                for pre1, fill1, node1 in RenderTree(node):
                    self.hash_table.set_val(node1, permission)

    def print_output(self):
        """
        |    print result
        |
        |   Returns:
        |       s_node_name(str): result string
        |
        """
        s_node_name = ""
        for pre, fill, node in RenderTree(self.org):
            if not self.hash_table.get_val(node.parent):  # if node.parent bool = False
                continue
            if not self.hash_table.get_val(node):  # if node bool = False
                while_node = node
                s_node_name = "-" + while_node.name + s_node_name[0:]
                while not while_node.is_root:
                    if while_node.parent.is_root:
                        s_node_name = "|" + while_node.parent.name + s_node_name[0:]
                    else:
                        s_node_name = "-" + while_node.parent.name + s_node_name[0:]
                    while_node = while_node.parent
        for pre, fill, node in RenderTree(self.org):
            if self.hash_table.get_val(node):  # if node bool = True
                self.org_name = node.name
                break
        return s_node_name

    def print_outputnew(self):
        """
        |    print result
        |
        |   Returns:
        |       s_node_name(str): result string
        |
        """
        s_node_name = ""
        for pre, fill, node in RenderTree(self.org):
            if not self.hash_table.get_val(node.parent):  # if node.parent bool = False
                continue
            if not self.hash_table.get_val(node):  # if node bool = False
                while_node = node
                if s_node_name == "":
                    s_node_name = while_node.name
                else:
                    s_node_name = s_node_name + " and " + while_node.name

        for pre, fill, node in RenderTree(self.org):
            if self.hash_table.get_val(node):  # if node bool = True
                self.org_name = node.name
                break
        return s_node_name

    def print_graph(self):
        for pre, fill, node in RenderTree(self.org):
            print("%s%s (%s)" % (pre, node.name, self.hash_table.get_val(node)))


class IntentVerification:
    """
    |   IntentVerification Class
    """
    def __init__(self, intent_structure, intent_text, intent_store):
        self.content_list = []
        self.requirements = intent_structure.get_requirements()
        self.options = intent_structure.get_options()
        self.intent_text = intent_text
        self.intent_store = intent_store
        self.option_list = np.empty(shape=[0, 2])

    def check_validation(self):
        """
        |   check intent validity
        |
        |   Returns:
        |       bool: returns if the intent is valid or not
        |
        """
        for requirement in self.requirements:
            if not (self.analyse_text(self.intent_text, requirement)):
                return False
        for obj, val in self.options:
            new_val = self.analyse_text_options(self.intent_text, obj)
            if new_val is None or new_val == val:
                self.option_list = np.append(self.option_list, [[obj, val]], axis=0)
            else:
                self.option_list = np.append(self.option_list, [[obj, new_val]], axis=0)
        return True

    def analyse_text(self, intent, vocabulary_list):
        """
        |   analyse the text through looking into
        |
        |   Returns:
        |       bool: returns if requirements word is found or not
        |
        """
        check = []
        for i in self.intent_store.get_specific_vocab("database", vocabulary_list):
            if i in intent:
                check.append("found")
                self.content_list.append(i)
            else:
                check.append("not found")
        if "found" in check:
            return True
        return False

    def analyse_text_options(self, intent, vocabulary_list):
        """
        |   analyse the intent for new option value
        |
        |   Returns:
        |       value(str): returns new value if exits
        |
        """
        for value in self.intent_store.get_specific_vocab("database", vocabulary_list):
            if value in intent:
                return value


class HashTable:
    """
    |   HashTable Class
    """
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    # Insert values into hash map
    def set_val(self, key, val):

        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    # Return searched value with specific key
    def get_val(self, key):

        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:
            return record_val
        else:
            return "No record found"

    # Remove a value with specific key
    def delete_val(self, key):

        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)
