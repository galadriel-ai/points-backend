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


@dataclass(frozen=True)
class UserProfileImage(User):
    profile_image_url: Optional[str]
    cached_profile_image_url: Optional[str]
