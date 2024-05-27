from web3 import AsyncWeb3

import settings


class Web3Repository:

    def __init__(self, rpc_url: str = settings.WEB3_RPC_URL):
        self.rpc_url = rpc_url
        self.web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc_url))

    async def is_wallet_balance_bigger_than(self, wallet_address: str, value: str, unit="ether") -> bool:
        formatted_address = self.web3_client.to_checksum_address(wallet_address)
        balance = await self.web3_client.eth.get_balance(formatted_address)
        return balance >= self.web3_client.to_wei(value, unit)
