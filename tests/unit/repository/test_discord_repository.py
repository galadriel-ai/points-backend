import pytest
from aioresponses import aioresponses
from points.repository.discord_repository import DiscordRepository


@pytest.fixture
def discord_repo():
    return DiscordRepository(guild_id="test_guild_id", token="test_token")


@pytest.mark.asyncio
async def test_get_users(discord_repo):
    with aioresponses() as m:
        # Mock response for the first page of members
        m.get(
            f"https://discord.com/api/v10/guilds/test_guild_id/members?limit=1000",
            payload=[
                {"user": {"id": "1", "username": "user1"}},
                {"user": {"id": "2", "username": "user2"}}
            ]
        )

        # Mock response for the second (and last) page of members
        m.get(
            f"https://discord.com/api/v10/guilds/test_guild_id/members?limit=1000&after=2",
            payload=[]
        )

        users = await discord_repo.get_users()

        assert len(users) == 2
        assert users[0].id == "1"
        assert users[0].username == "user1"
        assert users[1].id == "2"
        assert users[1].username == "user2"


@pytest.mark.asyncio
async def test_is_member(discord_repo):
    with aioresponses() as m:
        # Mock response for an existing member
        m.get(
            f"https://discord.com/api/v10/guilds/test_guild_id/members/1",
            status=200
        )

        # Mock response for a non-existing member
        m.get(
            f"https://discord.com/api/v10/guilds/test_guild_id/members/2",
            status=404
        )

        is_member_1 = await discord_repo.is_member("1")
        is_member_2 = await discord_repo.is_member("2")

        assert is_member_1 is True
        assert is_member_2 is False


@pytest.mark.asyncio
async def test_get_users_rate_limit(discord_repo):
    with aioresponses() as m:
        # Simulate rate-limited response
        m.get(
            "https://discord.com/api/v10/guilds/test_guild_id/members?limit=1000",
            status=429,
            headers={"X-RateLimit-Reset-After": "1"}
        )

        # Simulate successful retry response
        m.get(
            "https://discord.com/api/v10/guilds/test_guild_id/members?limit=1000",
            payload=[
                {"user": {"id": "1", "username": "user1"}},
                {"user": {"id": "2", "username": "user2"}}
            ]
        )

        users = await discord_repo.get_users()

        assert len(users) == 2
        assert users[0].id == "1"
        assert users[0].username == "user1"
        assert users[1].id == "2"
        assert users[1].username == "user2"


@pytest.mark.asyncio
async def test_is_member_rate_limit(discord_repo):
    with aioresponses() as m:
        # Simulate rate-limited response
        m.get(
            "https://discord.com/api/v10/guilds/test_guild_id/members/1",
            status=429,
            headers={"X-RateLimit-Reset-After": "1"}
        )

        # Simulate successful retry response
        m.get(
            "https://discord.com/api/v10/guilds/test_guild_id/members/1",
            status=200
        )

        is_member = await discord_repo.is_member("1")

        assert is_member is True
