from siwe import SiweMessage
from eth_utils import to_checksum_address

from points.repository.auth_repository import AuthRepositoryPsql

MESSAGE_TEMPLATE = """{DOMAIN} wants you to sign in with your Ethereum account:
{WALLET_ADDRESS}


URI: {URI}
Version: 1
Chain ID: {CHAIN_ID}
Nonce: {NONCE}
Issued At: {ISSUED_AT}"""

DOMAIN = "localhost"
URI = "http://localhost/login"
CHAIN_ID = "1"


def execute(
    signature: str,
    wallet_address: str,
    auth_repository: AuthRepositoryPsql
) -> bool:
    wallet_address = to_checksum_address(wallet_address)
    message_components = auth_repository.get_sign_message_components(wallet_address)
    message = MESSAGE_TEMPLATE.format(
        DOMAIN=DOMAIN,
        WALLET_ADDRESS=wallet_address,
        URI=URI,
        CHAIN_ID=CHAIN_ID,
        NONCE=message_components.nonce,
        ISSUED_AT=message_components.issued_at
    )

    try:
        siwe_message = SiweMessage.from_message(message=message)
        siwe_message.verify(signature, nonce=message_components.nonce, domain=DOMAIN)
        return True
    except Exception as exc:
        print(f"Failed to verify signature for {wallet_address}, exc:", exc)
        return False
