import allure

from api.geocode import GeocodeAPI
from utils.assert_util import AssertUtil
from utils.report import mark_case


@allure.feature("地理编码")
@allure.story("逆地理编码")
@allure.severity(allure.severity_level.CRITICAL)
def test_regeo(case):
    mark_case(case)
    AssertUtil().assert_response(GeocodeAPI().get_regeo(**case["params"]), case["expect"])
