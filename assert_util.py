
TYPE_MAP = {"str": str, "int": int, "list": list, "dict": dict, "bool": bool}

class AssertUtil:

    def assert_response(self,resp,expect):
        """断言"""
        assert resp.status_code == expect["http_status"], resp.text
        body = resp.json()

        for field, value in expect.get("body", {}).items():
            actual = body.get(field)
            assert actual == value, f"{field} 期望 {value!r}，实际 {actual!r}"

        for field in expect.get("has_keys", []):
            assert field in body, f"响应缺少字段 {field}"

        for field in expect.get("not_has_keys", []):
            assert field not in body, f"响应不应包含字段 {field}"

        for field, type_name in expect.get("types", {}).items():
            expected_type = TYPE_MAP[type_name]
            actual = body.get(field)
            assert isinstance(actual, expected_type), (
                f"{field} 类型应为 {type_name}，实际 {type(actual).__name__}"
            )