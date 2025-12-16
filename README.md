# Avanak

Python client library for Avanak voice message REST API.

## Installation

```bash
pip install avanak
```

## Usage

```python
from avanak import AvanakClient

client = AvanakClient(token="your_token")

# Get account status
status = client.account_status()
print(status.account_name)

# Send OTP
response = client.send_otp(length=4, number="09120000000")
print(response.generated_code)
```

## Development

This project uses uv for dependency management, ruff for linting and formatting.

```bash
uv sync
uv run ruff check .
uv run ruff format .
```