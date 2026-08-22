class LionAuthError(Exception):
    """Base exception for all LionAuth errors."""


class ConfigurationError(LionAuthError):
    """Raised when LionAuth configuration is invalid."""


class InvalidSecretError(LionAuthError):
    """Raised when a TOTP secret is invalid."""


class InvalidOTPError(LionAuthError):
    """Raised when an OTP is invalid."""