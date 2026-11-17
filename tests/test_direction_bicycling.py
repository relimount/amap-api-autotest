from api.direction import DirectionAPI
from assert_util import AssertUtil



def test_direction_bicycling(case):
    AssertUtil().assert_response(DirectionAPI().get_bicycling(**case["params"]), case["expect"])
