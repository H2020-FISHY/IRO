"""
|
|   file:       main.py
|
|   brief:
|   author:    
|   email:      
|   copyright:  © IDA - All rights reserved
"""
#from builtins import print
import os
from flask import Flask, render_template, request,  url_for, redirect, jsonify
from jinja2 import Environment, FileSystemLoader
from flask_classful import FlaskView, route
from intent_manager import IntentManager
from notification_manager import NotificationManager
import json
import ast
from requests import Session

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IRO'

try:
    tim_cfg_content = {
            "frontend" : {
                "ip" : os.environ["TIM_HOST"],
                "port" : os.environ["TIM_PORT"]
            },
            "tar": {
                "ip": os.environ["TIM_HOST"],
                "port": os.environ["TIM_PORT"]
            }
        }
    tim_config = json.dumps(tim_cfg_content)
except:
    print("TIM_HOST or TIM_PORT environment variable does not exist, setting None as TIM config...")
    tim_cfg_content = None

class UserInterface(FlaskView):
    """
    |   UserInterface Class
    """
    def __init__(self):
        self.session = Session()
        self.notification_manager = NotificationManager(self.session, tim_config)
        
        self.policies_filename = "export.txt"
        
        self.intent_manager = IntentManager(notif=self.notification_manager)

    def index(self):
        notifs = self.notification_manager.get_notifications(self.session, tim_config)
        msg = self.notification_manager.get_instructions()
        my_form, my_form_script = self.notification_manager.get_form("")

        return render_template('index.html',form_script=my_form_script, forms=my_form, message=msg, notifications=notifs)

    def post(self):
        msg = ''
        my_form = None
        my_form_script = None
        notifs = None
        if request.method == 'POST':
            
            if  'intentText' in request.form:
                intent_text = request.form.get('intentText')
                msg, my_form, my_form_script, notifs = self.intent_manager.reading_command(intent_text)
                if msg == "reports":
                    return redirect(url_for('UserInterface:alerts'))
            if 'threat_d_form' in request.form:
                threat_data =  request.form
                
                #return jsonify(request.form)
                msg = self.intent_manager.create_hspl_from_intent(threat_data,'wallet_id_attack_detection')                
                #msg = self.notification_manager.get_instructions_after_form()
                return render_template('index.html', formoutput=threat_data, message=msg)

        return render_template('index.html', form_script=my_form_script, forms=my_form, message=msg, notifications=notifs)

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
            r = self.session.get(f'http://{tim_config["tar"]["ip"]}:{tim_config["tar"]["port"]}/api/reports')
            r = r.content
            r = r.decode("UTF-8")
            r = ast.literal_eval(r)
            data = []
            for el in r:
                alert = json.loads(el['data'])
                alert = alert['attachments'][0]
                el['data'] = alert
                data.append(el)
            #print(data)
        except:
            with open("./tim/example_report.json", "r") as f:
                data = json.load(f)
            pass



        return render_template('Alerts.html', data=data)

    @route("/addIntent", methods=["POST"])
    def addintent(self):
        msg = ''
        return ""
    
    # TODO: update the interface after developing the policy builder classes
    @route("/policies", methods=["GET"])
    def export_policies(self):
        with open("./outputfiles/"+self.policies_filename, "r") as f:
            policies = f.read()
        return render_template('policies.html', policies=policies)

if __name__ == "__main__":
    UserInterface.register(app, route_base='/')
    certs_present = [os.path.exists(/crt/cert.pem),
                    os.path.exists(/crt/key.pem)]
    if all(certs_present):
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('/crt/cert.pem', '/crt/key.pem'))
    else
        app.run(host='0.0.0.0', port=5000, debug=True)
