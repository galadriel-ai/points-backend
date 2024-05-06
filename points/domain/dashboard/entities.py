from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    x_username: str
    points: int
    email: str
