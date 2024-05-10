from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_JOIN_DISCORD
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.repository.discord_repository import DiscordRepository
from points.service.auth.entities import LinkDiscordRequest
from points.service.auth.entities import LinkDiscordResponse


async def execute(
    request: LinkDiscordRequest,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
    discord_repository: DiscordRepository,
) -> LinkDiscordResponse:
    user_repository.update_discord_id_and_username(
        request.user_profile_id, request.discord_id, request.discord_username
    )
    is_discord_member = discord_repository.is_member(request.discord_id)
    if not is_discord_member:
        # user is not a member of the discord server, so no points are awarded
        return LinkDiscordResponse(success=True)
    events = event_repository.get_user_events(request.user_profile_id)
    filtered_events = [e for e in events if e.event_name == EVENT_JOIN_DISCORD.name]
    if not len(filtered_events):
        event_repository.add_event(
            QuestEvent(
                user_profile_id=request.user_profile_id,
                event_name=EVENT_JOIN_DISCORD.name,
                points=EVENT_JOIN_DISCORD.points,
                event_description=None,
                logs=None,
            )
        )
    return LinkDiscordResponse(success=True)
