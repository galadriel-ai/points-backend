from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

import pytest

import points.domain.events.handle_make_tx_events_use_case as use_case
from points.domain.events.entities import EVENT_MAKE_TX
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent

USER_ID = UUID("d95c433c-4bf9-4b55-8e7b-462399fd4313")


def setup():
    pass


@pytest.mark.asyncio
async def test_no_users():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = []
    explorer_repo = MagicMock()
    await use_case.execute(event_repo, explorer_repo)
    explorer_repo.get_transactions_from_account.assert_not_called()


@pytest.mark.asyncio
async def test_no_txs():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
        )
    ]
    explorer_repo = AsyncMock()
    explorer_repo.get_transactions_from_account.return_value = None
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_not_called()


@pytest.mark.asyncio
async def test_updates_one():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
        )
    ]
    explorer_repo = AsyncMock()
    explorer_repo.get_transactions_from_account.return_value = {
        "items": [{"type": "mock_item"}]
    }
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_MAKE_TX.name,
            points=EVENT_MAKE_TX.points,
            event_description=None,
            logs={"type": "mock_item"}
        )
    )
