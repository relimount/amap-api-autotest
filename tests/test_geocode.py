import pytest
import yaml

from api.geocode import GeocodeAPI
from assert_util import AssertUtil
from config import PROJECT_ROOT

CASE_FILE = PROJECT_ROOT / "testcases" / "geocode.yaml"
CASES = yaml.safe_load(CASE_FILE.read_text(encoding="utf-8"))["cases"]

geocode = GeocodeAPI()
assert_util = AssertUtil()

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["case"])
def test_geocode(case):
    resp = geocode.get_geocode(**case["params"])

    expect = case["expect"]
    assert_util.assert_response(resp, expect)

