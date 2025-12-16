# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-15

### Added
- Initial release of Avanak Python client library
- Support for all 17 Avanak REST API endpoints
- Comprehensive test suite with 20 unit tests
- CLI tool for easy API interaction
- Type hints and Pydantic models for all responses
- GitHub Actions CI/CD pipeline for multiple Python versions (3.8-3.14)
- Ruff linting and formatting configuration
- Pre-commit hooks setup
- Complete documentation and examples

### Features
- Account status management
- OTP (One-Time Password) sending
- Audio message upload and download
- Text-to-Speech (TTS) generation
- Quick send operations with and without TTS
- Campaign management (create, start, stop, monitor)
- Message management (list, get, delete)
- Statistics and reporting

### Technical Details
- Built with modern Python practices
- Uses `uv` for dependency management and building
- Comprehensive error handling and validation
- Mock-based testing to avoid API calls during development
- MIT licensed open source project