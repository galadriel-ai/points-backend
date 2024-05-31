from datetime import datetime
from datetime import timezone
from urllib.parse import urlencode
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.base import DiscoveryDocument
from fastapi_sso.sso.twitter import TwitterSSO
from fastapi_sso.sso.generic import create_provider
from starlette.requests import Request

import settings
from points import api_logger
from points.domain.auth.entities import TokenIssuer
from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository.auth_repository import AuthRepositoryPsql
from points.repository.event_repository import EventRepositoryPsql
from points.repository.user_repository import UserRepositoryPsql
from points.repository.web3_repository import Web3Repository
from points.repository.discord_repository import DiscordRepository
from points.repository.whitelist_repository import WhitelistRepository
from points.service import utils
from points.service.auth import access_token_service
from points.service.auth import generate_nonce_service
from points.service.auth import link_eth_wallet_service
from points.service.auth import link_discord_service
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.auth.entities import LinkDiscordRequest
from points.service.auth.entities import LinkDiscordResponse
from points.repository import utils as db_utils

TAG = "Auth"
router = APIRouter(prefix="/v1/auth")
router.tags = [TAG]

logger = api_logger.get()

MIN_TWITTER_ACCOUNT_AGE_DAYS = 21


class TwitterUpdatedSSO(TwitterSSO):
    scope = ["users.read", "follows.read", "tweet.read", "offline.access"]

    async def get_discovery_document(self) -> DiscoveryDocument:
        return {
            "authorization_endpoint": "https://twitter.com/i/oauth2/authorize",
            "token_endpoint": "https://api.twitter.com/2/oauth2/token",
            "userinfo_endpoint": "https://api.twitter.com/2/users/me?user.fields=created_at,profile_image_url",
        }


xtwitter_sso = TwitterUpdatedSSO(
    settings.TWITTER_CLIENT_ID,
    settings.TWITTER_CLIENT_SECRET,
    settings.TWITTER_AUTH_CALLBACK,
    allow_insecure_http=not settings.is_production(),
)

discord_discovery = {
    "authorization_endpoint": "https://discord.com/api/oauth2/authorize",
    "token_endpoint": "https://discord.com/api/oauth2/token",
    "userinfo_endpoint": "https://discord.com/api/users/@me",
}

DiscordProvider = create_provider(
    name="discord",
    discovery_document=discord_discovery,
    default_scope="identify guilds guilds.members.read",
)

discord_sso = DiscordProvider(
    client_id=settings.DISCORD_CLIENT_ID,
    client_secret=settings.DISCORD_CLIENT_SECRET,
    redirect_uri=settings.DISCORD_AUTH_CALLBACK,
    allow_insecure_http=not settings.is_production(),
)


@router.get("/x/login")
async def twitter_login():
    with xtwitter_sso:
        return await xtwitter_sso.get_login_redirect()


@router.get("/x/callback")
async def twitter_callback(request: Request):
    try:
        twitter_access_token = None
        with xtwitter_sso:
            twitter_user = await xtwitter_sso.verify_and_process(request, convert_response=False)
            user_x_id = twitter_user["data"]["id"]
            try:
                twitter_access_token = xtwitter_sso.access_token
                twitter_access_token_expires_at = int(xtwitter_sso.oauth_client.token.get("expires_at"))
                refresh_token = xtwitter_sso.oauth_client.refresh_token
            except:
                logger.error(f"Failed to parse twitter access token data, user_x_id={user_x_id}")

        whitelist_repository = WhitelistRepository()
        if not whitelist_repository.is_whitelisted(user_x_id):
            return RedirectResponse(
                url=settings.FRONTEND_AUTH_CALLBACK_URL + "?" + urlencode({"error": "no_access"}),
                status_code=status.HTTP_302_FOUND
            )

        user_x_name = twitter_user["data"]["username"]
        image_url = twitter_user["data"].get("profile_image_url")

        user_repository = UserRepositoryPsql(connection.get_session_maker())
        user = user_repository.get_by_x_id(user_x_id)
        user_id: UUID
        if not user:
            # Once the system is public, uncomment this part
            # created_at = twitter_user["data"].get("created_at")
            # created_at_dt = db_utils.now()
            # if created_at:
            #     created_at_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
            # now = db_utils.now()
            # if (now - created_at_dt).days < MIN_TWITTER_ACCOUNT_AGE_DAYS:
            #     return RedirectResponse(
            #         url=settings.FRONTEND_AUTH_CALLBACK_URL + "?" + urlencode({"error": "account too new"}),
            #         status_code=status.HTTP_302_FOUND
            #     )

            user_id = user_repository.insert(
                x_id=user_x_id,
                x_username=user_x_name,
                profile_image_url=image_url,
                wallet_address=None,
            )
        else:
            user_id = user.user_id

        auth_repo = AuthRepositoryPsql(connection.get_session_maker())
        try:
            if twitter_access_token:
                auth_repo.save_user_access_token(
                    user_id,
                    TokenIssuer.TWITTER,
                    twitter_access_token,
                    refresh_token,
                    twitter_access_token_expires_at
                )
        except Exception as e:
            logger.error(f"Failed to save user twitter access token, user_id={user_id}", exc_info=True)
            return RedirectResponse(
                url=settings.FRONTEND_AUTH_CALLBACK_URL + "?" + urlencode({"error": "unexpected error"}),
                status_code=status.HTTP_302_FOUND
            )

        access_token: str = access_token_service.create_access_token(user_x_id)
        response = RedirectResponse(
            url=settings.FRONTEND_AUTH_CALLBACK_URL
                + "?"
                + urlencode({"token": access_token}),
            status_code=status.HTTP_302_FOUND,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )


@router.post("/eth/nonce", response_model=GenerateNonceResponse)
async def generate_nonce_endpoint(
    request: GenerateNonceRequest,
    _: User = Depends(access_token_service.get_user_from_access_token),
) -> GenerateNonceResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    return generate_nonce_service.execute(request, auth_repository)


@router.post("/eth/link", response_model=LinkEthWalletResponse)
async def link_eth_wallet_endpoint(
    request: LinkEthWalletRequest,
    user: User = Depends(access_token_service.get_user_from_access_token),
) -> LinkEthWalletResponse:
    auth_repository = AuthRepositoryPsql(connection.get_session_maker())
    event_repository = EventRepositoryPsql(connection.get_session_maker())
    user_repository = UserRepositoryPsql(connection.get_session_maker())
    web3_repository = Web3Repository()
    return await link_eth_wallet_service.execute(
        request, user, auth_repository, event_repository, user_repository, web3_repository
    )


@router.get("/discord/link", response_model=LinkDiscordResponse)
async def link_discord_endpoint(
    user: User = Depends(access_token_service.get_user_from_access_token),
):
    with discord_sso:
        response = await discord_sso.get_login_redirect(state=str(user.user_id))
        return LinkDiscordResponse(redirect_url=response.headers["location"])


@router.get("/discord/callback")
async def discord_callback(request: Request):
    try:
        with discord_sso:
            user = await discord_sso.verify_and_process(request, convert_response=False)
            discord_access_token = discord_sso.access_token
            discord_access_token_expires_at = int(discord_sso.oauth_client.token.get("expires_at"))
            discord_refresh_token = discord_sso.oauth_client.refresh_token
        user_id = utils.get_uuid(request.query_params.get("state"))
        user_discord_id = user["id"]
        user_discord_username = user["username"]

        auth_repository = AuthRepositoryPsql(connection.get_session_maker())
        event_repository = EventRepositoryPsql(connection.get_session_maker())
        user_repository = UserRepositoryPsql(connection.get_session_maker())
        discord_callback = DiscordRepository()

        discord_response = await link_discord_service.execute(
            LinkDiscordRequest(
                user_profile_id=user_id,
                discord_id=user_discord_id,
                discord_username=user_discord_username,
                discord_token=discord_access_token,
                discord_refresh_token=discord_refresh_token,
                discord_token_expires_at=discord_access_token_expires_at,
            ),
            auth_repository,
            event_repository,
            user_repository,
            discord_callback,
        )
        return RedirectResponse(
            url=settings.FRONTEND_DISCORD_CALLBACK_URL
                + "?"
                + urlencode({"success": discord_response.success, "is_member": discord_response.is_member}),
            status_code=status.HTTP_302_FOUND,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred. Report this message to support: {e}",
        )
