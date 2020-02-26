#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import platform
import requests
import datetime
import uuid
from spider.tools.logtools import getDefaultLogger

# 初始化日志
# logger = Logger()
logger = getDefaultLogger()

# 添加当前路径到环境变量
sys.path.append(os.path.dirname(__file__))

# 读取日志配置文件信息
# log_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
# logging.config.fileConfig(log_conf_path)
# logger=logging.getLogger('output')


class Timer():
    def __init__(self):
        pass

    def start(self):
        self.start_time = datetime.datetime.now()

    def end(self):
        self.end_time = datetime.datetime.now()

    def getElapseSeconds(self):
        time_cost = self.end_time - self.start_time
        return time_cost.seconds


# def getRabbitmqConnection():
#     credentials = pika.PlainCredentials(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD)
#     connection = pika.BlockingConnection(
#         pika.ConnectionParameters(host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT, virtual_host='/',
#                                   credentials=credentials))
#     logger.info('rabbitmq连接：host='+Config.RABBITMQ_HOST+
#                 ', port='+str(Config.RABBITMQ_PORT)+
#                 ',user='+Config.RABBITMQ_USER+
#                 ',password='+Config.RABBITMQ_PASSWORD)
#     return connection




# 保存二进制对象到本机
def saveBinaryToLocal(content, filename):
    # content 目标二进制content
    # filename 保存文件的绝对路径，路径+文件名
    with open(filename, 'wb') as fp:
        fp.write(content)
        fp.close()


# 增量写字符串到本机
def saveStringIncrumentToLocal(content, filename):
    # 注意，需要换行的话，自行拼接在content中
    with open(filename, 'a+') as f:
        f.write(content)


# 全量写字符串到本机
def saveStringFullToLocal(content, filename):
    with open(filename, 'w+') as f:
        f.write(content)


# 转换汉字为拼音
# def toPinyin(char_to_turn,mode):
#     p=Pinyin()
#     if mode == 'quanpin':
#         # 全拼 小写
#         result=p.get_pinyin(char_to_turn,'')
#     elif mode == 'jianpin':
#         #简拼 小写
#         result=p.get_initials(char_to_turn,'').lower()
#     elif mode=='shoupin':
#         #首拼 大写
#         result=p.get_initials(char_to_turn)[0:1]
#     else:
#         pass
#     return  result

# 获取页面编码
def getPageEncoding(url):
    r = requests.get(url)
    pageencoding = requests.utils.get_encodings_from_content(str(r.content))
    return str(pageencoding)


# 判定操作系统
def getOSType():
    current_os_type = platform.uname()[0]
    if current_os_type == 'Windows' or current_os_type == 'Linux':
        pass
    else:
        logger.exception('无法匹配的操作系统')
        raise Exception
    return current_os_type


def getUUID():
    return str(uuid.uuid1()).replace('-', '')


def formatDateTime(days):
    # 用于计算日期差，并返回可写入MySQL的datetime类型数据，例如：days=-1，表示返回昨天的 yyyy-mm-dd hh24:mi:ss 数据（datetime类型）
    dateTime = str(datetime.datetime.now() + datetime.timedelta(days=days)).split('.')[0]
    dateTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

    return dateTime


def formatDate(days):
    # 用于计算日期差，并返回可写入MySQL的datetime类型数据，例如：days=-1，表示返回昨天的 yyyy-mm-dd数据（date类型）
    dateTime = str(datetime.datetime.now() + datetime.timedelta(days=days)).split('.')[0]
    date = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S').date()
    return date
