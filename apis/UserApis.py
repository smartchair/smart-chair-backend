from fastapi import Response
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from starlette import status

import model
from utils import generateHash, returnError
from utils.jsonReturnUtils import returnCreateUser, returnLogin
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
            response.status_code = status.HTTP_204_NO_CONTENT
            return returnError(statusCode=status.HTTP_204_NO_CONTENT,
                               title="user already registered",
                               detail="email already taken")
        user_info.password = generateHash(user_info.password)
        new = users_db['users'].insert_one(user_info.dict(by_alias=True))
        user_info.id = new.inserted_id
        response.status_code = status.HTTP_201_CREATED
        return returnCreateUser(response.status_code, user_info)

    def query_user(self, user_id: str):
        users_db = self.client.users
        return users_db['users'].find_one({"email": user_id})

    @staticmethod
    def login(user, data: model.UserLogin, manager: LoginManager, response: Response):
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return returnError(statusCode=status.HTTP_401_UNAUTHORIZED,
                               title="user not found",
                               detail="email not registered")
        if verify_password(user['password'], data.password):
            response.status_code = status.HTTP_200_OK
            access_token = manager.create_access_token(data={'sub': data.username})
            return returnLogin(statusCode=response.status_code, access_token=access_token)
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return returnError(statusCode=status.HTTP_401_UNAUTHORIZED,
                               title="Wrong password",
                               detail="Password did not match")
