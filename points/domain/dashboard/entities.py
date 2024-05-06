from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    x_username: str
    email: str
    wallet_address: Optional[str]


@dataclass(frozen=True)
class ScoredUser(User):
    points: int
