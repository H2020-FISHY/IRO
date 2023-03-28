import json
import os
#import pika
import sys

class NotificationConfigurationManager:
    def __init__(self) -> None:

        self.directory_path = './notification_store/reports'
        self.No_of_intents = len(os.listdir(self.directory_path))
        root_dir = os.listdir(self.directory_path)
        self.file_set = set()
        self.reset_notifications()
        

    def show_notification(self, show_notification_data):
        self.reset_notifications()
        for x in self.file_set: #range(1,self.No_of_intents+1):
            with open("./notification_store/reports/"+str(x), "r", encoding='utf-8') as f:
                load_notification_data=json.load(f)
                print(x)
                show_notification_data.append(load_notification_data)
            
        return show_notification_data
    # Notifications have possibly following status:
    # 1. Open
    # 2. Seen
    # 3. Deleted
    # 4. Created - This means chosen notification is created as intent.
    def notification_status(self, single_notification_status, single_notification_id):
        with open("./notification_store/reports/"+str(single_notification_id)+".json", "r", encoding='utf-8') as f:
            load_notification_data=json.load(f) 
        
        load_notification_data["Status"] = single_notification_status
        
        with open("./notification_store/reports/"+str(single_notification_id)+".json", "w", encoding='utf-8') as f:
            json.dump(load_notification_data, f, ensure_ascii=False, indent=4)

    def reset_notifications(self):
        self.file_set = set()
        for dir_, _, files in os.walk(self.directory_path):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, self.directory_path)
                rel_file = os.path.join(rel_dir, file_name)
                self.file_set.add(rel_file)
