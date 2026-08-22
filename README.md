# LionAuth

A reusable Python library for implementing **Time-based One-Time Password (TOTP) authentication**.

LionAuth provides the core functionality required to integrate authenticator-app-based authentication into Python applications.

It is designed to work with compatible authenticator applications such as **Google Authenticator** and **Microsoft Authenticator**.

---

## Features

- TOTP secret generation
- OTP generation
- OTP verification
- Configurable OTP digit length
- Configurable OTP time interval
- SHA1, SHA256, and SHA512 support
- Standard `otpauth://` provisioning URI generation
- Input validation
- Custom authentication exceptions
- Configurable verification window
- No database required
- No QR-code dependency
- Framework independent

---

## Requirements

- Python 3.10 or higher
- PyOTP 2.9 or higher

---

## Installation

Install LionAuth using pip:

```bash
pip install lionauth
```

---

# Quick Start

```python
from lionauth import TOTPAuthenticator

# Create the authenticator
auth = TOTPAuthenticator()

# Generate a TOTP secret
secret = auth.generate_secret()

print("Secret:", secret)

# Generate a provisioning URI
uri = auth.get_provisioning_uri(
    secret=secret,
    account_name="user@example.com",
)

print("Provisioning URI:", uri)

# Generate the current OTP
otp = auth.generate_otp(secret)

print("OTP:", otp)

# Verify the OTP
result = auth.verify(
    secret=secret,
    otp=otp,
)

print("Verified:", result)
```

Example output:

```text
Secret: JBSWY3DPEHPK3PXP
Provisioning URI: otpauth://totp/...
OTP: 123456
Verified: True
```

---

# How LionAuth Works

LionAuth implements **Time-based One-Time Password (TOTP)** authentication.

A TOTP system uses a shared secret between an application and an authenticator application. Both sides use the secret and the current time to generate the same temporary one-time password.

The basic process is:

```text
                     LionAuth
                        |
                        |
                 Generate Secret
                        |
                        v
                  TOTP Secret
                        |
              +---------+---------+
              |                   |
              v                   v
       Authenticator App      Application
              |                   |
              |                   |
        Generates OTP        Stores Secret
              |                   |
              +---------+---------+
                        |
                        v
                  User enters OTP
                        |
                        v
                LionAuth.verify()
                        |
                 +------+------+
                 |             |
               Valid         Invalid
                 |             |
                 v             v
               True      InvalidOTPError
```

The application integrating LionAuth is responsible for managing users and securely storing their TOTP secrets.

---

# Generating a Secret

Generate a new TOTP secret using:

```python
from lionauth import TOTPAuthenticator

auth = TOTPAuthenticator()

secret = auth.generate_secret()

print(secret)
```

The generated secret is a sensitive authentication credential.

Applications should:

- Store it securely.
- Protect it from unauthorized access.
- Never expose it unnecessarily.
- Never commit it to source control.
- Avoid logging it.

---

# Provisioning URI

LionAuth can generate a standard `otpauth://` provisioning URI.

```python
uri = auth.get_provisioning_uri(
    secret=secret,
    account_name="user@example.com",
)

print(uri)
```

Example:

```text
otpauth://totp/LionAuth:user%40example.com?secret=XXXXXXXX&issuer=LionAuth&algorithm=SHA1&digits=6&period=30
```

The URI contains the information required by compatible authenticator applications to configure the TOTP account.

LionAuth intentionally does **not** generate QR codes.

This keeps the library lightweight and allows the application integrating LionAuth to decide how the provisioning URI should be presented to the user.

For example, an application may choose to:

- Display the URI directly.
- Generate its own QR code.
- Provide the URI through another secure provisioning mechanism.

---

# Generating an OTP

Generate the current OTP using:

```python
otp = auth.generate_otp(secret)

print(otp)
```

Example:

```text
483921
```

The OTP changes according to the configured time interval.

---

# Verifying an OTP

Verify an OTP using:

```python
result = auth.verify(
    secret=secret,
    otp=otp,
)

print(result)
```

A valid OTP returns:

```python
True
```

An invalid OTP raises:

```python
InvalidOTPError
```

Example:

```python
from lionauth import (
    TOTPAuthenticator,
    InvalidOTPError,
)

auth = TOTPAuthenticator()

secret = auth.generate_secret()
otp = auth.generate_otp(secret)

try:
    auth.verify(secret, otp)
    print("Authentication successful")

except InvalidOTPError:
    print("Invalid authentication code")
```

---

# Configuration

LionAuth provides `TOTPConfig` for customizing TOTP behavior.

```python
from lionauth import (
    TOTPAuthenticator,
    TOTPConfig,
)

config = TOTPConfig(
    digits=6,
    interval=30,
    algorithm="SHA1",
    issuer="My Application",
    valid_window=0,
)

auth = TOTPAuthenticator(config)
```

---

# Configuration Options

| Option | Default | Description |
|---|---:|---|
| `digits` | `6` | Number of digits in the generated OTP |
| `interval` | `30` | Number of seconds before the OTP changes |
| `algorithm` | `SHA1` | Hashing algorithm |
| `issuer` | `LionAuth` | Application/service name |
| `valid_window` | `0` | Number of adjacent time windows accepted during verification |

### Supported algorithms

```text
SHA1
SHA256
SHA512
```

### Supported OTP digit lengths

```text
6
8
```

---

# Custom Configuration Example

```python
from lionauth import (
    TOTPAuthenticator,
    TOTPConfig,
)

config = TOTPConfig(
    digits=8,
    interval=60,
    algorithm="SHA256",
    issuer="My Application",
    valid_window=1,
)

auth = TOTPAuthenticator(config)

secret = auth.generate_secret()

otp = auth.generate_otp(secret)

print("OTP:", otp)

print("Verified:", auth.verify(secret, otp))
```

---

# Enrollment Workflow

A typical authenticator enrollment process looks like this:

```text
1. User chooses to enable authenticator authentication
                         |
                         v
2. Application requests a secret from LionAuth
                         |
                         v
3. LionAuth generates the secret
                         |
                         v
4. Application securely stores the secret
                         |
                         v
5. Application requests a provisioning URI
                         |
                         v
6. User configures their authenticator app
                         |
                         v
7. Authenticator app generates an OTP
                         |
                         v
8. User enters the OTP
                         |
                         v
9. Application calls LionAuth.verify()
                         |
                  +------+------+
                  |             |
                Valid         Invalid
                  |             |
                  v             v
          Enable TOTP       Reject OTP
```

The application should **not** mark TOTP as enabled merely because a secret was generated.

The user should first prove that their authenticator application is correctly configured by successfully providing a valid OTP.

A recommended enrollment state is:

```text
Secret generated
       |
       v
Pending enrollment
       |
       v
User provides OTP
       |
       v
OTP verified
       |
       v
TOTP enabled
```

---

# Authentication Workflow

After enrollment, authentication works like this:

```text
User
 |
 | Login
 v
Application
 |
 | Request OTP
 v
Authenticator App
 |
 | Generate current OTP
 v
User
 |
 | Enter OTP
 v
Application
 |
 | secret + OTP
 v
LionAuth
 |
 | verify()
 |
 +------------+
 |            |
 v            v
Valid       Invalid
 |            |
 v            v
True       Error
 |
 v
Application grants access
```

LionAuth verifies the OTP. The application remains responsible for deciding what happens after successful verification, such as creating a session or issuing a JWT.

---

# Exceptions

LionAuth provides its own exception hierarchy.

```python
from lionauth import (
    LionAuthError,
    ConfigurationError,
    InvalidSecretError,
    InvalidOTPError,
    InvalidInputError,
)
```

## Exception Hierarchy

```text
LionAuthError
|
+-- ConfigurationError
|
+-- InvalidSecretError
|
+-- InvalidOTPError
|
+-- InvalidInputError
```

---

## LionAuthError

`LionAuthError` is the base exception for LionAuth errors.

You can catch all LionAuth-specific errors using:

```python
from lionauth import LionAuthError

try:
    auth.verify(secret, otp)

except LionAuthError:
    print("A LionAuth error occurred")
```

---

## ConfigurationError

Raised when the TOTP configuration is invalid.

Example:

```python
from lionauth import (
    TOTPConfig,
    ConfigurationError,
)

try:
    config = TOTPConfig(
        digits=7,
    )

except ConfigurationError as error:
    print(error)
```

---

## InvalidSecretError

Raised when an invalid TOTP secret is supplied.

Example:

```python
from lionauth import InvalidSecretError

try:
    auth.generate_otp("")

except InvalidSecretError as error:
    print(error)
```

---

## InvalidOTPError

Raised when an OTP is invalid.

Example:

```python
from lionauth import InvalidOTPError

try:
    auth.verify(
        secret=secret,
        otp="123456",
    )

except InvalidOTPError:
    print("Invalid OTP")
```

---

## InvalidInputError

Raised when an input does not meet the expected requirements.

Example:

```python
from lionauth import InvalidInputError

try:
    auth.get_provisioning_uri(
        secret=secret,
        account_name="",
    )

except InvalidInputError as error:
    print(error)
```

---

# What LionAuth Does Not Handle

LionAuth is intentionally focused on TOTP authentication.

It does **not** manage:

- User accounts
- User registration
- Password authentication
- Password storage
- Databases
- JWT authentication
- Sessions
- Email delivery
- SMS OTP
- QR-code generation
- User permissions
- Roles
- Application-specific authorization

These responsibilities belong to the application integrating LionAuth.

This separation allows LionAuth to remain lightweight and framework independent.

---

# Database

LionAuth does not require a database.

The application using LionAuth is responsible for storing the user's TOTP secret.

For example, an application might have a user record containing:

```text
users
--------------------------------
id
email
name
totp_secret
totp_enabled
```

The exact database structure is left to the application.

The relationship is:

```text
Application Database
        |
        | TOTP secret
        v
     LionAuth
        |
        +-- Generate OTP
        |
        +-- Verify OTP
        |
        +-- Generate provisioning URI
```

LionAuth itself does not store users or TOTP secrets in a database.

---

# Security Considerations

TOTP secrets are sensitive authentication credentials.

Applications using LionAuth should:

- Store TOTP secrets securely.
- Protect secrets from unauthorized access.
- Never expose TOTP secrets in logs.
- Never expose secrets to clients unnecessarily.
- Protect secrets at rest using appropriate application and database security controls.
- Require successful OTP verification before completing enrollment.
- Use a reasonable `valid_window`.
- Protect authentication endpoints against brute-force attempts.
- Apply appropriate rate limiting to OTP verification endpoints.
- Avoid storing OTPs permanently.
- Never commit TOTP secrets to source control.
- Avoid returning TOTP secrets in API responses unless absolutely necessary.

### Important

A TOTP secret should be treated like a password.

Anyone who obtains the secret can generate valid OTPs for that account.

LionAuth provides the TOTP functionality, but the application integrating LionAuth is responsible for protecting the secret and the authentication endpoint.

---

# Development

Clone the project:

```bash
git clone <repository-url>
```

Enter the project directory:

```bash
cd LionAuth
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Install LionAuth with development dependencies:

```bash
pip install -e ".[dev]"
```

---

# Running Tests

LionAuth uses `pytest` for automated testing.

Run the complete test suite:

```bash
pytest
```

A successful test run should look similar to:

```text
======================== test session starts ========================

tests/test_config.py ........
tests/test_totp.py .........

========================= XX passed =========================
```

The exact number of tests may change as the project evolves.

---

# Building the Package

Install the Python build tool:

```bash
pip install build
```

Build LionAuth:

```bash
python -m build
```

The distribution files will be generated inside:

```text
dist/
```

Example:

```text
dist/
├── lionauth-0.1.0-py3-none-any.whl
└── lionauth-0.1.0.tar.gz
```

The `.whl` file is the wheel distribution and the `.tar.gz` file is the source distribution.

---

# Testing the Built Package

You can test the built package in a clean virtual environment.

Create a separate environment:

```bash
python -m venv test-env
```

Activate it:

### Linux/macOS

```bash
source test-env/bin/activate
```

### Windows

```powershell
test-env\Scripts\activate
```

Install the built wheel:

```bash
pip install dist/lionauth-0.1.0-py3-none-any.whl
```

Then test:

```python
from lionauth import TOTPAuthenticator

auth = TOTPAuthenticator()

secret = auth.generate_secret()

otp = auth.generate_otp(secret)

print(auth.verify(secret, otp))
```

Expected output:

```text
True
```

---

# Project Structure

```text
LionAuth/
|
+-- src/
|   |
|   +-- lionauth/
|       |
|       +-- __init__.py
|       +-- config.py
|       +-- exceptions.py
|       +-- totp.py
|
+-- tests/
|   |
|   +-- test_config.py
|   +-- test_totp.py
|
+-- pyproject.toml
+-- README.md
```

---

# Design Philosophy

LionAuth follows a simple principle:

> **LionAuth handles TOTP. The application handles everything else.**

This keeps the library:

- Lightweight
- Framework independent
- Database independent
- Easy to integrate
- Easy to test
- Reusable across Python applications

LionAuth can be integrated into applications built with:

- Django
- FastAPI
- Flask
- Other Python web frameworks
- CLI applications
- Custom Python applications

---

# Complete Example

```python
from lionauth import (
    TOTPAuthenticator,
    InvalidOTPError,
)

# Create the authenticator
auth = TOTPAuthenticator()

# Generate a secret during enrollment
secret = auth.generate_secret()

print("Secret:", secret)

# Generate a provisioning URI
uri = auth.get_provisioning_uri(
    secret=secret,
    account_name="user@example.com",
)

print("Provisioning URI:", uri)

# The user configures their authenticator application
# and obtains an OTP.

# Generate the current OTP for demonstration purposes
otp = auth.generate_otp(secret)

print("Current OTP:", otp)

# Verify the OTP
try:
    if auth.verify(
        secret=secret,
        otp=otp,
    ):
        print("Authentication successful")

except InvalidOTPError:
    print("Authentication failed")
```

---

# API Overview

| Method | Description |
|---|---|
| `generate_secret()` | Generates a new TOTP secret |
| `generate_otp(secret)` | Generates the current OTP |
| `verify(secret, otp)` | Verifies an OTP |
| `get_provisioning_uri(secret, account_name)` | Generates an `otpauth://` provisioning URI |

---

# Example Integration

LionAuth can be used as the TOTP layer inside a larger authentication system.

For example:

```text
                    Your Application
                           |
            +--------------+--------------+
            |                             |
            v                             v
       User Management              Authentication
            |                             |
            |                       +-----+-----+
            |                       |           |
            |                      Login       TOTP
            |                                   |
            |                                   v
            |                              LionAuth
            |                                   |
            |                              OTP verify
            |                                   |
            +---------------+-------------------+
                            |
                            v
                       Authorization
```

The application can use its existing authentication system while delegating TOTP operations to LionAuth.

---

# Version

Current version:

```text
0.1.0
```

---

# License

MIT

---

# Author

LionAuth is a reusable TOTP authentication library for Python applications.