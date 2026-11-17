import os

import pytest
import yaml

from config import PROJECT_ROOT
from utils.ratelimit import TokenBucket

_bucket = TokenBucket(rate_per_sec=float(os.getenv("AMAP_QPS", "2.5")))

@pytest.fixture(autouse=True)
def throttle():
    _bucket.acquire()
    yield

def pytest_generate_tests(metafunc):
    """统一约定式加载"""
    if "case" not in metafunc.fixturenames:
        return
    name = metafunc.module.__name__.split(".")[-1].replace("test_", "")
    case = yaml.safe_load((PROJECT_ROOT / "testcases" / f"{name}.yaml").read_text(encoding="utf-8"))["cases"]
    metafunc.parametrize("case", case, ids = lambda c: c["case"])