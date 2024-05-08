from dataclasses import dataclass


@dataclass
class SignMessageComponents:
    nonce: str
    issued_at: str
