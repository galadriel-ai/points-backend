from typing import Optional
from uuid import UUID

from points.domain.admin import verify_post_points_signature
from points.repository.admin_repository import AdminRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.service import error_responses
from points.service.admin.entities import PostPointsRequest

from points.service.admin.entities import PostPointsResponse
from points.domain.events.entities import QuestEvent
from points.service.dashboard import quests_service
from points.service.dashboard.entities import UserQuestsResponse


async def execute(
    request: PostPointsRequest,
    admin_repository: AdminRepositoryPsql,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
) -> PostPointsResponse:
    user = user_repository.get_by_x_username(request.x_username)
    if not user:
        raise error_responses.NotFoundAPIError(f"user with x_username: {request.x_username}")

    admin_wallet_addresses = admin_repository.get_admins_wallet_addresses()
    is_signature_valid = verify_post_points_signature.execute(
        request, admin_wallet_addresses)
    if not is_signature_valid:
        raise error_responses.InvalidSignatureError()

    event = QuestEvent(
        user_profile_id=user.user_id,
        event_name="manual",
        points=request.points,
        event_description=request.event_description,
        logs={},
        signature=request.signature
    )

    points_before: UserQuestsResponse = await quests_service.execute(user, event_repository)
    success = event_repository.add_event(event)
    points_after: UserQuestsResponse = await quests_service.execute(user, event_repository)
    return PostPointsResponse(
        success=success,
        points_before=points_before.total_points,
        points_after=points_after.total_points,
    )


def _validate_uuid(request: PostPointsRequest) -> Optional[UUID]:
    try:
        return UUID(request.user_profile_id)
    except:
        return None
