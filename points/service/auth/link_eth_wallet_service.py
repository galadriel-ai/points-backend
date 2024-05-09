from eth_utils import is_address

from points.domain.auth import verify_signature
from points.domain.dashboard.entities import User
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.error_responses import ValidationAPIError


def execute(
    request: LinkEthWalletRequest,
    user: User,
    auth_repository: AuthRepositoryPsql,
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
    return LinkEthWalletResponse(success=result)
