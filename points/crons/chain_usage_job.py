import asyncio
from typing import List

from points import api_logger
from points.domain.events.entities import EVENT_MAKE_TX
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.repository.explorer_repository import ExplorerRepositoryHTTP

logger = api_logger.get()


async def execute(
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP,
):
    # TODO: check other events too
    users: List[EventUser] = event_repository.get_users_by_missing_event(EVENT_MAKE_TX.name)
    for user in users:
        if not user.wallet_address:
            # Should not happen
            continue
        await _handle_event_make_tx(
            user,
            event_repository,
            explorer_repository
        )
        await asyncio.sleep(1)


async def _handle_event_make_tx(
    user: EventUser,
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP
):
    response = await explorer_repository.get_transactions_from_account(user.wallet_address)
    if not response or not len(response.get("items")):
        return
    event_repository.add_event(QuestEvent(
        user_profile_id=user.user_id,
        event_name=EVENT_MAKE_TX.name,
        points=EVENT_MAKE_TX.points,
        event_description=None,
        logs=response.get("items")[0]
    ))
