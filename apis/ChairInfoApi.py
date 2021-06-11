from datetime import datetime

from starlette import status

import model
from utils.jsonReturnUtils import returnChairInfo, returnChairProperty


class ChairInfoApi:

    def __init__(self, client):
        self.client = client
        self.db = self.client.chairs["chairs"]

    def log_chair_info(self, chair_info: model.ChairInfo):
        if hasattr(chair_info, 'id'):
            delattr(chair_info, 'id')
        new = self.db.insert_one(chair_info.dict(by_alias=True))
        chair_info.id = new.inserted_id
        return returnChairInfo(statusCode=status.HTTP_200_OK, chair_info=chair_info)

    def getCurrentTemp(self, chair_id: str):
        chair = self.db.find_one({"chairId": chair_id})
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName="currentTemp", value=chair['temp'])

    def getCurrentLum(self, chair_id: str):
        chair = self.db.find_one({"chairId": chair_id})
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName="currentLum", value=chair['lum'])

    def getAllPropDay(self, day: str, chair_id: str, prop: str):
        temps_array = []
        for doc in self.db.find(filter={"chairId": chair_id}):
            day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
            day_arg = datetime.strptime(day, "%d-%m-%y")
            if day_doc.day == day_arg.day:
                item = {"hour": day_doc.strftime("%H:%M:%S"), prop: doc[prop]}
                temps_array.append(item)
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName=prop, value=temps_array)

    def getAllProp(self, chair_id: str, prop:str):
        doc = self.db.find(filter={"chairId": chair_id})
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName="temps", value=doc['temp'])

