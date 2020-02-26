from bs4 import BeautifulSoup
import json
import decimal
# from dynaconf import settings as Config
from spider.config.settings import Config
from spider.tools.commontools import getUUID, formatDateTime
from spider.tools.webtools import myGetRequest
from spider.tools.mqtools import rabbitmqConnection
from spider.tools.locationtools import LocationTool
from spider.service.OnsaleService import OnsaleService
from spider.entity.OnsaleEntity import OnsaleEntity
from spider.tools.logtools import Logger
import traceback
import os
import re

currentFileName = os.path.basename(os.path.realpath(__file__))

logger = Logger(currentFileName.replace('.py', ''))

chengjiaoService = OnsaleService()
locationTool = LocationTool()



class ProcessOnsaleDetailQueue:
    def __init__(self):
        # self.queueName = queueName
        # # 初始化mq连接
        self.mqObj = rabbitmqConnection()
        # self.myConnection = self.mqObj.getRabbitmqConnection()
        self.readChannel = self.mqObj.getChannel(processQueue)

        # 获取runId
        self.run_id = getUUID()

    # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
    # 读取队列消息
    def callback(self, ch, method, properties, message):
        try:
            self.parse(message)
            # 当正常完成任务，会反馈给rabbitmq
            ch.basic_ack(delivery_tag=method.delivery_tag)
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

    def parse(self, message):
        dictObj = json.loads(message)

        province_id = dictObj.get('province_id')
        province_name = dictObj.get('province_name')
        city_id = dictObj.get('city_id')
        city_name = dictObj.get('city_name')
        area_id = dictObj.get('area_id')
        area_name = dictObj.get('area_name')
        town_id = dictObj.get('town_id')
        town_name = dictObj.get('town_name')
        title = dictObj.get('title')
        deal_date = dictObj.get('deal_date')
        community_name = dictObj.get('community_name')
        unit_price = dictObj.get('unit_price')
        url = dictObj.get('url')

        status_code, text, content = myGetRequest(url, Config.PROXY_FLAG)
        logger.info('开始处理[%s]，url:%s' % (community_name, url))
        soup = BeautifulSoup(text, "html.parser")

        infoSoup = soup.find_all('div', class_='info fr')[0]
        deal_price = infoSoup.find_all('span', class_='dealTotalPrice')[0].getText().strip()
        infoMsgSoup = infoSoup.find_all('div', class_='msg')[0].find_all('label')
        list_price = infoMsgSoup[0].getText().strip()
        cost_days = infoMsgSoup[1].getText().strip()
        reprice = infoMsgSoup[2].getText().strip()
        visit_num = infoMsgSoup[3].getText().strip()

        # 基本属性
        baseSoup = soup.find_all('div', class_='base')[0].find_all('li')
        if len(baseSoup) != 14:
            raise IndexError

        # 先获取全部key
        keyList = []
        for base in baseSoup:
            keyList.append(base.find_all('span')[0].getText())
        # print(keyList)
        # 再获取全部value
        valueList = []
        for base in baseSoup:
            # 去除span标签
            [s.extract() for s in base("span")]
            valueList.append(base.getText().strip())
        # print(valueList)
        # 组装字典
        baseDict = {}
        for x in range(0, len(keyList)):
            baseDict[keyList[x]] = valueList[x]
        # print(baseDict)
        rooms = baseDict['房屋户型']
        floor_info = baseDict['所在楼层']
        floor_area = baseDict['建筑面积']
        house_structure = baseDict['户型结构']
        actual_area = baseDict['套内面积']
        building_type = baseDict['建筑类型']
        north = baseDict['房屋朝向']
        build_year = baseDict['建成年代']
        decorate_type = baseDict['装修情况']
        building_structure = baseDict['建筑结构']
        hot = baseDict['供暖方式']
        elevator_rate = baseDict['梯户比例']
        property_limit = baseDict['产权年限']
        backup_elevator = baseDict['配备电梯']

        # 交易属性
        transSoup = soup.find_all('div', class_='transaction')[0].find_all('li')
        if len(transSoup) != 6:
            raise IndexError

        # 先获取全部key
        keyList = []
        for base in transSoup:
            keyList.append(base.find_all('span')[0].getText())
        # print(keyList)
        # 再获取全部value
        valueList = []
        for base in transSoup:
            # 去除span标签
            [s.extract() for s in base("span")]
            valueList.append(base.getText().strip())
        # print(valueList)
        # 组装字典
        transDict = {}
        for x in range(0, len(keyList)):
            transDict[keyList[x]] = valueList[x]

        bk_id = transDict['链家编号']
        deal_belong = transDict['交易权属']
        list_date = transDict['挂牌时间']
        house_usage = transDict['房屋用途']
        house_age = transDict['房屋年限']
        house_belong = transDict['房权所属']

        create_time = formatDateTime(0)
        # 经纬度
        lng,lat = locationTool.getBDLocation(city_name+area_name+community_name)

        # 入库
        id = getUUID()
        chengjiaoId = chengjiaoService.addOrInsert(OnsaleEntity(id=id,
                                                                bk_id=bk_id,
                                                                province_id=province_id,
                                                                province_name=province_name,
                                                                city_id=city_id,
                                                                city_name=city_name,
                                                                area_id=area_id,
                                                                area_name=area_name,
                                                                town_id=town_id,
                                                                town_name=town_name,
                                                                title=title,
                                                                community_name=community_name,
                                                                create_time=create_time,
                                                                unit_price=unit_price,
                                                                list_price=list_price,
                                                                deal_price=deal_price,
                                                                reprice=reprice,
                                                                cost_days=cost_days,
                                                                visit_num=visit_num,
                                                                deal_date=deal_date,
                                                                list_date=list_date,
                                                                rooms=rooms,
                                                                floor_info=floor_info,
                                                                floor_area=floor_area,
                                                                actual_area=actual_area,
                                                                house_structure=house_structure,
                                                                building_type=building_type,
                                                                building_structure=building_structure,
                                                                build_year=build_year,
                                                                decorate_type=decorate_type,
                                                                north=north,
                                                                hot=hot,
                                                                elevator_rate=elevator_rate,
                                                                property_limit=property_limit,
                                                                backup_elevator=backup_elevator,
                                                                house_age=house_age,
                                                                deal_belong=deal_belong,
                                                                house_usage=house_usage,
                                                                house_belong=house_belong,
                                                                lng=lng,
                                                                lat=lat,
                                                                url=url
                                                                ))

        if chengjiaoId != id:
            logger.debug('[%s]省，[%s]市，[%s]区，[%s]商圈，[%s]楼盘，在售id：[%s]，已存在' % (province_name,
                                                                          city_name,
                                                                          area_name,
                                                                          town_name,
                                                                          community_name,
                                                                          chengjiaoId))
        else:
            logger.info('[%s]省，[%s]市，[%s]区，[%s]商圈，[%s]楼盘，在售id：[%s]，入库成功' % (province_name,
                                                                          city_name,
                                                                          area_name,
                                                                          town_name,
                                                                          community_name,
                                                                          chengjiaoId))

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


if __name__ == '__main__':

    # 定义当前处理队列
    processQueue = Config.CHENGJIAO_DETAIL_QUEUE
    p = ProcessOnsaleDetailQueue()

    try:
        p.run()
    except KeyboardInterrupt:
        logger.info('============ 手动强制关闭连接 ============')
        p.mqObj.connection.close()
