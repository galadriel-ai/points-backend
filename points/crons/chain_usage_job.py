from points import api_logger
from points.domain.events import handle_make_tx_events_use_case
from points.domain.events import handle_make_deployment_events_use_case
from points.domain.events import handle_use_faucet_events_use_case
from points.repository.event_repository import EventRepositoryPsql
from points.repository.explorer_repository import ExplorerRepositoryHTTP

logger = api_logger.get()


async def execute(
    event_repository: EventRepositoryPsql,
    explorer_repository: ExplorerRepositoryHTTP,
) -> None:
    try:
        await handle_use_faucet_events_use_case.execute(event_repository, explorer_repository)
    except:
        logger.error("Error in handling faucet events", exc_info=True)

    try:
        await handle_make_tx_events_use_case.execute(event_repository, explorer_repository)
    except:
        logger.error("Error in handling user tx events", exc_info=True)

    try:
        await handle_make_deployment_events_use_case.execute(event_repository, explorer_repository)
    except:
        logger.error("Error in handling deployment events", exc_info=True)
