import os

import pymongo as pymongo
from fastapi import FastAPI, Response, Depends
from fastapi_login import LoginManager

import model
from apis import ChairInfoApi, UserApi

application = FastAPI()

ClIENT = pymongo.MongoClient(os.environ.get('MONGOURL'))
SECRET = os.environ.get('SECRET_KEY')

manager = LoginManager(SECRET, token_url='/users/login', use_cookie=True)

chair_apis = ChairInfoApi(ClIENT)
user_apis = UserApi(ClIENT)


@application.get('/')
async def hello_world():
    return {"hello": "World"}


@application.post('/log/info')
async def log_info(chair_info: model.ChairInfo):
    return chair_apis.log_chair_info(chair_info)


@application.post('/users/create_user')
async def create_user(user_info: model.UserInfo, response: Response):
    return user_apis.create_user(user_info, response)


@manager.user_loader
def query_user(user_id: str):
    return user_apis.query_user(user_id)


@application.post('/users/login')
async def login(data: model.UserLogin, response: Response):
    return user_apis.login(query_user(data.username), data, manager, response)


@application.get('/chair/current/temp/{chairId}')
async def get_current_temp(chairId, user=Depends(manager)):
    return chair_apis.getCurrentTemp(chairId)


@application.get('/chair/current/lum/{chairId}')
async def get_current_lum(chairId, user=Depends(manager)):
    return chair_apis.getCurrentLum(chairId)


@application.get('/chair/all/temp/{day}/chairId')
async def get_temp_all_day(chairId, day, user=Depends(manager)):
    return chair_apis.getAllTempsDay(chairId, day)
