import os

import pymongo as pymongo
from fastapi import FastAPI, Response
from starlette import status

import model
from apis import ChairInfoApi, UserApi
from utils import generateHash

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
    return chair_apis.log_chair_info(chair_info)


@application.post('/create/user')
async def create_user(user_info: model.UserInfo, response: Response):
    if hasattr(user_info, 'id'):
        delattr(user_info, 'id')
    users_db = ClIENT.users
    is_present = users_db['users'].find_one({"email": user_info.email})
    if is_present is not None:
        response.status_code = status.HTTP_200_OK
        return {"status": 'fail'}
    user_info.password = generateHash(user_info.password).encode('utf-8')
    new = users_db['users'].insert_one(user_info.dict(by_alias=True))
    user_info.id = new.inserted_id
    response.status_code = status.HTTP_201_CREATED
    return {'status': 'success', 'data': user_info}
