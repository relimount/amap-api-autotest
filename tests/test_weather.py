import pytest
import yaml

from api.weather import WeatherAPI
from assert_util import AssertUtil
from config import PROJECT_ROOT

CASE_FILE = PROJECT_ROOT / "testcases" / "weather.yaml"
CASE = yaml.safe_load(CASE_FILE.read_text(encoding="utf-8"))["cases"]

weather = WeatherAPI()
assert_util = AssertUtil()

@pytest.mark.parametrize("case", CASE, ids=lambda c: c["case"])
def test_weather(case):
    resp = weather.get_weather(**case["params"])
    assert_util.assert_response(resp, case["expect"])