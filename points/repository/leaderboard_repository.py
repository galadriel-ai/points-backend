from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from points.domain.dashboard.entities import UserProfileImage
from points.repository import utils


@dataclass
class LeaderboardEntry:
    user: UserProfileImage
    points: int


@dataclass
class RecentlyJoinedEntry:
    user: UserProfileImage
    joined_at: datetime


SQL_INSERT_ENTRY = """
INSERT INTO leaderboard (
    user_profile_id,
    points,
    created_at,
    last_updated_at
) VALUES (
    :user_profile_id,
    :points,
    :created_at,
    :last_updated_at
)
ON CONFLICT (user_profile_id) 
DO UPDATE SET points = :points, last_updated_at = :last_updated_at;
"""

SQL_GET_LEADERBOARD = """
SELECT 
    u.id AS user_profile_id,
    u.x_id,
    u.x_username,
    u.wallet_address,
    l.points,
    u.profile_image_url,
    u.cached_profile_image_url
FROM leaderboard l
INNER JOIN user_profile u ON l.user_profile_id = u.id
ORDER BY l.points DESC
LIMIT 10;
"""

SQL_GET_RECENTLY_JOINED = """
SELECT 
    id AS user_profile_id, 
    x_id, 
    x_username, 
    wallet_address,
    profile_image_url, 
    cached_profile_image_url, 
    created_at
FROM user_profile
ORDER BY created_at DESC
LIMIT 10;
"""


class LeaderboardRepositoryPsql:

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def insert_entry(self, user_profile_id: UUID, points: int):
        data = {
            "user_profile_id": user_profile_id,
            "points": points,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_INSERT_ENTRY), data)
            session.commit()
            return True

    def get_leaderboard(self) -> List[LeaderboardEntry]:
        result = []
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_LEADERBOARD))
            for row in rows:
                user = UserProfileImage(
                    user_id=row.user_profile_id,
                    x_id=row.x_id,
                    x_username=row.x_username,
                    wallet_address=row.wallet_address,
                    profile_image_url=row.profile_image_url,
                    cached_profile_image_url=row.cached_profile_image_url,
                )
                result.append(LeaderboardEntry(
                    user=user,
                    points=row.points
                ))
        return result

    def get_recently_joined(self) -> List[RecentlyJoinedEntry]:
        result = []
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_RECENTLY_JOINED))
            for row in rows:
                user = UserProfileImage(
                    user_id=row.user_profile_id,
                    x_id=row.x_id,
                    x_username=row.x_username,
                    wallet_address=row.wallet_address,
                    profile_image_url=row.profile_image_url,
                    cached_profile_image_url=row.cached_profile_image_url,
                )
                result.append(RecentlyJoinedEntry(
                    user=user,
                    joined_at=row.created_at
                ))
        return result
