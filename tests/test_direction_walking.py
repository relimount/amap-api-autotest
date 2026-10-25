import pytest
import yaml

from api.direction import DirectionAPI
from assert_util import AssertUtil
from config import PROJECT_ROOT

CASES_FILE = PROJECT_ROOT / "testcases" / "direction_walking.yaml"
CASES = yaml.safe_load(CASES_FILE.read_text(encoding="utf-8"))["cases"]
direct = DirectionAPI()

assert_util = AssertUtil()

@pytest.mark.parametrize("case", CASES, ids = lambda c : c["case"])
def test_direction_walking(case):
    resp = direct.get_walking(**case["params"])
    assert_util.assert_response(resp, case["expect"])