from dataclasses import dataclass
from typing import Dict
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class EventSpecification:
    name: str
    points: int


# TODO: kind of hardcoded here at the moment
EVENT_FAUCET = EventSpecification(name="used_faucet", points=50)
EVENT_MAKE_TX = EventSpecification(name="make_tx", points=50)
EVENT_DEPLOY_CONTRACT = EventSpecification(name="deploy_contract", points=200)


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
