from eth_utils import is_address

from points.domain.auth import verify_signature
from points.repository.auth_repository import AuthRepositoryPsql
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.error_responses import ValidationAPIError


def execute(
    request: LinkEthWalletRequest,
    auth_repository: AuthRepositoryPsql
) -> LinkEthWalletResponse:
    if not is_address(request.wallet_address):
        raise ValidationAPIError("wallet_address is incorrect")

    result = verify_signature.execute(
        signature=request.signature,
        wallet_address=request.wallet_address,
        auth_repository=auth_repository,
    )
    return LinkEthWalletResponse(success=result)
