import datetime
from uuid import UUID

from uuid_extensions import uuid7


def generate_uuid() -> UUID:
    return uuid7()


def now() -> datetime:
    try:
        return datetime.datetime.now(datetime.UTC)
    except AttributeError:
        return datetime.datetime.utcnow()
