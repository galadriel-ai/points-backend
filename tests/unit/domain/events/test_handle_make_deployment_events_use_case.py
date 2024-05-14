from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

import points.domain.events.handle_make_deployment_events_use_case as use_case
from points.domain.events.entities import EVENT_DEPLOY_CONTRACT
from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent

USER_ID = UUID("d95c433c-4bf9-4b55-8e7b-462399fd4313")

i = 0


def setup():
    global i
    i = 0


def setup_function():
    use_case.SLEEP_TIME = 0


async def test_no_users():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = []
    explorer_repo = MagicMock()
    await use_case.execute(event_repo, explorer_repo)
    explorer_repo.get_transactions_from_account.assert_not_called()


async def test_no_txs():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
            discord_id=None,
        )
    ]
    explorer_repo = AsyncMock()
    explorer_repo.get_transactions_from_account.return_value = None
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_not_called()


async def test_updates_one():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
            discord_id=None,
        )
    ]
    explorer_repo = AsyncMock()
    deployment_tx = {"tx_types": ["contract_creation"]}
    explorer_repo.get_transactions_from_account.return_value = {
        "items": [deployment_tx]
    }
    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_DEPLOY_CONTRACT.name,
            points=EVENT_DEPLOY_CONTRACT.points,
            event_description=None,
            logs=deployment_tx
        )
    )


async def test_paginates():
    event_repo = MagicMock()
    event_repo.get_users_by_missing_event.return_value = [
        EventUser(
            user_id=USER_ID,
            wallet_address="0xMock",
            discord_id=None,
        )
    ]
    explorer_repo = AsyncMock()
    deployment_tx = {"tx_types": ["contract_creation"]}

    async def mock_get_txs(*args, **kwargs):
        global i
        i = i + 1
        if i <= 1:
            return {
                "items": [
                    {"tx_types": ["totally_wrong"]},
                    {"some_random": "field"},
                ],
                "next_page_params": {
                    "some_param": "mock"
                }
            }
        return {
            "items": [deployment_tx]
        }

    explorer_repo.get_transactions_from_account = mock_get_txs

    await use_case.execute(event_repo, explorer_repo)
    event_repo.add_event.assert_called_with(
        QuestEvent(
            user_profile_id=USER_ID,
            event_name=EVENT_DEPLOY_CONTRACT.name,
            points=EVENT_DEPLOY_CONTRACT.points,
            event_description=None,
            logs=deployment_tx
        )
    )
    global i
    assert i > 1
