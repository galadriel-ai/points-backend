import time
from collections import defaultdict

DEFAULT_MAX_CALLS_PER_HOUR = 60 * 60


class RateLimiter:
    def __init__(self, max_calls_per_hour: int = DEFAULT_MAX_CALLS_PER_HOUR):
        self.calls = defaultdict(list)
        self.max_calls_per_hour = max_calls_per_hour

    def is_rate_limited(self, s):
        now = time.time()
        one_hour_ago = now - 3600
        self.calls[s] = [t for t in self.calls[s] if t > one_hour_ago]
        self.calls[s].append(now)
        return len(self.calls[s]) > self.max_calls_per_hour
