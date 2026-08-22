import pyotp
from .config import TOTPConfig


class TOTPAuthenticator:
    def __init__(self, config: TOTPConfig | None = None):
        self.config = config or TOTPConfig()

    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def _create_totp(self, secret: str) -> pyotp.TOTP:
        return pyotp.TOTP(
            secret,
            digits=self.config.digits,
            interval=self.config.interval,
            digest=self.config.algorithm.lower(),
        )

    def generate_otp(self, secret: str) -> str:
        totp = pyotp.TOTP(secret)
        return totp.now()

    def verify(self, secret: str, otp: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(otp)
    