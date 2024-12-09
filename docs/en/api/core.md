# Core API Reference

## DirectoryWatcher

Class responsible for monitoring directory changes.

```python
from src.core.watcher import DirectoryWatcher

watcher = DirectoryWatcher(
    source_dir="./src",
    callback=handle_change,
    ignore_rules=ignore_rules
)
```

### Methods

#### `__init__(source_dir: str, callback: Callable, ignore_rules: Optional[IgnoreRules] = None)`
- `source_dir`: Directory to watch
- `callback`: Function called when changes occur
- `ignore_rules`: Rules for ignoring files

#### `async start()`
Starts watching for changes.

#### `stop()`
Stops watching for changes.

## IgnoreRules

Class for managing file ignore patterns.

```python
from src.core.ignore_rules import IgnoreRules

rules = IgnoreRules(".deployignore")
```

### Methods

#### `__init__(ignore_file: Optional[str] = None)`
- `ignore_file`: Path to ignore rules file

#### `should_ignore(path: str) -> bool`
Checks if a path should be ignored.

#### `add_pattern(pattern: str)`
Adds a new ignore pattern.

## Constants

```python
from src.core.constants import *

# Directories
PROJECT_ROOT      # Current working directory
CONFIG_DIR        # ~/.noktech-deploy
DEFAULT_LOG_DIR   # ~/.noktech-deploy/logs

# Files
DEFAULT_CONFIG_FILE  # config.json
DEFAULT_IGNORE_FILE  # .deployignore

# Templates
DEFAULT_CONFIG_TEMPLATE   # Default configuration
DEFAULT_IGNORE_TEMPLATE   # Default ignore rules
``` 