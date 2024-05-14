import asyncio
from typing import List

import settings
from points.domain.events.entities import EVENT_JOIN_DISCORD
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.repository.discord_repository import DiscordRepository

SLEEP_TIME = 1


async def execute(
    event_repository: EventRepositoryPsql,
    discord_repository: DiscordRepository,
) -> None:
    users: List[EventUser] = event_repository.get_users_by_missing_event(
        EVENT_JOIN_DISCORD.name)
    for user in users:
        if not user.discord_id:
            continue
        await _handle_event(
            user,
            event_repository,
            discord_repository,
        )
        await asyncio.sleep(SLEEP_TIME)


async def _handle_event(
    user: EventUser,
    event_repository: EventRepositoryPsql,
    discord_repository: DiscordRepository
) -> None:
    is_member = await discord_repository.is_member(user.discord_id)
    if not is_member:
        return

    event_repository.add_event(QuestEvent(
        user_profile_id=user.user_id,
        event_name=EVENT_JOIN_DISCORD.name,
        points=EVENT_JOIN_DISCORD.points,
        event_description=None,
        logs=None
    ))
