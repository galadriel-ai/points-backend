from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from points.domain.events.entities import EVENT_JOIN_DISCORD
from points.service.auth.entities import LinkDiscordRequest, DiscordCallbackResponse
from points.domain.events.entities import QuestEvent
from points.service.auth import link_discord_service as service

user_profile_id = UUID("dbc72453-a34d-47a3-b8fe-2a30b4f29c2d")


@pytest.mark.asyncio
async def test_user_not_in_discord():
    request = LinkDiscordRequest(
        user_profile_id=user_profile_id,
        discord_id="12345",
        discord_username="testuser",
        discord_token="token",
        discord_refresh_token="refresh_token",
        discord_token_expires_at=1234567890,
    )
    auth_repository = MagicMock()
    event_repository = MagicMock()
    user_repository = MagicMock()
    discord_repository = MagicMock()
    discord_repository.is_member = AsyncMock(return_value=False)

    response = await service.execute(request, auth_repository, event_repository, user_repository, discord_repository)

    assert response == DiscordCallbackResponse(success=True, is_member=False)
    user_repository.update_discord_id_and_username.assert_called_once_with(
        request.user_profile_id, request.discord_id, request.discord_username
    )
    discord_repository.is_member.assert_called_once_with(request.discord_id, request.discord_token)
    event_repository.get_user_events.assert_not_called()
    event_repository.add_event.assert_not_called()


@pytest.mark.asyncio
async def test_user_already_has_discord_event():
    request = LinkDiscordRequest(
        user_profile_id=user_profile_id,
        discord_id="12345",
        discord_username="testuser",
        discord_token="token",
        discord_refresh_token="refresh_token",
        discord_token_expires_at=1234567890,
    )
    existing_event = QuestEvent(
        user_profile_id=request.user_profile_id,
        event_name=EVENT_JOIN_DISCORD.name,
        points=EVENT_JOIN_DISCORD.points,
        event_description=None,
        logs=None,
    )
    auth_repository = MagicMock()
    event_repository = MagicMock()
    event_repository.get_user_events.return_value = [existing_event]
    user_repository = MagicMock()
    discord_repository = MagicMock()
    discord_repository.is_member = AsyncMock(return_value=True)

    response = await service.execute(request, auth_repository, event_repository, user_repository, discord_repository)

    assert response == DiscordCallbackResponse(success=True, is_member=True)
    user_repository.update_discord_id_and_username.assert_called_once_with(
        request.user_profile_id, request.discord_id, request.discord_username
    )
    discord_repository.is_member.assert_called_once_with(request.discord_id, request.discord_token)
    event_repository.get_user_events.assert_called_once_with(request.user_profile_id)
    event_repository.add_event.assert_not_called()


@pytest.mark.asyncio
async def test_user_joining_discord():
    request = LinkDiscordRequest(
        user_profile_id=user_profile_id,
        discord_id="12345",
        discord_username="testuser",
        discord_token="token",
        discord_refresh_token="refresh_token",
        discord_token_expires_at=1234567890,
    )
    auth_repository = MagicMock()
    event_repository = MagicMock()
    event_repository.get_user_events.return_value = []
    user_repository = MagicMock()
    discord_repository = MagicMock()
    discord_repository.is_member = AsyncMock(return_value=True)

    response = await service.execute(request, auth_repository, event_repository, user_repository, discord_repository)

    assert response == DiscordCallbackResponse(success=True, is_member=True)
    user_repository.update_discord_id_and_username.assert_called_once_with(
        request.user_profile_id, request.discord_id, request.discord_username
    )
    discord_repository.is_member.assert_called_once_with(request.discord_id, request.discord_token)
    event_repository.get_user_events.assert_called_once_with(request.user_profile_id)
    event_repository.add_event.assert_called_once()
    event = event_repository.add_event.call_args[0][0]
    assert event.user_profile_id == request.user_profile_id
    assert event.event_name == EVENT_JOIN_DISCORD.name
    assert event.points == EVENT_JOIN_DISCORD.points
