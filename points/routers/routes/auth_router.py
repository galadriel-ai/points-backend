from fastapi import APIRouter

from points.repository import connection
from points.repository.auth_repository import AuthRepositoryPsql
from points.service.auth import generate_nonce_service
from points.service.auth import link_eth_wallet_service
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse

TAG = "Auth"
router = APIRouter()
router.tags = [TAG]


@router.post(
    "/v1/auth/eth/nonce",
    response_model=GenerateNonceResponse
)
async def generate_nonce_endpoint(
    request: GenerateNonceRequest,
) -> GenerateNonceResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    return generate_nonce_service.execute(request, auth_repository)


@router.post(
    "/v1/auth/eth/link",
    response_model=LinkEthWalletResponse
)
async def link_eth_wallet_endpoint(
    request: LinkEthWalletRequest
) -> LinkEthWalletResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    return link_eth_wallet_service.execute(request, auth_repository)
