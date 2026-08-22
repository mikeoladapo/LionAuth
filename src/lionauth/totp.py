import pyotp
import hashlib

from .config import TOTPConfig
from .exceptions import InvalidOTPError, InvalidSecretError


class TOTPAuthenticator:

    def __init__(self, config: TOTPConfig | None = None):
        self.config = config or TOTPConfig()

    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def _validate_secret(self, secret: str) -> None:
        if not isinstance(secret, str):
            raise InvalidSecretError("Secret must be a string")

        if not secret.strip():
            raise InvalidSecretError("Secret cannot be empty")

    def _create_totp(self, secret: str) -> pyotp.TOTP:
        self._validate_secret(secret)

        try:
            algorithms = {
                "SHA1": hashlib.sha1,
                "SHA256": hashlib.sha256,
                "SHA512": hashlib.sha512,
            }

            return pyotp.TOTP(
                secret,
                digits=self.config.digits,
                interval=self.config.interval,
                digest=algorithms[self.config.algorithm.upper()],
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
    
    def get_provisioning_uri(
        self,
        secret: str,
        account_name: str,
    ) -> str:
        totp = self._create_totp(secret)

        return totp.provisioning_uri(
            name=account_name,
            issuer_name=self.config.issuer,
        )
    