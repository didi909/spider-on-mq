import pika
import os
import sys
from spider.config.settings import Config
from spider.tools.logtools import getDefaultLogger

logger = getDefaultLogger()


# 添加当前路径到环境变量
sys.path.append(os.path.dirname(__file__))

class rabbitmqConnection:
    def __init__(self):
        # self.connection = self.getRabbitmqConnection()
        # self.channel = self.connection.channel()
        #
        # # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
        # self.channel.queue_declare(queue=queueName)
        self.connection = self.getConnection()

    # 创建连接
    def getConnection(self):
        credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=Config.RABBITMQ_HOST,
                                      port=Config.RABBITMQ_PORT,
                                      virtual_host=Config.RABBITMQ_VIRTUAL_HOST,
                                      credentials=credentials,
                                      heartbeat=0))
        logger.info('rabbitmq连接：host=' + Config.RABBITMQ_HOST +
                    ', port=' + str(Config.RABBITMQ_PORT) +
                    ',user=' + Config.RABBITMQ_USER +
                    ',password=' + Config.RABBITMQ_PASSWORD +
                    ',virtual host=' + Config.RABBITMQ_VIRTUAL_HOST)
        return connection

    # 获取channel
    def getChannel(self, queueName):
        channel = self.connection.channel()
        # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
        channel.queue_declare(queue=queueName, durable=True)

        return channel

    # 推送消息
    def pushMessageToMq(self, queueName, msg):
        channel = self.getChannel(queueName)
        # 放入队列
        # if self.connection.is_closed:
        #     logger.error('mq连接已关闭')
        channel.basic_publish(exchange='',
                              routing_key=queueName,
                              body=msg,
                              properties=pika.BasicProperties(delivery_mode=2)
                              )
        channel.close()
        logger.info('推送队列%s成功' % queueName)

    # 读取消息