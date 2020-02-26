from spider.entity.RegionEntity import RegionEntity
from spider.tools.dbtools import mysqlConnection


class RegionService:
    def __init__(self):
        # 初始化mysql连接
        self.mysqlSession = mysqlConnection()

    def addOrInsert(self, entity):
        # 判断是否存在
        oneResult = self.mysqlSession.query(RegionEntity).filter(RegionEntity.pid == entity.pid,
                                                                 RegionEntity.name == entity.name,
                                                                 RegionEntity.level == entity.level).first()
        if oneResult:
            # 如果存在
            return oneResult.id
        else:
            # 插入
            self.mysqlSession.addOne(entity)
            return entity.id

    def getIdByNameLevel(self, name, level):
        resultSet = self.mysqlSession.query(RegionEntity).filter(RegionEntity.name.like(name + '%'),
                                                     RegionEntity.level == level).first()

        id = resultSet.id

        return id
