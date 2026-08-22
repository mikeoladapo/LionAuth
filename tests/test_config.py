import pytest

from lionauth import ConfigurationError, TOTPConfig


def test_default_config():
    config = TOTPConfig()

    assert config.digits == 6
    assert config.interval == 30
    assert config.algorithm == "SHA1"
    assert config.issuer == "LionAuth"
    assert config.valid_window == 0


def test_custom_config():
    config = TOTPConfig(
        digits=8,
        interval=60,
        algorithm="SHA256",
        issuer="My App",
        valid_window=1,
    )

    assert config.digits == 8
    assert config.interval == 60
    assert config.algorithm == "SHA256"
    assert config.issuer == "My App"
    assert config.valid_window == 1


def test_invalid_digits():
    with pytest.raises(ConfigurationError):
        TOTPConfig(digits=7)


def test_invalid_interval():
    with pytest.raises(ConfigurationError):
        TOTPConfig(interval=0)


def test_invalid_algorithm():
    with pytest.raises(ConfigurationError):
        TOTPConfig(algorithm="BANANA")


def test_negative_valid_window():
    with pytest.raises(ConfigurationError):
        TOTPConfig(valid_window=-1)