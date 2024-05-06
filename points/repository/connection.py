import sqlalchemy
from sqlalchemy.orm import sessionmaker

import settings

engine = None
session_maker = None

DEFAULT_POOL_SIZE = 10
DEFAULT_POOL_OVERFLOW = 100
DEFAULT_POOL_TIMEOUT = 3


def init(
    user,
    password,
    db,
    host='localhost',
    port=5432,
    pool_size=DEFAULT_POOL_SIZE,
    pool_overflow=DEFAULT_POOL_OVERFLOW,
    pool_timeout=DEFAULT_POOL_TIMEOUT
):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    global engine, session_maker
    engine = sqlalchemy.create_engine(
        url,
        client_encoding='utf8',
        max_overflow=pool_overflow,
        pool_timeout=pool_timeout,
        pool_size=pool_size,
        pool_recycle=1800)
    session_maker = sessionmaker(bind=engine)


def init_default():
    _init_all(DEFAULT_POOL_SIZE, DEFAULT_POOL_OVERFLOW, DEFAULT_POOL_TIMEOUT)


def _init_all(pool_size: int, pool_overflow: int, pool_timeout: int):
    init(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        db=settings.DB_DATABASE,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        pool_size=pool_size,
        pool_overflow=pool_overflow,
        pool_timeout=pool_timeout
    )


def get_session_maker():
    global session_maker
    return session_maker
