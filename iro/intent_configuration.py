import json
import os
from datetime import datetime



class IntentConfigurationManager:
    def __init__(self) -> None:
        self.directory_path = './intent_store'
        self.No_of_intents = len(os.listdir(self.directory_path))
        
        
    def add_intent(self, intent_data):
        self.No_of_intents+= 1
        intent_data["ID"] = str(self.No_of_intents)
        current_time = str(datetime.now().replace(microsecond=0))
        intent_data["Created"] = current_time
        with open("./intent_store/intent_"+str(self.No_of_intents)+".json", "w", encoding='utf-8') as f:
            json.dump(intent_data, f, ensure_ascii=False, indent=4)



    def show_intent(self, show_intent_data):
        directory_path = './intent_store'
        No_of_intents = len(os.listdir(directory_path))
        for x in range(1,No_of_intents+1):
            with open("./intent_store/intent_"+str(x)+".json", "r", encoding='utf-8') as f:
                load_intent_data=json.load(f)
                show_intent_data.append(load_intent_data)
            
        return show_intent_data


    def delete_intent(self,empty_data,delete_intentid):
        with open("./intent_store/intent_"+str(delete_intentid)+".json", "w", encoding='utf-8') as f:
            json.dump(empty_data, f, ensure_ascii=False, indent=4)

    