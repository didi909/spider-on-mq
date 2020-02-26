# -*- coding: utf-8 -*-
# dynaconf用法：
#     默认情况下，dyanconf从项目根目录下的settings.py文件中读取配置，并且所有的大写变量将会被读取
#     如果不希望配置跟随项目，可以通过系统环境变量来指定配置文件的位置
#         # using module name
#         export DYNACONF_SETTINGS=myproject.production_settings
#         # or using location path
#         export DYNACONF_SETTINGS=/etc/myprogram/settings.py
#     也可以读取系统环境变量中的配置
import os

class Config:
    # 数据库配置
    MYSQL_HOST='127.0.0.1'
    MYSQL_PORT=3306
    MYSQL_USER='root'
    MYSQL_PASSWORD='root~1234'
    MYSQL_DBNAME='spider'
    MYSQL_CHARSET='utf8'
    MYSQL_SQL_PRINT_FLAG=False

    # 消息队列配置
    RABBITMQ_HOST='127.0.0.1'
    RABBITMQ_PORT=5772
    RABBITMQ_USER='guest'
    RABBITMQ_PASSWORD='guest'
    RABBITMQ_VIRTUAL_HOST='/onsale'


    # 系统配置
    # 是否使用代理模式 1-使用代理，2-不使用
    PROXY_FLAG = 1
    # 日志目录配置，迁移使用前注意修改
    # LOG_HOME = '/Users/admin/Documents/py/bk-loupan/logs'
    LOG_HOME = os.path.dirname(os.path.abspath(__file__))+'/../../logs'
    # LOG_HOME = '/app/py/bk/logs'
    #区域
    COUNTRY_LEVEL = 1
    PROVINCE_LEVEL = 2
    CITY_LEVEL = 3
    AREA_LEVEL = 4
    TOWN_LEVEL = 5

    # 消息队列（勿随意更改）
    # 1 省份队列
    PROVINCE_QUEUE='provinceQueue'
    # 2 城市队列
    CITY_QUEUE='cityQueue'
    # 3 区域队列
    AREA_QUEUE='areaQueue'
    # 4 商圈按页队列
    TOWN_BY_PAGE_QUEUE = 'townByPageQueue'
    # 5 在售明细队列
    CHENGJIAO_DETAIL_QUEUE='chengjiaoDetailQueue'
    # 错误队列
    ERROR_QUEUE = 'errorQueue'

    # 临时增加
    LNGLAT_QUEUE = 'lnglatQueue'

    # 业务配置
