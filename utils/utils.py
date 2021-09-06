from datetime import datetime, timedelta

from utils.jsonReturnUtils import returnAverageProps


def getLast5Days(day: str):
    date_day = datetime.strptime(day, "%d-%m-%y")

    d1 = (date_day - timedelta(days=1))
    d2 = (date_day - timedelta(days=2))
    d3 = (date_day - timedelta(days=3))
    d4 = (date_day - timedelta(days=4))
    return [
        datetime.strftime(date_day, "%d-%m-%y"),
        datetime.strftime(d1, "%d-%m-%y"),
        datetime.strftime(d2, "%d-%m-%y"),
        datetime.strftime(d3, "%d-%m-%y"),
        datetime.strftime(d4, "%d-%m-%y")
    ]


def buildDayMonth(date: datetime):
    return datetime.strftime(date, "%d-%m-%y")


def getAverages(dates: [], averages: []):
    value0 = [[], [], [], []]
    value1 = [[], [], [], []]
    value2 = [[], [], [], []]
    value3 = [[], [], [], []]
    value4 = [[], [], [], []]
    returns = []
    for value in averages:
        doc = value["doc"]
        day = datetime.strftime(value['dateTime'], "%d-%m-%y")
        if day == dates[0]:
            value0[0].append(doc['temp'])
            value0[1].append(doc['lum'])
            value0[2].append(doc['hum'])
            value0[3].append(doc['noise'])
        if day == dates[1]:
            value1[0].append(doc['temp'])
            value1[1].append(doc['lum'])
            value1[2].append(doc['hum'])
            value1[3].append(doc['noise'])
        if day == dates[2]:
            value2[0].append(doc['temp'])
            value2[1].append(doc['lum'])
            value2[2].append(doc['hum'])
            value2[3].append(doc['noise'])
        if day == dates[3]:
            value3[0].append(doc['temp'])
            value3[1].append(doc['lum'])
            value3[2].append(doc['hum'])
            value3[3].append(doc['noise'])
        if day == dates[4]:
            value4[0].append(doc['temp'])
            value4[1].append(doc['lum'])
            value4[2].append(doc['hum'])
            value4[3].append(doc['noise'])

    returns.append(returnAverageProps(value0, dates[0]))
    returns.append(returnAverageProps(value1, dates[1]))
    returns.append(returnAverageProps(value2, dates[2]))
    returns.append(returnAverageProps(value3, dates[3]))
    returns.append(returnAverageProps(value4, dates[4]))

    return returns
