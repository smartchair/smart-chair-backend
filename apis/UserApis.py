from fastapi.openapi.models import Response
from starlette import status

import model
from utils import generateHash


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
        user_info.password = generateHash(user_info.password).encode('utf-8')
        new = users_db['users'].insert_one(user_info.dict(by_alias=True))
        user_info.id = new.inserted_id
        response.status_code = status.HTTP_201_CREATED
        return {'status': 'success', 'data': user_info}
