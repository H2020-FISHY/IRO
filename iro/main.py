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
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader
from flask_classful import FlaskView, route
from intent_manager import IntentManager

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
        self.policies_filename = "export.txt"

    def index(self):
       return render_template('index.html')

    def post(self):
        msg = ''
        if request.method == 'POST':
            intent_text = request.form.get('intentText')
            msg = self.intent_manager.reading_command(intent_text)
        return render_template('index.html', message=msg)

    @route("/addIntent", methods=["POST"])
    def addintent(self):
        msg = ''
        return ""
    
    @route("/policies", methods=["GET"])
    def export_policies(self):
        with open("./output files/"+self.policies_filename, "r") as f:
            policies = f.read()
        return render_template('policies.html', policies=policies)

if __name__ == "__main__":
    UserInterface.register(app, route_base='/')
    app.run(debug=True)
