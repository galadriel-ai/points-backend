from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TokenIssuer(str, Enum):
    TWITTER = "twitter"


@dataclass
class SignMessageComponents:
    nonce: str
    issued_at: str


@dataclass(frozen=True)
class AccessToken:
    token_issuer: TokenIssuer
    access_token: str
    refresh_token: str
    expires_at: datetime


@dataclass
class DiscordUser:
    id: str
    username: str
