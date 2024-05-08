from unittest.mock import MagicMock

import pytest

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
    auth_repository = AuthRepositoryPsqlMock()

    result = service.execute(request, auth_repository)
    assert result == LinkEthWalletResponse(success=True)
    service.verify_signature.execute.assert_called_with(
        signature="0xMock1",
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079",
        auth_repository=auth_repository,
    )


def test_link_eth_wallet_invalid_wallet_address():
    request = LinkEthWalletRequest(
        signature="0xMock1",
        wallet_address="0xMock2"
    )
    auth_repository = AuthRepositoryPsqlMock()

    with pytest.raises(ValidationAPIError):
        service.execute(request, auth_repository)
