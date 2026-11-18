import os

import pytest
import yaml

import config as project_config
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
    name = metafunc.module.__name__.split(".")[-1].removeprefix("test_")
    case = yaml.safe_load((project_config.PROJECT_ROOT / "testcases" / f"{name}.yaml").read_text(encoding="utf-8"))["cases"]
    params = [pytest.param(c, marks=pytest.mark.smoke) if c.get("smoke") else c for c in case]
    metafunc.parametrize("case", params, ids = lambda c: c["case"])

def pytest_addoption(parser):
    parser.addoption("--env", default="prod", choices=list(project_config.ENVIRONMENT), help="被测环境")
    parser.addoption("--base-url", default=None, help="直接覆盖 base url，可指向 mock 或代理")

def pytest_configure(config):
    project_config.BASE_URL = config.getoption("--base-url") or project_config.ENVIRONMENT[config.getoption("--env")]
