from unittest.mock import MagicMock
from uuid import UUID

import pytest

from points.domain.dashboard.entities import User
from points.domain.events.entities import ORDERED_QUESTS
from points.domain.events.entities import QuestEvent
from points.service.dashboard import quests_service as service


def setup():
    pass


def get_user():
    return User(
        user_id=UUID("75d43b90-3aef-44d2-9bdc-39dc747214b3"),
        x_id="mock_x_id",
        x_username="mock_x_username",
        wallet_address="mock_wallet_address",
    )


@pytest.mark.asyncio
async def test_no_quests_done():
    event_repository = MagicMock()
    event_repository.get_user_events.return_value = []
    response = await service.execute(get_user(), event_repository)
    assert len(response.quests) == len(ORDERED_QUESTS)
    for i, quest in enumerate(ORDERED_QUESTS):
        assert response.quests[i].name == quest.name
        assert response.quests[i].is_completed is False


@pytest.mark.asyncio
async def test_second_quest_completed():
    event_repository = MagicMock()
    user = get_user()
    event_repository.get_user_events.return_value = [
        QuestEvent(
            user_profile_id=user.user_id,
            event_name=ORDERED_QUESTS[1].name,
            points=ORDERED_QUESTS[1].points,
            event_description="random",
            logs={},
        )
    ]
    response = await service.execute(get_user(), event_repository)
    assert response.quests[1].name == ORDERED_QUESTS[1].name
    assert response.quests[1].is_completed is True
