from pydantic import BaseModel, Field


class GenerateNonceRequest(BaseModel):
    eth_address: str = Field(description="ETH wallet address")


class GenerateNonceResponse(BaseModel):
    nonce: str = Field(description="Generated nonce for a given eth wallet address")


class LinkEthWalletRequest(BaseModel):
    signature: str = Field(
        description="Signature for the sign in with ethereum message"
    )


class LinkEthWalletResponse(BaseModel):
    success: bool = Field(
        description="Boolean indicating if wallet linking was successful"
    )
