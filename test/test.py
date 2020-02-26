
from spider.tools.commontools import commonRequest,yunProxy
from urllib.error import URLError
from urllib.request import ProxyHandler,build_opener
import requests
import re
from bs4 import BeautifulSoup

import json
# status_code, text, content = yunProxy('https://diqing.fang.ke.com/xiaoqu/',allowRedirects=False)
#
# print(text)

# status_code, text, content = yunProxy('https://hf.fang.ke.com/loupan/p_mdkjbjujh/xiangqing/')

# soup = BeautifulSoup(text, "html.parser")
# 逻辑：直接匹配 span class="label* 标签，两个一组（其中最后一个周边规划是单独一个，去掉不处理）

cityLoupanUrl = 'https://wh.ke.com/loupan'
matchObj = re.match( r'(.*)fang.ke.com(.*)', cityLoupanUrl, re.M|re.I)
if not matchObj:
    cityLoupanUrl=cityLoupanUrl.replace('ke.com','fang.ke.com')

print(cityLoupanUrl)