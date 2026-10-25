import pytest
import yaml

from api.direction import DirectionAPI
from assert_util import AssertUtil
from config import PROJECT_ROOT

CASE_FILE = PROJECT_ROOT / "testcases" / "direction_bicycling.yaml"
CASES = yaml.safe_load(CASE_FILE.read_text(encoding="utf-8"))['cases']
direction = DirectionAPI()
assert_util = AssertUtil()

@pytest.mark.parametrize("case", CASES, ids= lambda c: c["case"])
def test_direction_bicycling(case):
    resp = direction.get_bicycling(**case["params"])
    assert_util.assert_response(resp, case["expect"])