Quick Start
from lionauth import TOTPAuthenticator

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

# Generate an OTP
otp = auth.generate_otp(secret)

print("OTP:", otp)

# Verify the OTP
result = auth.verify(secret, otp)

print("Verified:", result)

Output:

Secret: JBSWY3DPEHPK3PXP
Provisioning URI: otpauth://totp/...
OTP: 123456
Verified: True
How LionAuth Works

LionAuth uses the Time-based One-Time Password (TOTP) standard.

The basic process is:

                    LionAuth
                       |
                       |
               Generate Secret
                       |
                       v
                 TOTP Secret
                       |
                       |
          +------------+------------+
          |                         |
          v                         v
    Authenticator App          Application
          |                         |
          |                         |
    Generates OTP             Stores Secret
          |                         |
          +------------+------------+
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
              True      InvalidOTPError

The application integrating LionAuth is responsible for managing users and securely storing their TOTP secrets.

Generating a Secret

Generate a new TOTP secret using:

from lionauth import TOTPAuthenticator

auth = TOTPAuthenticator()

secret = auth.generate_secret()

print(secret)

The generated secret should be treated as a sensitive authentication credential.

Applications should store it securely and should never expose it unnecessarily.

Provisioning URI

LionAuth can generate a standard otpauth:// provisioning URI.

uri = auth.get_provisioning_uri(
    secret=secret,
    account_name="user@example.com",
)

print(uri)

Example:

otpauth://totp/LionAuth:user%40example.com?secret=XXXXXXXX&issuer=LionAuth&algorithm=SHA1&digits=6&period=30

The URI contains the information required by compatible authenticator applications to configure the TOTP account.

LionAuth intentionally does not generate QR codes.

Applications are free to decide how they want to present the provisioning URI to users.

Generating an OTP

Generate the current OTP:

otp = auth.generate_otp(secret)

print(otp)

Example:

483921

The OTP changes according to the configured time interval.

Verifying an OTP

Verify an OTP using:

result = auth.verify(
    secret=secret,
    otp=otp,
)

print(result)

A valid OTP returns:

True

An invalid OTP raises:

InvalidOTPError

Example:

from lionauth import TOTPAuthenticator, InvalidOTPError

auth = TOTPAuthenticator()

secret = auth.generate_secret()
otp = auth.generate_otp(secret)

try:
    auth.verify(secret, otp)
    print("Authentication successful")

except InvalidOTPError:
    print("Invalid authentication code")
Configuration

LionAuth provides TOTPConfig for customizing the TOTP behavior.

from lionauth import TOTPAuthenticator, TOTPConfig

config = TOTPConfig(
    digits=6,
    interval=30,
    algorithm="SHA1",
    issuer="My Application",
    valid_window=0,
)

auth = TOTPAuthenticator(config)
Configuration Options
Option	Default	Description
digits	6	Number of digits in the generated OTP
interval	30	Number of seconds before the OTP changes
algorithm	SHA1	Hashing algorithm
issuer	LionAuth	Application/service name
valid_window	0	Number of adjacent time windows accepted during verification

Supported algorithms:

SHA1
SHA256
SHA512

Supported OTP digit lengths:

6
8
Example Custom Configuration
from lionauth import TOTPAuthenticator, TOTPConfig

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

print(otp)

print(auth.verify(secret, otp))
Enrollment Workflow

A typical authenticator enrollment process looks like this:

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
          Enable TOTP      Reject OTP

The application should not mark TOTP as enabled merely because a secret was generated.

The user should first prove that their authenticator application is correctly configured by successfully providing a valid OTP.

Authentication Workflow

After enrollment, authentication works like this:

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
Exceptions

LionAuth provides its own exception hierarchy.

from lionauth import (
    LionAuthError,
    ConfigurationError,
    InvalidSecretError,
    InvalidOTPError,
    InvalidInputError,
)
Exception Hierarchy
LionAuthError
|
+-- ConfigurationError
|
+-- InvalidSecretError
|
+-- InvalidOTPError
|
+-- InvalidInputError
LionAuthError

Base exception for LionAuth errors.

You can catch all LionAuth errors using:

from lionauth import LionAuthError

try:
    auth.verify(secret, otp)

except LionAuthError:
    print("A LionAuth error occurred")
ConfigurationError

Raised when the TOTP configuration is invalid.

Example:

from lionauth import TOTPConfig, ConfigurationError

try:
    config = TOTPConfig(
        digits=7
    )

except ConfigurationError as error:
    print(error)
InvalidSecretError

Raised when an invalid TOTP secret is supplied.

Example:

from lionauth import InvalidSecretError

try:
    auth.generate_otp("")

except InvalidSecretError as error:
    print(error)
InvalidOTPError

Raised when an OTP is invalid.

Example:

from lionauth import InvalidOTPError

try:
    auth.verify(
        secret=secret,
        otp="123456",
    )

except InvalidOTPError:
    print("Invalid OTP")
InvalidInputError

Raised when an input doesn't meet the expected requirements.

Example:

from lionauth import InvalidInputError

try:
    auth.get_provisioning_uri(
        secret=secret,
        account_name="",
    )

except InvalidInputError as error:
    print(error)
What LionAuth Does Not Handle

LionAuth is intentionally focused on TOTP authentication.

It does not manage:

User accounts
User registration
Password authentication
Password storage
Databases
JWT authentication
Sessions
Email delivery
SMS OTP
QR-code generation
User permissions
Roles
Application-specific authorization

These responsibilities belong to the application integrating LionAuth.

Database

LionAuth does not require a database.

The application using LionAuth is responsible for storing the user's TOTP secret.

For example, an application might have:

users
--------------------------------
id
email
name
totp_secret
totp_enabled

LionAuth only works with the secret provided by the application.

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
Security

TOTP secrets are sensitive authentication credentials.

Applications using LionAuth should:

Store TOTP secrets securely.
Never expose TOTP secrets in logs.
Never expose secrets to clients unnecessarily.
Encrypt or otherwise appropriately protect secrets at rest.
Require successful OTP verification before completing enrollment.
Use a reasonable valid_window.
Protect authentication endpoints against brute-force attempts.
Avoid returning secrets in API responses unless necessary.
Avoid storing OTPs permanently.
Never commit TOTP secrets to source control.

LionAuth itself does not store users or TOTP secrets in a database.

Development

Clone the project:

git clone <repository-url>

Enter the project directory:

cd LionAuth

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

Linux/macOS
source venv/bin/activate
Windows
venv\Scripts\activate

Install LionAuth with development dependencies:

pip install -e ".[dev]"
Running Tests

LionAuth uses pytest.

Run the complete test suite:

pytest

A successful test run should look similar to:

======================== test session starts ========================

tests/test_config.py ........
tests/test_totp.py .........

========================= 17 passed =========================
Building the Package

Install the build tool:

pip install build

Build LionAuth:

python -m build

The distribution files will be generated inside:

dist/

Example:

dist/
├── lionauth-0.1.0-py3-none-any.whl
└── lionauth-0.1.0.tar.gz
Project Structure
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
Design Philosophy

LionAuth follows a simple principle:

LionAuth handles TOTP. The application handles everything else.

This keeps the library:

Lightweight
Framework independent
Database independent
Easy to integrate
Easy to test
Reusable across Python applications

LionAuth can be integrated into applications built with frameworks such as:

Django
FastAPI
Flask
Other Python web frameworks
CLI applications
Custom Python applications
Complete Example
from lionauth import (
    TOTPAuthenticator,
    InvalidOTPError,
)

# Create authenticator
auth = TOTPAuthenticator()

# Generate a secret during enrollment
secret = auth.generate_secret()

# Generate provisioning URI
uri = auth.get_provisioning_uri(
    secret=secret,
    account_name="user@example.com",
)

print("Configure your authenticator using:")
print(uri)

# Generate current OTP
otp = auth.generate_otp(secret)

print("Current OTP:", otp)

# Verify OTP
try:
    if auth.verify(secret, otp):
        print("Authentication successful")

except InvalidOTPError:
    print("Authentication failed")
License

MIT

Author

LionAuth is a reusable TOTP authentication library for Python applications.


