from spider.entity.OnsaleEntity import OnsaleEntity
from spider.tools.dbtools import mysqlConnection


class OnsaleService:
    def __init__(self):
        # 初始化mysql连接
        self.mysqlSession = mysqlConnection()

    def addOrInsert(self, entity):
        # 判断是否存在
        oneResult = self.mysqlSession.query(OnsaleEntity).filter(OnsaleEntity.bk_id == entity.bk_id).first()
        if oneResult:
            # 如果存在
            return oneResult.id
        else:
            # 插入
            self.mysqlSession.addOne(entity)
            return entity.id
        # self.mysqlSession.addOne(entity)
        # return entity.id

    def getZeroLocationByCityName(self, cityName):

        resultSet = self.mysqlSession.query(OnsaleEntity).filter(OnsaleEntity.lng == 0,
                                                                    OnsaleEntity.city_name == cityName).all()

        return resultSet

    def updateLngLatById(self, id, lng, lat):

        try:
            self.mysqlSession.query(OnsaleEntity).filter(OnsaleEntity.id == id).update(
                {OnsaleEntity.lng: lng, OnsaleEntity.lat: lat})
            self.mysqlSession.commit()
        except:
            self.mysqlSession.rollback()


