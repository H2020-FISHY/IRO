import pika, json, sys, os, base64

class RMQproducer:
    def __init__(self, routingKey, config):

        self.config = config
        self.routingKey = routingKey
        self.exchange = self.config["exchange"]
        self.connection = self._create_connection()

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

    def send_message(self, message):

        channel = self.connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

        channel.queue_declare(queue=self.routingKey)

        channel.basic_publish(exchange=self.exchange,
                            routing_key=self.routingKey,
                            body=json.dumps(message))

        channel.close()

        self.connection.close()

        print(" [x] Sent %r" % message)

key = "edc_remediation_proposals"
notification_producer_config = {'host': 'fishymq.xlab.si',
                                'port': 45672,
                                'exchange' : "edc_remediationsedcpoli_proposals",
                                'login':'tubs',
                                'password':'sbut'}

if __name__ == '__main__':

    try:

        init_rabbit = RMQproducer(key, notification_producer_config)
        message = {"correlation_id": "test", 'type': 'proposal', 'recommended_remediation': 'filter_ip_port_recipe', 'remediations': [{'id': 'filter_payload_recipe', 'description': 'Filter payload on impacted node', 'details': 'This is a Recipe'}, {'id': 'filter_ip_port_recipe', 'description': 'Filter ip and port on impacted node', 'details': 'This is a Recipe'}, {'id': 'monitorr_traffic_recipe', 'description': 'Monitor traffic on impacted node', 'details': 'This is a Recipe'}, {'id': 'put_into_reconfiguration_recipe', 'description': 'Put impacted nodes into reconfiguration net', 'details': 'This is a Recipe'}, {'id': 'redirect_domains', 'description': 'Redirect DNS queries directed to malicious domains', 'details': 'This is a Recipe'}, {'id': 'add_honeypot_recipe', 'description': 'Add honeypot for each impacted node', 'details': 'This is a Recipe'}, {'id': 'shutdown_recipe', 'description': 'Shutdown impacted nodes', 'details': 'This is a Recipe'}, {'id': 'isolate_recipe', 'description': 'Isolate impacted nodes', 'details': 'This is a Recipe'}, {'id': 'fishy_security_recipe', 'description': 'Apply fishy security policy', 'details': 'This is a Recipe'}]}
        init_rabbit.send_message(message)

    except KeyboardInterrupt:

        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
