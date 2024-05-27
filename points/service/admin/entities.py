from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class PostPointsRequest(BaseModel):
    x_username: str = Field(
        description="Case insensitive x username",
        examples=["galadriel_ai"])
    points: int = Field(
        description="How many points to add to selected user",
        examples=[20]
    )
    event_description: str = Field(
        description="The event description that explains why the points were added.",
        examples=["Won the weekly discord challenge"]
    )
    signature: str = Field(
        description="Signature",
        examples=["0xSignatureAbc"]
    )
    wallet_address: str = Field(
        description="Wallet address of the signer",
        examples=["0xMock"]
    )

    def construct_signed_message(self, ):
        return f"{self.wallet_address} is giving {self.points} points to @{self.x_username.lower()}.\n{self.event_description}"


class PostPointsResponse(BaseModel):
    success: bool = Field(
        description="Boolean indicating wether the request was successful",
        examples=[True]
    )
    points_before: Optional[int] = Field()
    points_after: Optional[int] = Field()
