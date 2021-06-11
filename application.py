import os

import pymongo as pymongo
from fastapi import FastAPI, Response, Depends
from fastapi_login import LoginManager

import model
from apis import ChairInfoApi, UserApi
from apis.QuestionsApi import QuestionApi
from model.chair_info import GetPropModel

application = FastAPI()

ClIENT = pymongo.MongoClient(os.environ.get('MONGOURL'))
SECRET = os.environ.get('SECRET_KEY')

manager = LoginManager(SECRET, token_url='/users/login', use_cookie=True)

chair_apis = ChairInfoApi(ClIENT)
user_apis = UserApi(ClIENT)
question_apis = QuestionApi(ClIENT)


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


@application.get('/chair/day/{prop}')
async def get_prop_all_day(prop: str, getTempModel: GetPropModel, user=Depends(manager)):
    return chair_apis.getAllPropDay(day=getTempModel.day, chair_id=getTempModel.chairId, prop=prop)


@application.get('/chair/all/{prop}/{chairId}')
async def get_prop_all(prop: str, chairId: str):
    return chair_apis.getAllProp(chairId, prop=prop)


@application.post('/users/{userId}/add-chair')
async def add_user_chair(userId, chairUser: model.ChairIn, response: Response, user=Depends(manager)):
    return user_apis.add_chair_user(user=query_user(userId), response=response, chair=chairUser)


@application.post('/users/{userId}/remove-chair')
async def remove_user_chair(userId, chairUser: model.ChairIn, response: Response, user=Depends(manager)):
    return user_apis.remove_chair_user(user=query_user(userId), response=response, chair=chairUser)


@application.get('/questions')
async def get_question(user=Depends(manager)):
    return question_apis.loadQuestion()


@application.post('/questions/answer')
async def post_answer(answer: model.AnswerIn, user=Depends(manager)):
    return question_apis.postAnswer(answer)


@application.get('/users/{userId}/get-chairs')
async def get_chairs(userId, response: Response, user=Depends(manager)):
    return user_apis.get_all_chairs(userId, response)
