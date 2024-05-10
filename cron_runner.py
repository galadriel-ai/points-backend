import asyncio
from typing import Awaitable
from typing import Callable

import settings
from points import api_logger
from points.crons import chain_usage_job
from points.crons import discord_members_job
from points.repository import connection
from points.repository.event_repository import EventRepositoryPsql
from points.repository.discord_repository import DiscordRepository
from points.repository.explorer_repository import ExplorerRepositoryHTTP
from points.repository.leaderboard_repository import LeaderboardRepositoryPsql

logger = api_logger.get()


async def start_cron_jobs():
    tasks = [
        (_run_chain_usage_job, "Chain usage by wallet job", 60),
        (_run_leaderboard_job, "Leaderboard job", 60),
        (_run_discord_members_job, "Discord members job", 60),
    ]

    await asyncio.gather(*[_cron_runner(*t) for t in tasks])
    logger.info("Cron jobs done")


async def _cron_runner(
    job_callback: Callable[..., Awaitable[None]],
    job_name: str,
    timeout: int,
    *args
):
    while True:
        try:
            logger.debug(f"Started {job_name} job")
            await job_callback(*args)
            logger.debug(
                f"Finished {job_name} job, restarting in {timeout} seconds")
            await asyncio.sleep(timeout)
        except Exception as e:
            logger.error(f"{job_name} job failed, restarting", exc_info=True)
            await asyncio.sleep(timeout)


async def _run_chain_usage_job():
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    explorer_repository = ExplorerRepositoryHTTP(settings.EXPLORER_API_BASE_URL)
    await chain_usage_job.execute(event_repository, explorer_repository)


async def _run_leaderboard_job():
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    leaderboard_repository = LeaderboardRepositoryPsql(connection.get_session_maker())
    total_points = event_repository.get_total_points()
    for data in total_points:
        leaderboard_repository.insert_entry(data["user_profile_id"], data["points"])


async def _run_discord_members_job():
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    discord_repository = DiscordRepository()
    await discord_members_job.execute(event_repository, discord_repository)


if __name__ == "__main__":
    connection.init_default()
    asyncio.run(start_cron_jobs())
