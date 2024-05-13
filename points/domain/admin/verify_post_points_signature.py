from typing import List

from eth_account.messages import encode_defunct
from web3 import Web3

from points.service.admin.entities import PostPointsRequest

w3 = Web3()


def execute(request: PostPointsRequest, admin_wallet_addresses) -> bool:
    message = encode_defunct(text=request.construct_signed_message())
    address = w3.eth.account.recover_message(message, signature=request.signature)
    address = address.lower()
    if not request.wallet_address.lower() == address:
        return False

    admin_wallet_addresses = _convert_addresses(admin_wallet_addresses)
    if address in admin_wallet_addresses:
        return True
    return False


def _convert_addresses(addresses: List[str]) -> List[str]:
    result = []
    for address in addresses:
        result.append(address.lower())
    return result
