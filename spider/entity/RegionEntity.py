from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class RegionEntity(Base):
    # 表的名字:
    __tablename__ = 'basic_region_copy1'

    # 表的结构:
    id = Column(String(32), primary_key=True)
    name = Column(String(255))
    level = Column(Integer)
    pid = Column(String(32))
