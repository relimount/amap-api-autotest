import allure

from api.direction import DirectionAPI
from utils.assert_util import AssertUtil
from utils.report import mark_case


@allure.feature("路径规划")
@allure.story("骑行")
@allure.severity(allure.severity_level.CRITICAL)
def test_direction_bicycling(case):
    mark_case(case)
    AssertUtil().assert_response(DirectionAPI().get_bicycling(**case["params"]), case["expect"])
