import pyotp
import hashlib

from .config import TOTPConfig
from .exceptions import InvalidOTPError, InvalidSecretError, InvalidInputError


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

    def _validate_otp(self, otp: str) -> None:
        if not isinstance(otp, str):
            raise InvalidInputError("OTP must be a string")

        if not otp.isdigit():
            raise InvalidOTPError("OTP must contain only digits")

        if len(otp) != self.config.digits:
            raise InvalidOTPError(
                f"OTP must contain exactly {self.config.digits} digits"
            )
        
    def verify(self, secret: str, otp: str) -> bool:
        self._validate_otp(otp)

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

        if not isinstance(account_name, str):
            raise InvalidInputError(
                "account_name must be a string"
            )

        if not account_name.strip():
            raise InvalidInputError(
                "account_name cannot be empty"
            )

        totp = self._create_totp(secret)

        return totp.provisioning_uri(
            name=account_name,
            issuer_name=self.config.issuer,
        )
        