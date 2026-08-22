import pyotp

from .config import TOTPConfig
from .exceptions import InvalidOTPError, InvalidSecretError


class TOTPAuthenticator:

    def __init__(self, config: TOTPConfig | None = None):
        self.config = config or TOTPConfig()

    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def _create_totp(self, secret: str) -> pyotp.TOTP:
        try:
            return pyotp.TOTP(
                secret,
                digits=self.config.digits,
                interval=self.config.interval,
                digest=self.config.algorithm.lower(),
            )
        except Exception as exc:
            raise InvalidSecretError("Invalid TOTP secret") from exc

    def generate_otp(self, secret: str) -> str:
        totp = self._create_totp(secret)
        return totp.now()

    def verify(self, secret: str, otp: str) -> bool:
        totp = self._create_totp(secret)

        try:
            is_valid = totp.verify(
                otp,
                valid_window=self.config.valid_window,
            )
        except Exception as exc:
            raise InvalidSecretError("Invalid TOTP secret") from exc

        if not is_valid:
            raise InvalidOTPError("Invalid OTP")

        return True