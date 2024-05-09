from unittest.mock import MagicMock

import pytest

from points.domain.dashboard.entities import User
from points.service.auth import link_eth_wallet_service as service
from points.service.auth.entities import LinkEthWalletRequest
from points.service.auth.entities import LinkEthWalletResponse
from points.service.error_responses import ValidationAPIError
from tests.unit.mocks.mock_auth_repository import AuthRepositoryPsqlMock


def setup_function():
    service.verify_signature = MagicMock()
    service.verify_signature.execute.return_value = True


def test_link_eth_wallet():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    user = User(
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()


    result = service.execute(request, user, auth_repository, user_repository)
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
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()


    result = service.execute(request, user, auth_repository, user_repository)
    assert result == LinkEthWalletResponse(success=True)
    user_repository.update_wallet_address.assert_called_with(user.x_id, "0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079")


def test_link_eth_wallet_invalid_wallet_address():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0xMock2"
    )
    user = User(
        x_id="mock_id",
        x_username="mock_name",
        wallet_address=None,
    )
    auth_repository = AuthRepositoryPsqlMock()
    user_repository = MagicMock()

    with pytest.raises(ValidationAPIError):
        service.execute(request, user, auth_repository, user_repository)
