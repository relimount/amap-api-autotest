import requests

from config import AMAP_KEY, BASE_URL, TIMEOUT


class GeocodeAPI:

    def __init__(self):
        self.session = requests.Session()
        self.timeout = TIMEOUT
        self.session.params = {"key": AMAP_KEY}

    def get_geocode(self, address = None, **optional):
        params = {"address": address, **optional}
        params = {k: v for k, v in params.items() if v is not None}
        return self.session.get(f"{BASE_URL}v3/geocode/geo", params=params, timeout=self.timeout)