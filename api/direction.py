import requests

from config import TIMEOUT, AMAP_KEY, BASE_URL


class DirectionAPI:
    def __init__(self):
        self.session = requests.session()
        self.timeout = TIMEOUT


    def get_walking(self, origin = None, destination = None, key = AMAP_KEY, **optional):
        params = {"origin" : origin, "destination" : destination, "key" : key ,**optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(url = f"{BASE_URL}v3/direction/walking", params = params)

    def get_transit(self, origin = None, destination = None, city = None, key = AMAP_KEY, **optional):
        params = {"origin" : origin, "destination" : destination, "city" : city, "key" : key ,**optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(url = f"{BASE_URL}v3/direction/transit/integrated", params = params)

    def get_driving(self, origin = None, destination = None, key = AMAP_KEY, **optional):
        params = {"origin" : origin, "destination" : destination, "key" : key ,**optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(url = f"{BASE_URL}v3/direction/driving", params = params)

    def get_bicycling(self, origin = None, destination = None, key = AMAP_KEY, **optional):
        params = {"origin" : origin, "destination" : destination, "key" : key ,**optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(url = f"{BASE_URL}v4/direction/bicycling", params = params)
