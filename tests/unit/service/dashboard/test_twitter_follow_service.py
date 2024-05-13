import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

from points.domain.auth.entities import AccessToken
from points.domain.auth.entities import TokenIssuer
from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_FOLLOW_ON_X
from points.domain.events.entities import QuestEvent
from points.service.dashboard import twitter_follow_service as service
from points.service.dashboard.entities import FollowTwitterResponse

USER_ID = UUID("c2c6cdda-3152-4f7a-8c97-f75c2426d7bf")


def setup():
    service.api_logger = MagicMock()


def _get_user() -> User:
    return User(
        user_id=USER_ID,
        x_id="1337",
        x_username="crypto hacker",
        wallet_address="0x00000"
    )


async def test_already_following():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = [
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_FOLLOW_ON_X.name,
            points=EVENT_FOLLOW_ON_X.points,
            event_description=None,
            logs=None,
        )
    ]
    auth_repo = MagicMock()

    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        AsyncMock(),
    )
    assert result == FollowTwitterResponse(is_following=True)
    auth_repo.get_user_access_token.assert_not_called()


async def test_no_token_found():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = None
    twitter_repo = AsyncMock()

    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=False)
    twitter_repo.get_is_following_account.assert_not_called()


async def test_not_following_valid_token():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2100, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo = AsyncMock()
    twitter_repo.get_is_following_account.return_value = False

    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=False)
    twitter_repo.get_new_access_token.assert_not_called()


async def test_is_following_valid_token():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2100, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo = AsyncMock()
    twitter_repo.get_is_following_account.return_value = True

    user = _get_user()
    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=True)
    twitter_repo.get_new_access_token.assert_not_called()
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_FOLLOW_ON_X.name,
            points=EVENT_FOLLOW_ON_X.points,
            event_description=None,
            logs=None,
        )
    )


async def test_is_following_old_token():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo = AsyncMock()
    twitter_repo.get_new_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2100, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo.get_is_following_account.return_value = True

    user = _get_user()
    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=True)
    twitter_repo.get_new_access_token.assert_called_with("mock_refresh_token")
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_FOLLOW_ON_X.name,
            points=EVENT_FOLLOW_ON_X.points,
            event_description=None,
            logs=None,
        )
    )


async def test_not_following_old_token():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo = AsyncMock()
    new_token = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2100, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo.get_new_access_token.return_value = new_token
    twitter_repo.get_is_following_account.return_value = False

    user = _get_user()
    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=False)
    auth_repo.save_user_access_token.assert_called_with(
        user.user_id,
        TokenIssuer.TWITTER,
        new_token.access_token,
        new_token.refresh_token,
        int(new_token.expires_at.timestamp()),
    )
    twitter_repo.get_new_access_token.assert_called_with("mock_refresh_token")
    event_repo.add_event.assert_not_called()


async def test_fail_to_get_new_token():
    event_repo = MagicMock()
    event_repo.get_user_events.return_value = []
    auth_repo = MagicMock()
    auth_repo.get_user_access_token.return_value = AccessToken(
        token_issuer=TokenIssuer.TWITTER,
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        expires_at=datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC),
    )
    twitter_repo = AsyncMock()
    twitter_repo.get_new_access_token.return_value = None

    result = await service.execute(
        _get_user(),
        event_repo,
        auth_repo,
        twitter_repo,
    )
    assert result == FollowTwitterResponse(is_following=False)
    twitter_repo.get_new_access_token.assert_called_with("mock_refresh_token")
    twitter_repo.get_is_following_account.assert_not_called()
