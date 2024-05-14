from points.domain.auth.entities import TokenIssuer
from points.domain.events.entities import EVENT_JOIN_DISCORD
from points.domain.events.entities import QuestEvent
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.repository.discord_repository import DiscordRepository
from points.service.auth.entities import LinkDiscordRequest
from points.service.auth.entities import LinkDiscordResponse


async def execute(
    request: LinkDiscordRequest,
    auth_repository: AuthRepositoryPsql,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
    discord_repository: DiscordRepository,
) -> LinkDiscordResponse:
    user_repository.update_discord_id_and_username(
        request.user_profile_id, request.discord_id, request.discord_username
    )
    auth_repository.save_user_access_token(
        user_id=request.user_profile_id, 
        token_issuer=TokenIssuer.DISCORD,
        access_token=request.discord_token,
        refresh_token=request.discord_refresh_token,
        expires_at=request.discord_token_expires_at,
    )
    is_discord_member = await discord_repository.is_member(request.discord_id, request.discord_token)
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
