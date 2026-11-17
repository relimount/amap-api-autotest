from api.geocode import GeocodeAPI
from assert_util import AssertUtil

def test_geocode(case):
    AssertUtil().assert_response(GeocodeAPI().get_geocode(**case["params"]), case["expect"])
