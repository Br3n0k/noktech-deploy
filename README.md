# NokTech Deploy

![NokTech Deploy Logo](src/assets/logo.webp)

Advanced deployment client with multiple protocol support and real-time file monitoring.

![Version](https://img.shields.io/badge/version-0.1.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [💻 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🛠️ Development](#️-development)
- [📊 Testing](#-testing)
- [📝 Logging](#-logging)
- [📦 Building](#-building)
- [📖 Documentation](#-documentation)
- [📄 License](#-license)

## ✨ Features

- **Multiple Protocol Support**
  - SSH/SFTP (password or key-based)
  - FTP
  - Local (filesystem/network)
- **Real-time Monitoring**
  - File change detection
  - Automatic deployment
  - Customizable ignore rules
- **Interactive CLI**
  - User-friendly interface
  - Progress tracking
  - Colored output
- **Comprehensive Logging**
  - Detailed operation logs
  - Version tracking
  - Error reporting
- **Automatic Version Checking**
  - Remote version comparison
  - Update notifications
  - Version history logging
- **Cross-platform Support**
  - Windows
  - Linux
  - macOS

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
python build.py all
```

## 💻 Usage

### Basic Commands

```bash
# Interactive Mode
noktech-deploy

# SSH Deployment
noktech-deploy --protocol ssh --host example.com --user deploy

# FTP Deployment
noktech-deploy --protocol ftp --host ftp.example.com --user ftpuser

# Local Deployment
noktech-deploy --protocol local --source ./data --dest /backup
```

## 📁 Project Structure

```plaintext
noktech-deploy/
├── src/                    # Source code
│   ├── assets/            # Project assets
│   ├── core/              # Core functionality
│   │   ├── config.py      # Configuration management
│   │   ├── constants.py   # Project constants
│   │   ├── progress.py    # Progress tracking
│   │   └── watcher.py     # File monitoring
│   ├── deployers/         # Protocol implementations
│   │   ├── ssh.py         # SSH/SFTP deployer
│   │   ├── ftp.py         # FTP deployer
│   │   └── local.py       # Local filesystem deployer
│   ├── i18n/              # Internationalization
│   │   └── lang/          # Language files
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── build.py              # Build script
├── main.py               # Entry point
└── pyproject.toml        # Project configuration
```

## 📙️ Configuration

The system uses a JSON configuration file located at `.noktech-deploy/config.json`:

```json
{
    "parallel_deploy": false,
    "ignore_patterns": [
        "*.pyc",
        "__pycache__",
        ".git"
    ],
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "key_path": "~/.ssh/id_rsa"
        }
    }
}
```

## 🛠️ Development

```bash
# Setup development environment
poetry install
poetry shell

# Code formatting
ruff check --fix .
black .

# Type checking
mypy src/

# Update version
python build.py version 0.1.3
```

## 📊 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific tests
poetry run pytest tests/test_deployers.py -v
```

## 📝 Logging

Logs are stored in `.noktech-deploy/logs/`:

```bash
# View deployment logs
cat .noktech-deploy/logs/deploy-YYYY-MM.log

# View version logs
cat .noktech-deploy/logs/version-YYYY-MM.log

# Clean old logs
noktech-deploy --clean-logs
```

## 📦 Building

```bash
# Complete build process
python build.py all

# Clean build artifacts
python build.py clean

# Build package only
python build.py package

# Build executable
python build.py exe
```

## 📖 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Advanced Configuration](docs/configuration.md)
- [Ignore Rules System](docs/ignore_rules.md)
- [API Reference](docs/api.md)
- [Changelog](CHANGELOG.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

### **Brendown Ferreira**

- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: [br3n0k@gmail.com](mailto:br3n0k@gmail.com)

---

Built with ❤️ by Brendown Ferreira
