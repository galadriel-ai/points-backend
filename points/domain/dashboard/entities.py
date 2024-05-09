from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class User:
    user_id: UUID
    x_id: str
    x_username: str
    wallet_address: Optional[str]


@dataclass(frozen=True)
class ScoredUser(User):
    points: int
