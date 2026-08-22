from dataclasses import dataclass
from .exceptions import ConfigurationError


@dataclass(frozen=True)
class TOTPConfig:
    digits: int = 6
    interval: int = 30
    algorithm: str = "SHA1"
    issuer: str = "LionAuth"
    valid_window: int = 0

    def __post_init__(self):
        if self.digits not in (6, 8):
            raise ConfigurationError(
                "digits must be either 6 or 8"
            )

        if self.interval <= 0:
            raise ConfigurationError(
                "interval must be greater than 0"
            )

        if self.algorithm.upper() not in {
            "SHA1",
            "SHA256",
            "SHA512",
        }:
            raise ConfigurationError(
                "algorithm must be SHA1, SHA256, or SHA512"
            )

        if self.valid_window < 0:
            raise ConfigurationError(
                "valid_window cannot be negative"
            )

        if not self.issuer.strip():
            raise ConfigurationError(
                "issuer cannot be empty"
            )