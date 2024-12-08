<div align="right">
    <a href="README.md">🇧🇷 Português</a> &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="README_en.md">🇺🇸 English</a>
</div>

# NokTech Deploy

<p align="center">
  <img src="src/assets/logo.webp" alt="NokTech Deploy Logo" width="200"/>
</p>

An advanced and flexible deployment client with support for multiple protocols and real-time change monitoring.
Perfect for developers who need a robust and reliable solution to automate the deployment process,
whether via SSH, FTP, or even locally.

## 📋 Features

- **Multiple Protocols**
  - SSH/SFTP (password or SSH key)
  - FTP
  - Local (local/network file copy)
- **Real-time Watching**
  - Automatically detects and syncs changes
  - Support for creation, modification, and deletion events
- **Advanced Ignore System**
  - Compatible with .gitignore patterns
  - Support for multiple ignore files
- **Interactive Interface**
  - User-friendly CLI mode
  - Support for automation arguments
- **Multi-language Support**
  - English
  - Portuguese
- **Complete Logging**
  - Detailed operation logs
  - Support for different log levels

## 🚀 Installation

### Via pip
```bash
pip install noktech-deploy
```

### Development
```bash
git clone https://github.com/Br3n0k/noktech-deploy.git
cd noktech-deploy
poetry install
```

## 💻 Usage

### Interactive Mode
```bash
noktech-deploy
```

### SSH
```bash
noktech-deploy --protocol ssh --host example.com --user deploy --files-path ./dist --dest-path /var/www/app
```

### FTP
```bash
noktech-deploy --protocol ftp --host ftp.example.com --user ftpuser --files-path ./site --dest-path /public_html
```

### Local
```bash
noktech-deploy --protocol local --files-path ./data --dest-path /mnt/backup
```

### Watch Mode
```bash
noktech-deploy --protocol ssh --host example.com --watch
```

## 📝 Configuration

### .deployignore
```plaintext
# Development files
__pycache__/
*.pyc
venv/

# Build and temporary
dist/
build/
*.tmp
*.log
```

### config.json
```json
{
    "default_protocol": "ssh",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy"
        }
    }
}
```

## 📚 Documentation

- [Quick Start Guide](docs/quickstart.md)
- [Advanced Configuration](docs/configuration.md)
- [API Reference](docs/api.md)
- [Contributing](docs/contributing.md)

## 📄 License

MIT License - see [LICENSE](LICENSE) for more information.

## 👤 Author

**Brendown Ferreira**
- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: br3n0k@gmail.com

## 🔗 Useful Links

- [Changelog](CHANGELOG.md)
- [Report Bug](https://github.com/Br3n0k/noktech-deploy/issues)
- [Request Feature](https://github.com/Br3n0k/noktech-deploy/issues) 