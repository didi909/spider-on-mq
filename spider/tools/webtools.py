
import sys
import os
import requests
import random
from spider.tools.logtools import getDefaultLogger
from spider.tools.commontools import Timer

# 初始化日志
# logger = Logger()
logger = getDefaultLogger()

# 添加当前路径到环境变量
sys.path.append(os.path.dirname(__file__))

# 读取日志配置文件信息
# log_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
# logging.config.fileConfig(log_conf_path)
# logger=logging.getLogger('output')

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


agents = [
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)"]

agents1 = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

# 调用亿牛云ip代理
# @retry(MaxRetryError,tries=3,delay=2)
def yunProxy(targetUrl, allowRedirects=True):
    # 要访问的目标页面
    # targetUrl = "http://httpbin.org/ip"

    # 要访问的目标HTTPS页面
    # targetUrl = "https://httpbin.org/ip"

    # 代理服务器
    proxyHost = "u2603.b5.t.16yun.cn"
    proxyPort = "6460"

    # 代理隧道验证信息
    proxyUser = "16GTRVNW"
    proxyPass = "113964"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    # 设置 http和https访问都是用HTTP代理
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    #  设置IP切换头
    tunnel = random.randint(1, 10000)
    # headers = {"Proxy-Tunnel": str(tunnel)}
    headers = {
        'User-Agent': random.choice(agents),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Proxy-Tunnel': str(tunnel),
        # 'cookie': 'id58=vCaRgFxrouXR187muEsGMQ==; 58tj_uuid=bf456b38-1bbf-4e08-bf27-244ab4a11670; als=0; xxzl_deviceid=mKFYo9GTUvguayxW6CBGsGWwzJEZe6c4mTLDsAC0X5OzLJEIUr7G%2BbHAr6EJH4pU; wmda_uuid=b6d906965f553d71f61539464a9cf059; wmda_new_uuid=1; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1566350992; gr_user_id=e62e057f-73a9-487c-bdfb-e2e84ab4d078; sessionid=91402a68-11d7-4b77-ac83-c1cc3ea86932; duibiId=; __utma=253535702.1300739056.1576759806.1576759806.1576759806.1; __utmc=253535702; __utmz=253535702.1576759806.1.1.utmcsr=wh.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/hongshan/hezu/1/; myfeet_tooltip=end; city=wh; 58home=wh; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1577245612; Hm_lpvt_3bb04d7a4ca3846dcc66a99c3e861511=1577245612; Hm_lvt_e15962162366a86a6229038443847be7=1577245613; Hm_lpvt_e15962162366a86a6229038443847be7=1577245613; wmda_visited_projects=%3B2385390625025%3B1409632296065%3B11187958619315%3B1731916484865%3B7405785748279; dirname=wh; cid=158; fang_user_common=914b55e092eb1a2e6ae3884b94d10865; crmvip=""; dk_cookie=""; fcity=wh; addaction=041201_1578110517389; xxzl_smartid=5f931eb77e7e58cc55c5c2053721111c; vip=vipusertype%3D0%26vipuserpline%3D0%26v%3D1%26vipkey%3D75e50469c43873a4bb9d8c6f6c26e976%26masteruserid%3D56772097627927; wmda_visited_projects=%3B2385390625025%3B1409632296065%3B11187958619315%3B1731916484865%3B3381039819650%3B10104579731767%3B2286118353409; www58com="UserID=68648617763084&UserName=ycajlls2h"; 58cooper="userid=68648617763084&username=ycajlls2h"; 58uname=ycajlls2h; xxzl_cid=e08ba0f8d97643c9a7b7d13fb999539b; xzuid=905af901-2ca9-4b3b-a219-8d9abcfa469d; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; new_uv=75; popup_loginstab_second=1; ppStore_fingerprint=34657F769A297AE69A00D1EE0698769F9ED960F8523C5CDD%EF%BC%BF1579054775701; PPU="UID=68648617763084&UN=ycajlls2h&TT=50436d536134f04c20f07b5564f15b39&PBODY=LT-AaU0XZ6TE5LUf7RtNzqDHoPL7JvrjsOor2B2eamULOTo4YXbI5iF7C6m1uKhZQRbD1YV916NKhLZ7ZuP-vwBKa3j429xQrPRXY5k-wjPZiCH3G6GRTsfnkjsqVo66HglA-KVCwo-iBdZNIV1Cut61f30FgB-cVSVxGcK1ERw&VER=1"; wmda_session_id_7405785748279=1579062996639-aa172b1b-5ce8-c4b1'

    }
    timer = Timer()
    timer.start()
    resp = requests.get(targetUrl, proxies=proxies, headers=headers, allow_redirects=allowRedirects)
    timer.end()
    logger.debug('url：[%s]，耗时：[%s]秒' % (targetUrl, str(timer.getElapseSeconds())))
    # status_code 状态码，int
    # text htlm信息
    # content 二进制信息，用于下载图片
    return resp.status_code, resp.text, resp.content


def myGetRequest(url, mode, allowRedirects=True):
    if mode == 1:
        # 执行代理模式
        status_code, text, content = yunProxy(url, allowRedirects)
    else:
        # 执行常规模式
        status_code, text, content = commonRequest(url)

    return status_code, text, content


def commonRequest(targetUrl):
    #  设置IP切换头
    tunnel = random.randint(1, 10000)

    headers = {
        'User-Agent': random.choice(agents),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    resp = requests.get(targetUrl, headers=headers)
    return resp.status_code, resp.text, resp.content


def checkCodeRequest(targetUrl):
    #  设置IP切换头
    tunnel = random.randint(1, 10000)

    headers = {
        'User-Agent': random.choice(agents),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'cookie': 'id58=vCaRgFxrouXR187muEsGMQ==; 58tj_uuid=bf456b38-1bbf-4e08-bf27-244ab4a11670; als=0; xxzl_deviceid=mKFYo9GTUvguayxW6CBGsGWwzJEZe6c4mTLDsAC0X5OzLJEIUr7G%2BbHAr6EJH4pU; wmda_uuid=b6d906965f553d71f61539464a9cf059; wmda_new_uuid=1; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1566350992; gr_user_id=e62e057f-73a9-487c-bdfb-e2e84ab4d078; sessionid=91402a68-11d7-4b77-ac83-c1cc3ea86932; duibiId=; __utma=253535702.1300739056.1576759806.1576759806.1576759806.1; __utmc=253535702; __utmz=253535702.1576759806.1.1.utmcsr=wh.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/hongshan/hezu/1/; myfeet_tooltip=end; city=wh; 58home=wh; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1577245612; Hm_lpvt_3bb04d7a4ca3846dcc66a99c3e861511=1577245612; Hm_lvt_e15962162366a86a6229038443847be7=1577245613; Hm_lpvt_e15962162366a86a6229038443847be7=1577245613; wmda_visited_projects=%3B2385390625025%3B1409632296065%3B11187958619315%3B1731916484865%3B7405785748279; dirname=wh; cid=158; fang_user_common=914b55e092eb1a2e6ae3884b94d10865; crmvip=""; dk_cookie=""; fcity=wh; addaction=041201_1578110517389; xxzl_smartid=5f931eb77e7e58cc55c5c2053721111c; vip=vipusertype%3D0%26vipuserpline%3D0%26v%3D1%26vipkey%3D75e50469c43873a4bb9d8c6f6c26e976%26masteruserid%3D56772097627927; wmda_visited_projects=%3B2385390625025%3B1409632296065%3B11187958619315%3B1731916484865%3B3381039819650%3B10104579731767%3B2286118353409; www58com="UserID=68648617763084&UserName=ycajlls2h"; 58cooper="userid=68648617763084&username=ycajlls2h"; 58uname=ycajlls2h; xxzl_cid=e08ba0f8d97643c9a7b7d13fb999539b; xzuid=905af901-2ca9-4b3b-a219-8d9abcfa469d; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; new_uv=75; popup_loginstab_second=1; ppStore_fingerprint=34657F769A297AE69A00D1EE0698769F9ED960F8523C5CDD%EF%BC%BF1579054775701; PPU="UID=68648617763084&UN=ycajlls2h&TT=50436d536134f04c20f07b5564f15b39&PBODY=LT-AaU0XZ6TE5LUf7RtNzqDHoPL7JvrjsOor2B2eamULOTo4YXbI5iF7C6m1uKhZQRbD1YV916NKhLZ7ZuP-vwBKa3j429xQrPRXY5k-wjPZiCH3G6GRTsfnkjsqVo66HglA-KVCwo-iBdZNIV1Cut61f30FgB-cVSVxGcK1ERw&VER=1"; wmda_session_id_7405785748279=1579062996639-aa172b1b-5ce8-c4b1'
    }

    resp = requests.get(targetUrl, headers=headers)
    return resp.status_code, resp.text, resp.content


def commonPost(targetUrl, allowRedirects):
    #  设置IP切换头
    tunnel = random.randint(1, 10000)

    headers = {
        'User-Agent': random.choice(agents),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Proxy-Tunnel': str(tunnel)
    }

    resp = requests.post(targetUrl, headers=headers, allow_redirects=allowRedirects)
    return resp.status_code, resp.text, resp.content
