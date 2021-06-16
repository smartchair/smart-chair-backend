from datetime import datetime

import pytz
from starlette import status

import model
from utils.jsonReturnUtils import returnChairInfo, returnChairProperty


class ChairInfoApi:

    def __init__(self, client):
        self.client = client
        self.db = self.client.chairs

    def log_chair_info(self, chair_info: model.ChairInfoIn):

        timezone = pytz.timezone('America/Sao_Paulo')
        date = timezone.localize(datetime.now())
        official = date.replace(hour=(date.hour - 3))
        time = official.strftime("%d-%m-%y %H:%M:%S")

        chairInfo_db = model.ChairInfo(id=chair_info.id,
                                       chairId=chair_info.chairId,
                                       temp=chair_info.temp,
                                       presence=chair_info.presence,
                                       noise=chair_info.noise,
                                       lum=chair_info.lum,
                                       hum=chair_info.hum,
                                       time=time)
        if hasattr(chairInfo_db, 'id'):
            delattr(chairInfo_db, 'id')
        new = self.db["chairs"].insert_one(chairInfo_db.dict(by_alias=True))
        chairInfo_db.id = new.inserted_id
        return returnChairInfo(statusCode=status.HTTP_200_OK, chair_info=chair_info)

    def getCurrentProp(self, chair_id: str, prop: str):
        chair = self.db["chairs"].find_one({"chairId": chair_id})
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName="current" + prop.capitalize(),
                                   value=chair[prop])

    def getAllPropDay(self, day: str, chair_id: str, prop: str):
        temps_array = []
        for doc in self.db["chairs"].find(filter={"chairId": chair_id}):
            day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
            day_arg = datetime.strptime(day, "%d-%m-%y")
            if day_doc.day == day_arg.day:
                item = {"hour": day_doc.strftime("%H:%M:%S"), prop: doc[prop]}
                temps_array.append(item)
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName=prop.capitalize(), value=temps_array)

    def getAllProp(self, chair_id: str, prop: str):
        props_array = []
        for doc in self.db["chairs"].find(filter={"chairId": chair_id}):
            props_array.append(doc[prop])
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName=prop.capitalize() + 's',
                                   value=props_array)

    def postLum(self, postLum: model.postLum):
        new = self.db["lums"].insert_one(postLum.dict(by_alias=True))
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName='Lum', value=postLum)

    def getAllLums(self, userId: str):
        lumArray = []
        for doc in self.db['lums'].find(filter={"userId": userId}):
            lumArray.append(doc['lum'])
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName='Lums',
                                   value=lumArray)
