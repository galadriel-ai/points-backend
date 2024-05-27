from points.domain.admin import verify_post_points_signature
from points.service.admin.entities import PostPointsRequest

VALID_ADDRESS = "0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"
VALID_ADDRESS2 = "0xAB0bd413941bB7f05d3825d5d67103e91AEf1A1D"
INVALID_ADDRESS = "0x49f2e94b9015d3d02AD484FC5A9fDa9bDe359222"


def test_incorrect_address():
    request = PostPointsRequest(
        x_username="0663e0f5-caca-7340-8000-76ea01fd2325",
        points=567,
        event_description="test2",
        signature="0xcbd07de2f14d856c1bfdf5303938a186a8ef9ffa7fa47d42923760b991c0bd217fde969eb52e1046ae54f0f7e364ebb0abeb1a940884f2643faeb3cfcde19d161b",
        wallet_address=INVALID_ADDRESS
    )

    result = verify_post_points_signature.execute(request, [VALID_ADDRESS])
    assert not result


def test_invalid_uuid():
    request = PostPointsRequest(
        x_username="0663e0f5",
        points=567,
        event_description="test2",
        signature="0xcbd07de2f14d856c1bfdf5303938a186a8ef9ffa7fa47d42923760b991c0bd217fde969eb52e1046ae54f0f7e364ebb0abeb1a940884f2643faeb3cfcde19d161b",
        wallet_address=VALID_ADDRESS
    )

    result = verify_post_points_signature.execute(request, [VALID_ADDRESS])
    assert not result


def test_valid_but_not_whitelisted():
    request = PostPointsRequest(
        x_username="0663e0f5-caca-7340-8000-76ea01fd2325",
        points=567,
        event_description="test2",
        signature="0xcbd07de2f14d856c1bfdf5303938a186a8ef9ffa7fa47d42923760b991c0bd217fde969eb52e1046ae54f0f7e364ebb0abeb1a940884f2643faeb3cfcde19d161b",
        wallet_address=VALID_ADDRESS
    )

    result = verify_post_points_signature.execute(request, [INVALID_ADDRESS])
    assert not result


def test_valid():
    request = PostPointsRequest(
        x_username="randomGuy",
        points=567,
        event_description="test2",
        signature="0x00d19a2b4fbaf0d8498c8be6e92e2554990a01fc4cb504602e5885c168333f717df457dfb7b91383c810ec3b7f123e59245916079825e5e3067997575076c79e1b",
        wallet_address=VALID_ADDRESS2
    )

    result = verify_post_points_signature.execute(request, [VALID_ADDRESS, VALID_ADDRESS2])
    assert result
