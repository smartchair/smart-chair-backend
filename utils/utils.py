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
    return array


def getMeans(dates: [], means: [], prop: str):
    value0 = []
    value1 = []
    value2 = []
    value3 = []
    value4 = []
    for value in means:
        day = datetime.strptime(value['time'], '%d-%m-%y %H:%M:%S')
        if day.day == dates[0].day:
            print(day.day)
            value0.append(value[prop])
        if day.day == dates[1].day:
            print(day.day)
            value1.append(value[prop])
        if day.day == dates[2].day:
            print(day.day)
            value2.append(value[prop])
        if day.day == dates[3].day:
            print(day.day)
            value3.append(value[prop])
        if day.day == dates[4].day:
            print(day.day)
            value4.append(value[prop])

    return [
        numpy.mean(value0),
        numpy.mean(value1),
        numpy.mean(value2),
        numpy.mean(value3),
        numpy.mean(value4)
    ]
