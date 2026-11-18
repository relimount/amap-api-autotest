import allure

from api.direction import DirectionAPI
from assert_util import AssertUtil
from utils.report import mark_case


@allure.feature("路径规划")
@allure.story("公交")
@allure.severity(allure.severity_level.CRITICAL)
def test_direction_transit(case):
    mark_case(case)
    AssertUtil().assert_response(DirectionAPI().get_transit(**case["params"]), case["expect"])
