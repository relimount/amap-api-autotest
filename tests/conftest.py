import os

import pytest

from utils.ratelimit import TokenBucket

_bucket = TokenBucket(rate_per_sec=float(os.getenv("AMAP_QPS", "2.5")))

@pytest.fixture(autouse=True)
def throttle():
    _bucket.acquire()
    yield