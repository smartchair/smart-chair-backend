from datetime import datetime

import pymongo
import pytz
from starlette import status

import model
from utils import getLast5Days, getAverages, buildDayMonth
from utils.jsonReturnUtils import returnChairInfo, returnChairProperty, returnChairPropertyEmpty, \
    returnCurrentChairProperty


class ChairInfoApi:

    def __init__(self, client):
        self.client = client
        self.db = self.client.chairs

    def log_chair_info(self, chair_info: model.ChairInfoIn):

        date = datetime.now()
        timezone = pytz.timezone("America/Sao_Paulo")
        date_and_time_sp = date.astimezone(timezone)
        time = date_and_time_sp.strftime("%d-%m-%y %H:%M:%S")

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
        chair = self.db["chairs"].find_one({"chairId": chair_id}, sort=[('_id', pymongo.DESCENDING)])
        if chair is None:
            return returnChairPropertyEmpty()
        else:
            day_doc = datetime.strptime(chair['time'], '%d-%m-%y %H:%M:%S')
            time = {
                "hour": day_doc.strftime('%H:%M:%S'),
                "day": day_doc.strftime('%d-%m-%y'),
            }
            return returnCurrentChairProperty(statusCode=status.HTTP_200_OK,
                                              propertyName="current" + prop.capitalize(),
                                              value=chair[prop],
                                              time=time)

    def getAllPropDay(self, day: str, chair_id: str, prop: str):
        temps_array = []
        chairs = self.db["chairs"].find(filter={"chairId": chair_id})
        if chairs is None:
            return returnChairPropertyEmpty()
        else:
            for doc in chairs:
                day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
                day_doc_str = datetime.strftime(day_doc, "%d-%m-%y")
                if day_doc_str == day:
                    item = {"hour": day_doc.strftime('%H:%M:%S'),
                            "day": day_doc.strftime('%d-%m-%y'),
                            prop: doc[prop]}
                    temps_array.append(item)
            return returnChairProperty(statusCode=status.HTTP_200_OK,
                                       propertyName=prop.capitalize(),
                                       value=temps_array)

    def getAllProp(self, chair_id: str, prop: str):
        props_array = []
        chairs = self.db["chairs"].find(filter={"chairId": chair_id})
        if chairs is None:
            return returnChairPropertyEmpty()
        else:
            for doc in chairs:
                item = {"dateTime": doc['time'],
                        prop: doc[prop]}
                props_array.append(item)
            return returnChairProperty(statusCode=status.HTTP_200_OK,
                                       propertyName=prop.capitalize() + 's',
                                       value=props_array)

    def postLum(self, postLum: model.postLum):
        self.db["lums"].insert_one(postLum.dict(by_alias=True))
        return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName='Lum', value=postLum)

    def getAllLums(self, userId: str):
        lumArray = []
        lums = self.db['lums'].find(filter={"userId": userId})
        if lums is None:
            return returnChairPropertyEmpty()
        else:
            for doc in lums:
                lumArray.append(doc['lum'])
            return returnChairProperty(statusCode=status.HTTP_200_OK, propertyName='Lums',
                                       value=lumArray)

    def getPropAverage(self, chair_id: str, date: str):
        dates = getLast5Days(date)
        means = []
        chairs = self.db["chairs"].find(filter={"chairId": chair_id}, sort=[('_id', pymongo.DESCENDING)])
        if chairs is None:
            return returnChairPropertyEmpty()
        else:
            for doc in chairs:
                day_doc = datetime.strptime(doc['time'], '%d-%m-%y %H:%M:%S')
                test = buildDayMonth(day_doc)
                if test in dates:
                    item = {"dateTime": day_doc,
                            "doc": doc}
                    means.append(item)

        return getAverages(dates, means)
