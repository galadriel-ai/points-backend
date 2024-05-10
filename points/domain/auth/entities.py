from dataclasses import dataclass
from datetime import datetime


@dataclass
class SignMessageComponents:
    nonce: str
    issued_at: str


@dataclass(frozen=True)
class TwitterAccessToken:
    access_token: str
    refresh_token: str
    expires_at: datetime
