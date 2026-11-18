
import allure
import pytest

from utils.assert_util import AssertUtil, MISSING

pytestmark = [
    allure.feature("断言引擎"),
    allure.story("引擎自测"),
    allure.severity(allure.severity_level.BLOCKER),
]


class FakeResp:
    """假的Response"""

    def __init__(self, payload=None, status_code=200, text=""):
        self._payload = payload
        self.status_code = status_code
        self.text = text

    def json(self):
        if self._payload is None:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._payload


@pytest.fixture(autouse=True)
def throttle():
    """覆盖 conftest的fixture"""
    yield


util = AssertUtil()


def should_pass(payload, expect, status_code=200):
    util.assert_response(FakeResp(payload, status_code), expect)


def should_fail(payload, expect, status_code=200):
    with pytest.raises(AssertionError):
        util.assert_response(FakeResp(payload, status_code), expect)


class TestGetByPath:
    """路径解析"""

    def test_top_level_field(self):
        assert util._get_by_path({"status": "1"}, "status") == "1"

    def test_nested_dict(self):
        assert util._get_by_path({"a": {"b": {"c": 1}}}, "a.b.c") == 1

    def test_list_index(self):
        assert util._get_by_path({"g": [{"adcode": "110105"}]}, "g.0.adcode") == "110105"

    def test_dict_and_list_mixed(self):
        data = {"route": {"paths": [{"steps": [{"instruction": "向东"}]}]}}
        assert util._get_by_path(data, "route.paths.0.steps.0.instruction") == "向东"

    def test_missing_key_returns_sentinel(self):
        assert util._get_by_path({"a": 1}, "b") is MISSING

    def test_missing_nested_key_returns_sentinel(self):
        assert util._get_by_path({"a": {"b": 1}}, "a.c") is MISSING

    def test_index_out_of_range_returns_sentinel(self):
        assert util._get_by_path({"g": [1]}, "g.9") is MISSING

    def test_non_numeric_index_on_list_returns_sentinel(self):
        assert util._get_by_path({"g": [1]}, "g.abc") is MISSING

    def test_scalar_in_the_middle_returns_sentinel(self):
        assert util._get_by_path({"a": "str"}, "a.b") is MISSING

    def test_empty_path_raises(self):
        with pytest.raises(ValueError):
            util._get_by_path({}, "")

    def test_non_string_path_raises(self):
        with pytest.raises(ValueError):
            util._get_by_path({}, None)

    def test_top_level_list(self):
        assert util._get_by_path([{"a": 1}], "0.a") == 1


class TestBodyAssert:
    """body字段精确匹配。"""

    def test_value_equal(self):
        should_pass({"status": "1"}, {"http_status": 200, "body": {"status": "1"}})

    def test_value_not_equal(self):
        should_fail({"status": "1"}, {"http_status": 200, "body": {"status": "0"}})

    def test_nested_value_equal(self):
        payload = {"regeocode": {"addressComponent": {"adcode": "110105"}}}
        should_pass(payload, {"http_status": 200, "body": {"regeocode.addressComponent.adcode": "110105"}})

    def test_missing_field_expecting_null_must_fail(self):
        """回归：字段根本不存在，即使期望值是 null 也必须失败。"""
        should_fail({"status": "1"}, {"http_status": 200, "body": {"lives.0": None}})

    def test_existing_field_null_expecting_null_passes(self):
        """字段存在且值为null，期望null应该通过。"""
        should_pass({"lives": [None]}, {"http_status": 200, "body": {"lives.0": None}})

    def test_empty_list_element(self):
        """非法city时高德返回lives=[[]]，用它断言lives.0 == []。"""
        should_pass({"lives": [[]]}, {"http_status": 200, "body": {"lives.0": []}})


class TestTypeAssert:
    """类型校验"""

    def test_int_ok(self):
        should_pass({"x": 3}, {"http_status": 200, "types": {"x": "int"}})

    def test_int_rejects_bool(self):
        """回归：isinstance(True, int) 为 True，必须显式排除。"""
        should_fail({"x": True}, {"http_status": 200, "types": {"x": "int"}})

    def test_bool_ok(self):
        should_pass({"x": True}, {"http_status": 200, "types": {"x": "bool"}})

    def test_float_ok(self):
        should_pass({"x": 1.5}, {"http_status": 200, "types": {"x": "float"}})

    def test_float_accepts_int(self):
        should_pass({"x": 3}, {"http_status": 200, "types": {"x": "float"}})

    def test_null_ok(self):
        should_pass({"x": None}, {"http_status": 200, "types": {"x": "null"}})

    def test_str_rejects_int(self):
        should_fail({"x": 3}, {"http_status": 200, "types": {"x": "str"}})

    def test_missing_field_must_fail(self):
        should_fail({"y": 1}, {"http_status": 200, "types": {"x": "int"}})

    def test_unknown_type_name_raises_value_error(self):
        with pytest.raises(ValueError, match="未知的类型配置"):
            util.assert_response(FakeResp({"x": 1.5}), {"http_status": 200, "types": {"x": "float64"}})


class TestHasKeys:

    def test_has_keys_hit(self):
        should_pass({"count": "1"}, {"http_status": 200, "has_keys": ["count"]})

    def test_has_keys_miss(self):
        should_fail({"count": "1"}, {"http_status": 200, "has_keys": ["route"]})

    def test_not_has_keys_miss(self):
        should_pass({"count": "1"}, {"http_status": 200, "not_has_keys": ["route"]})

    def test_not_has_keys_hit(self):
        should_fail({"count": "1"}, {"http_status": 200, "not_has_keys": ["count"]})

    def test_nested_not_has_keys_on_empty_list(self):
        """lives=[[]] 时继续往下取 city 应该取不到。"""
        should_pass({"lives": [[]]}, {"http_status": 200, "not_has_keys": ["lives.0.city"]})


class TestGuard:
    """写错用例要报错，不能静默通过。"""
    def test_http_status_mismatch(self):
        should_fail({"status": "1"}, {"http_status": 200, "body": {"status": "1"}}, status_code=500)

    def test_unknown_expect_key_raises(self):
        with pytest.raises(ValueError):
            util.assert_response(FakeResp({"a": 1}), {"http_status": 200, "haskey": ["a"]})

    def test_non_json_response_raises_assertion(self):
        with pytest.raises(AssertionError):
            util.assert_response(FakeResp(None, text="<html>502 Bad Gateway</html>"), {"http_status": 200})

    def test_empty_expect_only_checks_status(self):
        should_pass({"anything": 1}, {"http_status": 200})

    def test_missing_http_status_raises_value_error(self):
        with pytest.raises(ValueError, match="未配置http_status"):
            util.assert_response(FakeResp({"a": 1}), {"body": {}})

