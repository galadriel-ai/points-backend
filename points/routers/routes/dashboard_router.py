from fastapi import APIRouter

from points.repository import connection
from points.repository.user_repository import UserRepositoryPsql
from points.service.dashboard.entities import DashboardRequest
from points.service.dashboard.entities import DashboardResponse
from points.service.dashboard.entities import UserListItem

TAG = "Router"
router = APIRouter()
router.tags = [TAG]


@router.post(
    "/v1/dashboard",
    response_model=DashboardResponse
)
async def endpoint(
    request: DashboardRequest,
) -> DashboardResponse:
    users = [
        UserListItem(
            x_name="@mock1",
            points="5000 XP"
        ),
        UserListItem(
            x_name="@mock2",
            points="4000 XP"
        ),
        UserListItem(
            x_name="@mock3",
            points="3000 XP"
        )
    ]
    user_repository = UserRepositoryPsql(connection.get_session_maker())
    recently_joined = user_repository.get_recently_joined(10)
    return DashboardResponse(
        leaderboard_users=users,
        recently_joined_users=[UserListItem(
            x_name=u.x_username,
            points=str(u.points),
        ) for u in recently_joined],
    )
