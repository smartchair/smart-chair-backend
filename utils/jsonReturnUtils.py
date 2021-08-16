from datetime import datetime
from typing import Any

import numpy

import model


def returnError(statusCode: int, title: str, detail: str):
    return {
        "errors": [
            {
                "status": statusCode,
                "title": title,
                "detail": detail
            }
        ]
    }


def returnCreateUser(statusCode: int, data: model.UserInfo):
    return {
        "data": [{
            "user": data,
            "status": statusCode
        }]
    }


def returnLogin(statusCode: int, access_token: Any):
    return {
        "data": [{
            "status": statusCode,
            "token": access_token
        }]
    }


def returnChairInfo(statusCode: int, chair_info: model.chair_info):
    return {
        "data": [{
            'status': statusCode,
            'chairInfo': chair_info
        }]
    }


def returnChairProperty(statusCode: int, propertyName: str, value: Any):
    return {
        "data": [{
            "status": statusCode,
            propertyName: value
        }]
    }


def returnChairPropertyEmpty():
    return {
        "data": [{
            "status": 201,
            "message": "Não há informações registradas para essa cadeira"
        }]
    }


def returnChairAddition(statusCode: int, user_id: str, chair_ids: []):
    return {
        'data': [{
            "status": statusCode,
            "userId": user_id,
            "chairs": chair_ids
        }]
    }


def returnChangePassword(statusCode: int):
    return {
        "data": [{
            "status": statusCode,
            "message": "Senha atualizada com sucesso"
        }]
    }


def returnChairDeletion(statusCode: int, user_id: str, chair_ids: []):
    return {
        'data': [{
            "status": statusCode,
            "userId": user_id,
            "chairs": chair_ids
        }]
    }


def returnQuestion(statusCode: int, question):
    return {
        'data': [{
            'status': statusCode,
            'question_id': str(question['_id']),
            'question': question['question']
        }]
    }


def returnAnswer(statusCode: int, answer):
    return {
        'data': [{
            'status': statusCode,
            'question_id': answer.question_id,
            'answer': answer.answer
        }]
    }


def returnChairIds(statusCode: int, array: [], userId: str):
    return {
        'data': [{
            'status': statusCode,
            "userId": userId,
            'chairs': array
        }]
    }


def returnAverageProps(valueArray: [], day: str):
    for a in valueArray:
        if not a:
            a.append(0)
    return {
        "averageTemp": numpy.mean(valueArray[0]),
        "averageLum": numpy.mean(valueArray[1]),
        "averageHum": numpy.mean(valueArray[2]),
        "averageNoise": numpy.mean(valueArray[3]),
        "day": datetime.strptime(day, "%d-%m-%y")
    }
