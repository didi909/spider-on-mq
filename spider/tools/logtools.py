#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import logging
import os.path
import time
#from dynaconf import settings as Config
from spider.config.settings import Config

project_path = ''  #定义项目目录
logHome=Config.LOG_HOME

class Logger(object):
    def __init__(self,fileNamePrefix=''):
        '''''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''

        # fileNamePrefix如果为空则使用totallog
        if fileNamePrefix == '':
            fileNamePrefix = 'total'
        current_time=time.strftime('%Y%m%d%H%M',
                                   time.localtime(time.time()))  # 返回当前时间
        # current_path=os.path.dirname(os.path.abspath(project_path))  # 返回当前目录
        # path1=current_path  #指定分隔符对字符串进行切片
        # # path1=current_path.split(project_path)  #指定分隔符对字符串进行切片
        # path2=[path1, project_path]
        # # path2=[path1[0], project_path]
        # path3=''
        # new_name=path3.join(path2) + '/logs/' #在该路径下新建下级目录
        if os.path.exists(logHome):
            new_name = logHome
        else:
            raise Exception('日志文件目录：%s不存在' % logHome)

        # dir_time注释掉，logs目录下不区分时间
        # dir_time = time.strftime('%Y%m%d', time.localtime(time.time()))  #返回当前时间的年月日作为目录名称
        dir_time = ''
        isExists=os.path.exists(new_name + dir_time)   #判断该目录是否存在
        if not isExists:
            os.makedirs(new_name + dir_time)
            print(new_name + dir_time + "目录创建成功")

        # else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(new_name + "目录 %s 已存在" % dir_time)

        try:
            # 创建一个logger(初始化logger)
            self.log = logging.getLogger(fileNamePrefix)
            # print(logging)
            # 手工清理已经存在的handlers，否则会出现日志重复打印的问题
            if len(self.log.handlers) > 0:
                tmpFileHandler = self.log.handlers[0]
                tmpStreamHandler = self.log.handlers[1]
                self.log.removeHandler(tmpFileHandler)
                self.log.removeHandler(tmpStreamHandler)

            # self.log.setLevel(logging.INFO)
            self.log.setLevel(logging.DEBUG)

            # 如果case组织结构式 /testsuit/featuremodel/xxx.py ， 那么得到的相对路径的父路径就是项目根目录
            log_name = new_name  + dir_time + '/' + fileNamePrefix+'_'+current_time + '.log'  #定义日志文件的路径以及名称

            # 创建一个handler，用于写入日志文件
            self.fh = logging.FileHandler(log_name)
            self.fh.setLevel(logging.INFO)

            # 再创建一个handler，用于输出到控制台
            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging.INFO)

            # 定义handler的输出格式 [%(filename)s] %(module)s.%(funcName)s.[line:%(lineno)d]
            formatter = logging.Formatter('[%(asctime)s] - [%(filename)s] %(module)s.%(funcName)s.[line:%(lineno)d] - %(levelname)s - %(message)s')
            self.fh.setFormatter(formatter)
            self.ch.setFormatter(formatter)

            # 给logger添加handler
            self.log.addHandler(self.fh)
            self.log.addHandler(self.ch)
        except Exception as e:
            print("输出日志失败！ %s" % e)

    # 日志接口，用户只需调用这里的接口即可，这里只定位了INFO, WARNING, ERROR三个级别的日志，可根据需要定义更多接口

    def debug(self,msg):
        self.log.debug(msg)
        # self.log.removeHandler(self.ch)
        # self.log.removeHandler(self.fh)
        return

    def info(self,msg):
        self.log.info(msg)
        # self.log.removeHandler(self.ch)
        # self.log.removeHandler(self.fh)
        return

    def warning(self,msg):
        self.log.warning(msg)
        # self.log.removeHandler(self.ch)
        # self.log.removeHandler(self.fh)
        return

    def error(self, msg):
        self.log.error(msg)
        # self.log.removeHandler(self.ch)
        # self.log.removeHandler(self.fh)
        return

    def exception(self, msg):
        self.log.exception(msg)
        # self.log.removeHandler(self.ch)
        # self.log.removeHandler(self.fh)
        return

def getDefaultLogger():
    logger = Logger()
    return logger

if __name__ == '__main__':

    logger = Logger()
    logger.debug('This is debug')
    logger.info('This is info')
    logger.warning('This is warning')
    logger.error('This is error')
    logger.exception('This is exception')