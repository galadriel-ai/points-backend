from typing import List

from pydantic import BaseModel
from pydantic import Field


class DashboardRequest(BaseModel):
    class Config:
        json_schema_extra = {
            "example": {}
        }


class LeaderboardItem(BaseModel):
    x_username: str = Field(description="Users x handle name")
    points: int = Field(description="Amount of points user has")


class RecentlyJoinedItem(BaseModel):
    x_username: str = Field(description="Users x handle name")
    joined_at: str = Field(description="Time when the user joined")


class DashboardResponse(BaseModel):
    leaderboard_users: List[LeaderboardItem] = Field(
        description="A list of leaderboard users."
    )
    recently_joined_users: List[RecentlyJoinedItem] = Field(
        description="A list of recently joined users."
    )


class UserQuest(BaseModel):
    name: str = Field(description="Quest name")
    points: int = Field(description="How many points the quest is worth")
    is_completed: bool = Field(description="Has the current user completed this quest")


class UserQuestsResponse(BaseModel):
    total_points: int = Field(
        description="Total points the user has"
    )
    quests: List[UserQuest] = Field(
        description="Ordered list on quests by user"
    )
