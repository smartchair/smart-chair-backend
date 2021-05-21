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
