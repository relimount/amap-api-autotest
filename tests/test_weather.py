from api.weather import WeatherAPI
from assert_util import AssertUtil



def test_weather(case):
    AssertUtil().assert_response(WeatherAPI().get_weather(**case["params"]), case["expect"])