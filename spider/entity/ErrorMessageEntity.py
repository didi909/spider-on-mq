from sqlalchemy import Column, String,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class ErrorMessageEntity(Base):
    # 表的名字:
    __tablename__ = 'bk_error_message'

    # 表的结构:
    id = Column(String(32), primary_key=True)
    run_id =Column(String(32))
    file_name=Column(String(255))
    message =Column(String(8000))
    create_time =Column(DateTime)
    soup = Column(Text)