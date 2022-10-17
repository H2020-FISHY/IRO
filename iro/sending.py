#!/usr/bin/env python
import pika
import json

credentials = pika.PlainCredentials('tubs', 'sbut')
# try to establish connection and check its status
try:
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='fishymq.xlab.si', 
                          port=45672,
                          virtual_host='/', 
                          credentials=credentials))


  #connection = pika.BlockingConnection(parameters)
  if connection.is_open:
    print('OK')
   # connection.close()
    #exit(0)
except Exception as error:
  print('Error:', error.__class__.__name__)
  exit(1)

channel = connection.channel()
channel.queue_declare(queue='reports.#')
data ='{"source":"test", "data":"test"}'
message = json.dumps(data) 
channel.basic_publish(exchange='',
                      routing_key='reports.#',
                      body=message)
print(" [x] Sent 'Test!'")
connection.close()
