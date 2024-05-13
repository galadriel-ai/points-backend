import json
from typing import Dict
from typing import List
from uuid import UUID

import psycopg2
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from points.domain.events.entities import EventUser
from points.domain.events.entities import QuestEvent
from points.repository import utils

SQL_INSERT_EVENT = """
INSERT INTO quest_event (
    id,
    user_profile_id,
    event_name,
    event_description,
    points,
    logs,
    signature,
    created_at,
    last_updated_at
) VALUES (
    :id,
    :user_profile_id,
    :event_name,
    :event_description,
    :points,
    :logs,
    :signature,
    :created_at,
    :last_updated_at
)
"""

SQL_GET_WALLETS_BY_MISSING_EVENTS = """
SELECT
    up.id AS user_profile_id,
    up.wallet_address
FROM
    user_profile up
LEFT JOIN
    quest_event qe
ON
    up.id = qe.user_profile_id
AND
    qe.event_name = :event_name
WHERE
    qe.id IS NULL
    AND up.wallet_address IS NOT NULL;
"""

SQL_GET_EVENTS_BY_USER_X_ID = """
SELECT
    up.id AS user_profile_id,
    qe.event_name,
    qe.event_description,
    qe.points,
    qe.logs
FROM quest_event qe
LEFT JOIN user_profile up on qe.user_profile_id = up.id
WHERE up.id = :user_profile_id;
"""

SQL_GET_AGGREGATED_POINTS_PER_USER = """
SELECT user_profile_id, SUM(points) AS total_points
FROM quest_event
GROUP BY user_profile_id;
"""


class EventRepositoryPsql:
    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    def add_event(self, event: QuestEvent) -> bool:
        data = {
            "id": utils.generate_uuid(),
            "user_profile_id": event.user_profile_id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "points": event.points,
            "logs": json.dumps(event.logs) if event.logs else None,
            "signature": event.signature,
            "created_at": utils.now(),
            "last_updated_at": utils.now(),
        }
        try:
            with self.session_maker() as session:
                session.execute(text(SQL_INSERT_EVENT), data)
                session.commit()
            return True
        except Exception as exc:
            print("Error in EventRepositoryPsql.add_event():", exc)
            return False

    def get_users_by_missing_event(self, event_name: str) -> List[EventUser]:
        data = {
            "event_name": event_name,
        }
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_WALLETS_BY_MISSING_EVENTS), data)
            users: List[EventUser] = []
            for row in rows:
                users.append(
                    EventUser(
                        user_id=row.user_profile_id,
                        wallet_address=row.wallet_address,
                    )
                )
            return users

    def get_user_events(self, user_profile_id: UUID) -> List[QuestEvent]:
        data = {
            "user_profile_id": user_profile_id
        }
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_EVENTS_BY_USER_X_ID), data)
            users: List[QuestEvent] = []
            for row in rows:
                users.append(
                    QuestEvent(
                        user_profile_id=row.user_profile_id,
                        event_name=row.event_name,
                        points=row.points,
                        event_description=row.event_description,
                        logs=row.logs,
                    )
                )
            return users

    def get_total_points(self) -> List[Dict]:
        result = []
        with self.session_maker() as session:
            rows = session.execute(text(SQL_GET_AGGREGATED_POINTS_PER_USER))
            for row in rows:
                result.append({
                    "user_profile_id": row[0],
                    "points": row[1],
                })
        return result
