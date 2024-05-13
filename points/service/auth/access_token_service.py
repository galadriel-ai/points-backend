from datetime import timedelta
from typing import Optional

from fastapi import Security
from fastapi.security import APIKeyHeader
from jose import JWTError
from jose import jwt
from jose.constants import ALGORITHMS

import settings
from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository import utils
from points.repository.user_repository import UserRepositoryPsql
from points.service import error_responses

ACCESS_TOKEN_EXPIRE_DAYS: int = 3

API_KEY_NAME = "Authorization"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def create_access_token(x_id: str) -> str:
    expires_in = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    expire = utils.now() + expires_in

    to_encode = {
        "x_id": x_id,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHMS.HS256)
    return encoded_jwt


def get_user_from_access_token(session_token: str = Security(API_KEY_HEADER)) -> Optional[User]:
    return get_user_from_access_token_str(session_token)


def get_user_from_access_token_str(session_token: str) -> Optional[User]:
    x_id: str = _get_access_token_payload(session_token)
    return _get_user_from_x_id(x_id)


def _get_access_token_payload(session_token: str) -> Optional[str]:
    try:
        payload = jwt.decode(session_token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHMS.HS256])
        x_id: str = payload.get("x_id")
        if x_id is None:
            raise error_responses.InvalidCredentialsAPIError("Token could not be validated")
        return x_id
    except JWTError:
        raise error_responses.InvalidCredentialsAPIError("Invalid access token")
    except:
        raise error_responses.InvalidCredentialsAPIError()


def _get_user_from_x_id(x_id: str) -> User:
    user_repository = UserRepositoryPsql(connection.get_session_maker())
    user = user_repository.get_by_x_id(x_id)
    if not user:
        raise error_responses.InvalidCredentialsAPIError()
    return user
