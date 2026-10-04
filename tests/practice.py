from email.policy import strict

_MISSING = object()


def _get_by_path(data, path, default=_MISSING, strict=True):
    if not isinstance(path, str) or not path:
        if strict:
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

if __name__ == '__main__':
    data = {
        "status": 200,
        "list":[
            {
                "formatted_address" : "北京市朝阳区阜通东大街6号",
                "country" : "中国",
            },
            {
                "formatted_address" : "上海市浦东新区世纪大道100号",
                "country" : "中国",
            }
        ]
    }
    path = "list.0.formatted_address"
    print(_get_by_path(data, path))

