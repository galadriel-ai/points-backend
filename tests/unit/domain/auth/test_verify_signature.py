from points.domain.auth import verify_signature
from tests.unit.mocks.mock_auth_repository import AuthRepositoryPsqlMock

auth_repository = AuthRepositoryPsqlMock()

SIGNATURE = "0x8b3b8bd7fe7eade3680460835489fd375e6bbc489413b0287e1d9669b4a5d49610c18c005062080bf48b08a5e7e4c147c1cdd4d88ce86a2294a70c1ee061a53e1b"
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
    result = verify_signature.execute(
        SIGNATURE, WALLET_ADDRESS_INCORRECT, auth_repository)
    assert not result
