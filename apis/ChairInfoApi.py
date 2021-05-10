
import model


class ChairInfoApi:

    def __init__(self, client):
        self.client = client

    def log_chair_info(self, chair_info: model.ChairInfo):
        if hasattr(chair_info, 'id'):
            delattr(chair_info, 'id')
        chairs_db = self.client.chairs
        new = chairs_db["chairs"].insert_one(chair_info.dict(by_alias=True))
        chair_info.id = new.inserted_id
        return {'chairinfo': chair_info}
