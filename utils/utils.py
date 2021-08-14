from datetime import datetime

import numpy as numpy


def getLast5Days(day: str):
    date_day = datetime.strptime(day, "%d-%m-%y")
    array = [
        date_day,
        date_day.replace(day=date_day.day - 1),
        date_day.replace(day=date_day.day - 2),
        date_day.replace(day=date_day.day - 3),
        date_day.replace(day=date_day.day - 4)
    ]
    print(array)
    return array


def getMeans(dates: [], means: [], prop: str):
    value0 = []
    value1 = []
    value2 = []
    value3 = []
    value4 = []
    for value in means:
        if value["dateTime"].day == dates[0].day:
            value0.append(value[prop])
        if value["dateTime"].day == dates[1].day:
            value1.append(value[prop])
        if value["dateTime"].day == dates[2].day:
            value2.append(value[prop])
        if value["dateTime"].day == dates[3].day:
            value3.append(value[prop])
        if value["dateTime"].day == dates[4].day:
            value4.append(value[prop])

    return [
        numpy.mean(value0),
        numpy.mean(value1),
        numpy.mean(value2),
        numpy.mean(value3),
        numpy.mean(value4)
    ]
