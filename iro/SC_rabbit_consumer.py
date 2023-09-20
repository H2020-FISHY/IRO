
#import  notification_configuration as ntc
import pika, sys, os
import json
from datetime import datetime

class SCsubscriber:
    def __init__(self, queueName, bindingKey, config):
      self.queueName = queueName
      self.bindingKey = bindingKey
      self.config = config
      #self.notif_counter = 10
      self.connection = self._create_connection()
      self.sc_path = "/iro/notification_store/smart_contracts/verified_sc.json"

    def __del__(self):
      self.connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(self.config['login'], self.config['password']) # 'tubs', 'sbut')
        parameters = pika.ConnectionParameters(host=self.config['host'], 
                          port=self.config['port'],
                          virtual_host='/', 
                          credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        #parameters=pika.ConnectionParameters(host=self.config['host'],  port = self.config['port'])
        return connection

    def on_message_callback(self, channel, method, properties, body):
        print(" [x] Received %r" % body)
        binding_key = method.routing_key
        info = json.loads(body.decode('utf-8'))
        
        notif = {
            "ID": info["id"],
            "Name": "SC"+ str(info["id"]),
            "type": info["type"],
            "link": info["link"],
            "tx_hash": info["tx_hash"],
            "error_message": info["error_message"],
            "Time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "Status": "Open"
            }
        
        fpath = "/iro/notification_store/smart_contracts"+"notification_SC_"+info["id"]+".json"
        with open(fpath, 'w') as f:
            _notif = json.dumps(notif)
            f.write(_notif)
        with open(self.sc_path) as sc_file:
            json_decoded = json.load(sc_file)
        json_decoded[info["id"]] = notif["error_message"]
        with open(self.sc_path, 'w') as sc_file:
            json.dump(json_decoded, sc_file)


        #self.notif_counter += 1


    def setup(self):
        channel = self.connection.channel()
        #channel.exchange_declare(exchange=self.config['exchange'])
        # This method creates or checks a queue
        channel.queue_declare(queue=self.queueName)
        # Binds the queue to the specified exchang
        channel.queue_bind(queue=self.queueName,exchange=self.config['exchange'],routing_key=self.bindingKey)
        channel.basic_consume(queue=self.queueName,
        on_message_callback=self.on_message_callback, auto_ack=True)
        print('[*] Waiting for data for ' + self.queueName + '. To exit press CTRL+C')
        try:
            
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

def run_rabbit():
    # Smart Contracts RabbitMQ parameters
    #SCqueueName = 'SCQueue'
    #SCkey = 'sc.validation'
    #SCnotification_consumer_config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'sc-results', 'login':'tubs', 'password':'sbut'}
    try:
        SCqueueName = os.environ["SC_QUEUE_NAME"]
        SCkey = os.environ["SC_KEY"]
        SCnotification_consumer_config =  { 'host': os.environ["RABBIT_NOTIF_HOST"], 'port': os.environ["RABBIT_NOTIF_PORT"], 'exchange' : os.environ["RABBIT_SC_EXCHANGE"], 'login':os.environ["RABBIT_NOTIF_LOGIN"], 'password':os.environ["RABBIT_NOTIF_PASS"]} 
    except:
        SCqueueName = 'SCQueue'
        SCkey = 'sc.validation'
        SCnotification_consumer_config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'sc-results', 'login':'tubs', 'password':'sbut'}


    try:
        init_rabbit = SCsubscriber(SCqueueName, SCkey , SCnotification_consumer_config)
        init_rabbit.setup()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
