


class NotificationManager:
    """
    |   NotificationManager Class
    """
    def __init__(self):
        """
        |    Create Intent Manager
        | 
        """
        self.notifs = self.get_notifications()
    
    def get_notifications(self):
        return ""

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
            
            'Use:  iro add "intent"   to add more intents\n '
            'Use:  iro status         to check intents\n'
            'Use:  iro push           to send to controller\n'
            'write anything to see more instructions\n'

        )
    
    def get_intents(self):
        intents = (
            "- wallet_id_attack_detection\n"
            ".. more intents will be added .."
        )
        return intents

    def get_form(self, intent_name):
        form, script = None, None
        wallet_detection_form =  [ {
                   'subject': [{'name':'Wallet ID 0', 'val':'Wallet ID 0'},
        {'name':'Wallet ID 1', 'val':'Wallet ID 1'},
        {'name':'Wallet ID 2', 'val':'Wallet ID 2'}],
                   'time': [{'name':'Second', 'val':'second'},
                   {'name':'Minute', 'val':'minute'},
                   {'name':'Hour', 'val':'hour'},
                   {'name':'Day', 'val':'day'}],
                   'action':[ 'notify', 'no_authorise_access'], 
                   'object_notif':[ 'supply_chain_operator', 'island_operator'],
                   'object_access':[ 'internet_traffic', 'intranet_traffic', 'all_traffic']
     
                   }
    ]
        wallet_detection_script = [{
            'action':[ 'notify', 'no_authorise_access'], 
            'object':[ 'internet_traffic', 'intranet_traffic', 'all_traffic','supply_chain_operator', 'island_operator'],
            'object_notif':[ 'supply_chain_operator', 'island_operator'],
            'object_access':[ 'internet_traffic', 'intranet_traffic', 'all_traffic']
     
            }
        ]

        if intent_name == "wallet_detection":
            return wallet_detection_form, wallet_detection_script
            
        return form, script