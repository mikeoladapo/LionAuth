import pyotp

class TOTPAuthenticator:
    def generate_secret(self) -> str:
        return pyotp.random_base32()

    def generate_otp(self, secret: str) -> str:
        totp = pyotp.TOTP(secret)
        return totp.now()

    def verify(self, secret: str, otp: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(otp)
    