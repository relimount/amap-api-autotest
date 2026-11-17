from api.geocode import GeocodeAPI
from assert_util import AssertUtil


def test_regeo(case):
    AssertUtil().assert_response(GeocodeAPI().get_regeo(**case["params"]), case["expect"])

