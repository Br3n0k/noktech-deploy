# Quick Start Guide

## Installation

```bash
pip install noktech-deploy
```

## Basic Usage

### Interactive Mode

The easiest way to get started is using interactive mode:

```bash
noktech-deploy
```

The program will guide you through the necessary options.

### SSH Deployment

```bash
noktech-deploy --protocol ssh \
               --host example.com \
               --user deploy \
               --files-path ./dist \
               --dest-path /var/www/app
```

### Local Deployment

```bash
noktech-deploy --protocol local \
               --files-path ./data \
               --dest-path /mnt/backup
```

## Basic Configuration

### .deployignore File

Create a `.deployignore` file in your project root:

```plaintext
# Ignore development files
__pycache__/
*.pyc
venv/
node_modules/

# Ignore temporary files
*.tmp
*.log
```

### Global Configuration

Create a `config.json` file in `~/.noktech-deploy/`:

```json
{
    "default_protocol": "ssh",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "dest_path": "/var/www/app"
        },
        "staging": {
            "protocol": "ftp",
            "host": "staging.example.com",
            "user": "ftpuser",
            "dest_path": "/public_html"
        }
    }
}
```

## Next Steps

- Read about [Advanced Configuration](configuration.md)
- Learn about the [Ignore System](ignore_rules.md)
- Explore the [API Reference](api.md) 