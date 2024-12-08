<div align="right">
    <a href="README.md">🇧🇷 Português</a> &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="README_en.md">🇺🇸 English</a>
</div>

# NokTech Deploy

<p align="center">
  <img src="src/assets/logo.webp" alt="NokTech Deploy Logo" width="200"/>
</p>

I'm sure you've been in situations where you needed to deploy files to a server in different scenarios and IDEs,
and ended up facing problems such as: having to use different programs or scripts for each situation, having to manually
configure each host, or even wasting time configuring file ignores. NokTech Deploy was created to solve these problems!
With it, you can deploy files to a server quickly and easily, with support for multiple protocols and real-time change monitoring.
And best of all, it's open source!

An advanced and flexible deployment client with support for multiple protocols and real-time change monitoring.

## 📋 Features

- **Multiple Protocols**
  - SSH/SFTP (password or SSH key)
  - FTP
  - Local (local/network file copy)
- **Real-time Watching**
- **Advanced Ignore System**
- **Interactive Interface**
- **Multi-language Support**
- **Complete Logging**

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
Run without arguments for guided interface:
```bash
noktech-deploy
```

### SSH with Password
```bash
noktech-deploy --protocol ssh \
               --host example.com \
               --user deploy \
               --password "your_password" \
               --dest-path /var/www/app \
               --files-path ./dist
```

### SSH with Key
```bash
noktech-deploy --protocol ssh \
               --host example.com \
               --user deploy \
               --key-path ~/.ssh/id_rsa \
               --dest-path /var/www/app \
               --files-path ./dist
```

### FTP
```bash
noktech-deploy --protocol ftp \
               --host ftp.example.com \
               --user ftpuser \
               --password pass123 \
               --dest-path /public_html \
               --files-path ./site
```

### Local
```bash
noktech-deploy --protocol local \
               --dest-path /mnt/backup \
               --files-path ./data
```

### Watch Mode
```bash
noktech-deploy --protocol ssh \
               --host example.com \
               --watch \
               # ... other options ...
```

## 📝 Configuration

### Ignored Files

#### .deployignore (Recommended)
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

#### Via Command Line
```bash
noktech-deploy --ignore-patterns "*.temp" "logs/*" \
               # ... other options ...
```

[Complete ignore documentation](docs/ignore_rules.md)

### Persistent Settings

NokTech Deploy stores settings in `~/.noktech-deploy/config.json`:

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

- [API Reference](docs/api.md)
- [Supported Protocols](docs/protocols.md)
- [Watch Mode](docs/watching.md)
- [Development](docs/development.md)
- [Examples](docs/examples.md)

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add: amazing feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Brendown Ferreira**
- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: br3n0k@gmail.com

## 🔗 Useful Links

- [Changelog](CHANGELOG.md)
- [Report Bug](https://github.com/Br3n0k/noktech-deploy/issues)
- [Request Feature](https://github.com/Br3n0k/noktech-deploy/issues) 