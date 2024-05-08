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
