import asyncio
from typing import Dict
from typing import List
from typing import Optional

from points.domain.events.entities import EVENT_DEPLOY_CONTRACT
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.repository.explorer_repository import ExplorerRepositoryHTTP

SLEEP_TIME = 1


async def execute(
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP,
) -> None:
    users: List[EventUser] = event_repository.get_users_by_missing_event(
        EVENT_DEPLOY_CONTRACT.name)
    for user in users:
        if not user.wallet_address:
            continue
        await _handle_event(
            user,
            event_repository,
            explorer_repository
        )
        await asyncio.sleep(SLEEP_TIME)


async def _handle_event(
    user: EventUser,
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP
) -> None:
    deployment_tx_logs = await _get_deployment_tx_logs(user, explorer_repository)
    if deployment_tx_logs:
        event_repository.add_event(QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_DEPLOY_CONTRACT.name,
            points=EVENT_DEPLOY_CONTRACT.points,
            event_description=None,
            logs=deployment_tx_logs
        ))


async def _get_deployment_tx_logs(
    user: EventUser,
    explorer_repository: ExplorerRepositoryHTTP
) -> Optional[Dict]:
    response = await explorer_repository.get_transactions_from_account(
        user.wallet_address)
    while response and len(response.get("items")):
        for item in response.get("items", []):
            if "contract_creation" in item.get("tx_types", []):
                return item

        if response.get("next_page_params"):
            response = await explorer_repository.get_transactions_from_account(
                user.wallet_address, response)
        else:
            response = None
    return None
