from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import os
import sys
from spider.config.settings import Config
from spider.tools.logtools import getDefaultLogger

logger = getDefaultLogger()


# 添加当前路径到环境变量
sys.path.append(os.path.dirname(__file__))

class mysqlConnection:
    def __init__(self):
        self.session = self.getConnection()
        # pass

    def getConnection(self):
        # 初始化数据库连接:
        engine = create_engine('mysql+mysqlconnector://' +
                               Config.MYSQL_USER + ':' +
                               Config.MYSQL_PASSWORD + '@' +
                               Config.MYSQL_HOST + ':' +
                               str(Config.MYSQL_PORT) + '/' +
                               Config.MYSQL_DBNAME,
                               encoding=Config.MYSQL_CHARSET,
                               echo=Config.MYSQL_SQL_PRINT_FLAG)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        logger.info('mysql连接信息：mysql+mysqlconnector://' +
                    Config.MYSQL_USER + ':' +
                    Config.MYSQL_PASSWORD + '@' +
                    Config.MYSQL_HOST + ':' +
                    str(Config.MYSQL_PORT) + '/' +
                    Config.MYSQL_DBNAME)
        return self.session

    def query(self, entites, **kwargs):
        return self.session.query(entites, **kwargs)

    def closeConnection(self):
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    # 提交一条
    def addOne(self, entity):
        self.session.add(entity)
        self.session.commit()

    # 批量提交
    def addBatch(self, entityList):
        # 设置一个批次的数量
        batchNum = 500
        counter = 0
        for entity in entityList:

            self.session.add(entity)
            counter += 1

            if counter == batchNum:
                self.session.commit()
                counter = 0

        self.session.commit()

    # 根据主键删除
    # def deleteById(self):