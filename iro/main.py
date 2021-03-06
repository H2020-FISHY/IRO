"""
|
|   file:       main.py
|
|   brief:
|   author:    Mounir Bensalem
|   email:     mounir.bensalem@tu-bs.de
|   copyright:  © IDA - All rights reserved
"""
#from builtins import print
import os
import sys
from flask import Flask, render_template, request,  url_for, redirect, jsonify
from jinja2 import Environment, FileSystemLoader
from flask_classful import FlaskView, route
from intent_manager import IntentManager
from learningAndReasoning.notifications.notification_manager import NotificationManager
import json
import ast
import requests
from requests import Session


PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'IRO'
tim_config = None
try:
    tim_cfg_content = {
            "frontend" : {
                "url" : os.environ["TIM_URL"]
            },
            "tar": {
                "url" : os.environ["TIM_URL"]
            }
        }
    tim_config = tim_cfg_content #json.dumps(tim_cfg_content)
except:
    
    
    print("TIM_HOST or TIM_PORT environment variable does not exist, setting None as TIM config...")
    tim_cfg_content = None

class UserInterface(FlaskView):
    """
    |   UserInterface Class
    """
    def __init__(self):
        self.session = Session()
        self.notification_manager = NotificationManager( self.session, tim_config)
        
        
        self.intent_manager = IntentManager(notif=self.notification_manager)

    def index(self):
        notifs = self.notification_manager.get_notifications(self.session, tim_config)
        msg = self.notification_manager.get_instructions()
        my_form, my_form_script,  HTMLtemplate, JStemplate = self.notification_manager.get_form("")

        return render_template('index.html',form_script=my_form_script, forms=my_form, message=msg, notifications=notifs)

    def post(self):
        msg = ''
        my_form = None
        my_form_script = None
        list_options = None
        notifs = None
        if request.method == 'POST':
            
            if  'intentText' in request.form:
                intent_text = request.form.get('intentText')
                msg, my_form, my_form_script,HTMLtemplate,JStemplate, notifs = self.intent_manager.reading_command(intent_text)
                if  isinstance(msg, list):
                    list_options = msg.copy()
                    msg = None

                if msg == "reports":
                    return redirect(url_for('UserInterface:alerts'))
            if 'threat_d_form' in request.form:
                threat_data =  request.form
                
                #return jsonify(request.form)
                msg = self.intent_manager.create_hspl_from_intent(threat_data,'wallet_id_attack_detection')                
                #msg = self.notification_manager.get_instructions_after_form()
                return render_template('index.html', formoutput=threat_data, message=msg)

        return render_template('index.html', form_script=my_form_script, forms=my_form, message=msg, htmltemplate=HTMLtemplate, jstemplate=JStemplate,notifications=notifs, message_list=list_options)

    @route("/alerts", methods=['GET', 'POST'])
    def alerts(self):
        if request.method == 'POST':
            # do stuff when the form is submitted

            # redirect to end the POST handling
            # the redirect can be to the same route or somewhere else
            return redirect(url_for('UserInterface:index'))

        # show reports from TIM
        data = None
        
        try:
            #r = self.session.get(f'http://{tim_config["tar"]["ip"]}:{tim_config["tar"]["port"]}/api/reports')
            #r = requests.get('https://fishy.xlab.si/tar/api/reports')
            
            r = requests.get(tim_config["tar"]["url"])
            print(r)
            r = r.content
            r = r.decode("UTF-8")
            r = ast.literal_eval(r)
            data = []
            print(len(r))
            for el in r:
                try:
                    alert = json.loads(el['data'])
                
                    if alert != "testAPI":
                        alert = alert["attachments"][0]   
                    el['data'] = alert
                    data.append(el)
                except:
                    pass
        except:
            with open("./tim/example_report.json", "r") as f:
                #data = json.load(f)
                pass
            pass



        return render_template('Alerts.html', data=data)

    @route("/api/policies/all", methods=["GET"])
    def api(self):
        msg = self.intent_manager.intent_store.get_all_generated_policies()
        return jsonify(msg)



if __name__ == "__main__":
    UserInterface.register(app, route_base='/')
    certs_present = [os.path.exists('/crt/cert.pem'),
                    os.path.exists('/crt/key.pem')]
    print("Detected [certificate, private key]: ", certs_present)
    if all(certs_present):
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('/crt/cert.pem', '/crt/key.pem'))
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
