"""报告层辅助：用例标注、失败信息附加。只影响 Allure 展示，不改变执行逻辑。"""

import re

import allure

SEVERITY = {
    "blocker": allure.severity_level.BLOCKER,
    "critical": allure.severity_level.CRITICAL,
    "normal": allure.severity_level.NORMAL,
    "minor": allure.severity_level.MINOR,
}

_KEY_RE = re.compile(r"(key=)[^&]+")


def mask_key(url):
    return _KEY_RE.sub(r"\1***", url or "")


def mark_case(case):
    allure.dynamic.title(case["case"])

    level = case.get("severity")
    if level:
        if level not in SEVERITY:
            raise ValueError(f"未知的 severity：{level}，可选 {list(SEVERITY)}")
        allure.dynamic.severity(SEVERITY[level])


def attach_failure(resp):
    """URL响应体贴进报告"""
    url = getattr(getattr(resp, "request", None), "url", None)
    if url:
        allure.attach(
            mask_key(url),
            name="请求 URL",
            attachment_type=allure.attachment_type.TEXT,
        )
    text = getattr(resp, "text", "") or ""
    if text:
        allure.attach(
            text[:2000],
            name="响应体",
            attachment_type=allure.attachment_type.JSON,
        )