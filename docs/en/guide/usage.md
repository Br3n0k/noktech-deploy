# Usage

## Basic Commands

### Interactive Mode
```bash
noktech-deploy
```

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

### Watch Mode
```bash
noktech-deploy --watch \
               --protocol local \
               --files-path ./src \
               --dest-path ./dist
```

## Command Options

- `--protocol`: Deployment protocol (ssh, local)
- `--host`: Remote host
- `--user`: Username
- `--password`: Password (not recommended, use SSH key)
- `--key-path`: SSH key path
- `--files-path`: Source directory
- `--dest-path`: Destination directory
- `--watch`: Enable watch mode
- `--ignore`: Ignore patterns
- `--log-level`: Log level (debug, info, warning, error)
- `--config`: Custom config file path

## Examples

### Deploy with SSH Key
```bash
noktech-deploy --protocol ssh \
               --host prod.example.com \
               --user deploy \
               --key-path ~/.ssh/deploy_key \
               --files-path ./build \
               --dest-path /var/www/prod
```

### Watch Mode with Custom Ignore
```bash
noktech-deploy --watch \
               --protocol local \
               --files-path ./src \
               --dest-path ./dist \
               --ignore "*.tmp,*.cache"
``` 