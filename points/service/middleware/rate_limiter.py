import time
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from typing import Optional

DEFAULT_MAX_CALLS_PER_HOUR = 60 * 60


@dataclass(frozen=True)
class EndpointRateLimit:
    endpoint: str
    limit_per_hour: int


ENDPOINT_RATE_LIMITS: List[EndpointRateLimit] = [
    EndpointRateLimit(
        endpoint="/v1/dashboard/user/follow_twitter",
        limit_per_hour=3,
    ),
]


class RateLimiter:
    def __init__(self, max_calls_per_hour: int = DEFAULT_MAX_CALLS_PER_HOUR):
        self.calls = defaultdict(list)
        self.max_calls_per_hour = max_calls_per_hour

    def is_rate_limited(self, s, calls_per_hour: Optional[int] = None):
        if not calls_per_hour:
            calls_per_hour = self.max_calls_per_hour
        now = time.time()
        one_hour_ago = now - 3600
        self.calls[s] = [t for t in self.calls[s] if t > one_hour_ago]
        self.calls[s].append(now)
        return len(self.calls[s]) > calls_per_hour
