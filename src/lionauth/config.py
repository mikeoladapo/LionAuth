from dataclasses import dataclass


@dataclass(frozen=True)
class TOTPConfig:
    digits: int = 6
    interval: int = 30
    algorithm: str = "SHA1"
    issuer: str = "LionAuth"
    valid_window: int = 0