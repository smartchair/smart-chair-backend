from datetime import datetime

import numpy as numpy


def getLast5Days(day: str):
    date_day = datetime.strptime(day, "%d-%m-%y")
    array = [
        datetime.strftime(date_day, "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 1), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 2), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 3), "%d-%m-%y"),
        datetime.strftime(date_day.replace(day=date_day.day - 4), "%d-%m-%y")
    ]
    print(array)
    return array


def buildDayMonth(date: datetime):
    abc = datetime.strftime(date, "%d-%m-%y")
    return abc


def getMeans(dates: [], means: [], prop: str):
    value0 = []
    value1 = []
    value2 = []
    value3 = []
    value4 = []
    for value in means:
        day = datetime.strftime(value['dateTime'], "%d-%m-%y")
        print(day)
        if day == dates[0]:
            value0.append(value[prop])
        if day == dates[1]:
            value1.append(value[prop])
        if day == dates[2]:
            value2.append(value[prop])
        if day == dates[3]:
            value3.append(value[prop])
        if day == dates[4]:
            value4.append(value[prop])

    return [
        numpy.mean(value0),
    ]
