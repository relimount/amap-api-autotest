from api.direction import DirectionAPI
from assert_util import AssertUtil

def test_direction_walking(case):
    AssertUtil().assert_response(DirectionAPI().get_walking(**case["params"]), case["expect"])