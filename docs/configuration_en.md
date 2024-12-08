# Configuration

## Global Configuration File

The main configuration file is located at `~/.noktech-deploy/config.json`.

### Basic Structure

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy"
        }
    }
}
```

## Configuration Options

### Global Settings

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| default_protocol | string | Default protocol | "ssh" |
| log_level | string | Log level | "info" |
| default_ignore_file | string | Default ignore file | "~/.deployignore" |
| log_file | string | Log file | "~/.noktech-deploy/deploy.log" |

### Host Settings

| Option | Type | Description | Required |
|--------|------|-------------|----------|
| protocol | string | Deploy protocol | Yes |
| host | string | Host address | Yes* |
| user | string | Username | Yes* |
| password | string | Password | No |
| key_path | string | SSH key path | No |
| port | number | Port | No |
| dest_path | string | Destination path | Yes |

*Not required for "local" protocol

## Supported Protocols

### SSH/SFTP

```json
{
    "protocol": "ssh",
    "host": "example.com",
    "user": "deploy",
    "key_path": "~/.ssh/id_rsa",
    "port": 22,
    "dest_path": "/var/www/app"
}
```

### FTP

```json
{
    "protocol": "ftp",
    "host": "ftp.example.com",
    "user": "ftpuser",
    "password": "pass123",
    "dest_path": "/public_html"
}
```

### Local

```json
{
    "protocol": "local",
    "dest_path": "/mnt/backup"
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| NOKTECH_CONFIG | Configuration file path |
| NOKTECH_LOG_LEVEL | Log level |
| NOKTECH_IGNORE_FILE | Ignore file |
| NOKTECH_SSH_KEY | SSH key path |
| NOKTECH_PASSWORD | Authentication password |

## Complete Examples

### Multiple Environments

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "key_path": "~/.ssh/id_rsa",
            "dest_path": "/var/www/app"
        },
        "staging": {
            "protocol": "ftp",
            "host": "staging.example.com",
            "user": "ftpuser",
            "password": "pass123",
            "dest_path": "/public_html"
        },
        "backup": {
            "protocol": "local",
            "dest_path": "/mnt/backup"
        }
    }
}
```

### Configuration with Ignore Patterns

```json
{
    "default_protocol": "ssh",
    "default_ignore_file": "~/.deployignore",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "ignore_patterns": [
                "*.tmp",
                "*.log",
                "node_modules/"
            ]
        }
    }
}
```

## Troubleshooting

### Order of Precedence

1. Command line arguments
2. Environment variables
3. Project configuration file
4. Global configuration file
5. Default values

### Tips

- Use environment variables for sensitive information
- Keep passwords out of version control
- Use SSH keys when possible
- Configure appropriate log levels 