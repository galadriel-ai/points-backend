from fastapi import APIRouter

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
    return GenerateNonceResponse(nonce="abcdeabcd")


@router.post(
    "/v1/auth/eth/link",
    response_model=LinkEthWalletResponse
)
async def link_eth_wallet_endpoint(
    request: LinkEthWalletRequest
) -> LinkEthWalletResponse:
    return LinkEthWalletResponse(success=True)
