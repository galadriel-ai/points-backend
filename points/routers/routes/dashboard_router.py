from typing import List

from fastapi import APIRouter
from fastapi import Depends

import settings
from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.leaderboard_repository import LeaderboardEntry
from points.repository.leaderboard_repository import LeaderboardRepositoryPsql
from points.repository.leaderboard_repository import RecentlyJoinedEntry
from points.repository.twitter_repository import TwitterRepositoryHTTP
from points.service.auth import access_token_service
from points.service.dashboard import quests_service
from points.service.dashboard import twitter_follow_service
from points.service.dashboard.entities import DashboardRequest
from points.service.dashboard.entities import DashboardResponse
from points.service.dashboard.entities import FollowTwitterResponse
from points.service.dashboard.entities import LeaderboardItem
from points.service.dashboard.entities import RecentlyJoinedItem
from points.service.dashboard.entities import UserQuestsResponse

TAG = "Dashboard"
router = APIRouter(prefix="/v1")
router.tags = [TAG]


# Uncomment when needed
# @router.get(
#     "/dashboard",
#     response_model=DashboardResponse,
# )
# async def endpoint() -> DashboardResponse:
#     repository = LeaderboardRepositoryPsql(connection.get_session_maker())
#     leaderboard = repository.get_leaderboard()
#     recently_joined = repository.get_recently_joined()
#     return DashboardResponse(
#         leaderboard_users=_map_leaderboard(leaderboard),
#         recently_joined_users=_map_recently_joined(recently_joined)
#     )


def _map_leaderboard(leaderboard: List[LeaderboardEntry]) -> List[LeaderboardItem]:
    result = []
    for item in leaderboard:
        result.append(LeaderboardItem(
            x_username=item.user.x_username,
            points=item.points,
            profile_image_url=item.user.cached_profile_image_url,
        ))
    return result


def _map_recently_joined(
    recently_joined: List[RecentlyJoinedEntry]
) -> List[RecentlyJoinedItem]:
    result = []
    for item in recently_joined:
        result.append(RecentlyJoinedItem(
            x_username=item.user.x_username,
            joined_at=str(item.joined_at),
            profile_image_url=item.user.cached_profile_image_url,
        ))
    return result


@router.get(
    "/dashboard/user",
    response_model=UserQuestsResponse
)
async def endpoint_user(
    user: User = Depends(access_token_service.get_user_from_access_token)
):
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    return await quests_service.execute(user, event_repository)


@router.post(
    "/dashboard/user/follow_twitter",
    response_model=FollowTwitterResponse
)
async def endpoint_user(
    user: User = Depends(access_token_service.get_user_from_access_token)
):
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    twitter_repository = TwitterRepositoryHTTP(
        settings.TWITTER_CLIENT_ID, settings.TWITTER_CLIENT_SECRET)
    return await twitter_follow_service.execute(user, event_repository, auth_repository, twitter_repository)
