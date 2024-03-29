import pika, sys, os
import json

class RMQSingleMessageSubscriber:

    def __init__(self, queueName, bindingKey, config):

        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.exchange = self.config["exchange"]
        self.connection = self._create_connection()
        self.received_message = None

    def __del__(self):

        if self.connection.is_open:
            self.connection.close()

    def _create_connection(self):

        credentials = pika.PlainCredentials(self.config['login'], self.config['password'])
        parameters = pika.ConnectionParameters(host=self.config['host'],
                          port=self.config['port'],
                          virtual_host='/',
                          credentials=credentials)
        #parameters = pika.ConnectionParameters("host.docker.internal")
        #parameters = pika.ConnectionParameters("127.0.0.1")
        connection = pika.BlockingConnection(parameters)

        return connection

    def on_message_callback(self, channel, method, properties, body):
        print(" [x] Received %r" % body)
        message = json.loads(body.decode('utf-8'))
        if "correlation_id" in message.keys(): # check that this is a GUI related message (temporary fix for the rabbitmq echo issue)
            self.received_message = message
        channel.basic_ack(delivery_tag=method.delivery_tag)
        if "correlation_id" in message.keys(): # check that this is a GUI related message (temporary fix for the rabbitmq echo issue)
            channel.close()
        #channel.stop_consuming()

    def setup(self):
        channel = self.connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

        # This method creates or checks a queue
        channel.queue_declare(queue=self.queueName)

        # Binds the queue to the specified exchange
        channel.queue_bind(queue=self.queueName,
                        exchange=self.config['exchange'],
                        routing_key=self.bindingKey)

        channel.basic_consume(queue=self.queueName,
                            on_message_callback=self.on_message_callback,
                            auto_ack=False)

        self.connection.process_data_events(time_limit=1.0)

        channel.stop_consuming()

    def get_received_message(self):
        return self.received_message


queueName = 'remediation_proposals'
key = "remediation_proposals"
notification_consumer_config = {'host': 'fishymq.xlab.si',
                                'port': 45672,
                                'exchange' : "remediationsedcpoli_proposals",
                                'login':'tubs',
                                'password':'sbut'}

if __name__ == '__main__':

    init_rabbit = RMQSingleMessageSubscriber(queueName, key, notification_consumer_config)
    init_rabbit.setup()
    received_message = init_rabbit.get_received_message()
    print("Received message:", received_message)
