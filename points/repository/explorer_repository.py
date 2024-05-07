from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union
from urllib.parse import urlencode
from urllib.parse import urljoin

import aiohttp

from points import api_logger

logger = api_logger.get()


class ExplorerRepositoryHTTP:

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_transactions_from_account(
        self,
        account_address: str,
        previous_response: Optional[Dict] = None
    ) -> Optional[Dict]:
        return await self._get_transactions_by_account(account_address, "from", previous_response)

    async def get_transactions_to_account(
        self,
        account_address: str,
        previous_response: Optional[Dict] = None
    ) -> Optional[Dict]:
        return await self._get_transactions_by_account(account_address, "to", previous_response)

    async def _get_transactions_by_account(
        self, account_address: str,
        filter_value: Union[Literal["from", "to"]],
        # pass in previous response to get next page
        previous_response: Optional[Dict] = None,
    ) -> Optional[Dict]:
        pagination_url_str = self._get_pagination_params(previous_response)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    urljoin(
                        self.base_url,
                        f"addresses/{account_address}/transactions?filter={filter_value}{pagination_url_str}"
                    )
                ) as response:
                    if response.status == 404:
                        return None
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            logger.error("Failed to query user transactions", str(e))
        return None

    def _get_pagination_params(self, previous_response: Optional[Dict]) -> str:
        if not previous_response or not previous_response.get("next_page_params"):
            return ""
        return "&" + urlencode(previous_response.get("next_page_params"))
