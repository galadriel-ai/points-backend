import uuid_extensions as uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Index
from sqlalchemy import text

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
    __table_args__ = (
        Index('idx_unique_signature', 'signature', unique=True,
              postgresql_where=text("signature IS NOT NULL AND signature != ''")),
        {},
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    user_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey(UserProfile.id),
        nullable=False
    )

    event_name = Column(ENUM(
        "connect_wallet",
        "used_faucet",
        "make_tx",
        "deploy_contract",
        "join_discord",
        "follow_galardiel_on_x",
        "manual",
        name='event_name_enum'
    ), nullable=False, unique=False)
    event_description = Column(String, nullable=True, unique=False)
    points = Column(Integer, nullable=False, unique=False)
    logs = Column(JSON, nullable=True, unique=False)
    signature = Column(String, nullable=True, unique=False)

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


class UserToken(Base):
    __tablename__ = "user_token"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    __table_args__ = (
        UniqueConstraint("user_profile_id", "token_issuer", name="_user_issuer_uc"),
    )
    user_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey(UserProfile.id),
        nullable=False,
    )
    token_issuer = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, nullable=False)
