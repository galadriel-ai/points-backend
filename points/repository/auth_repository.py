from points.domain.auth.entities import SignMessageComponents


# TODO: implement real logic!
class AuthRepositoryPsql:

    def generate_sign_message_components(
        self,
        wallet_address: str
    ) -> SignMessageComponents:
        return SignMessageComponents(
            nonce="cqaakoZsXxz",
            issued_at="2024-05-06T21:01:02.000Z"
        )

    def get_sign_message_components(
        self,
        wallet_address: str
    ) -> SignMessageComponents:
        return SignMessageComponents(
            nonce="cqaakoZsXxz",
            issued_at="2024-05-06T21:01:02.000Z"
        )
