import asyncio
from typing import List

import settings
from points.domain.events.entities import EVENT_FAUCET
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.repository.explorer_repository import ExplorerRepositoryHTTP


async def execute(
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP,
) -> None:
    users: List[EventUser] = event_repository.get_users_by_missing_event(EVENT_FAUCET.name)
    for user in users:
        if not user.wallet_address:
            # Should not happen
            continue
        await _handle_event(
            user,
            event_repository,
            explorer_repository,
        )
        await asyncio.sleep(1)


async def _handle_event(
    user: EventUser,
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP
) -> None:
    response = await explorer_repository.get_transactions_to_account(user.wallet_address)
    if not response or not len(response.get("items")):
        return

    is_faucet_tx_present = False
    for tx in response.get("items", []):
        if tx.get("from", {}).get("hash", "").lower() == settings.FAUCET_ADDRESS.lower():
            is_faucet_tx_present = True
            break
    if not is_faucet_tx_present:
        return

    event_repository.add_event(QuestEvent(
        user_profile_id=user.user_id,
        event_name=EVENT_FAUCET.name,
        points=EVENT_FAUCET.points,
        event_description=None,
        logs=response.get("items")[0]
    ))
