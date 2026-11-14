TYPE_MAP = {"str": str, "int": int, "list": list, "dict": dict, "bool": bool}
_ALLOWED_KEYS = {"http_status", "body", "has_keys", "not_has_keys", "types"}

class _MissingType:
    """哨兵值"""
    def __repr__(self):
        return "<字段不存在>"


_MISSING = _MissingType()

class AssertUtil:

    def _get_by_path(self, data, path, default=_MISSING):

        if not isinstance(path, str) or not path:
            raise ValueError("path为非空字符串")

        cur = data
        for part in path.split("."):
            try:
                if isinstance(cur, list):
                    cur = cur[int(part)]
                elif isinstance(cur, dict):
                    cur = cur[part]
                else:
                    return default
            except (KeyError, ValueError, IndexError):
                return default
        return cur

    def _safe_json(self, resp):
        """防error"""
        try:
            return resp.json()
        except ValueError:
            raise AssertionError(f"响应不是json")

    def _type_ok(self, actual, type_name):
        """防bool误判"""
        if type_name == "int":
            return isinstance(actual, int) and not isinstance(actual, bool)
        if type_name == "bool":
            return isinstance(actual, bool)
        if type_name == "float":
            return isinstance(actual, (int, float)) and not isinstance(actual, bool)
        if type_name == "null":
            return actual is None
        return isinstance(actual, TYPE_MAP[type_name])

    def assert_response(self, resp, expect):
        """按 expect 的声明逐层校验响应"""
        assert resp.status_code == expect["http_status"], resp.text
        data = self._safe_json(resp)
        # 防静默假绿
        unexpect = set(expect) - _ALLOWED_KEYS
        if unexpect:
            raise ValueError(f"expect 里有未知的键：{unexpect}")

        for field, value in expect.get("body", {}).items():
            actual = self._get_by_path(data, field)
            assert actual is not _MISSING, f"字段缺失：{field}"
            assert actual == value, f"{field} 期望 {value!r}，实际 {actual!r}"

        for field in expect.get("has_keys") or []:
            assert self._get_by_path(data, field) is not _MISSING, f"缺少字段 {field}"

        for field in expect.get("not_has_keys") or []:
            assert self._get_by_path(data, field) is _MISSING, f"多出字段 {field}"

        for field, type_name in expect.get("types", {}).items():
            actual = self._get_by_path(data, field)
            assert actual is not _MISSING, f"字段缺失：{field}"
            assert self._type_ok(actual, type_name), f"{field} 类型应为 {type_name}，实际 {type(actual).__name__}"