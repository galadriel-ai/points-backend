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


async def execute(
    request: PostPointsRequest,
    admin_repository: AdminRepositoryPsql,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
) -> PostPointsResponse:
    user_profile_id = _validate_uuid(request)
    if not user_profile_id:
        raise error_responses.ValidationAPIError("user_profile_id is not valid")

    user = user_repository.get_by_user_id(user_profile_id)
    if not user:
        raise error_responses.NotFoundAPIError(f"user with {user_profile_id} id")

    admin_wallet_addresses = admin_repository.get_admins_wallet_addresses()
    is_signature_valid = verify_post_points_signature.execute(
        request, admin_wallet_addresses)
    if not is_signature_valid:
        raise error_responses.InvalidSignatureError()

    event = QuestEvent(
        user_profile_id=user_profile_id,
        event_name="manual",
        points=request.points,
        event_description=request.event_description,
        logs={},
        signature=request.signature
    )
    success = event_repository.add_event(event)
    return PostPointsResponse(success=success)


def _validate_uuid(request: PostPointsRequest) -> Optional[UUID]:
    try:
        return UUID(request.user_profile_id)
    except:
        return None
