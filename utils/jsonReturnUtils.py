from typing import Any

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


def returnChairAddition(statusCode: int, user_id: str, chair_ids: []):
    return {
        'data': [{
            "status": statusCode,
            "email": user_id,
            "chair_ids": chair_ids
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


def returnChairIds(statusCode: int, array: []):
    return {
        'data': [{
            'status': statusCode,
            'chairs': array
        }]
    }
