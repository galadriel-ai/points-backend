from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

import points.domain.events.handle_join_discord_events_use_case as use_case
import settings
from points.domain.events.entities import EVENT_JOIN_DISCORD
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent

USER_ID = UUID("20a61707-9c43-4e8c-9eed-b46fe1fb8705")


def setup():
    pass


def setup_function():
    use_case.SLEEP_TIME = 0


async def test_no_users():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = []
    discord_repo = MagicMock()

    await use_case.execute(event_repo, discord_repo)

    discord_repo.is_member.assert_not_called()


async def test_not_a_member():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address=None,
            discord_id="1234",
        )
    ]
    discord_repo = AsyncMock()
    discord_repo.is_member.return_value = False

    await use_case.execute(event_repo, discord_repo)

    event_repo.add_event.assert_not_called()


async def test_updates_one():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address=None,
            discord_id="1234",
        )
    ]
    discord_repo = AsyncMock()
    discord_repo.is_member.return_value = True

    await use_case.execute(event_repo, discord_repo)
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_JOIN_DISCORD.name,
            points=EVENT_JOIN_DISCORD.points,
            event_description=None,
            logs=None
        )
    )
