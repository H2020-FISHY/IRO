import json
#from flask import Flask, redirect, request, render_template, url_for
from flask import request
import os
import sys
_cwd = os.getcwd()
sys.path.append(_cwd+ '/policies/remediation')
from rabbit_consumer_single_with_timeout import RMQSingleMessageSubscriber
from rabbit_producer import RMQproducer

#app = Flask(__name__)

#### RabbitMQ conf
queueName = 'edc_remediation_proposals'
key = "edc_remediation_proposals"
notification_consumer_config = {'host': 'fishymq.xlab.si',
                                'port': 45672,
                                'exchange' : "edc_remediationsedcpoli_proposals",
                                'login':'tubs',
                                'password':'sbut'}
####

current_remediations = []
remediation_correlation_id = None
global_token = None



def get_last_remediations():
    init_rabbit = RMQSingleMessageSubscriber(queueName, key, notification_consumer_config)
    init_rabbit.setup()
    received_message = init_rabbit.get_received_message()
    print("Received last remediation:", received_message)
    return received_message


#@app.route('/', methods=['GET', 'POST'])
def main_remediation():
    global current_remediations
    global remediation_correlation_id

    message = get_last_remediations()
    if message is not None:
        if len(message["remediations"]) != 0:
            current_remediations = message["remediations"]
            remediation_correlation_id = message["correlation_id"]
            for remediation in current_remediations:
                if remediation["id"] == message["recommended_remediation"]:
                    remediation["tag"] = "recommended"

    success_notice = "The chosen remediation has been enforced."

    return ('EDC - Proposed remediations',
                current_remediations,
                False,
                success_notice)


    #return render_template('remediation.html', title='EDC - Proposed remediations',
    #                       items=current_remediations,
    #                       show_success_notice=False,
    #                       success_notice=success_notice)

#@app.route('/remediation_selected', methods=['GET', 'POST'])
def remediation_selected(_show_success_notice=None):
    #print(__name__)

    if request.args.get('show_success_notice', 'false') == 'true':
        show_success_notice = True
    elif _show_success_notice == 'true':
        show_success_notice = True
    else:
        show_success_notice = False

    success_notice = "The chosen remediation has been enforced."

    return ('EDC - Proposed remediations',
                [],
                show_success_notice,
                success_notice)



    #return render_template('remediation.html', title='EDC - Proposed remediations',
    #                       items=[],
    #                       show_success_notice=show_success_notice,
    #                       success_notice=success_notice)


#@app.route('/accept/<item_id>', methods=['POST'])
def accept(item_id):
    global current_remediations
    global remediation_correlation_id

    routingKey = "edc_remediation_selection"
    notification_producer_config = {'host': 'fishymq.xlab.si',
                                    'port': 45672,
                                    'exchange' : "edc_remediationsedcpoli_selection",
                                    'login':'tubs',
                                    'password':'sbut'}

    init_rabbit_producer = RMQproducer(routingKey, notification_producer_config)
    message = {"selected_remediation": item_id, "correlation_id": remediation_correlation_id}
    init_rabbit_producer.send_message(message)

    current_remediations = []
    remediation_correlation_id = None

    return  "true"

#if __name__ == '__main__':
#    #app.run(host="0.0.0.0", port=28999, debug=True) # accessible on all network interfaces
#    app.run(host="127.0.0.1", port=28999, debug=True) # accessible on the loopback interface (127.0.0.1 or localhost)
#    print(app.template_folder)
