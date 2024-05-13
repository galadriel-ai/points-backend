from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from points.domain.dashboard.entities import User
from points.repository import utils

SQL_INSERT_USER = """
INSERT INTO user_profile (
    id,
    x_id,
    x_username,
    wallet_address,
    created_at,
    last_updated_at
)
VALUES (
    :id,
    :x_id,
    :x_username,
    :wallet_address,
    :created_at,
    :last_updated_at
);
"""

SQL_GET_BY_X_ID = """
SELECT 
    id, 
    x_id, 
    x_username, 
    wallet_address 
FROM user_profile
WHERE x_id = :x_id;
"""

SQL_GET_BY_ID = """
SELECT id, x_id, x_username, wallet_address 
FROM user_profile 
WHERE id = :id;
"""

SQL_UPDATE_WALLET_ADDRESS = """
UPDATE user_profile 
SET 
    wallet_address = :wallet_address,
    last_updated_at = :last_updated_at
WHERE
    x_id = :x_id;
"""

SQL_GET_MOST_RECENT = """
SELECT 
    id,
    x_id,
    x_username,
    wallet_address
FROM user_profile
ORDER BY id DESC
LIMIT :count;
"""


class UserRepositoryPsql:
    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def insert(
        self,
        x_id: str,
        x_username: str,
        wallet_address: Optional[str]
    ) -> UUID:
        user_id = utils.generate_uuid()
        data = {
            "id": user_id,
            "x_id": x_id,
            "x_username": x_username,
            "wallet_address": wallet_address,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_INSERT_USER), data)
            session.commit()
        return user_id

    def get_by_x_id(self, x_id: str) -> Optional[User]:
        data = {
            "x_id": x_id,
        }
        with self.session_maker() as session:
            row = session.execute(text(SQL_GET_BY_X_ID), data).first()
            if row:
                return User(
                    user_id=row.id,
                    x_id=row.x_id,
                    x_username=row.x_username,
                    wallet_address=row.wallet_address,
                )
        return None

    def get_by_user_id(self, user_profile_id: UUID) -> Optional[User]:
        data = {
            "id": str(user_profile_id)
        }
        with self.session_maker() as session:
            row = session.execute(text(SQL_GET_BY_ID), data).first()
            if row:
                return User(
                    user_id=row.id,
                    x_id=row.x_id,
                    x_username=row.x_username,
                    wallet_address=row.wallet_address,
                )

    def update_wallet_address(self, x_id: str, wallet_address: str):
        data = {
            "x_id": x_id,
            "wallet_address": wallet_address.lower(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_UPDATE_WALLET_ADDRESS), data)
            session.commit()

    def get_recently_joined(self, count: int) -> List[User]:
        data = {
            "count": count,
        }
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_MOST_RECENT), data)
            users = []
            for row in rows:
                users.append(User(
                    user_id=row.id,
                    x_id=row.x_id,
                    x_username=row.x_username,
                    wallet_address=row.wallet_address,
                ))
            return users
