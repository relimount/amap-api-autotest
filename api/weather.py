import requests

from config import TIMEOUT, AMAP_KEY, BASE_URL


class WeatherAPI:

    def __init__(self):
        self.session = requests.Session()
        self.timeout = TIMEOUT

    def get_weather(self, city = None, key = AMAP_KEY, **optional):
        params = {'city' : city, 'key' : key, **optional}
        params = { k: v for k, v in params.items() if v is not None }
        return self.session.get(f'{BASE_URL}v3/weather/weatherInfo', params=params, timeout=self.timeout)
        