import ast
import json
import requests
import os
import sys
_cwd = os.getcwd()
sys.path.append(_cwd+ '/learningAndReasoning/notifications')
sys.path.append(_cwd+ '/knowledgeBase/policyStore')
sys.path.append(_cwd+ '/knowledgeBase/intentStore')
import policyStoreManager as psm
import intentStoreManager as ism


class NotificationManager:
    """
    |   NotificationManager Class
    """
    def __init__(self, session, tim_config):
        """
        |    Create Notification Manager
        | 
        """
        self.policyStore = psm.PolicyStoreManager()
        self.intentStore = ism.IntentStoreManager()
        self.notifs = self.get_notifications(session,tim_config)
        self.last_event_id_read = None
        self.last_event_id_treated = None
    
    def get_all_reports(self, _pilot=None):
        # show reports from TIM
        data = None
        
        try:
            #r = requests.get('https://fishy.xlab.si/tar/api/reports')
            r = requests.get(os.environ["TIM_URL"])  # 'https://fishy.xlab.si/tar/api/reports/v2')
            #r = requests.get(tim_config["tar"]["url"])
            r = r.content
            r = r.decode("UTF-8")
            r = ast.literal_eval(r)
            data = []
            pilot = None
            #print(len(r))
            #print(r)
            #print('/////////////////////////////////')
            for el in r:
                element = el.copy()

                try:
                    #_id = element['id']
                    #_device_product = element['device_product']
                    #_device_version = element['device_version']
                    #_event_name = element['event_name']
                    #_device_event_class_id = element['device_event_class_id']
                    #_severity = element['severity']
                    _extensions_list = element['extensions_list']
                    _pilot_ = element['pilot']

                    if _pilot == _pilot_:
                        


                        _text = "" #"*** pilot: "+_pilot_+" *** [TO BE REMOVED]\n"
                        try:

                            for _key, data_info in ast.literal_eval(_extensions_list).items():
                                try:
                                    if "," in str(data_info):
                                        tmp_val =  ",\n      ".join(str(data_info).split(","))
                                        _text += "*  "+_key + ": " + tmp_val + "\n"
                                    elif ";" in str(data_info):
                                        tmp_val =  ";\n      ".join(str(data_info).split(";"))
                                        _text += "*  "+_key + ": " + tmp_val + "\n"
                                    else:
                                        _text += "*  "+_key + ": " + str(data_info) + "\n"
                                except:
                                    pass
                        except:
                            pass

                        element['text'] = _text
                        data.append(element)
                    else:
                        pass

                except:
                    try:
                        alert = json.loads(el['data'])
                    except:
                        alert = el['data']
                        pass
                    if alert != 'test':

                        if el['source'] == "SACM":
                            try:
                                _text = ""
                                for _key, data_info in ast.literal_eval(el['data']).items():
                                    try:
                                        if "," in str(data_info):
                                            tmp_val =  ",\n".join(str(data_info).split(","))
                                            _text += _key + ": " + tmp_val + "\n"
                                        else:
                                            _text += _key + ": " + str(data_info) + "\n"
                                    except:
                                        pass
                                alert = {"id":el['id'], "sc_id":str(ast.literal_eval(el['data'])['AssessmentResultID']), "title": "Source: SACM" , "text": _text , "fields":[{"title": "Sender", "value":ast.literal_eval(el['data'])['Sender']},{"title": "Outcome", "value":ast.literal_eval(el['data'])['Outcome']}]} # "Source: SACM\n pilot: "+ ast.literal_eval(el['data'])['pilot']+ "\ntimestamp: "+ast.literal_eval(el['data'])['@timestamp']+"\n AssessmentResultID: "+ ast.literal_eval(el['data'])['AssessmentResultID'],
                                    
                                #alert = {"title": "test", "text": "SACM", "fields":[{"title": "test", "value":"test"},{"title": "test", "value":"test"}]}
                                element['data'] = alert
                            except:
                                raise Exception("E: Error in reading SACM data")

                        
                        else:
                            alert = {"id":"test", "title": "test", "text": "test", "fields":[{"title": "test", "value":"test"},{"title": "test", "value":"test"}]}
                    else:
                        alert = {"id":"test","title": "test", "text": "test", "fields":[{"title": "test", "value":"test"},{"title": "test", "value":"test"}]}
                    #el['data'] = alert
                    element['data'] = alert
                    data.append(element)
                
        except:
            with open("./tim/example_report.json", "r") as f:
                #data = json.load(f)
                pass
            pass
        return data
        
    
    def get_notifications(self, session, tim_config):
        
        notifs = []
            
        # add reports from TIM
        
        try:
            #r = session.get(f'http://{tim_config["tar"]["ip"]}:{tim_config["tar"]["port"]}/api/reports')
            #r = self.session.get('https://fishy.xlab.si/tar/api/reports')
            #r = requests.get('https://fishy.xlab.si/tar/api/reports')
            r = requests.get( os.environ["TIM_URL"]) #tim_config["tar"]["url"])
            r = r.content
            r = r.decode("UTF-8")
            r = ast.literal_eval(r)
            
            for el in r:
                try:
                    alert = json.loads(el['data'])
                    if alert != "testAPI":
                        alert = alert["attachments"][0]   
                    el['data'] = alert
                    notifs.append(el)
                except:
                    pass
        except:
            with open("./tim/example_report.json", "r") as f:
                #notifs = json.load(f)
                pass
            pass
        self.notifs = notifs
        # get only latest and not treated
        self.get_latest_event_id_read()
        self.get_latest_event_id_treated()
        self.push_events_to_policyStore()
        return notifs

    def get_latest_event_id_read(self):
        return 0

    def get_latest_event_id_treated(self):
        return 0
    
    def push_events_to_policyStore(self):
        policy_config = self.policyStore.get_policyStore_config()
        if self.notifs != []:
            for el in self.notifs:
                pass

            pass

        return 0

    def get_instructions(self):

        return (
            "usage : iro <command> <args> \n"
            "\n"
            'add "intent"        read new intents/rules\n'
            "intents             show the list of intents\n"
            "status              show intent register status\n"
            "push                solve conflict and send to\n"
            "                    controller\n"
            "reset               reset intent register\n"
            "\n"
            "usage : reports  <args>\n"
            "\n"
            "                    show reports summary\n"
            "'tool name'         show reports from a tool\n"
        )
    
    def get_instructions_after_form(self):

        return (
            "Submitted successfully!!\n"
            
            'Use:  iro add "intent"   to add more intents\n'
            'Use:  iro status         to check intents\n'
            'Use:  iro push           to send to controller\n'
            'write anything to see more instructions\n'

        )
    
    def get_intents(self):
        intents = self.intentStore.get_all_intents()
        #[
        #    "wallet_id_attack_detection",
        #    ".. more intents will be added .."
        #]
        return intents

    def get_form(self, intent_json):
        form, script, HTMLtemplate, JStemplate = None, None, "None", None
        try:
            


            #intent_name = intent_json["intentname"]
            intent_id = intent_json["id"]
            

            if intent_json['use_template']:
                HTMLtemplate = intent_json['HTMLtemplate']
                JStemplate = intent_json['JStemplate']
            else:
                # get/generate html and js templates from attributes
                pass
            


            form, script = self.policyStore.getPolicyFormAndScript(intent_id)
            

        except:
            #HTMLtemplate = "except"
            pass
        
        return form, script, HTMLtemplate, JStemplate
