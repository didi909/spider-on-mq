from bs4 import BeautifulSoup
import math
import json
#from dynaconf import settings as Config
from spider.config.settings import Config
from spider.tools.logtools import Logger
from spider.tools.commontools import getUUID, Timer
from spider.tools.webtools import myGetRequest
from spider.tools.mqtools import rabbitmqConnection
from spider.service.RegionService import RegionService
from spider.entity.RegionEntity import RegionEntity
from urllib3.exceptions import MaxRetryError
import traceback
import os

currentFileName = os.path.basename(os.path.realpath(__file__))

logger = Logger(currentFileName.replace('.py',''))


regionService = RegionService()

class ProcessCommunityQueue:
    def __init__(self):
        # self.queueName = queueName
        # 初始化消息队列
        self.mqObj = rabbitmqConnection()
        # self.myConnection = self.mqObj.getRabbitmqConnection()
        self.readChannel = self.mqObj.getChannel(processQueue)
        # 获取runId
        self.run_id = getUUID()

    # 读取队列消息
    def callback(self, ch, method, properties, message):
        try:
            self.parse(message)
            # 当正常完成任务，会反馈给rabbitmq
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except MaxRetryError:
            ch.basic_reject(delivery_tag=method.delivery_tag)
        except Exception:
            # 发告警
            # 打印异常
            # traceback.print_exc()
            # 推送异常
            error_message = traceback.format_exc()
            logger.error(error_message)
            ch.basic_reject(delivery_tag=method.delivery_tag)
            dict = {'run_id': self.run_id, 'error_message': error_message}
            self.mqObj.pushMessageToMq(Config.ERROR_QUEUE, json.dumps(dict))

    def run(self):
        try:
            # 设置预处理数量，可用来分配每个消费者的处理数量，并发消费时需要用
            self.readChannel.basic_qos(prefetch_count=50)
            # 告诉rabbitmq，用callback来接收消息
            self.readChannel.basic_consume(processQueue, self.callback)

            logger.info('开始读取%s队列' % processQueue)
            # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
            self.readChannel.start_consuming()
        except Exception:
            # 打印异常
            # traceback.print_exc()
            # 推送异常
            error_message = traceback.format_exc()
            logger.error(error_message)
            dict = {'run_id': self.run_id, 'error_message': error_message}
            self.mqObj.pushMessageToMq(Config.ERROR_QUEUE, json.dumps(dict))

    # 解析队列消息，业务逻辑
    def parse(self, message):
        dictObj=json.loads(message)

        province_id=dictObj.get('province_id')
        province_name=dictObj.get('province_name')
        city_name=dictObj.get('city_name')
        cityUrl=dictObj.get('cityUrl')
        cityOnsaleUrl = dictObj.get('cityOnsaleUrl')

        # # 目前已知雄安是没有二手在售的
        # if city_name == '雄安新区' or city_name =='江阴':
        #     logger.info('[%s]市跳过，暂不处理')
        #     return
        logger.info('处理[%s]市,在售Url：[%s]' % (city_name, cityOnsaleUrl))
        # ，这里比较特殊，因为在bk执行https://diqing.fang.ke.com/loupan/楼盘url的时候，如果不存在会走302跳转，这里不让他跳转，否则后续判断不对
        cityOnsaleUrl='https://xan.ke.com/ershoufang/'
        status_code, text, content = myGetRequest(cityOnsaleUrl, Config.PROXY_FLAG,allowRedirects=False)
        soup = BeautifulSoup(text, "html.parser")
        id = getUUID()
        # 插入市到数据库
        city_id = regionService.addOrInsert(RegionEntity(id=id,
                                                        pid=province_id,
                                                        name=city_name,
                                                        level=Config.CITY_LEVEL
                                                        ))
        if city_id != id:
            logger.warning('城市id：[%s]，name：[%s]，已存在' % (city_id, city_name))
        else:
            logger.info('城市id：[%s]，name：[%s]，入库成功' % (city_id, city_name))

        if status_code == 200:
            # 判断当前页面的总套数
            totalOnsale = soup.find_all('h2',class_='total fl')[0].find_all('span')[0].getText().strip()
            if totalOnsale =='0':
                # 有页面但没有在售数据
                logger.warning('[%s]市没有在售数据，url：%s' % (city_name, cityOnsaleUrl))
            # 有在售
            # 抓区县信息
            areaSoup = soup.find_all('a',attrs={'data-click-evtid':'12339'})
            for area in areaSoup:
                areaUri = area['href']
                area_name = area.getText().strip()
                areaUrl = cityUrl + areaUri

                id=getUUID()

                # 插入区域数据库
                area_id = regionService.addOrInsert(RegionEntity(id=id,
                                                                 pid=province_id,
                                                                 name=city_name,
                                                                 level=Config.AREA_LEVEL
                                                                 ))

                # 组装数据推送到区域队列
                dict = {
                        'province_id':province_id,
                        'province_name':province_name,
                        'city_id':city_id,
                        'city_name':city_name,
                        'cityUrl':cityUrl,
                        'area_id':area_id,
                        'area_name':area_name,
                        'areaUrl':areaUrl
                        }
                self.pushResult(dict)

        else:
            logger.info('[%s]市没有在售数据，url：%s' % (city_name, cityOnsaleUrl))
        # # 推送本次结果
        # self.pushResult(targetQueue,dict)


    def pushResult(self,dict):
        # 推送小区明细队列
        self.mqObj.pushMessageToMq(targetQueue, json.dumps(dict))

if __name__ == '__main__':
    # 定义当前处理队列
    processQueue=Config.CITY_QUEUE
    # 定义处理完成后推送的队列
    targetQueue=Config.AREA_QUEUE

    tq=ProcessCommunityQueue()
    tq.run()