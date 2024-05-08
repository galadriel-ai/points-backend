from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    x_id: str
    x_username: str
    wallet_address: Optional[str]


@dataclass(frozen=True)
class ScoredUser(User):
    points: int
