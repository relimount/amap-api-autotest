import allure

from api.weather import WeatherAPI
from utils.assert_util import AssertUtil
from utils.report import mark_case


@allure.feature("天气")
@allure.story("实况与预报")
@allure.severity(allure.severity_level.CRITICAL)
def test_weather(case):
    mark_case(case)
    AssertUtil().assert_response(WeatherAPI().get_weather(**case["params"]), case["expect"])
