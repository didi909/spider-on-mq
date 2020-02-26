from spider.tools.webtools import myGetRequest
from spider.tools.logtools import getDefaultLogger
import json
# import decimal
from decimal import *

# 设置decimal默认经度
getcontext().prec = 10
# 初始化日志
# logger = Logger()
logger = getDefaultLogger()

class LocationTool:
    def __init__(self):
        pass


    # 根据地址获取百度经纬度
    # http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
    # 默认取第一条
    def getBDLocation(self,address,output='json'):

        ak='BQ5ngn47h1qhvnV9lAWh1NNPZaS4vTrW'
        url = '''http://api.map.baidu.com/geocoding/v3/?address=%s&output=%s&ak=%s''' % (address,output,ak)

        status_code, text, content = myGetRequest(url,0)

        resultJson =json.loads(text)
        status=resultJson['status']
        if status != 0:
            # 告警，退出
            logger.error('获取经纬度出现异常,异常代码:[%s]' % str(status))
        lng = resultJson['result']['location']['lng']
        lat = resultJson['result']['location']['lat']
        # 手工截取小数点后六位
        # print(lng)
        # print(lat)
        lng = Decimal(lng).quantize(Decimal('0.000000'))
        lat = Decimal(lat).quantize(Decimal('0.000000'))
        return  lng,lat

if __name__ == '__main__':
    location = LocationTool()
    lng,lat=location.getBDLocation('湖州汇丰花园北苑')
    # print(lng)
    # print(lat)