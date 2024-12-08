# Watch Mode

Watch mode allows monitoring real-time changes and automatic deployment.

## How It Works

- Monitors file creation, modification, and deletion
- Respects ignore rules
- Debouncing to prevent multiple deploys
- Logging of all operations

## Usage

```bash
noktech-deploy --watch \
    --protocol ssh \
    --host example.com \
    --files-path ./src \
    --dest-path /var/www/app
```

## Advanced Settings

### Debouncing

The wait time between change detection and deployment can be configured:

```bash
noktech-deploy --watch \
    --watch-delay 2.0  # Wait 2 seconds
```

### Events

You can choose which events to watch:

```bash
noktech-deploy --watch \
    --watch-events create,modify  # Ignores deletions
```

### Filters

Filter specific files during watching:

```bash
noktech-deploy --watch \
    --watch-pattern "*.js,*.css"  # Only JS and CSS