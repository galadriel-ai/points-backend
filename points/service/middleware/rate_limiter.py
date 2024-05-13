import time
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from typing import Optional

from points.service.auth import access_token_service

DEFAULT_MAX_CALLS_PER_HOUR = 60 * 60


@dataclass(frozen=True)
class EndpointRateLimit:
    endpoint: str
    max_calls_per_hour: int


ENDPOINT_RATE_LIMITS: List[EndpointRateLimit] = [
    EndpointRateLimit(
        endpoint="/v1/dashboard/user/follow_twitter",
        max_calls_per_hour=3,
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

    def is_endpoint_rate_limited(self, endpoint: str, api_key: Optional[str]) -> bool:
        rate_limited_endpoints = [l for l in ENDPOINT_RATE_LIMITS if l.endpoint in endpoint]
        if not api_key or not len(rate_limited_endpoints):
            return False
        try:
            user = access_token_service.get_user_from_access_token_str(api_key)
        except:
            # Endpoint needs to handle user authentication stuff
            return False
        rate_limitting_key = rate_limited_endpoints[0].endpoint + str(user.user_id)
        if user and self.is_rate_limited(
            rate_limitting_key, rate_limited_endpoints[0].max_calls_per_hour,
        ):
            return True
        return False

    def get_endpoint_calls_per_hour(self, endpoint: str) -> int:
        rate_limited_endpoints = [l for l in ENDPOINT_RATE_LIMITS if l.endpoint in endpoint]
        if len(rate_limited_endpoints):
            return rate_limited_endpoints[0].max_calls_per_hour
        return self.max_calls_per_hour
