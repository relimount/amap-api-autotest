import allure

from api.geocode import GeocodeAPI
from utils.assert_util import AssertUtil
from utils.report import mark_case


@allure.feature("地理编码")
@allure.story("正向与异常")
@allure.severity(allure.severity_level.CRITICAL)
def test_geocode(case):
    mark_case(case)
    AssertUtil().assert_response(GeocodeAPI().get_geocode(**case["params"]), case["expect"])
