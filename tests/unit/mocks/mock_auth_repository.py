from typing import Optional

from points.domain.auth.entities import SignMessageComponents


class AuthRepositoryPsqlMock:

    def insert_sign_message_components(
        self,
        wallet_address: str,
        nonce: str,
        issued_at: str,
    ) -> bool:
        return True

    def get_sign_message_components(
        self,
        wallet_address: str
    ) -> Optional[SignMessageComponents]:
        return SignMessageComponents(
            nonce="cqaakoZsXxz",
            issued_at="2024-05-06T21:01:02.000Z"
        )
