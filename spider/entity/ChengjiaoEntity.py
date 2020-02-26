from sqlalchemy import Column, String, Integer,Text,DateTime,DECIMAL,Date
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class OnsaleEntity(Base):
    # 表的名字:
    __tablename__ = 'cj_chengjiao'

    # 表的结构:
    id = Column(String(32),primary_key=True)
    bk_id = Column(String(32))
    province_id = Column(String(32))
    province_name = Column(String(255))
    city_id = Column(String(32))
    city_name = Column(String(255))
    area_id = Column(String(32))
    area_name = Column(String(255))
    town_id = Column(String(32))
    town_name = Column(String(255))
    create_time = Column(DateTime)

    title = Column(String(255))
    community_name = Column(String(255))
    unit_price = Column(String(255))
    list_price = Column(String(255))
    deal_price = Column(String(255))
    reprice = Column(String(32))
    cost_days = Column(String(32))
    visit_num = Column(String(32))
    deal_date = Column(String(32))
    list_date = Column(String(32))
    rooms = Column(String(32))
    floor_info = Column(String(64))
    floor_area = Column(String(32))
    actual_area = Column(String(32))
    house_structure = Column(String(32))
    building_type = Column(String(32))
    building_structure = Column(String(32))
    build_year = Column(String(32))
    decorate_type = Column(String(32))
    north = Column(String(32))
    hot = Column(String(32))
    elevator_rate = Column(String(32))
    property_limit = Column(String(32))
    backup_elevator = Column(String(32))
    house_age = Column(String(32))
    deal_belong = Column(String(32))
    house_usage = Column(String(32))
    house_belong = Column(String(32))

    lng = Column(DECIMAL(10,6))
    lat = Column(DECIMAL(10,6))
    url =  Column(String(512))
