import os

import pymongo as pymongo
from fastapi import FastAPI
from fastapi.openapi.models import Response

import model
from apis import ChairInfoApi, UserApi

application = FastAPI()

ClIENT = pymongo.MongoClient(os.environ.get('MONGOURL'))
# SECRET = os.environ.get('SECRET_KEY')

chair_apis = ChairInfoApi(ClIENT)
user_apis = UserApi(ClIENT)


@application.get('/')
async def hello_world():
    return {"hello": "World"}


@application.post('/log/info')
async def log_info(chair_info: model.ChairInfo):
    chair_apis.log_chair_info(chair_info)


@application.post('/create/user')
async def create_user(user_info: model.UserInfo, response: Response):
    return user_apis.create_user(user_info=user_info, response=response)
