import uuid_extensions as uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)

    x_id = Column(String, nullable=False, unique=True)
    x_username = Column(String, nullable=False, unique=False)

    wallet_address = Column(String, nullable=True, unique=False)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)


class QuestEvent(Base):
    __tablename__ = "quest_event"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    user_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey(UserProfile.id),
        nullable=False
    )

    event_name = Column(String, nullable=False, unique=False)
    event_description = Column(String, nullable=True, unique=False)
    points = Column(Integer, nullable=False, unique=False)
    logs = Column(JSON, nullable=True, unique=False)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)


class EthSignInChallenges(Base):
    __tablename__ = "eth_signin_challenge"
    wallet_address = Column(String, primary_key=True, nullable=False)
    nonce = Column(String, nullable=False, unique=False)
    issued_at = Column(String, nullable=False, unique=False)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)


class Leaderboard(Base):
    __tablename__ = "leaderboard"
    user_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey(UserProfile.id),
        primary_key=True,
        nullable=False
    )
    points = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)
