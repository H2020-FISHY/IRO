"""
|
|   file:       main.py
|
|   brief:
|   author:    
|   email:      
|   copyright:  © IDA - All rights reserved
"""
import os
from flask import Flask, render_template, request,  url_for, redirect
from jinja2 import Environment, FileSystemLoader
from flask_classful import FlaskView, route
from intent_manager import IntentManager
from notification_manager import NotificationManager

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IRO'


class UserInterface(FlaskView):
    """
    |   UserInterface Class
    """
    def __init__(self):
        self.intent_manager = IntentManager()
        self.notification_manager = NotificationManager()
        self.policies_filename = "export.txt"

    def index(self):
        notifs = self.notification_manager.get_notifications()

        return render_template('index.html', notifications=notifs)

    def post(self):
        msg = ''
        if request.method == 'POST':
            intent_text = request.form.get('intentText')
            msg = self.intent_manager.reading_command(intent_text)
            if msg == "reports":
                return render_template('Alerts.html')
        return render_template('index.html', message=msg)

    @route("/alerts", methods=['GET', 'POST'])
    def alerts(self):
        if request.method == 'POST':
            # do stuff when the form is submitted

            # redirect to end the POST handling
            # the redirect can be to the same route or somewhere else
            return redirect(url_for('index'))

        # show the form, it wasn't submitted
        return render_template('Alerts.html')

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
    app.run(host='0.0.0.0', port=5000, debug=True)
