from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class EventSpecification:
    name: str
    points: int


# TODO: kind of hardcoded here at the moment
EVENT_CONNECT_WALLET = EventSpecification(name="connect_wallet", points=50)
EVENT_FAUCET = EventSpecification(name="used_faucet", points=50)
EVENT_MAKE_TX = EventSpecification(name="make_tx", points=50)
EVENT_DEPLOY_CONTRACT = EventSpecification(name="deploy_contract", points=200)
EVENT_JOIN_DISCORD = EventSpecification(name="join_discord", points=50)
EVENT_FOLLOW_ON_X = EventSpecification(name="follow_galardiel_on_x", points=25)

ORDERED_QUESTS = [
    EVENT_CONNECT_WALLET,
    EVENT_FAUCET,
    EVENT_MAKE_TX,
    EVENT_DEPLOY_CONTRACT,
    EVENT_JOIN_DISCORD,
    EVENT_FOLLOW_ON_X,
]


@dataclass(frozen=True)
class EventUser:
    user_id: UUID
    wallet_address: Optional[str]


@dataclass(frozen=True)
class QuestEvent:
    user_profile_id: UUID
    event_name: str
    points: int

    event_description: Optional[str]
    logs: Optional[Dict]


@dataclass(frozen=True)
class UserEvents:
    event_user: EventUser
    events: List[QuestEvent]
