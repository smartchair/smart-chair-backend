from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection

import model


class ChairInfoApi:

    def __init__(self, client):
        self.client = client
        self.db = self.client.chairs["chairs"]

    def log_chair_info(self, chair_info: model.ChairInfo):
        if hasattr(chair_info, 'id'):
            delattr(chair_info, 'id')
        new = self.db.insert_one(chair_info.dict(by_alias=True))
        chair_info.id = new.inserted_id
        return {'chairinfo': chair_info}

    def getCurrentTemp(self, chair_id: str):
        chair = self.db.find_one({"chairId": chair_id})
        return {
            "currentTemp": chair['temp']
        }

    def getCurrentLum(self, chair_id: str):
        chair = self.db.find_one({"chairId": chair_id})
        return {
            "currentLum": chair['lum']
        }

    def getAllTempsDay(self, day: str, chair_id: str):
        temps_array = []
        for doc in self.db.find(filter={"chairId": chair_id}):
            day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
            day_arg = datetime.strptime(day, "%d-%m-%y")
            print("DOC " + str(day_doc.day))
            print("ARG " + str(day_arg.day))
            if day_doc.day == day_arg.day:
                temps_array.append({day_doc.hour, doc['temp']})
        return temps_array
