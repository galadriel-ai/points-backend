from unittest.mock import MagicMock

import pytest

from points.service.auth import generate_nonce_service as service
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.error_responses import ValidationAPIError
from tests.unit.mocks.mock_auth_repository import AuthRepositoryPsqlMock

NONCE = "abcdefg"
ISSUED_AT = "mock-time00"


def setup_function():
    service.generate_nonce = MagicMock()
    service.generate_nonce.return_value = NONCE

    service.generate_issued_at = MagicMock()
    service.generate_issued_at.execute.return_value = ISSUED_AT


def test_execute():
    request = GenerateNonceRequest(
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    auth_repository = AuthRepositoryPsqlMock()
    result = service.execute(request, auth_repository)
    assert result == GenerateNonceResponse(
        nonce=NONCE,
        issued_at=ISSUED_AT,
    )


def test_execute_invalid_wallet_address():
    request = GenerateNonceRequest(
        wallet_address="0xMock"
    )
    auth_repository = AuthRepositoryPsqlMock()
    with pytest.raises(ValidationAPIError):
        service.execute(request, auth_repository)
