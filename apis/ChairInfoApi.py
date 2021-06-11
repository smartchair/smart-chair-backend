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

    def getCurrentProp(self, chair_id: str, prop: str):
        chair = self.db.find_one({"chairId": chair_id})
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName="current" + prop, value=chair[prop])

    def getAllPropDay(self, day: str, chair_id: str, prop: str):
        temps_array = []
        for doc in self.db.find(filter={"chairId": chair_id}):
            day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
            day_arg = datetime.strptime(day, "%d-%m-%y")
            if day_doc.day == day_arg.day:
                item = {"hour": day_doc.strftime("%H:%M:%S"), prop: doc[prop]}
                temps_array.append(item)
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName=prop, value=temps_array)

    def getAllProp(self, chair_id: str, prop: str):
        props_array = []
        for doc in self.db.find(filter={"chairId": chair_id}):
            props_array.append(doc[prop])
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName=prop, value=props_array)
