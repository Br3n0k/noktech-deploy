<div align="right">
    <a href="README.md">🇧🇷 Português</a> &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="README_en.md">🇺🇸 English</a>
</div>

<div align="center">
  <img src="src/assets/logo.webp" alt="NokTech Deploy Logo" width="200"/>
  <h1>NokTech Deploy</h1>
  <p><strong>Advanced deployment client with multiple protocol support</strong></p>
  
  [![Version](https://img.shields.io/badge/version-0.1.2-blue.svg)](https://github.com/Br3n0k/noktech-deploy)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.8.1+-yellow.svg)](https://www.python.org/)
  [![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
</div>

## 📋 Index

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [💻 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [🛠️ Development](#️-development)
- [📊 Tests](#-tests)
- [📝 Logs](#-logs)
- [📦 Build](#-build)
- [📖 Documentation](#-documentation)
- [📄 License](#-license)

## ✨ Features

- **Multiple Protocols**
  - SSH/SFTP (password or SSH key)
  - FTP
  - Local (local/network copy)
- **Real-time Monitoring**
- **Advanced Ignore System**
- **Interactive Interface**
- **Complete Logging System**
- **Automatic Version Check**
  - Remote version comparison
  - Version mismatch logging
  - Outdated version alerts
- **Multi-platform Support**
  - Windows
  - Linux
  - MacOS

## 🚀 Installation
```bash
# Via pip
pip install noktech-deploy

# Via Poetry
poetry add noktech-deploy

# From source
git clone https://github.com/Br3n0k/noktech-deploy
cd noktech-deploy
poetry install
python build_config.py build
```

## 💻 Usage

### Basic Commands
```bash
# Interactive Mode
noktech-deploy

# SSH Deploy
noktech-deploy --protocol ssh --host example.com --user deploy

# FTP Deploy
noktech-deploy --protocol ftp --host ftp.example.com --user ftpuser

# Local Deploy
noktech-deploy --protocol local --files-path ./data --dest-path /backup
```

### Advanced Commands
```bash
# Watch Mode
noktech-deploy --watch --files-path ./src

# Custom Ignore
noktech-deploy --ignore-file ./custom.ignore

# Custom Logging
noktech-deploy --log-dir ./logs --log-level debug

# Alternative Config
noktech-deploy --config-file ./deploy.json
```

## ⚙️ Configuration

### Directory Structure
```
.noktech-deploy/
├── config/           # System configurations
│   └── config.json   # Main configuration
├── logs/            # System logs
│   ├── deploy-YYYY-MM.log
│   └── version-YYYY-MM.log
└── .deployignore    # Ignore rules
```

### Main configuration file (config.json)
```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "log_dir": ".noktech-deploy/logs",
    "watch_delay": 1000,
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "port": 22,
            "user": "deploy",
            "password": "secure_password",
            "key_path": null,
            "dest_path": "/var/www/app",
            "timeout": 30,
            "keep_alive": true,
            "compression": true,
            "ignore_file": ".deployignore",
            "backup": {
                "enabled": true,
                "max_backups": 5,
                "path": "/var/backups/app"
            },
            "hooks": {
                "pre_deploy": "echo 'Starting deploy'",
                "post_deploy": "echo 'Deploy finished'"
            },
            "retry": {
                "attempts": 3,
                "delay": 5
            }
        }
    }
}
```

## 🛠️ Development

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run linting
poetry run ruff check .
poetry run black .

# Update version
poetry run python scripts/update_version.py <version>
```

## 📊 Tests

```bash
# Run all tests
poetry run pytest

# Tests with coverage
poetry run pytest --cov=src

# Specific tests
poetry run pytest tests/test_deployers.py -v

# HTML coverage report
poetry run pytest --cov=src --cov-report=html
```

## 📝 Logs

```bash
# View deploy logs
cat .noktech-deploy/logs/deploy-$(date +%Y-%m).log

# View version logs
cat .noktech-deploy/logs/version-$(date +%Y-%m).log

# List all logs
ls -l .noktech-deploy/logs/

# Clean old logs (keeps last 30 days)
noktech-deploy --clean-logs

# Check current version
noktech-deploy --version
```

## 📦 Build

```bash
# Complete build
poetry run python -m build

# Clean only
poetry run python -m build clean

# Build package
poetry build

# Install locally
pip install dist/noktech_deploy-*.whl
```

## 📖 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Advanced Configuration](docs/configuration.md)
- [Ignore System](docs/ignore_rules.md)
- [API Reference](docs/api.md)
- [Changelog](CHANGELOG.md)

### Version Check
NokTech Deploy automatically checks if your local version is up to date with the remote version in the official repository. When a version mismatch is detected:

1. An alert message is displayed
2. The mismatch is logged
3. User is notified to update

Version logs are stored in:
```
.noktech-deploy/logs/version-YYYY-MM.log
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Brendown Ferreira**
- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: br3n0k@gmail.com