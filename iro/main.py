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
import time
from datetime import datetime
from flask import Flask, g, render_template, request,  url_for, redirect, jsonify
from jinja2 import Environment, FileSystemLoader
from flask_classful import FlaskView, route
from intent_manager import IntentManager
#from notification_manager import NotificationManager
from learningAndReasoning.notifications.notification_manager import NotificationManager
from intent_configuration import IntentConfigurationManager as icm
from notification_configuration import NotificationConfigurationManager as ncm
import CR_rabbit_consumer as crc
import SC_rabbit_consumer as scc

import json
import ast
import requests
#from flask_oidc import OpenIDConnect
from requests import Session
from threading import Thread
import jwt

import policies.remediation.api as rem


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
                "ip" : os.environ["TIM_HOST"],
                "port" : os.environ["TIM_PORT"],
                "url" : os.environ["TIM_URL"]
            },
            "tar": {
                "ip": os.environ["TIM_HOST"],
                "port": os.environ["TIM_PORT"],
                "url" : os.environ["TIM_URL"]
            }
        }
    tim_config = tim_cfg_content #json.dumps(tim_cfg_content)
except:
    
    
    print("TIM_HOST or TIM_PORT environment variable does not exist, setting None as TIM config...")
    tim_cfg_content = None

# Configuring Keyclock
#app.config.update({
#        'SECRET_KEY': 'TESTING-ANURAG',
#        'TESTING': True,
#        'DEBUG': True,
#        'OIDC_CLIENT_SECRETS': 'client_secrets.json',
#        'OIDC_OPENID_REALM': 'fishy-realm',
#        'OIDC_INTROSPECTION_AUTH_METHOD': 'bearer',
#        'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
#        'OIDC_TOKEN_TYPE_HINT': 'access_token',
#        'OIDC-SCOPES': ['openid']
#    })
#oidc = OpenIDConnect(app)

# Central repository RabbitMQ parameters CR_QUEUE_NAME  CR_KEY


try:
    CRqueueName = os.environ["CR_QUEUE_NAME"]
    CRkey = os.environ["CR_KEY"]
    notification_consumer_config =  { 'host': os.environ["RABBIT_NOTIF_HOST"], 'port': os.environ["RABBIT_NOTIF_PORT"], 'exchange' : os.environ["RABBIT_NOTIF_EXCHANGE"], 'login':os.environ["RABBIT_NOTIF_LOGIN"], 'password':os.environ["RABBIT_NOTIF_PASS"]} 
except:
    CRqueueName = "IROQueue"
    CRkey = "reports.#"
    notification_consumer_config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'tasks', 'login':'tubs', 'password':'sbut'}

# Smart Contracts RabbitMQ parameters
try:
    SCqueueName = os.environ["SC_QUEUE_NAME"]
    SCkey = os.environ["SC_KEY"]
    SCnotification_consumer_config =  { 'host': os.environ["RABBIT_NOTIF_HOST"], 'port': os.environ["RABBIT_NOTIF_PORT"], 'exchange' : os.environ["RABBIT_SC_EXCHANGE"], 'login':os.environ["RABBIT_NOTIF_LOGIN"], 'password':os.environ["RABBIT_NOTIF_PASS"]} 
except:
    SCqueueName = 'SCQueue'
    SCkey = 'sc.validation'
    SCnotification_consumer_config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'sc-results', 'login':'tubs', 'password':'sbut'}

class UserInterface(FlaskView):
    """
    |   UserInterface Class
    """
    def __init__(self):
        self.session = Session()
        self.notification_manager = NotificationManager( self.session, tim_config)
        
        
        self.intent_manager = IntentManager(notif=self.notification_manager)
        self.intent_conf_manager = icm()
        self.notification_conf_manager = ncm()
        #try:
        self.oicd_url = os.environ["OICD_URL"] 
        #except:
        #    self.oicd_url = "https://fishy-idm.dsi.uminho.pt/auth/realms/fishy-realm/protocol/openid-connect/userinfo"
        self.oicd_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        self.test_allowed = True
        self.login_session = ""
        self.error_message = ""
        self.public_key = """-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl0DdHKvVtT1ONng1dOHXbgfnryrtOxJAsrrOwrnqkVELDresRh4VNJPX7wdbgXFjn/THqTWErG3k7SFoDHkcT3vsS66yjAPBNLQpQmphS34hxUzRQo5hON70t4+UY3HdZ9ejk5YmiyMKvoD9XoEISYoFnrPWQBLdNmTIKfW9TJxDVXzazwhc+HajT/ruSsluOaDja/MidMk1sQ8ILMOPLxdC/oInD90XpPRj5LkzITBPJYeP9IzpzzaNo5P8kJKYIwNSoIPzMtPhEBz4oiBtE3XTsQ+oxj+5mxb1AebHIzQyf29f8QXxHoLwy/dQj9WODNnL6elRkOxD9tQrQz/kAQIDAQAB\n-----END PUBLIC KEY-----"""


        
        '''

        self.session = Session()
        self.notification_manager = NotificationManager(self.session, tim_config)
        
        self.policies_filename = "export.txt"
        
        self.intent_manager = IntentManager(notif=self.notification_manager)

        self.intent_conf_manager = icm()
        self.notification_conf_manager = ncm()
        '''

    def index(self):
        try:
            try:
                self.error_message = "reading session token ..."
                print(self.error_message)
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    self.error_message = "keyclock last token file does not exist!"
                    return render_template('404.html',error="MISSING TOKEN: " + self.error_message) 
            #payload='access_token=' + self.login_session

            self.error_message = "requesting user info ..."
            payload = {
                'access_token': self.login_session,
                }
            #response = requests.post(self.oicd_url,
            #                         data=payload,
            #                         verify=False,
            #                         )
            
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False,)
            
            
            
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json #json.loads(response.text)
                _pilot = user_info['pilot']
                notifs = self.notification_manager.get_notifications(self.session, tim_config)
                msg = self.notification_manager.get_instructions()
                my_form, my_form_script,  HTMLtemplate, JStemplate = self.notification_manager.get_form("")
                show_notification_data = []
                self.notification_conf_manager.show_notification(show_notification_data, _pilot)
                return render_template('index.html',form_script=my_form_script, forms=my_form, message=msg, notifications=notifs, show_notification_data=show_notification_data,user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED: " )#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN: " + self.error_message) #'MISSING TOKEN'
    def post(self):
        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session 
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload,verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                msg = ''
                my_form = None
                my_form_script = None
                list_options = None
                notifs = None
                
                if request.method == 'POST':
                    #raise Exception("I am not reading the content")
                    if  'intentText' in request.form:              
                        intent_text = request.form.get('intentText')
                        msg, my_form, my_form_script, notifs = self.intent_manager.reading_command(intent_text)
                        
                        if  isinstance(msg, list):
                            list_options = msg.copy()
                            msg = None

                        if msg == "reports":
                            return redirect(url_for('UserInterface:alerts'))
                        if msg == "hello":
                            return redirect(url_for('UserInterface:index'))
                        if msg== "EDC":
                            return redirect(url_for('UserInterface:remediation'))
                    if 'threat_d_form' in request.form:
                        threat_data =  request.form
                        
                        #return jsonify(request.form)
                        msg = self.intent_manager.create_hspl_from_intent(threat_data,'wallet_id_attack_detection')                
                        #msg = self.notification_manager.get_instructions_after_form()
                        return render_template('index.html', formoutput=threat_data, message=msg, user_info=user_info)
                    if 'pmem_config_form' in request.form:
                        threat_data =  request.form
                        
                        #return jsonify(request.form)
                        msg = self.intent_manager.create_policy_from_intent(threat_data,'pmem_config_form')                
                        #msg = self.notification_manager.get_instructions_after_form()
                        return render_template('index.html', formoutput=threat_data, message=msg, user_info=user_info)

                return render_template('index.html', form_script=my_form_script, forms=my_form, message=msg, notifications=notifs, message_list=list_options, user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'

    @route("/alerts/", methods=['GET', 'POST'])
    def alerts(self):
        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                show_notification_data=[]
                self.notification_conf_manager.show_notification(show_notification_data,  _pilot)

                # Get all reports
                data = self.notification_manager.get_all_reports(_pilot=_pilot)
                
                sc_path = "/iro/notification_store/smart_contracts/verified_sc.json"
                try:
                    with open(sc_path) as sc_file:
                        json_decoded = json.load(sc_file)                         
                    
                    smart_contracts = json_decoded#.keys()
                except:
                    smart_contracts = []


                return render_template('tables.html', data=data, smart_contracts=smart_contracts, show_notification_data=show_notification_data, user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'


    @route("/inputintents", methods=['GET', 'POST'])
    def inputintents(self):
        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session 
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                msg = ''
                my_form = None
                my_form_script = None
                list_options = None
                notifs = None
                HTMLtemplate = None
                JStemplate = None

                if request.method == 'POST': 
                    if  'readIntentText' in request.form:
                        intent_text = request.form['readIntentText']
                        msg, my_form, my_form_script,HTMLtemplate,JStemplate, notifs = self.intent_manager.reading_command(intent_text)
                        #intent_text = request.form['readIntentText']
                        #msg, my_form, my_form_script, notifs = self.intent_manager.reading_command(intent_text)
                        #msg ="test"
                        if  isinstance(msg, list):
                            list_options = msg.copy()
                            msg = None
                        return jsonify({'readIntentText': msg, 'my_form': my_form, 'my_form_script':my_form_script, 'HTMLtemplate':HTMLtemplate, 'JStemplate':JStemplate }) 
                    

                return render_template('index.html', form_script=my_form_script, forms=my_form, message=msg, notifications=notifs, message_list=list_options,  user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'
    
    @route("/intents", methods=['GET', 'POST'])
    def intents(self):
        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session 
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                empty_data={'Status': 'Deleted', 'Time': str(datetime.now().replace(microsecond=0)) }
                intent_data={}
                show_intent_data=[]
                self.intent_conf_manager.show_intent(show_intent_data)
                create_intentid=int(self.intent_conf_manager.No_of_intents+1)
                show_notification_data = []
                self.notification_conf_manager.show_notification(show_notification_data, _pilot)

                if request.method == 'POST':

                    if 'create_intentname' in request.form:    
                        create_intentname=request.form['create_intentname']
                        intent_data["Name"]=create_intentname
                        create_intentsource=request.form['create_intentsource']
                        intent_data["Source"]=create_intentsource
                        create_intentattributes=request.form['create_intentattributes']
                        intent_data["Attributes"] = create_intentattributes
                        create_intentvalue=request.form['create_intentvalue']
                        intent_data["Value"] = create_intentvalue
                        self.intent_conf_manager.add_intent(intent_data) 
                        return jsonify({'create_intentid': create_intentid,'create_intentname': create_intentname, 'create_intentsource': create_intentsource, 'create_intentattributes': create_intentattributes
                        ,'create_intentvalue': create_intentvalue })   
                    
                    if 'delete_intentid' in request.form:
                        
                        delete_intentid=request.form['delete_intentid']

                        self.intent_conf_manager.delete_intent(empty_data,delete_intentid)
                        
                        return jsonify({'delete_intentid': delete_intentid })   

                    if 'show_intentid' in request.form:
                        
                        show_intentid=int(request.form['show_intentid'])
                        show_intentattribute=show_intent_data[show_intentid-1]['Attributes']
                        show_intentvalue=show_intent_data[show_intentid-1]['Value']
                        return jsonify({'show_intentid': show_intentid, 'show_intentattribute' : show_intentattribute, 'show_intentvalue': show_intentvalue})
                        
                return render_template('intents.html', intent_data=intent_data, show_intent_data=show_intent_data, create_intentid=create_intentid, show_notification_data=show_notification_data, user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'

    @route("/policies", methods=['GET', 'POST'])
    def policies(self):
        show_notification_data = []
        self.notification_conf_manager.show_notification(show_notification_data)
        
        return render_template('policies.html', show_notification_data=show_notification_data)
        
    #@route('/api', methods=['GET'])#    @oidc.accept_token(require_token=True, scopes_required=['openid'])
    #def hello_api(self):
    #    """OAuth 2.0 protected API endpoint accessible via AccessToken"""
    #    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})

    @route("/remediation", methods=['GET', 'POST'])
    def remediation(self): 

        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                show_notification_data=[]
                self.notification_conf_manager.show_notification(show_notification_data,  _pilot)
                
                ################
                (_title, _items, _show_success_notice, _success_notice) = rem.main_remediation()

                return render_template('remediation.html', title=_title,
                           items=_items,
                           show_success_notice=_show_success_notice,
                           success_notice=_success_notice, 
                           show_notification_data=show_notification_data, 
                           user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'

    
    @route("/remediation_selected", methods=['GET', 'POST'])
    def remediation_selected(self, _show_success_notice=None):

        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                show_notification_data=[] 
                self.notification_conf_manager.show_notification(show_notification_data,  _pilot)
                ##############
                (_title, _items, _show_success_notice, _success_notice) = rem.remediation_selected(_show_success_notice=_show_success_notice)
                return render_template('remediation.html', title=_title,
                           items=_items,
                           show_success_notice=_show_success_notice,
                           success_notice=_success_notice, 
                           show_notification_data=show_notification_data, 
                           user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'

    

    @route("/accept_remediation/<item_id>", methods=['GET', 'POST'])
    def accept_remediation(self, item_id):

        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                show_notification_data=[]
                self.notification_conf_manager.show_notification(show_notification_data,  _pilot)
                
                ##############
                _show_success_notice = rem.accept(item_id)
                return redirect(url_for('UserInterface:remediation_selected', show_success_notice=_show_success_notice))
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'

    

        
    #@route('/api', methods=['GET'])#    @oidc.accept_token(require_token=True, scopes_required=['openid'])
    #def hello_api(self):
    #    """OAuth 2.0 protected API endpoint accessible via AccessToken"""
    #    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})



    @route("/notifications", methods=['GET', 'POST'])
    def notifications(self):
        try:
            try:
                self.login_session = request.args['session']
                with open("./keyclock_last_token.json") as token_file:
                    json_decoded = json.load(token_file)
                json_decoded["token"] = self.login_session
                with open("./keyclock_last_token.json", 'w') as token_file:
                    json.dump(json_decoded, token_file)
            except:
                try:
                    with open("./keyclock_last_token.json", "r") as f:
                        data = json.load(f)
                        self.login_session = data["token"]
                        
                except:
                    return render_template('404.html',error="MISSING TOKEN")
            payload='access_token=' + self.login_session 
            #response = requests.request("POST", self.oicd_url, headers=self.oicd_headers, data=payload, verify=False)
            access_token_json = jwt.decode(self.login_session, self.public_key, audience='account')
            
            if access_token_json: # response.status_code == 200: # or self.test_allowed == True:
                self.error_message = "reading user info ..."
                user_info = access_token_json
                _pilot = user_info['pilot']
                intent_data={}
                n_id = request.args.get('n_id', None)
                # notification_selection is set to all in default to show all notification.
                notification_selection = 'All'
                show_notification_data=[]
                single_notification_data=[]
                self.notification_conf_manager.show_notification(show_notification_data, _pilot)

                open_notifications=0
                create_intentid=int(self.intent_conf_manager.No_of_intents+1)
                

                #selecting particular notification from another page.
                if n_id!=None:
                    notification_selection = 'Single'
                
                    #set status to seen.
                    single_notification_status = 'Seen'
                    
                    single_notification_id=[i for i,_ in enumerate(show_notification_data) if _["ID"] == n_id][0]
                    self.notification_conf_manager.notification_status(single_notification_status, n_id)
                    single_notification_name=show_notification_data[single_notification_id]['Name']
                    single_notification_source=show_notification_data[single_notification_id]['Source']
                    single_notification_id = n_id
                    single_notification_data=[{"ID": single_notification_id, "Name": single_notification_name, "Source": single_notification_source, "Status": single_notification_status }]

                # return to ajax in notification page without reloading.

                if 'single_notification_id' in request.form:
                    

                    single_notification_status = request.form['single_notification_status']
                    notification_selection = 'Single'
                    
                    nn_id=request.form['single_notification_id']
                    single_notification_id=[i for i,_ in enumerate(show_notification_data) if _["ID"] == nn_id][0]
                
                    #single_notification_id=request.form['single_notification_id']
                    self.notification_conf_manager.notification_status(single_notification_status, nn_id)
                    count_notifications=-1
                    for i in range(0,len(show_notification_data)):
                        if show_notification_data[i]['Status']=='Open':
                            count_notifications+=1
                    if count_notifications==-1:
                        count_notifications=0
                    single_notification_name=show_notification_data[single_notification_id]['Name']
                    single_notification_source=show_notification_data[single_notification_id]['Source']
                    single_notification_id = request.form['single_notification_id']
                    single_notification_data=[{"ID": single_notification_id, "Name": single_notification_name, "Source": single_notification_source, "Status": single_notification_status }]
                    return jsonify({'single_notification_id': single_notification_id, 'single_notification_name' : single_notification_name, 'single_notification_source': single_notification_source, 'count_notifications' : count_notifications})

                if 'delete_notificationid' in request.form:
                    notification_status= 'Deleted'   
                    delete_notificationid=request.form['delete_notificationid']
                    self.notification_conf_manager.notification_status(notification_status, delete_notificationid)    
                    return jsonify({'delete_notificationid': delete_notificationid })   

                if 'show_notificationid' in request.form:   
                    #show_notificationid=int(request.form['show_notificationid'])
                    nn_id=request.form['show_notificationid']
                    #print(nn_id)
                    show_notificationid=[i for i,_ in enumerate(show_notification_data) if _["ID"] == nn_id][0]
                
                    show_notificationattribute=show_notification_data[show_notificationid]['Time']
                    show_notificationvalue=",\n".join(show_notification_data[show_notificationid]['Value'].split(","))
                    #print(show_notificationvalue)
                    show_notificationid=request.form['show_notificationid']
                    return jsonify({'show_notificationid': show_notificationid, 'show_notificationattribute' : show_notificationattribute, 'show_notificationvalue': show_notificationvalue})
                if 'create_intentid' in request.form:
                        
                        nn_id=request.form['create_intentid']
                        create_intentid=[i for i,_ in enumerate(show_notification_data) if _["ID"] == nn_id][0]
                
                        notification_status= 'Created'   
                        self.notification_conf_manager.notification_status(notification_status, nn_id)  
                        create_intentname=show_notification_data[create_intentid]['Name']
                        intent_data["Name"]=create_intentname
                        create_intentsource=show_notification_data[create_intentid]['Source']
                        intent_data["Source"]=create_intentsource
                        create_intentattributes=show_notification_data[create_intentid]['Attributes']
                        intent_data["Attributes"]=create_intentattributes   
                        create_intentvalue=show_notification_data[create_intentid]['Value']
                        intent_data["Value"]=create_intentvalue   
                        self.intent_conf_manager.add_intent(intent_data) 
                        create_intentid=request.form['create_intentid']

                        return jsonify({'create_intentid': create_intentid})

                return render_template('notifications.html', show_notification_data=show_notification_data, n_id=n_id, notification_selection=notification_selection, single_notification_data=single_notification_data, open_notifications=open_notifications, user_info=user_info)
            else:
                return render_template('404.html',error="NOT CONNECTED")#'NOT CONNECTED'
        except:
            return render_template('404.html',error="MISSING TOKEN") #'MISSING TOKEN'
            

def runAppssl():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False, ssl_context=('/crt/cert.pem', '/crt/key.pem'))

def runApp():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

	
if __name__ == "__main__":
    UserInterface.register(app, route_base='/')
    certs_present = [os.path.exists('/crt/cert.pem'),
                    os.path.exists('/crt/key.pem')]
    print("Detected [certificate, private key]: ", certs_present)
    try:
        if all(certs_present):
            #app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('/crt/cert.pem', '/crt/key.pem'))
            Thread(target=runAppssl).start()
            Thread(target = crc.run_rabbit).start()
            Thread(target = crc.run_rabbit).start()
        else:
            #app.run(host='0.0.0.0', port=5000, debug=True)
            Thread(target=runApp).start()
            Thread(target = crc.run_rabbit).start()
            Thread(target = scc.run_rabbit).start()
    
    except Exception as e:
        print("Unexpected error:" + str(e))
