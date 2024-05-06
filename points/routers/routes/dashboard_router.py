from fastapi import APIRouter

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
            name="Mock 1",
            x_name="@mock1",
            points="5000 XP"
        ),
        UserListItem(
            name="Mock 2",
            x_name="@mock2",
            points="4000 XP"
        ),
        UserListItem(
            name="Mock 3",
            x_name="@mock3",
            points="3000 XP"
        )
    ]
    return DashboardResponse(
        leaderboard_users=users,
        recently_joined_users=users,
    )
