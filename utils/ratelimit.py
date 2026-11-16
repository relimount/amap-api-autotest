import threading
import time


class TokenBucket:
    """令牌桶"""
    def __init__(self, rate_per_sec = 2.5, capacity = 1.0):
        self.rate = rate_per_sec
        self.capacity = capacity
        self._tokens = 0.0
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, tokens = 1.0):
        with self._lock:
            now = time.monotonic()
            self._tokens = min(self.capacity, (now - self._last) * self.rate + self._tokens)
            self._last = now
            if self._tokens - tokens >= 0:
                self._tokens -= tokens
                return
            wait_time = (tokens - self._tokens) / self.rate
            self._last += wait_time
            self._tokens = 0.0
        time.sleep(wait_time)
