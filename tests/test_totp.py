import pytest

from lionauth import (
    InvalidInputError,
    InvalidOTPError,
    InvalidSecretError,
    TOTPAuthenticator,
)


@pytest.fixture
def auth():
    return TOTPAuthenticator()


def test_generate_secret(auth):
    secret = auth.generate_secret()

    assert isinstance(secret, str)
    assert len(secret) > 0


def test_generate_otp(auth):
    secret = auth.generate_secret()

    otp = auth.generate_otp(secret)

    assert isinstance(otp, str)
    assert len(otp) == 6
    assert otp.isdigit()


def test_verify_correct_otp(auth):
    secret = auth.generate_secret()
    otp = auth.generate_otp(secret)

    assert auth.verify(secret, otp) is True


def test_verify_wrong_otp(auth):
    secret = auth.generate_secret()

    with pytest.raises(InvalidOTPError):
        auth.verify(secret, "123456")


def test_empty_secret(auth):
    with pytest.raises(InvalidSecretError):
        auth.generate_otp("")


def test_invalid_otp_format(auth):
    secret = auth.generate_secret()

    with pytest.raises(InvalidOTPError):
        auth.verify(secret, "abcdef")


def test_invalid_otp_length(auth):
    secret = auth.generate_secret()

    with pytest.raises(InvalidOTPError):
        auth.verify(secret, "123")


def test_empty_account_name(auth):
    secret = auth.generate_secret()

    with pytest.raises(InvalidInputError):
        auth.get_provisioning_uri(
            secret=secret,
            account_name="",
        )


def test_provisioning_uri(auth):
    secret = auth.generate_secret()

    uri = auth.get_provisioning_uri(
        secret=secret,
        account_name="user@example.com",
    )

    assert uri.startswith("otpauth://totp/")
    assert "LionAuth" in uri
    assert "user%40example.com" in uri