from typing import List, Dict
import asyncio
import aiohttp
import settings

from points.domain.auth.entities import DiscordUser


class DiscordRepository:
    BASE_URL = "https://discord.com/api/v10"
    PAGE_LIMIT = 1000

    def __init__(
        self,
        guild_id: str = settings.DISCORD_GUILD_ID,
        token: str = settings.DISCORD_TOKEN,
    ):
        self.token = token
        self.guild_id = guild_id

    async def _get_request(self, url: str, params: Dict = {}, token=None):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else f"Bot {self.token}",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                if response.status == 429:
                    await asyncio.sleep(int(response.headers["X-RateLimit-Reset-After"]))
                    return await self._get_request(url, params=params)
                response.raise_for_status()
                return await response.json()

    async def get_users(self) -> List[DiscordUser]:
        url = f"{self.BASE_URL}/guilds/{self.guild_id}/members"
        members = []
        params = {"limit": self.PAGE_LIMIT}

        while True:
            data = await self._get_request(url, params=params)
            members.extend(
                [DiscordUser(id=member["user"]["id"], username=member["user"]["username"]) for member in data])

            if len(data) <  self.PAGE_LIMIT:
                break
            params["after"] = data[-1]["user"]["id"]

        return members

    async def is_member(self, member_id: str, user_token: str = None) -> bool:
        url = (f"{self.BASE_URL}/users/@me/guilds/{self.guild_id}/member" if user_token
               else f"{self.BASE_URL}/guilds/{self.guild_id}/members/{member_id}")
        try:
            await self._get_request(url, token=user_token)
            return True
        except aiohttp.ClientResponseError:
            return False
