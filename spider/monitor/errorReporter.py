import json
#from dynaconf import settings as Config
from spider.config.settings import Config
from spider.tools.commontools import mysqlConnection,rabbitmqConnection,getUUID,formatDateTime
from spider.tools.logtools import Logger,getDefaultLogger
from spider.entity.ErrorMessageEntity import ErrorMessageEntity
import os

# logger =Logger()
logger = getDefaultLogger()

currentFileName = os.path.basename(os.path.realpath(__file__))


# 捕获异常，即时发送
class ErrorReporter:
# 从mq读取异常
    def __init__(self):
        # self.queueName = queueName
        # 初始化消息队列
        self.mqObj = rabbitmqConnection()
        self.channel = self.mqObj.getChannel(queueName)

        # 初始化mysql连接
        self.mysqlSession = mysqlConnection()
        # 获取runId
        self.run_id = getUUID()

    def callbackErrorLog(self, ch, method, properties, message):
        self.parseErrorLog(message)
        # 当完成任务后，会反馈给rabbitmq
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def parseErrorLog(self,message):
        dict =json.loads(message)
        run_id = dict.get('run_id')

        file_name = dict.get('file_name')
        error_message = dict.get('error_message')
        create_time=formatDateTime(0)
        soup = dict.get('soup')
        id = getUUID()

        # 异常入库（为本次运行统计做准备）
        self.mysqlSession.addOne(ErrorMessageEntity(id=id,
                                                    run_id=run_id,
                                                    file_name=file_name,
                                                    message=error_message,
                                                    create_time=create_time,
                                                    soup=soup))
        logger.info('已入库，异常id:%s,异常信息:%s' % (id,error_message[0:100]))
        # 发送异常(目前采用邮件)

    def run(self):
        # 告诉rabbitmq，用callback来接收消息
        self.channel.basic_consume(queueName, self.callbackErrorLog)

        logger.info('开始读取%s队列' % queueName)
        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        self.channel.start_consuming()

queueName = Config.ERROR_QUEUE
e = ErrorReporter()
e.run()