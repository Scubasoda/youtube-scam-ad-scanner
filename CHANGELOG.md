# Changelog

All notable changes to the YouTube Scam Ad Scanner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-10

### Added
- Initial release of YouTube Scam Ad Scanner
- Core scanning functionality with heuristic-based detection
- Domain analysis features:
  - Suspicious TLD detection (.xyz, .top, .click, etc.)
  - IP address detection
  - Long domain name detection
  - Multiple hyphens/digits detection
  - HTTPS verification
- Content analysis features:
  - Scam keyword detection
  - Urgency language detection
  - Too-good-to-be-true phrase detection
  - Excessive punctuation detection
  - Popup/alert script detection
  - Password field detection
  - Form analysis
  - Meta tag validation
- Risk scoring system with four levels (MINIMAL, LOW, MEDIUM, HIGH)
- Command-line interface using Click
- Color-coded terminal output using Colorama
- JSON output option for integration
- Comprehensive test suite with pytest
- Batch URL scanning script
- Configuration system for easy customization

### Documentation
- README.md with project overview and quick start
- SETUP.md with detailed installation instructions
- EXAMPLES.md with usage examples and patterns
- CONTRIBUTING.md with contribution guidelines
- LICENSE (MIT)
- Sample URLs file for testing
- Inline code documentation and docstrings

### Development
- Python package structure
- pytest configuration
- .gitignore for Python projects
- Type hints throughout codebase
- Modular design for easy extension

## [Unreleased]

### Planned
- Browser extension for automatic ad capture
- Machine learning model integration
- Selenium-based dynamic page analysis
- Screenshot capture and visual analysis
- Database of known scam domains
- API service for remote scanning
- Web dashboard for results visualization
- Enhanced reporting with PDF export
- Multi-language support for international scams
- Performance optimizations with async/await
- Caching layer for repeated scans

---

## Release Notes Format

### Added
New features and functionality

### Changed
Changes to existing functionality

### Deprecated
Features that will be removed in future releases

### Removed
Features that have been removed

### Fixed
Bug fixes

### Security
Security-related changes
