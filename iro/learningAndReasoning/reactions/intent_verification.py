import sys
import os
_cwd = os.getcwd()
sys.path.append(_cwd+ '/learningAndReasoning/reactions')
sys.path.append(_cwd+ '/policies/pmem')
sys.path.append(_cwd+ '/templates/tmp_register')
import json
import ast
from jinja2 import Template
from datetime import datetime
import requests

class IntentVerification:
    def __init__(self) -> None:
        self.status = []
        self.add_intents()
        pass

    def get_intents(self):
        pass

    def get_intent_by_name(self, name):
        pass

    def verify_all_intents(self, event):
        if event["pilot"] == "F2F":
            if event["device_product"] == "PMEM":
                self.verify_pmem_intents(event)
                print()
        
        pass

    def verify_intent(self, intent):
        pass

    def add_intents(self):
        # TODO: add the intents to verification and create status
        self.status.append(0)
        self.status.append(0)

    def verify_pmem_intents(self, event):
        
         
        if "DDOS" in event["event_name"]:
            _attack = "DDoS"
        extensions_list = ast.literal_eval(event["extensions_list"])
        _src_ip = extensions_list["Source.IP"]
        _dst_ip = extensions_list["Destination.IP"]
        _src_port = extensions_list["Src.Port"]
        _dst_port = extensions_list["Dst.Port"]
        _severity = event["severity"]

        pmem_intent_1 = "pmem_DDoS_dst_ip_dst_port.json"
        pmem_intent_2 = "pmem_DDoS_src_ip_None.json"


        try:
            with open(_cwd +"/policies/pmem/"+ pmem_intent_1, "r", encoding='utf-8') as f:
                    load_pmem_intent=json.load(f)
                    if load_pmem_intent["severity"] == "Low":
                        check_severity = True
                    elif load_pmem_intent["severity"] == "Medium":
                        if _severity != "Low":
                            check_severity = True
                    else:
                        if _severity == "High":
                            check_severity = True
                        else:
                            check_severity = False
                    try:

                        if check_severity:
                            self.status[0] += 1
                            #check the needed xml template
                            
                            
                            fname = _cwd+ "/templates/tmp_register/hspl2.xml"
                            
                            structured_data_hspl = {"id":"hspl2",
                                                    "port":_dst_port, 
                                                    "severity":load_pmem_intent["severity"], 
                                                    "hspl_object":[
                                                        {
                                                            "id":"hspl"+str(self.status[0]), 
                                                            "action":load_pmem_intent['action'],
                                                            "object":load_pmem_intent['object']
                                                            }
                                                            ]
                                                            }
                            
                            with open(fname, 'r') as hspl_template:
                                hspl_file = hspl_template.read()

                            html_hspl = Template(hspl_file).render(objects=structured_data_hspl)
                            
                            
                            
                            #check the needed attack info template
                            fnamea = _cwd+ "/templates/tmp_register/attack_id1.txt"
                            with open(fnamea, 'r') as attack_template:
                                attack_file = attack_template.read()
                            structured_data_attacker = {'name':_src_ip,'type':'PORT','id':_dst_port}
                            html_info = Template(attack_file).render(attacker=structured_data_attacker) #render_template(fnamea, attacker=structured_data_attacker)
                            html_info = json.loads(html_info)

                            # save policies
                            _timestamp = datetime.now()
                            url = "https://fishy.xlab.si/tar/api/policies"
                            data = {"source": "IRO", "status": "both", "timestamp": str(_timestamp), "HSPL": html_hspl, "attack_info": html_info}

                            headers = {'Content-type': 'application/json'}
                            
                            r = requests.post(url, data=json.dumps(data), headers=headers)
                            #print(r.status_code)
                            self.create_notification(event)
                    except:
                        pass
        except:
            pass

        try:        
            with open(_cwd +"/policies/pmem/"+ pmem_intent_2, "r", encoding='utf-8') as f:
                    load_pmem_intent=json.load(f)
                    #print(load_pmem_intent)
                    if load_pmem_intent["severity"] == "Low":
                        check_severity = True
                    elif load_pmem_intent["severity"] == "Medium":
                        if _severity != "Low":
                            check_severity = True
                    else:
                        if _severity == "High":
                            check_severity = True
                        else:
                            check_severity = False
                    try:

                        if check_severity:
                            #check the needed xml template
                            self.status[1] += 1
                            
                            
                            fname = _cwd+ "/templates/tmp_register/hspl3.xml"
                            structured_data_hspl = {
                                'id':'hspl3',
                                'ip':_src_ip, 
                                'severity':load_pmem_intent["severity"],
                                'hspl_object':[
                                    {
                                        'id':'hspl'+str(self.status[1]),
                                        'action':load_pmem_intent['action'],
                                        'object':load_pmem_intent['object']
                                        }
                                        ]
                                        }
                            with open(fname, 'r') as hspl_template:
                                hspl_file = hspl_template.read()

                            html_hspl = Template(hspl_file).render(objects=structured_data_hspl)
                            
                            
                            #check the needed attack info template
                            fnamea = _cwd+ "/templates/tmp_register/attack_id1.txt"
                            with open(fnamea, 'r') as attack_template:
                                attack_file = attack_template.read()
                            structured_data_attacker = {'name':_src_ip,'type':'IP','id':_src_ip}
                            html_info = Template(attack_file).render(attacker=structured_data_attacker) #render_template(fnamea, attacker=structured_data_attacker)
                            html_info = json.loads(html_info)

                            
                            
                            # save policies
                            _timestamp = datetime.now()
                            url = "https://fishy.xlab.si/tar/api/policies"
                            data = {"source": "IRO", "status": "both", "timestamp": str(_timestamp), "HSPL": html_hspl, "attack_info": html_info}
                            headers = {'Content-type': 'application/json'}
                            r = requests.post(url, data=json.dumps(data), headers=headers)
                            #print(r.status_code)
                            self.create_notification(event)


                    except:
                        pass
        
        except:
            pass
        
        pass

    def create_notification(self, event):
        # create notif info
        data = { 
                "Name": "Intent verified:" + event["event_name"], #_event_name,
                "Source": "PMEM",
                "Attributes": event["device_version"],
                "Value": event["extensions_list"],
                "ID": event["id"],
                "pilot": event["pilot"],
                "Time": event["updated_at"],
                "Status": "Open"
                }
        
        fpath = _cwd+ "/notification_store/reports/"+ event["id"]+".json"
        with open(fpath, 'w') as f:
            notif = json.dumps(data)
            f.write(notif)

