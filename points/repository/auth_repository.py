from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from points.domain.auth.entities import SignMessageComponents
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
