import pytest

from points.repository.auth_repository import AuthRepositoryPsql
from points.service.auth import generate_nonce_service as service
from points.service.auth.entities import GenerateNonceRequest
from points.service.auth.entities import GenerateNonceResponse
from points.service.error_responses import ValidationAPIError


def test_execute():
    request = GenerateNonceRequest(
        wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
    )
    auth_repository = AuthRepositoryPsql()
    result = service.execute(request, auth_repository)
    assert result == GenerateNonceResponse(
        nonce="cqaakoZsXxz",
        issued_at="2024-05-06T21:01:02.000Z",
    )


def test_execute_invalid_wallet_address():
    request = GenerateNonceRequest(
        wallet_address="0xMock"
    )
    auth_repository = AuthRepositoryPsql()
    with pytest.raises(ValidationAPIError):
        service.execute(request, auth_repository)
