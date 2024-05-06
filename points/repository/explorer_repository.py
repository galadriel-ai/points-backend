from typing import Dict
from typing import Optional
from urllib.parse import urljoin

import aiohttp

from points import api_logger

logger = api_logger.get()


class ExplorerRepositoryHTTP:

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_transactions_from_account(self, wallet_address: str) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    urljoin(
                        self.base_url,
                        f"addresses/{wallet_address}/transactions?filter=from"
                    )
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            logger.error("Failed to query user transactions", str(e))
        return None
