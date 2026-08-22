# LionAuth

A reusable Python library for implementing **Time-based One-Time Password (TOTP) authentication**.

LionAuth provides the core functionality needed to integrate authenticator-app-based authentication into Python applications.

It works with authenticator applications such as **Google Authenticator** and **Microsoft Authenticator**.

---

## Features

- TOTP secret generation
- OTP generation
- OTP verification
- Configurable OTP digits
- Configurable time interval
- SHA1, SHA256, and SHA512 support
- Provisioning URI generation
- Input validation
- Custom authentication exceptions
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