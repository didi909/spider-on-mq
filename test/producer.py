import pika
import os
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host = '39.98.170.203',port = 5772,virtual_host = '/',credentials = credentials))
channel = connection.channel()
# 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
channel.queue_declare(queue='hello')

for x in range(1,10):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=str(x))
print(" [x] Sent 'Hello World!'")
connection.close()
