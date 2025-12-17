# Avanak

[![CI](https://github.com/pouralijan/avanak-python/actions/workflows/test.yml/badge.svg)](https://github.com/pouralijan/avanak-python/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/avanak.svg)](https://pypi.org/project/avanak/)
[![Python versions](https://img.shields.io/pypi/pyversions/avanak.svg)](https://pypi.org/project/avanak/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python client library for Avanak voice message REST API. Avanak is a Persian voice messaging service that allows you to send voice messages, OTP codes, and manage campaigns programmatically.

## Features

- ✅ **Complete API Coverage**: All 17 Avanak REST API endpoints
- ✅ **Type Safety**: Full type hints and Pydantic models
- ✅ **Easy to Use**: Simple, intuitive API design
- ✅ **Well Tested**: Comprehensive test suite with 20+ unit tests
- ✅ **CLI Tool**: Command-line interface for quick operations
- ✅ **Modern Python**: Supports Python 3.8+ with modern practices

## Installation

```bash
pip install avanak
```

Or with uv (recommended):

```bash
uv add avanak
```

## Quick Start

```python
from avanak import AvanakClient

# Initialize client with your API token
client = AvanakClient(token="your_api_token")

# Get account status
status = client.account_status()
print(f"Account: {status.account_name}")
print(f"Credit: {status.remaind_credit} Rials")

# Send OTP (One-Time Password)
otp = client.send_otp(length=4, number="09120000000")
print(f"OTP Code: {otp.generated_code}")

# Generate text-to-speech
tts = client.generate_tts(
    text="سلام، این یک پیام صوتی آزمایشی است",
    title="Test Message"
)
print(f"Message ID: {tts.id}")

# Send quick voice message
result = client.quick_send(
    message_id=tts.id,
    number="09120000000"
)
print(f"Send Status: {result['Status']}")
```

## CLI Usage

The package includes a command-line tool for quick operations:

```bash
# After installation, use the avanak command directly
avanak account-status
avanak send-otp 4 09120000000
avanak generate-tts "Hello World" "Greeting"

# Or run as a module
python -m avanak account-status
```

## API Reference

### Account Management
- `account_status()` - Get account information and credit balance

### OTP Operations
- `send_otp(length, number, ...)` - Send one-time password

### Message Management
- `upload_message_base64(title, base64, ...)` - Upload audio file
- `download_message(message_id)` - Download audio file
- `generate_tts(text, title, ...)` - Generate text-to-speech
- `get_message(message_id)` - Get message details
- `delete_message(message_id)` - Delete message
- `get_messages(skip, take)` - List messages

### Sending Operations
- `quick_send(message_id, number, ...)` - Send existing message
- `quick_send_with_tts(text, number, ...)` - Send TTS message directly

### Campaign Management
- `create_campaign(title, numbers, message_id, ...)` - Create bulk campaign
- `start_campaign(campaign_id, ...)` - Start campaign
- `stop_campaign(campaign_id)` - Stop campaign
- `get_campaign(campaign_id)` - Get campaign details
- `get_campaign_numbers_by_campaign_id(campaign_id)` - Get campaign recipients

### Reporting
- `get_quick_send(quick_send_id)` - Get send status
- `get_quick_send_statistics(start_date, end_date)` - Get statistics

## Authentication

Get your API token from the [Avanak Portal](https://portal.avanak.ir). The token can be provided via:

1. **Environment variable**: `export AVANAK_TOKEN=your_token`
2. **File**: Save token in `~/.avanak_token`
3. **Direct parameter**: `AvanakClient(token="your_token")`

## Development

This project uses modern Python development tools:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v

# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Build package
uv build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://github.com/pouralijan/avanak-python#readme)
- 🐛 [Issues](https://github.com/pouralijan/avanak-python/issues)
- 💬 [Avanak Portal](https://portal.avanak.ir)
