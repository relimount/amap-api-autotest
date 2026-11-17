from api.direction import DirectionAPI
from assert_util import AssertUtil


def test_direction_driving(case):
    AssertUtil().assert_response(DirectionAPI().get_driving(**case["params"]), case["expect"])