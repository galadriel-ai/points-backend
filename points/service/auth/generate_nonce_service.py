from eth_utils import is_address

from points.repository.auth_repository import AuthRepositoryPsql
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.error_responses import ValidationAPIError


def execute(
    request: GenerateNonceRequest,
    auth_repository: AuthRepositoryPsql
) -> GenerateNonceResponse:
    if not is_address(request.wallet_address):
        raise ValidationAPIError("wallet_address is incorrect")

    components = auth_repository.generate_sign_message_components(
        request.wallet_address)
    return GenerateNonceResponse(
        nonce=components.nonce,
        issued_at=components.issued_at,
    )
