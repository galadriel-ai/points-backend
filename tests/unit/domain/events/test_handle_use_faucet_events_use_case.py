from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

import points.domain.events.handle_use_faucet_events_use_case as use_case
import settings
from points.domain.events.entities import EVENT_FAUCET
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent

USER_ID = UUID("20a61707-9c43-4e8c-9eed-b46fe1fb8705")


def setup():
    pass


def setup_function():
    use_case.SLEEP_TIME = 0


async def test_no_users():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = []
    explorer_repo = MagicMock()
    await use_case.execute(event_repo, explorer_repo)
    explorer_repo.get_transactions_to_account.assert_not_called()


async def test_no_txs():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
        )
    ]
    explorer_repo = AsyncMock()
    explorer_repo.get_transactions_to_account.return_value = None
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_not_called()


async def test_no_txs_from_faucet():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
        )
    ]
    explorer_repo = AsyncMock()
    item = {"from": {"hash": "some random address here"}}
    explorer_repo.get_transactions_to_account.return_value = {
        "items": [item]
    }
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_not_called()


async def test_updates_one():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
        )
    ]
    explorer_repo = AsyncMock()
    item = {"from": {"hash": settings.FAUCET_ADDRESS}}
    explorer_repo.get_transactions_to_account.return_value = {
        "items": [item]
    }
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_FAUCET.name,
            points=EVENT_FAUCET.points,
            event_description=None,
            logs={"from": {"hash": settings.FAUCET_ADDRESS}}
        )
    )
