from typing import List

from points.domain.dashboard.entities import User
from points.domain.events.entities import ORDERED_QUESTS
from points.domain.events.entities import QuestEvent
from points.repository.event_repository import EventRepositoryPsql
from points.service.dashboard.entities import UserQuest
from points.service.dashboard.entities import UserQuestsResponse


async def execute(
    user: User,
    event_repository: EventRepositoryPsql,
) -> UserQuestsResponse:
    user_events: List[QuestEvent] = event_repository.get_user_events(user.user_id)

    formatted_quests: List[UserQuest] = []
    for event in ORDERED_QUESTS:
        formatted_quests.append(
            UserQuest(
                name=event.name,
                points=event.points,
                is_completed=bool([e for e in user_events if e.event_name == event.name]),
            )
        )

    return UserQuestsResponse(
        total_points=sum(e.points for e in user_events),
        quests=formatted_quests,
    )
