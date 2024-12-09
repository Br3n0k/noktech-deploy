# Configuration

## Configuration File

The configuration file is located at `~/.noktech-deploy/config.json` and follows this structure:

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "log_dir": "~/.noktech-deploy/logs",
    "watch_delay": 1000,
    "hosts": {
        "local": {
            "protocol": "local",
            "dest_path": "./deploy",
            "ignore_file": ".deployignore",
            "backup": {
                "enabled": true,
                "max_backups": 5,
                "path": "./backups"
            },
            "hooks": {
                "pre_deploy": "",
                "post_deploy": ""
            },
            "retry": {
                "attempts": 3,
                "delay": 5
            }
        }
    },
    "ignore_patterns": [
        "*.pyc",
        "__pycache__/",
        "*.log",
        ".git/"
    ]
}
```

## Options

- `default_protocol`: Default deployment protocol (ssh, local)
- `log_level`: Logging level (debug, info, warning, error)
- `log_dir`: Directory for log files
- `watch_delay`: Delay between file checks in watch mode (milliseconds)
- `hosts`: Configuration for different deployment targets
- `ignore_patterns`: Global patterns to ignore during deployment

## Ignore Rules

Create a `.deployignore` file in your project root to specify files to ignore:

```text
# Development files
__pycache__/
*.pyc
.git/

# Temporary files
*.log
*.tmp
``` 