import time

import pytest


@pytest.fixture(autouse=True)
def throttle():
    time.sleep(0.4)
    yield