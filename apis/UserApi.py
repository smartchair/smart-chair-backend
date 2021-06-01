from fastapi import Response
from fastapi_login import LoginManager
from starlette import status

import model
from utils import generateHash, returnError
from utils.jsonReturnUtils import returnCreateUser, returnLogin, returnChairAddition, returnChairIds
from utils.passUtils import verify_password


class UserApi:
    def __init__(self, client):
        self.client = client

    def create_user(self, user_info: model.UserInfo, response: Response):
        if hasattr(user_info, 'id'):
            delattr(user_info, 'id')
        users_db = self.client.users['users']
        is_present = users_db.find_one({"email": user_info.email})
        if is_present is not None:
            response.status_code = status.HTTP_200_OK
            return returnError(statusCode=status.HTTP_200_OK,
                               title="Usuário já registrado",
                               detail="Email já utilizado")
        user_info.password = generateHash(user_info.password)
        new = users_db.insert_one(user_info.dict(by_alias=True))
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
                               title="Usuário não encontrado",
                               detail="Email não registrado")
        if verify_password(user['password'], data.password):
            response.status_code = status.HTTP_200_OK
            access_token = manager.create_access_token(data={'sub': data.username})
            manager.set_cookie(response, access_token)
            return returnLogin(statusCode=response.status_code, access_token=access_token)
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return returnError(statusCode=status.HTTP_401_UNAUTHORIZED,
                               title="Senha incorreta",
                               detail="A senha não está correta")

    def add_chair_user(self, user, chair: model.ChairIn, response: Response):
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return returnError(statusCode=status.HTTP_401_UNAUTHORIZED,
                               title="Usuário não encontrado",
                               detail="Email não registrado")
        else:
            filter_user = {'email': user['email']}
            new = user['chairs']
            temp_array = []
            for u in new:
                if u['chairId'] == chair.chairId:
                    u['chairNickname'] = chair.chairNickname
                temp_array.append(u['chairId'])
            if chair.chairId not in temp_array:
                new.append(dict(chair))
            new_value = {"$set": {'chairs': new}}
            self.client.users['users'].update_one(filter_user, new_value)
            response.status_code = status.HTTP_200_OK
            return returnChairAddition(statusCode=response.status_code, user_id=user['email'],
                                       chair_ids=new)

    def get_all_chairs(self, user_id, response: Response):
        users_db = self.client.users['users']
        is_present = users_db.find_one({"email": user_id})
        response.status_code = status.HTTP_200_OK
        return returnChairIds(statusCode=response.status_code, array=is_present['chairs'], userId=user_id)
