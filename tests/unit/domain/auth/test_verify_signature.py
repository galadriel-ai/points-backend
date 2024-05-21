import pytest

from points.domain.auth import verify_signature
from points.service import error_responses
from tests.unit.mocks.mock_auth_repository import AuthRepositoryPsqlMock

auth_repository = AuthRepositoryPsqlMock()

SIGNATURE = "0x04f9b0110cf14a9766907d8fc7a5113f5549e882eddbe4609681a7df988334a917cfd1edb6b554b00c4891fe1471a12871bd7e159f49577286d35c16c312323f1c"
WALLET_ADDRESS = "0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
WALLET_ADDRESS_INCORRECT = "0x46030eB314F9d74901B29A7d16835659c37174C7"


def test_verify_signature():
    result = verify_signature.execute(SIGNATURE, WALLET_ADDRESS, auth_repository)
    assert result


def test_verify_signature_lower_case_address():
    result = verify_signature.execute(
        SIGNATURE, WALLET_ADDRESS.lower(), auth_repository)
    assert result


def test_verify_signature_wrong_address():
    with pytest.raises(error_responses.InvalidSignatureError):
        verify_signature.execute(
            SIGNATURE, WALLET_ADDRESS_INCORRECT, auth_repository)
