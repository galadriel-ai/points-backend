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
