from eth_account.messages import encode_defunct
from web3 import Web3

from points.service.admin.entities import PostPointsRequest

w3 = Web3()


def execute(request: PostPointsRequest, admin_wallet_addresses) -> bool:
    message = encode_defunct(text=request.construct_signed_message())
    address = w3.eth.account.recover_message(message, signature=request.signature)
    if not request.wallet_address == address:
        return False

    if address in admin_wallet_addresses:
        return True
    return False
