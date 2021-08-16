from datetime import datetime

import numpy as numpy

from utils.jsonReturnUtils import returnAverageProps


def getLast5Days(day: str):
    date_day = datetime.strptime(day, "%d-%m-%y")
    return [
        datetime.strftime(date_day, "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 1), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 2), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 3), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 4), "%d-%m-%y")
    ]


def buildDayMonth(date: datetime):
    return datetime.strftime(date, "%d-%m-%y")


def getMeans(dates: [], means: []):
    value0 = [[], [], [], []]
    value1 = [[], [], [], []]
    value2 = [[], [], [], []]
    value3 = [[], [], [], []]
    value4 = [[], [], [], []]
    returns = []
    for value in means:
        day = datetime.strftime(value['dateTime'], "%d-%m-%y")
        if day == dates[0]:
            value0[0].append(value['temp'])
            value0[1].append(value['lum'])
            value0[2].append(value['hum'])
            value0[3].append(value['noise'])
            returns.append(returnAverageProps(value0, day))
        if day == dates[1]:
            value1[0].append(value['temp'])
            value1[1].append(value['lum'])
            value1[2].append(value['hum'])
            value1[3].append(value['noise'])
            returns.append(returnAverageProps(value1, day))
        if day == dates[2]:
            value2[0].append(value['temp'])
            value2[1].append(value['lum'])
            value2[2].append(value['hum'])
            value2[3].append(value['noise'])
            returns.append(returnAverageProps(value2, day))
        if day == dates[3]:
            value3[0].append(value['temp'])
            value3[1].append(value['lum'])
            value3[2].append(value['hum'])
            value3[3].append(value['noise'])
            returns.append(returnAverageProps(value3, day))
        if day == dates[4]:
            value4[0].append(value['temp'])
            value4[1].append(value['lum'])
            value4[2].append(value['hum'])
            value4[3].append(value['noise'])
            returns.append(returnAverageProps(value4, day))

    return returns
