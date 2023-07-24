
#import  notification_configuration as ntc
import pika, sys, os
import json
import ast

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
        _device_product = "Not Defined"
        _time = "Error"
        _pilot = "Not Defined"
        _event_name = "Not Defined"



        # Parse CEF format
        try:
            _id = info["details"]['id']
        except:
            try:
                _id = info['id']
            except:
                _id = "Not Defined"
        # Parse device_event_class_id
        try:
            _device_event_class_id = info["details"]['device_event_class_id']
        except:
            _device_event_class_id = "Not Defined"
        # Parse 
        try:
            
            _extensions_list = ast.literal_eval(info["details"]['extensions_list'])
        except:
            _extensions_list = ""

        # Parse severity
        try:
            _severity = info["details"]['severity']
        except:
            _severity = "Not Defined"

        try:
            _event_name = info["details"]['event_name']
        except:
            _event_name = "Not Defined"
        

        # Parse time
        try:
            _time = info["details"]["updated_at"]
        except:
            try:
                _time = _extensions_list['ts']
            except:
                _time = "Not Defined"
        # Parse device_version
        try:
            _device_version = info["details"]['device_version']
        except:
            _device_version = "Not Defined"
        # Parse source
        try:
            _device_product = info["details"]['device_product']
        except:
            try:
                _device_product = info["details"]["report"]["source"]
            except:
                try:
                    _device_product = info["details"]["device_product"]
                except:
                    _device_product = "Not Defined"
        # Parse pilot
        try:
            _pilot_ = info["details"]['pilot']
        except:
            try:
                pilot = info["details"]["report"]["data"]["pilot"]
            except:
                _pilot = "Not Defined"






        
        
        # create notif info
        notif = { 
                "Name": _event_name, #_event_name,
                "Source": _device_product,
                "Attributes": _device_version,
                "Value": _extensions_list,
                "ID": _id,
                "pilot": _pilot,
                "Time": _time,
                "Status": "Open"
                }
        

        
        # save notif info and state
        fpath = "notification_store/reports/"+_id+".json"
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
    
def run_rabbit(): #queueName, bindingKey , config):
    #https://fishy.xlab.si/tar/api/reports/v2

    # Central repository RabbitMQ parameters
    queueName = 'IROQueue'
    bindingKey = 'reports.#'
    config = { 'host': 'fishymq.xlab.si', 'port': 45672, 'exchange' : 'tasks', 'login':'tubs', 'password':'sbut'}

    try:
        init_rabbit = RMQsubscriber(queueName, bindingKey , config)
        init_rabbit.setup()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    
