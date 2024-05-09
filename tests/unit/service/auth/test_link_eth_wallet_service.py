from unittest.mock import MagicMock
from uuid import UUID

import pytest

from points.domain.dashboard.entities import User
from points.domain.events.entities import EVENT_CONNECT_WALLET
from points.domain.events.entities import QuestEvent
from points.service.auth import link_eth_wallet_service as service
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.error_responses import ValidationAPIError
from tests.unit.mocks.mock_auth_repository import AuthRepositoryPsqlMock

random_uuid = UUID("dbc72453-a34d-47a3-b8fe-2a30b4f29c2d")


def setup_function():
    service.verify_signature = MagicMock()
    service.verify_signature.execute.return_value = True


def get_event_repository():
    repo = MagicMock()
    repo.get_user_events.return_value = []
    return repo


def test_link_eth_wallet():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    user = User(
        user_id=random_uuid,
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    result = service.execute(request, user, auth_repository, get_event_repository(), user_repository)
    assert result == LinkEthWalletResponse(success=True)
    service.verify_signature.execute.assert_called_with(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079",
        auth_repository=auth_repository,
    )


def test_save_user_eth_wallet():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    user = User(
        user_id=random_uuid,
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    result = service.execute(request, user, auth_repository, get_event_repository(), user_repository)
    assert result == LinkEthWalletResponse(success=True)
    user_repository.update_wallet_address.assert_called_with(user.x_id, "0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079")


def test_link_eth_wallet_invalid_wallet_address():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0xMock2"
    )
    user = User(
        user_id=random_uuid,
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    with pytest.raises(ValidationAPIError):
        service.execute(request, user, auth_repository, get_event_repository(), user_repository)


def test_add_event():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    user = User(
        user_id=random_uuid,
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    event_repo = get_event_repository()
    result = service.execute(request, user, auth_repository, event_repo, user_repository)
    assert result == LinkEthWalletResponse(success=True)

    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_CONNECT_WALLET.name,
            points=EVENT_CONNECT_WALLET.points,
            event_description=None,
            logs=None,
        )
    )


def test_not_add_event_if_exists():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    user = User(
        user_id=random_uuid,
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    event_repo = get_event_repository()
    event_repo.get_user_events.return_value = [
        QuestEvent(
            user_profile_id=user.user_id,
            event_name=EVENT_CONNECT_WALLET.name,
            points=EVENT_CONNECT_WALLET.points,
            event_description=None,
            logs=None,
        )
    ]
    result = service.execute(request, user, auth_repository, event_repo, user_repository)
    assert result == LinkEthWalletResponse(success=True)

    event_repo.add_event.assert_not_called()
