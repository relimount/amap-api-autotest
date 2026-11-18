import requests

import config
from config import AMAP_KEY, TIMEOUT


class GeocodeAPI:

    def __init__(self):
        self.session = requests.Session()
        self.timeout = TIMEOUT

    def get_geocode(self, address = None, key = AMAP_KEY, **optional):
        params = {"address": address, "key":key, **optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(f"{config.BASE_URL}v3/geocode/geo", params=params, timeout=self.timeout)

    def get_regeo(self, location = None, key = AMAP_KEY, **optional):
        params = {"location": location, "key":key, **optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(f"{config.BASE_URL}v3/geocode/regeo", params=params, timeout=self.timeout)