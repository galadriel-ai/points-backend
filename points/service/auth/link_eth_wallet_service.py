from eth_utils import is_address

from points.domain.auth import verify_signature
from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_CONNECT_WALLET
from points.domain.events.entities import QuestEvent
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.error_responses import ValidationAPIError


def execute(
    request: LinkEthWalletRequest,
    user: User,
    auth_repository: AuthRepositoryPsql,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
) -> LinkEthWalletResponse:
    if not is_address(request.wallet_address):
        raise ValidationAPIError("wallet_address is incorrect")

    result: bool = verify_signature.execute(
        signature=request.signature,
        wallet_address=request.wallet_address,
        auth_repository=auth_repository,
    )
    if result:
        user_repository.update_wallet_address(user.x_id, request.wallet_address)

        events = event_repository.get_user_events(user.user_id)
        filtered_events = [e for e in events if e.event_name == EVENT_CONNECT_WALLET.name]
        if not len(filtered_events):
            event_repository.add_event(QuestEvent(
                user_profile_id=user.user_id,
                event_name=EVENT_CONNECT_WALLET.name,
                points=EVENT_CONNECT_WALLET.points,
                event_description=None,
                logs=None,
            ))
    return LinkEthWalletResponse(success=result)
