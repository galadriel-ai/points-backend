from base64 import b64encode
from datetime import timedelta
from typing import Optional

import aiohttp

import points.repository.utils as db_utils
import settings
from points import api_logger
from points.domain.auth.entities import TwitterAccessToken
from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_FOLLOW_ON_X
from points.domain.events.entities import QuestEvent
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.service.dashboard.entities import FollowTwitterResponse

logger = api_logger.get()


async def execute(
    user: User,
    event_repository: EventRepositoryPsql,
    auth_repository: AuthRepositoryPsql,
) -> FollowTwitterResponse:
    user_events = event_repository.get_user_events(user_profile_id=user.user_id)
    is_following_already = bool([e for e in user_events if e.event_name == EVENT_FOLLOW_ON_X.name])
    if is_following_already:
        return FollowTwitterResponse(is_following=True)

    token: TwitterAccessToken = auth_repository.get_user_twitter_token(user.user_id)
    if not token:
        return FollowTwitterResponse(is_following=False)
    if token.expires_at < db_utils.now():
        new_token = await _get_new_access_token(token.refresh_token)
        if new_token:
            auth_repository.save_user_twitter_token(
                user.user_id,
                new_token.access_token,
                new_token.refresh_token,
                int(new_token.expires_at.timestamp())
            )
            token = new_token

    is_following = await _get_is_following(token.access_token)
    if is_following:
        event_repository.add_event(QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_FOLLOW_ON_X.name,
            points=EVENT_FOLLOW_ON_X.points,
            event_description=None,
            logs=None,
        ))

    return FollowTwitterResponse(is_following=is_following)


async def _get_is_following(access_token: str):
    try:
        async with aiohttp.ClientSession() as session:
            session.headers.update({
                "Authorization": f"Bearer {access_token}"
            })
            res = await session.get("https://api.twitter.com/2/users/1384448028774383616?user.fields=connection_status")
            res_json = await res.json()
            return "following" in res_json.get("data", {}).get("connection_status", [])
    except Exception as e:
        logger.error("Failed to query user twitter following status", exc_info=True)
    return False


async def _get_new_access_token(refresh_token: str) -> Optional[TwitterAccessToken]:
    client_creds = f"{settings.TWITTER_CLIENT_ID}:{settings.TWITTER_CLIENT_SECRET}"
    client_creds_b64 = b64encode(client_creds.encode()).decode()

    url = "https://api.twitter.com/2/oauth2/token"
    try:
        headers = {
            'Authorization': f'Basic {client_creds_b64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field("refresh_token", refresh_token)
            form_data.add_field("grant_type", "refresh_token")
            form_data.add_field("client_id", settings.TWITTER_CLIENT_ID)

            session.headers.update(headers)
            async with session.post(url, data=form_data) as response:
                res_json = await response.json()
            return TwitterAccessToken(
                access_token=res_json["access_token"],
                refresh_token=res_json["refresh_token"],
                expires_at=db_utils.now() + timedelta(seconds=res_json["expires_in"])
            )
    except Exception as e:
        logger.error("Failed to get new user twitter access token", exc_info=True)
        return None
