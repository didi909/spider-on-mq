import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host = '39.98.170.203',port = 5772,virtual_host = '/',credentials = credentials))
channel = connection.channel()
# 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
channel.queue_declare(queue='hello')

# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    if run(body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_reject(delivery_tag=method.delivery_tag)

    # 当工作者完成任务后，会反馈给rabbitmq

    # ch.basic_ack(delivery_tag = method.delivery_tag)
    # 打印消息体
    # print(body.decode())

def run(message):
    if message.decode() == 'hi':
        print('出现了异常')
        return False
    print(message.decode())
    return True
# 告诉rabbitmq，用callback来接收消息
channel.basic_consume('hello',callback)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
channel.start_consuming()