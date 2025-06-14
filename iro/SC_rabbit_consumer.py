
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
      self.sc_path = "notification_store/smart_contracts/verified_sc.json"

    def __del__(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except:
                pass

    def _create_connection(self):
        host     = os.getenv("AMQP_HOST", "localhost")
        port     = int(os.getenv("AMQP_PORT", 5672))
        vhost    = os.getenv("AMQP_VHOST", "/")
        rmquser       = os.getenv("RABBITMQ_USER", "tubs")
        rmqpass       = os.getenv("RABBITMQ_PASS", "sbut")
        credentials = pika.PlainCredentials(rmquser, rmqpass)

        parameters  = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=credentials
        )

        try:
            connection = pika.BlockingConnection(parameters)
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            return None

    def on_message_callback(self, channel, method, properties, body):
        print(" [x] Received %r" % body)
        binding_key = method.routing_key
        print(" [x] Received %r" % body)
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
        
        fpath = "notification_store/smart_contracts"+"notification_SC_"+info["id"]+".json"
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
        channel.exchange_declare(exchange="sc-results", exchange_type="direct", durable=True)
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
