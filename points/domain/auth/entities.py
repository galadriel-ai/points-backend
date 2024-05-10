from dataclasses import dataclass


@dataclass
class SignMessageComponents:
    nonce: str
    issued_at: str


@dataclass
class DiscordUser:
    id: str
    username: str