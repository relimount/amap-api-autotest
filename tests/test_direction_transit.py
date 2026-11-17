from api.direction import DirectionAPI
from assert_util import AssertUtil

def test_direction_transit(case):
    AssertUtil().assert_response(DirectionAPI().get_transit(**case["params"]), case["expect"])
