from bs4 import BeautifulSoup
import json
# from dynaconf import settings as Config
from spider.config.settings import Config
from spider.tools.logtools import Logger
from spider.tools.commontools import getUUID, Timer
from spider.tools.webtools import myGetRequest
from spider.tools.mqtools import rabbitmqConnection
from spider.service.RegionService import RegionService
import traceback
import os
import re

# 捕获每个城市url
# 打开城市新房页面
# 打开每个区域进行遍历，在区域的list中就有楼盘的区域商圈信息

currentFileName = os.path.basename(os.path.realpath(__file__))
logger = Logger(currentFileName.replace('.py',''))


allCityPageUrl = "https://www.ke.com/city/"
chengjiaoUri = '/ershoufang/'

regionService = RegionService()


class ProcessProvinceQueue:
    def __init__(self):
        # self.queueName = queueName
        # 初始化消息队列
        self.mqObj = rabbitmqConnection()
        self.pushChannel = self.mqObj.getChannel(targetQueue)
        # 获取runId
        self.run_id = getUUID()

    def run(self):
        try:
            status_code, text, content = myGetRequest(allCityPageUrl, Config.PROXY_FLAG)
            html_data = text
            soup = BeautifulSoup(html_data, "html.parser")
            allProviceElements = soup.find_all('div', class_="city_province")

            for p in allProviceElements:

                province_name = p.find_all('div', class_="city_list_tit c_b")[0].getText().strip()
                province_id = regionService.getIdByNameLevel(province_name, Config.PROVINCE_LEVEL)
                # print(province_name)
                # if province_name != '陕西':
                #     continue
                print(province_name)
                if province_name=='美国':
                    break
                logger.info('处理[%s]省' % (province_name))
                # 处理城市数据



                for c in p.find_all('li', class_="CLICKDATA"):
                    # 组装数据，推送到城市队列
                    city_name = c.getText().strip()
                    # if city_name !='西安':
                    #     continue

                    # id = getUUID()
                    cityUrl = 'https:' + c.find_all('a')[0]['href']
                    logger.info('处理[%s]市,cityUrl：[%s]' % (city_name, cityUrl))

                    # 判断城市是否有楼盘
                    cityOnsaleUrl = cityUrl + chengjiaoUri
                    # matchObj = re.match( r'(.*)fang.ke.com(.*)', cityOnsaleUrl, re.M|re.I)
                    # if not matchObj:
                    #     cityOnsaleUrl=cityOnsaleUrl.replace('ke.com','fang.ke.com')

                    dict={
                        'province_id':province_id,
                        'province_name':province_name,
                        'city_name':city_name,
                        'cityUrl':cityUrl,
                        'cityOnsaleUrl':cityOnsaleUrl
                    }

                    self.pushResult(dict)

                    # 由于在售数据量比较大，先只获取各省会城市的数据
                    exit()

        except Exception:
            # 打印异常
            traceback.print_exc()
            # 推送异常
            error_message = traceback.format_exc()
            dict = {'run_id': self.run_id, 'file_name': currentFileName, 'error_message': error_message, 'soup': ''}
            self.mqObj.pushMessageToMq(Config.ERROR_QUEUE, json.dumps(dict))

    def pushResult(self,dict):
        # 推送小区明细队列
        self.mqObj.pushMessageToMq(targetQueue, json.dumps(dict))



if __name__ == '__main__':

    # 定义当前处理队列
    # processQueue = Config.CITY_QUEUE
    # 定义处理完成后推送的队列
    targetQueue = Config.CITY_QUEUE

    d = ProcessProvinceQueue()

    timer = Timer()

    try:
        timer.start()
        # d.runRegions()
        d.run()
        # d.runHouseSummary()
        timer.end()

        logger.info('运行正常结束，耗时：%s秒' % str(timer.getElapseSeconds()))
    except KeyboardInterrupt:
        logger.info('============ 手动强制关闭连接 ============')
        logger.info('耗时：%s秒' % str(timer.getElapseSeconds()))
