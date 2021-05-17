from fastapi import Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

import model
from utils import generateHash
from utils.passUtils import verify_password


class UserApi:
    def __init__(self, client):
        self.client = client

    def create_user(self, user_info: model.UserInfo, response: Response):
        if hasattr(user_info, 'id'):
            delattr(user_info, 'id')
        users_db = self.client.users
        is_present = users_db['users'].find_one({"email": user_info.email})
        if is_present is not None:
            response.status_code = status.HTTP_200_OK
            return {"status": 'fail'}
        user_info.password = generateHash(user_info.password)
        new = users_db['users'].insert_one(user_info.dict(by_alias=True))
        user_info.id = new.inserted_id
        response.status_code = status.HTTP_201_CREATED
        return {'status': 'success', 'data': user_info}

    def query_user(self, user_id: str):
        users_db = self.client.users
        return users_db['users'].find_one({"email": user_id})

    @staticmethod
    def login(user, data: model.UserLogin):
        password = data.password
        print('armazenado ' + str(user['password']['key']))
        print ('enviado ' + password)
        if not user:
            return {"status": 'no user'}
        elif verify_password(user['password'], password):
            return {'status': 'wrong_pass'}
        else:
            return {'status': 'Success'}
