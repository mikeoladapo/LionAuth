import pyotp

class TOTPAuthenticator:
    def generate_secret(self) -> str:
        return pyotp.random_base32()