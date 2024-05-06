from typing import List

from pydantic import BaseModel
from pydantic import Field


class DashboardRequest(BaseModel):
    class Config:
        json_schema_extra = {
            "example": {}
        }


class UserListItem(BaseModel):
    x_name: str = Field(description="Users x handle name")
    points: str = Field(description="Amount of points user has")


class DashboardResponse(BaseModel):
    leaderboard_users: List[UserListItem] = Field(
        description="A list of leaderboard users."
    )
    recently_joined_users: List[UserListItem] = Field(
        description="A list of recently joined users."
    )
