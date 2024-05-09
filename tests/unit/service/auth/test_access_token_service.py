from points.service.auth import access_token_service as service


def setup():
    pass


def test_minimal():
    x_id: str = "mock_id"
    token = service.create_access_token(x_id)
    parsed_x_id = service._get_access_token_payload(token)
    assert parsed_x_id == x_id


def test_minimal_get_user():
    x_id: str = "mock_id"
    token = service.create_access_token(x_id)
    parsed_x_id = service._get_access_token_payload(token)
    assert parsed_x_id == x_id
