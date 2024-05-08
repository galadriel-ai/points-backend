from typing import List

from fastapi import APIRouter

from points.repository import connection
from points.repository.leaderboard_repository import LeaderboardEntry
from points.repository.leaderboard_repository import LeaderboardRepositoryPsql
from points.repository.leaderboard_repository import RecentlyJoinedEntry
from points.service.dashboard.entities import DashboardRequest
from points.service.dashboard.entities import DashboardResponse
from points.service.dashboard.entities import LeaderboardItem
from points.service.dashboard.entities import RecentlyJoinedItem

TAG = "Dashboard"
router = APIRouter()
router.tags = [TAG]


@router.post(
    "/v1/dashboard",
    response_model=DashboardResponse
)
async def endpoint(
    request: DashboardRequest,
) -> DashboardResponse:
    repository = LeaderboardRepositoryPsql(connection.get_session_maker())
    leaderboard = repository.get_leaderboard()
    recently_joined = repository.get_recently_joined()
    return DashboardResponse(
        leaderboard_users=_map_leaderboard(leaderboard),
        recently_joined_users=_map_recently_joined(recently_joined)
    )


def _map_leaderboard(leaderboard: List[LeaderboardEntry]) -> List[LeaderboardItem]:
    result = []
    for item in leaderboard:
        result.append(LeaderboardItem(
            x_username=item.user.x_username,
            points=item.points,
        ))
    return result


def _map_recently_joined(
    recently_joined: List[RecentlyJoinedEntry]
) -> List[RecentlyJoinedItem]:
    result = []
    for item in recently_joined:
        result.append(RecentlyJoinedItem(
            x_username=item.user.x_username,
            joined_at=str(item.joined_at)
        ))
    return result
