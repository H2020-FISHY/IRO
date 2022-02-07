

import string


class ListOfActions:
    """
    |   ListOfActions Class
    """
    def __init__(self) -> None:
        self.list_of_actions = ["no_authorise_access","notify"]

    def add_actions(self, actions):
        if isinstance(actions, string):
            self.list_of_actions.append(actions)
        elif isinstance(actions, list):
            self.list_of_actions.extend(actions)
        else:
            raise TypeError("E: actions must be string or list of strings!")
    
    def get_actions(self):
        return self.list_of_actions
    
    def is_an_action(self, action):
        if action in self.list_of_actions:
            return True
        else:
            return False

class Action:
    """
    |   Action Class
    """
    def __init__(self, action, list_of_actions=None) -> None:
        if list_of_actions is None:
            self.list_of_actions = ListOfActions()
        if isinstance(list_of_actions, ListOfActions):
            if list_of_actions.is_an_action(action):
                self.action = action
            else:
                raise TypeError("plz give a correct action!")
        else:
            raise TypeError("plz give a correct list_of_actions!")


class EnablingConditions:
    """
    |   EnablingConditions Class
    """
    def __init__(self) -> None:
        self.threshold = []

    def add_condition(self, threshold):
        self.threshold.append(threshold)

class Threshold:
    """
    |   Threshold Class
    """
    def __init__(self, subject=None, value=0, period=0, time= None) -> None:
        if subject is None:
            subject = Subject()
        if time is None:
            time = TimeStructure()

        self.subject: Subject = subject
        self.value = value
        self.period = period
        self.time: TimeStructure = time

class TimeStructure:
    """
    |   TimeStructure Class
    """
    def __init__(self, second=0, minute=0, hour=0, day=0) -> None:
        self.second: int = second
        self.minute: int = minute
        self.hour: int = hour
        self.day: int = day
    
class ListOfObjects:
    """
    |   ListOfObjects Class
    """
    def __init__(self) -> None:
        self.list_of_objects = ["internet_traffic","intranet_traffic"]

    def add_objects(self, objects):
        if isinstance(objects, string):
            self.list_of_objects.append(objects)
        elif isinstance(objects, list):
            self.list_of_objects.extend(objects)
        else:
            raise TypeError("E: objects must be string or list of strings!")
    
    def get_objects(self):
        return self.list_of_objects
    
    def is_an_object(self, object):
        if object in self.list_of_objects:
            return True
        else:
            return False

class Object:
    """
    |   Object Class
    """
    def __init__(self, object, list_of_objects=None) -> None:
        if list_of_objects is None:
            self.list_of_objects = ListOfObjects()
        if isinstance(list_of_objects, ListOfObjects):
            if list_of_objects.is_an_object(object):
                self.object = object
            else:
                raise TypeError("plz give a correct object!")
        else:
            raise TypeError("plz give a correct list_of_objects!")


class Subject:
    """
    |   Subject Class
    """
    def __init__(self, subject_type=None, value=None) -> None:
        if subject_type is None:
            raise TypeError("plz give a correct subject_type")
        elif value is None:
            raise TypeError("plz give a value!")
        else:
            self.subject_type: SubjectType = subject_type
            self.value: string = value


class ListOfSubjectTypes:
    """
    |   ListOfSubjectTypes Class
    """
    def __init__(self) -> None:
        self.list_of_subject_types = ['ip_address', 'username', 'wallet_id', 'did']
    
    def add_subject_type(self, subject_type):
        self.list_of_subject_types.append(subject_type)

    def is_in_subject_types(self, subject_type):
        if subject_type in self.list_of_subject_types:
            return True
        else:
            return False


class SubjectType(ListOfSubjectTypes):
    """
    |   SubjectType Class
    """
    def __init__(self, stype) -> None:
        super().__init__()
        if self.is_in_subject_types(stype):
            self.type = stype
        else:
            raise TypeError("plz give a correct subject type")
    

class HSPLList:
    """
    |   HSPLList Class
    | TODO: complete the definition and methods
    """
    def __init__(self) -> None:
        self.hspl_list = []

    def add_hspl(self, hsplreaction):
        if isinstance(hsplreaction, HSPLReaction):
            self.hspl_list.append(hsplreaction)

class HSPLReaction:
    """
    |   HSPLReaction Class
    | TODO: complete the definition and methods
    """
    def __init__(self) -> None:
        self.enabling_conditions = None
        self.hspl = []
    
    def add_hspl(self, hspl):
        if isinstance(hspl, HSLP):
            self.hspl.append(hspl)

class HSLP:
    """
    |   HSLP Class
    | TODO: complete the definition and methods
    """
    def __init__(self, subject=None, action=None, object=None) -> None:
        self.subject: Subject = subject
        self.action: Action = action
        self.object: Object = object
 

# print("works")
# print(Subject(subject_type=SubjectType("ip_address"),value="None").subject_type)