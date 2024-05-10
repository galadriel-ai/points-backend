from urllib.parse import urlencode

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.twitter import TwitterSSO
from starlette.requests import Request

import settings
from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.repository.web3_repository import Web3Repository
from points.service.auth import access_token_service
from points.service.auth import generate_nonce_service
from points.service.auth import link_eth_wallet_service
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse

TAG = "Auth"
router = APIRouter(prefix="/v1/auth")
router.tags = [TAG]

xtwitter_sso = TwitterSSO(
    settings.TWITTER_CLIENT_ID,
    settings.TWITTER_CLIENT_SECRET,
    settings.TWITTER_AUTH_CALLBACK,
    allow_insecure_http=not settings.is_production()
)


@router.get("/x/login")
async def twitter_login():
    with xtwitter_sso:
        return await xtwitter_sso.get_login_redirect()


@router.get("/x/callback")
async def twitter_callback(request: Request):
    try:
        with xtwitter_sso:
            user = await xtwitter_sso.verify_and_process(request)
        user_x_id = user.id
        user_x_name = user.display_name

        user_repository = UserRepositoryPsql(connection.get_session_maker())
        existing_user = user_repository.get_by_x_id(user_x_id)
        if not existing_user:
            user_repository.insert(
                x_id=user_x_id,
                x_username=user_x_name,
                wallet_address=None,
            )
        access_token: str = access_token_service.create_access_token(user_x_id)
        response = RedirectResponse(
            url=settings.FRONTEND_AUTH_CALLBACK_URL + "?" + urlencode({"token": access_token}),
            status_code=status.HTTP_302_FOUND
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}"
        )


@router.post(
    "/eth/nonce",
    response_model=GenerateNonceResponse
)
async def generate_nonce_endpoint(
    request: GenerateNonceRequest,
    _: User = Depends(access_token_service.get_user_from_access_token),
) -> GenerateNonceResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    return generate_nonce_service.execute(request, auth_repository)


@router.post(
    "/eth/link",
    response_model=LinkEthWalletResponse
)
async def link_eth_wallet_endpoint(
    request: LinkEthWalletRequest,
    user: User = Depends(access_token_service.get_user_from_access_token),
) -> LinkEthWalletResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    user_repository = UserRepositoryPsql(connection.get_session_maker())
    web3_repository = Web3Repository()
    return await link_eth_wallet_service.execute(
        request,
        user,
        auth_repository,
        event_repository,
        user_repository,
        web3_repository
    )
