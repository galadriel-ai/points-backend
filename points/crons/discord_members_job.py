from points import api_logger
from points.domain.events import handle_join_discord_events_use_case
from points.repository.discord_repository import DiscordRepository
from points.repository.event_repository import EventRepositoryPsql


logger = api_logger.get()


async def execute(
    event_repository: EventRepositoryPsql,
    discord_repository: DiscordRepository,
) -> None:
    try:
        await handle_join_discord_events_use_case.execute(event_repository, discord_repository)
    except:
        logger.error("Error in handling discord members", exc_info=True)
