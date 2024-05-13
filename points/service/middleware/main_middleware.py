import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from points import api_logger
from points.service.auth import access_token_service
from points.service.error_responses import APIErrorResponse
from points.service.error_responses import RateLimitExceededAPIError
from points.service.middleware import util
from points.service.middleware.entitites import RequestStateKey
from points.service.middleware.rate_limiter import ENDPOINT_RATE_LIMITS
from points.service.middleware.rate_limiter import RateLimiter
from points.utils.http_headers import add_response_headers

logger = api_logger.get()

rate_limiter = RateLimiter()


class MainMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = util.get_state(request, RequestStateKey.REQUEST_ID)
        ip_address = util.get_state(request, RequestStateKey.IP_ADDRESS)
        country = util.get_state(request, RequestStateKey.COUNTRY)

        api_key = request.headers.get("authorization")
        formatted_ip = ip_address or request.client.host or "default"
        logger.info(f"REQUEST RATE LIMITTING INFO: " f" {str(rate_limiter.calls)}")
        if rate_limiter.is_rate_limited(formatted_ip):
            """logger.error(
                f"Error while handling request. request_id={request_id} "
                f"request_path={request.url.path}"
                f"status code={429}"
                f"code={error.to_code()}"
                f"message={error.to_message()}",
                exc_info=is_exc_info
            )"""
            raise RateLimitExceededAPIError(
                f"API rate limited to {rate_limiter.max_calls_per_hour} calls per hour."
            )

        rate_limited_endpoints = [l for l in ENDPOINT_RATE_LIMITS if request.url.path in l.endpoint]
        if api_key and len(rate_limited_endpoints):
            try:
                user = access_token_service.get_user_from_access_token_str(api_key)
                rate_limitting_key = rate_limited_endpoints[0].endpoint + str(user.user_id)
                if user and rate_limiter.is_rate_limited(
                    rate_limitting_key, rate_limited_endpoints[0].limit_per_hour,
                ):
                    raise RateLimitExceededAPIError(
                        f"Endpoint rate limited to {rate_limited_endpoints[0].limit_per_hour} calls per hour."
                    )
            except RateLimitExceededAPIError as e:
                raise e
            except:
                # Endpoint should handle any token checks etc
                pass
        try:
            logger.info(
                f"REQUEST STARTED "
                f"request_id={request_id} "
                f"request_path={request.url.path} "
                f"ip={ip_address} "
                f"country={country} "
            )
            before = time.time()
            response: Response = await call_next(request)

            duration = time.time() - before
            process_time = (time.time() - before) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)
            if response.status_code != 404:
                logger.info(
                    f"REQUEST COMPLETED "
                    f"request_id={request_id} "
                    f"request_path={request.url.path} "
                    f"completed_in={formatted_process_time}ms "
                    f"status_code={response.status_code}"
                )
            return await _get_response_with_headers(response, duration)
        except Exception as error:
            if isinstance(error, APIErrorResponse):
                is_exc_info = error.to_status_code() == 500
                logger.error(
                    f"Error while handling request. request_id={request_id} "
                    f"request_path={request.url.path}"
                    f"status code={error.to_status_code()}"
                    f"code={error.to_code()}"
                    f"message={error.to_message()}",
                    exc_info=is_exc_info,
                )
            else:
                logger.error(
                    f"Error while handling request. request_id={request_id} "
                    f"request_path={request.url.path}",
                    exc_info=True,
                )
            raise error


async def _get_response_with_headers(response, duration):
    response = await add_response_headers(response, duration)
    return response
