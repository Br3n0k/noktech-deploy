# Usage Examples

## Basic Deployment

### SSH/SFTP

```bash
# Basic SSH deployment
noktech-deploy --protocol ssh \
               --host example.com \
               --user deploy \
               --files-path ./dist \
               --dest-path /var/www/app

# Deploy with SSH key
noktech-deploy --protocol ssh \
               --host example.com \
               --user deploy \
               --key-path ~/.ssh/id_rsa \
               --files-path ./dist \
               --dest-path /var/www/app
```

### FTP

```bash
# Basic FTP deployment
noktech-deploy --protocol ftp \
               --host ftp.example.com \
               --user ftpuser \
               --password mypassword \
               --files-path ./site \
               --dest-path /public_html

# Secure FTP deployment (FTPS)
noktech-deploy --protocol ftps \
               --host ftps.example.com \
               --user ftpuser \
               --password mypassword \
               --files-path ./site \
               --dest-path /public_html
```

### Local

```bash
# Local copy
noktech-deploy --protocol local \
               --files-path ./data \
               --dest-path /mnt/backup

# Network share copy
noktech-deploy --protocol local \
               --files-path ./project \
               --dest-path //server/shared
```

## Watch Mode

### Basic Watch

```bash
# Watch changes and deploy via SSH
noktech-deploy --protocol ssh \
               --host example.com \
               --watch \
               --files-path ./src

# Watch with custom ignore patterns
noktech-deploy --protocol ssh \
               --host example.com \
               --watch \
               --ignore-patterns "*.tmp,*.log" \
               --files-path ./src
```

### Watch with Specific Events

```bash
# Watch only creation and modification
noktech-deploy --protocol ssh \
               --host example.com \
               --watch \
               --events create,modify \
               --files-path ./src

# Watch with sync delay
noktech-deploy --protocol ssh \
               --host example.com \
               --watch \
               --delay 2 \
               --files-path ./src
```

## Advanced Configuration

### Using Configuration File

```json
// config.json
{
    "default_protocol": "ssh",
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
            "dest_path": "/public_html"
        }
    }
}
```

```bash
# Use predefined configuration
noktech-deploy --config production --files-path ./dist

# Override configurations
noktech-deploy --config staging \
               --dest-path /var/www/temp \
               --files-path ./dist
```

### Ignoring Files

```plaintext
# .deployignore
*.log
*.tmp
node_modules/
__pycache__/
.git/
```

```bash
# Use custom ignore file
noktech-deploy --protocol ssh \
               --host example.com \
               --ignore-file ./custom-ignore \
               --files-path ./src

# Combine multiple patterns
noktech-deploy --protocol ssh \
               --host example.com \
               --ignore-patterns "*.tmp,*.log" \
               --ignore-file .deployignore \
               --files-path ./src
```

## Script Integration

### Shell Script

```bash
#!/bin/bash

# Deploy to multiple environments
environments=("staging" "production")

for env in "${environments[@]}"; do
    echo "Deploying to $env..."
    noktech-deploy --config "$env" --files-path ./dist
done
```

### Python Script

```python
from noktech_deploy import DeployClient, Args

async def deploy_to_multiple():
    client = DeployClient()
    environments = ["staging", "production"]
    
    for env in environments:
        args = Args(
            config=env,
            files_path="./dist",
            watch=True
        )
        await client.run(args)

if __name__ == "__main__":
    import asyncio
    asyncio.run(deploy_to_multiple())
``` 