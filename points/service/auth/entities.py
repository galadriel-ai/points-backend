from uuid import UUID
from pydantic import BaseModel, Field


class GenerateNonceRequest(BaseModel):
    wallet_address: str = Field(
        description="ETH wallet address",
        examples=["0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"])


class GenerateNonceResponse(BaseModel):
    nonce: str = Field(description="Generated nonce for a given eth wallet address")
    issued_at: str = Field(description="Datetime when the nonce was issued")


class LinkEthWalletRequest(BaseModel):
    signature: str = Field(
        description="Signature for the sign in with ethereum message"
    )
    wallet_address: str = Field(
        description="ETH wallet address",
        examples=["0x3FABFC6ae7A14c9abBad96Ac2704a7F8D555a079"])


class LinkEthWalletResponse(BaseModel):
    success: bool = Field(
        description="Boolean indicating if wallet linking was successful"
    )


class LinkDiscordRequest(BaseModel):
    user_profile_id: UUID = Field(
        description="User profile ID",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    discord_id: str = Field(
        description="Discord user ID",
        examples=["123456789012345678"]
    )
    discord_username: str = Field(
        description="Discord username",
        examples=["username"]
    ),
    discord_token: str = Field(
        description="Discord access token",
        examples=["token"]
    ),
    discord_refresh_token: str = Field(
        description="Discord refresh token",
        examples=["refresh_token"]
    ),
    discord_token_expires_at: int = Field(
        description="Discord token expiration time",
        examples=[1630000000]
    )


class LinkDiscordResponse(BaseModel):
    success: bool = Field(
        description="Boolean indicating if discord linking was successful"
    )
