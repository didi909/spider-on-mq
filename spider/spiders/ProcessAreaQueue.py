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

logger = Logger(currentFileName.replace('.py', ''))

regionService = RegionService()

chengjiaoNumPerPage = 30
chengjiaoPageMax =100

class ProcessAreaQueue:
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
        dictObj = json.loads(message)

        province_id = dictObj.get('province_id')
        province_name = dictObj.get('province_name')
        city_id = dictObj.get('city_id')
        city_name = dictObj.get('city_name')
        cityUrl = dictObj.get('cityUrl')
        area_id=dictObj.get('area_id')
        area_name = dictObj.get('area_name')
        areaUrl = dictObj.get('areaUrl')

        logger.info('处理[%s]区,url:[%s] ' % (area_name, areaUrl))
        # 打开区县url，抓取商圈信息
        status_code, text, content = myGetRequest(areaUrl, Config.PROXY_FLAG)

        soup = BeautifulSoup(text,"html.parser")
        # 获取到该区下面的全部商圈的url然后推送
        townSoupTemp = soup.find_all(attrs={"data-role": "ershoufang"})

        # if townSoupTemp == []:
        if len(townSoupTemp[0].find_all('div')) == 1:
            # 如果是空集合，表示该区县下没有商圈，采用区县名称作为商圈名称
            town_name = area_name
            id = getUUID()
            townSoupTemp = BeautifulSoup(text, "html.parser")

            # 插入商圈到数据库
            town_id = regionService.addOrInsert(RegionEntity(id=id,
                                                             pid=province_id,
                                                             name=city_name,
                                                             level=Config.TOWN_LEVEL
                                                             ))

            townUrl = areaUrl
            logger.info('处理[%s]商圈,url:%s ' % (town_name, townUrl))
            # 抓取商圈页面的小区总数-用于计算总页数
            totalOnsaleNum = int(
                townSoupTemp.find_all('div', class_='total fl')[0].find_all('span')[0].getText().strip())
            # 计算总页数
            totalPageNum = self.getCurrentPages(totalOnsaleNum)

            for x in range(1,totalPageNum+1):
                townUrlByPage=townUrl+'/pg'+str(x)
                # 组装数据推送到区域队列
                dict = {
                    'province_id': province_id,
                    'province_name': province_name,
                    'city_id': city_id,
                    'city_name': city_name,
                    'cityUrl': cityUrl,
                    'area_id': area_id,
                    'area_name': area_name,
                    'town_id': town_id,
                    'town_name':town_name,
                    'townUrlByPage':townUrlByPage
                }
                self.pushResult(dict)


        else:
            for t in townSoupTemp[0].find_all('div')[1].find_all('a'):
                town_name = t.getText()
                id = getUUID()
                townUri = t['href']
                townUrl = cityUrl + townUri

                townSoupTemp = soup

                # 插入商圈到数据库
                town_id = regionService.addOrInsert(RegionEntity(id=id,
                                                                 pid=province_id,
                                                                 name=city_name,
                                                                 level=Config.TOWN_LEVEL
                                                                 ))

                # 抓取商圈页面的小区总数-用于计算总页数
                totalOnsaleNum = int(
                    townSoupTemp.find_all('div', class_='total fl')[0].find_all('span')[0].getText())
                # 计算总页数
                totalPageNum = self.getCurrentPages(totalOnsaleNum)

                logger.info('处理[%s]商圈,url:%s,获取到[%d]页数据 ' % (town_name, townUrl,totalPageNum))

                for x in range(1, totalPageNum + 1):
                    townUrlByPage = townUrl + 'pg' + str(x)
                    # 组装数据推送到区域队列
                    dict = {
                        'province_id': province_id,
                        'province_name': province_name,
                        'city_id': city_id,
                        'city_name': city_name,
                        'area_id': area_id,
                        'area_name': area_name,
                        'town_id': town_id,
                        'town_name': town_name,
                        'townUrlByPage': townUrlByPage
                    }
                    self.pushResult(dict)


    def pushResult(self, dict):
        # 推送小区明细队列
        self.mqObj.pushMessageToMq(targetQueue, json.dumps(dict))

    def getCurrentPages(self,totalOnsaleNum):
        if (totalOnsaleNum/chengjiaoNumPerPage > chengjiaoPageMax):
            totalPageNum = chengjiaoPageMax
        else:
            totalPageNum = math.ceil(totalOnsaleNum/chengjiaoNumPerPage)

        return totalPageNum

if __name__ == '__main__':
    # 定义当前处理队列
    processQueue = Config.AREA_QUEUE
    # 定义处理完成后推送的队列
    targetQueue = Config.TOWN_BY_PAGE_QUEUE

    tq = ProcessAreaQueue()
    tq.run()
