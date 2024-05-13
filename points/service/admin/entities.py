from pydantic import BaseModel, Field


class PostPointsRequest(BaseModel):
    user_profile_id: str = Field(
        description="User profile ID to add points to",
        examples=["ca249bf4-fd2f-467a-b7c7-749d50a15d00"])
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

    def construct_signed_message(self):
        return f"{self.wallet_address} is giving {self.points} points to {self.user_profile_id}.\n{self.event_description}"


class PostPointsResponse(BaseModel):
    success: bool = Field(
        description="Boolean indicating wether the request was successful",
        examples=[True]
    )
