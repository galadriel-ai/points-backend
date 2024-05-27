from typing import List

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

WHITELIST_X_IDS = [
    "755403332",  # KasparPeterson
    "1384448028774383616",  # Galadriel_AI
]

SQL_GET_ADMINS_WALLET_ADDRESSES = """
SELECT wallet_address 
FROM user_profile 
WHERE x_id IN :x_ids;
"""


class AdminRepositoryPsql:

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def get_admins_wallet_addresses(self) -> List[str]:
        result = []
        data = {"x_ids": tuple(WHITELIST_X_IDS)}
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_ADMINS_WALLET_ADDRESSES), data)
            for row in rows:
                result.append(row.wallet_address.lower())
        return result
