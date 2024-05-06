import uuid_extensions as uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)

    email = Column(String, nullable=False, unique=True)
    x_username = Column(String, nullable=False, unique=True)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)


