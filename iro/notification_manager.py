import ast
import json
import requests
class NotificationManager:
    """
    |   NotificationManager Class
    """
    def __init__(self, session, tim_config):
        """
        |    Create Intent Manager
        | 
        """
        self.notifs = self.get_notifications(session, tim_config)
    
    def get_notifications(self, session, tim_config):
        
        notifs = []
            
        # add reports from TIM
        
        try:
            #r = session.get(f'http://{tim_config["tar"]["ip"]}:{tim_config["tar"]["port"]}/api/reports')
            #r = self.session.get('https://fishy.xlab.si/tar/api/reports')
            #r = requests.get('https://fishy.xlab.si/tar/api/reports')
            r = requests.get(tim_config["tar"]["url"])
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
        return notifs

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

        intents = [
            "wallet_id_attack_detection",
            ".. more intents will be added .."
        ]
        return intents

    def get_form(self, intent_name):

        form, script = None, None
        WALLET_IDS = [ 
            0xb5707bdcd820694303496b74d56895902a009943,
            0x35a69278fea8d80d9490b64cd52915575149a898,
            0x99245a929029d8b5f6c12b7d80158f71fac19198
            ]
        wallet_detection_form =  [ {
                   'subject': [{'name':'Malicious_User1', 'val':'0xb5707bdcd820694303496b74d56895902a009943'},
        {'name':'Malicious_User2', 'val':'0x35a69278fea8d80d9490b64cd52915575149a898'},
        {'name':'Malicious_User3', 'val':'0x99245a929029d8b5f6c12b7d80158f71fac19198'}],
                   'time': [{'name':'Second', 'val':'second'},
                   {'name':'Minute', 'val':'minute'},
                   {'name':'Hour', 'val':'hour'},
                   {'name':'Day', 'val':'day'}],
                   'action':[ 'notify', 'no_authorise_access'], 
                   'object_notif':[ 'supply_chain_operator', 'island_operator'],
                   'object_access':[ 'Web App', 'internet_traffic', 'intranet_traffic', 'all_traffic']
     
                   }
    ]
        wallet_detection_script = [{
            'action':[ 'notify', 'no_authorise_access'], 
            'object':[ 'internet_traffic', 'intranet_traffic', 'all_traffic','supply_chain_operator', 'island_operator'],
            'object_notif':[ 'supply_chain_operator', 'island_operator'],
            'object_access':[ 'Web App', 'internet_traffic', 'intranet_traffic', 'all_traffic']
     
            }
        ]

        if intent_name == "wallet_detection":
            return wallet_detection_form, wallet_detection_script
            
        return form, script