
#import  notification_configuration as ntc
import pika, sys, os
import json

class RMQsubscriber:
    def __init__(self, queueName, bindingKey, config):
      self.queueName = queueName
      self.bindingKey = bindingKey
      self.config = config
      #self.notif_counter = 10
      self.connection = self._create_connection()

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
        print(" [x] Received %r" % body)
        info = json.loads(body.decode('utf-8'))
        
        notif = { 
            "Name":  info["id"],
            "Source": info["details"]["report"]["source"],
            "Attributes": "Data",
            "Value": info["details"]["report"]["data"],
            "ID": info["id"],
            "Time": "2022-07-20 22:48:41",
            "Status": "Open"
            }
        
        fpath = "notification_store/reports/"+info["id"]+".json"
        with open(fpath, 'w') as f:
            notif = json.dumps(notif)
            f.write(notif)
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


queueName = 'IROQueue'
key = 'reports.#'
notification_consumer_config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'tasks', 'login':'tubs', 'password':'sbut'}

if __name__ == '__main__':
    try:
       init_rabbit = RMQsubscriber(queueName, key, notification_consumer_config)
       init_rabbit.setup()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
      
