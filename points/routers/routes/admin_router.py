from fastapi import APIRouter

import settings
from points.repository import connection
from points.repository.admin_repository import AdminRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.service.admin import post_points_service
from points.service.admin.entities import PostPointsRequest
from points.service.admin.entities import PostPointsResponse

TAG = "Admin"
router = APIRouter(prefix="/v1/auth")
router.tags = [TAG]


@router.post(
    "/admin/points",
    response_model=PostPointsResponse,
    include_in_schema=not settings.is_production()
)
async def post_points(
    request: PostPointsRequest,
) -> PostPointsResponse:
    admin_repository = AdminRepositoryPsql(connection.get_session_maker())
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    user_repository = UserRepositoryPsql(connection.get_session_maker())
    return await post_points_service.execute(
        request=request,
        admin_repository=admin_repository,
        event_repository=event_repository,
        user_repository=user_repository)
