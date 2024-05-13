from datetime import timedelta
from base64 import b64encode
from typing import Optional

import aiohttp

import settings
from points import api_logger
from points.domain.auth.entities import TwitterAccessToken
from points.repository import utils

TWITTER_API_BASE_URL = "https://api.twitter.com/2"

logger = api_logger.get()


class TwitterRepositoryHTTP:

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    async def get_new_access_token(self, refresh_token: str) -> Optional[TwitterAccessToken]:
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = b64encode(client_creds.encode()).decode()

        url = f"{TWITTER_API_BASE_URL}/oauth2/token"
        try:
            headers = {
                "Authorization": f"Basic {client_creds_b64}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            async with aiohttp.ClientSession() as session:
                form_data = aiohttp.FormData()
                form_data.add_field("refresh_token", refresh_token)
                form_data.add_field("grant_type", "refresh_token")
                form_data.add_field("client_id", self.client_id)

                session.headers.update(headers)
                async with session.post(url, data=form_data) as response:
                    res_json = await response.json()
                return TwitterAccessToken(
                    access_token=res_json["access_token"],
                    refresh_token=res_json["refresh_token"],
                    expires_at=utils.now() + timedelta(seconds=res_json["expires_in"])
                )
        except Exception as e:
            logger.error("Failed to get new user twitter access token", exc_info=True)
            return None

    async def get_is_following_account(
        self,
        access_token: str,
        following_account_id: str = settings.GALADRIEL_TWITTER_USER_ID
    ) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                session.headers.update({
                    "Authorization": f"Bearer {access_token}"
                })
                res = await session.get(
                    f"{TWITTER_API_BASE_URL}/users/{following_account_id}?user.fields=connection_status")
                res_json = await res.json()
                return "following" in res_json.get("data", {}).get("connection_status", [])
        except Exception as e:
            logger.error("Failed to query user twitter following status", exc_info=True)
        return False
