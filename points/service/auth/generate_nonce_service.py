from eth_utils import is_address

from siwe import generate_nonce

from points.domain.auth import generate_issued_at
from points.repository.auth_repository import AuthRepositoryPsql
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.error_responses import InternalServerAPIError
from points.service.error_responses import ValidationAPIError


def execute(
    request: GenerateNonceRequest,
    auth_repository: AuthRepositoryPsql
) -> GenerateNonceResponse:
    if not is_address(request.wallet_address):
        raise ValidationAPIError("wallet_address is incorrect")

    nonce = generate_nonce()
    issued_at = generate_issued_at.execute()

    result = auth_repository.insert_sign_message_components(
        wallet_address=request.wallet_address,
        nonce=nonce,
        issued_at=issued_at,
    )
    if not result:
        raise InternalServerAPIError()
    return GenerateNonceResponse(
        nonce=nonce,
        issued_at=issued_at,
    )
