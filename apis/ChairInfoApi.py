import model


class ChairInfoApi:

    def __init__(self, client):
        self.client = client
        self.client = self.client.chairs["chairs"]

    def log_chair_info(self, chair_info: model.ChairInfo):
        if hasattr(chair_info, 'id'):
            delattr(chair_info, 'id')
        new = self.client.insert_one(chair_info.dict(by_alias=True))
        chair_info.id = new.inserted_id
        return {'chairinfo': chair_info}

    def getCurrentTemp(self, chair_id: str):
        chair = self.client.find_one({"chairId": chair_id})
        return {
            "chairId": chair.chairId,
            "currentTemp": chair.temp
        }

    def getCurrentLum(self, chair_id: str):
        chair = self.client.find_one({"chairId": chair_id})
        print(chair)
        return {
            "currentLum": chair.lum
        }
