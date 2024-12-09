# Utils API Reference

## Logger

Class for managing application logs.

```python
from src.utils.logger import Logger

logger = Logger(log_file="app.log", log_level="DEBUG")
logger.info("Operation completed")
```

### Methods

#### `__init__(log_file: Optional[str] = None, log_level: str = "INFO")`
- `log_file`: Path to log file
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### `debug(message: str)`
Log debug message.

#### `info(message: str)`
Log info message.

#### `warning(message: str)`
Log warning message.

#### `error(message: str)`
Log error message.

## Config

Class for managing configuration.

```python
from src.utils.config import Config

config = Config("config.json")
host = config.get("host", "localhost")
```

### Methods

#### `__init__(config_file: Optional[str] = None)`
- `config_file`: Path to configuration file

#### `get(key: str, default: Any = None) -> Any`
Get configuration value.

#### `set(key: str, value: Any)`
Set configuration value.

#### `save_config()`
Save configuration to file.

## I18n

Class for internationalization.

```python
from src.i18n import I18n

i18n = I18n()
message = i18n.get("error.not_found")
```

### Methods

#### `__init__(lang: Optional[str] = None)`
- `lang`: Language code (e.g., "en_us", "pt_br")

#### `get(key: str, **kwargs) -> str`
Get translated message.
- `key`: Message key
- `kwargs`: Format parameters

#### `set_language(lang: str)`
Change current language. 