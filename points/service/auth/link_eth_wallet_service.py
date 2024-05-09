from eth_utils import is_address

from points.domain.auth import verify_signature
from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_CONNECT_WALLET
from points.domain.events.entities import QuestEvent
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.repository.web3_repository import Web3Repository
from points.service import error_responses
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse


async def execute(
    request: LinkEthWalletRequest,
    user: User,
    auth_repository: AuthRepositoryPsql,
    event_repository: EventRepositoryPsql,
    user_repository: UserRepositoryPsql,
    web3_repository: Web3Repository,
) -> LinkEthWalletResponse:
    if not is_address(request.wallet_address):
        raise error_responses.ValidationAPIError("wallet_address is incorrect")

    is_wallet_funded = await _is_enough_funds(request.wallet_address, web3_repository)
    if not is_wallet_funded:
        raise error_responses.InvalidCredentialsAPIError("Wallet does not have enough funds")

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


async def _is_enough_funds(wallet_address: str, web3_repository: Web3Repository,) -> bool:
    try:
        return await web3_repository.is_wallet_balance_bigger_than(wallet_address, "0.1")
    except:
        raise error_responses.InternalServerAPIError()
