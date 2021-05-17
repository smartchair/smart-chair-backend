import os

import pymongo as pymongo
from fastapi import FastAPI, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException

import model
from apis import ChairInfoApi, UserApi
from utils.passUtils import verify_password

application = FastAPI()

ClIENT = pymongo.MongoClient(os.environ.get('MONGOURL'))
SECRET = os.environ.get('SECRET_KEY')

manager = LoginManager(SECRET, token_url='/users/login')

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
async def login(data: model.UserLogin):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        return {"status":'no user'}
    elif verify_password(user['password'], password):
        return {'status':'wrong_pass'}

    return {'status': 'Success'}
