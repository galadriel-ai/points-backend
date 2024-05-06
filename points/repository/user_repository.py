from typing import List

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from points.domain.dashboard.entities import User
from points.repository import utils

SQL_INSERT_USER = """
INSERT INTO user_profile (
    id,
    x_username,
    email,
    wallet_address,
    created_at,
    last_updated_at
)
VALUES (
    :id,
    :x_username,
    :email,
    :wallet_address,
    :created_at,
    :last_updated_at
);
"""

SQL_UPDATE_WALLET_ADDRESS = """
UPDATE user_profile 
SET 
    wallet_address = :wallet_address,
    last_updated_at = :last_updated_at
WHERE
    email = :email;
"""

SQL_GET_MOST_RECENT = """
SELECT 
    email,
    x_username,
    wallet_address
FROM user_profile
ORDER BY id DESC
LIMIT :count;
"""


class UserRepositoryPsql:
    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def insert(self, user: User):
        data = {
            "id": utils.generate_uuid(),
            "email": user.email.lower(),
            "x_username": user.x_username,
            "wallet_address": user.wallet_address,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_INSERT_USER), data)
            session.commit()

    def update_wallet_address(self, email: str, wallet_address: str):
        data = {
            "email": email.lower(),
            "wallet_address": wallet_address,
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
                    x_username=row.x_username,
                    email=row.email,
                    wallet_address=row.wallet_address,
                ))
            return users
