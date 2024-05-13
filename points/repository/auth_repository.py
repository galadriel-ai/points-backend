from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from points.domain.auth.entities import SignMessageComponents
from points.domain.auth.entities import TokenIssuer
from points.domain.auth.entities import AccessToken
from points.repository import utils

SQL_INSERT_CHALLENGE = """
INSERT INTO eth_signin_challenge (
    wallet_address,
    nonce,
    issued_at,
    created_at,
    last_updated_at
) VALUES (
    :wallet_address,
    :nonce,
    :issued_at,
    :created_at,
    :last_updated_at
)
ON CONFLICT (wallet_address) 
DO UPDATE SET nonce = :nonce, issued_at = :issued_at, last_updated_at = :last_updated_at;
"""

SQL_GET_CHALLENGE = """
SELECT nonce, issued_at 
FROM eth_signin_challenge 
WHERE wallet_address = :wallet_address
"""

SQL_INSERT_USER_TWITTER_TOKEN = """
INSERT INTO user_token (
    id,
    user_profile_id,
    token_issuer,
    access_token,
    refresh_token,
    expires_at,
    created_at,
    last_updated_at
) VALUES (
    :id,
    :user_profile_id,
    :token_issuer,
    :access_token,
    :refresh_token,
    :expires_at,
    :created_at,
    :last_updated_at
)
ON CONFLICT (user_profile_id, token_issuer) 
DO UPDATE SET access_token = :access_token, refresh_token = :refresh_token, expires_at = :expires_at, last_updated_at = :last_updated_at;
"""

SQL_GET_ACCESS_TOKEN = """
SELECT
    token_issuer,
    access_token,
    refresh_token,
    expires_at
FROM user_token
WHERE user_profile_id = :user_profile_id;
"""


class AuthRepositoryPsql:

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def insert_sign_message_components(
        self,
        wallet_address: str,
        nonce: str,
        issued_at: str,
    ) -> bool:
        data = {
            "wallet_address": wallet_address.lower(),
            "nonce": nonce,
            "issued_at": issued_at,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_INSERT_CHALLENGE), data)
            session.commit()
            return True

    def get_sign_message_components(
        self,
        wallet_address: str
    ) -> Optional[SignMessageComponents]:
        data = {"wallet_address": wallet_address.lower()}
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_CHALLENGE), data)
            for row in rows:
                return SignMessageComponents(
                    nonce=row[0],
                    issued_at=row[1],
                )

    def save_user_access_token(
        self,
        user_id: UUID,
        token_issuer: TokenIssuer,
        access_token: str,
        refresh_token: str,
        expires_at: int
    ) -> None:
        data = {
            "id": utils.generate_uuid(),
            "user_profile_id": user_id,
            "token_issuer": token_issuer.value,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        with self.session_maker() as session:
            session.execute(text(SQL_INSERT_USER_TWITTER_TOKEN), data)
            session.commit()

    def get_user_access_token(self, user_id: UUID) -> Optional[AccessToken]:
        data = {"user_profile_id": user_id}
        with self.session_maker() as session:
            row = session.execute(text(SQL_GET_ACCESS_TOKEN), data).first()
            if row:
                return AccessToken(
                    token_issuer=TokenIssuer(row.token_issuer),
                    access_token=row.access_token,
                    refresh_token=row.refresh_token,
                    expires_at=utils.datetime_from_timestamp(row.expires_at),
                )
            return None
