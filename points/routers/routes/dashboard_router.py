from fastapi import APIRouter
from fastapi import Depends
from starlette.responses import JSONResponse

from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository.user_repository import UserRepositoryPsql
from points.service.auth import access_token_service
from points.service.dashboard.entities import DashboardRequest
from points.service.dashboard.entities import DashboardResponse
from points.service.dashboard.entities import UserListItem

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
            points="0",
        ) for u in recently_joined],
    )


@router.get(
    "/v1/dashboard/user",
    response_model=DashboardResponse
)
async def endpoint_user(
    user: User = Depends(
        access_token_service.get_user_from_access_token)
):
    return JSONResponse({"x_username": user.x_username})
