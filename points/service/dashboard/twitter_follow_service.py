import points.repository.utils as db_utils
from points import api_logger
from points.domain.auth.entities import TwitterAccessToken
from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_FOLLOW_ON_X
from points.domain.events.entities import QuestEvent
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.twitter_repository import TwitterRepositoryHTTP
from points.service.dashboard.entities import FollowTwitterResponse

logger = api_logger.get()

TWITTER_API_BASE_URL = "https://api.twitter.com/2"


async def execute(
    user: User,
    event_repository: EventRepositoryPsql,
    auth_repository: AuthRepositoryPsql,
    twitter_repository: TwitterRepositoryHTTP
) -> FollowTwitterResponse:
    user_events = event_repository.get_user_events(user_profile_id=user.user_id)
    is_following_already = bool([e for e in user_events if e.event_name == EVENT_FOLLOW_ON_X.name])
    if is_following_already:
        return FollowTwitterResponse(is_following=True)

    token: TwitterAccessToken = auth_repository.get_user_twitter_token(user.user_id)
    if not token:
        return FollowTwitterResponse(is_following=False)
    if token.expires_at < db_utils.now():
        new_token = await twitter_repository.get_new_access_token(token.refresh_token)
        if new_token:
            auth_repository.save_user_twitter_token(
                user.user_id,
                new_token.access_token,
                new_token.refresh_token,
                int(new_token.expires_at.timestamp())
            )
            token = new_token
        else:
            return FollowTwitterResponse(is_following=False)

    is_following = await twitter_repository.get_is_following_account(token.access_token)
    if is_following:
        event_repository.add_event(QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_FOLLOW_ON_X.name,
            points=EVENT_FOLLOW_ON_X.points,
            event_description=None,
            logs=None,
        ))

    return FollowTwitterResponse(is_following=is_following)
