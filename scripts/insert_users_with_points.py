from points.domain.dashboard.entities import User
from points.repository import connection
from points.repository.user_repository import UserRepositoryPsql

connection.init_default()

repository = UserRepositoryPsql(connection.get_session_maker())

user1 = User(
    x_username="juhan",
    email="juhan@joku.com",
    wallet_address="0xa61347Fef2cF2D83a1d2c97E74BC142c22c40cA0",
)

user2 = User(
    x_username="kaspar",
    email="kaspar@nftport.xyz",
    wallet_address="0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079",
)

repository.insert(user1)
repository.insert(user2)
