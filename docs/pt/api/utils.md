# Referência da API de Utils

## Logger

Classe para gerenciar logs da aplicação.

```python
from src.utils.logger import Logger

logger = Logger(log_file="app.log", log_level="DEBUG")
logger.info("Operação concluída")
```

### Métodos

#### `__init__(log_file: Optional[str] = None, log_level: str = "INFO")`
- `log_file`: Caminho do arquivo de log
- `log_level`: Nível de log (DEBUG, INFO, WARNING, ERROR)

#### `debug(message: str)`
Registra mensagem de debug.

#### `info(message: str)`
Registra mensagem de informação.

#### `warning(message: str)`
Registra mensagem de aviso.

#### `error(message: str)`
Registra mensagem de erro.

## Config

Classe para gerenciar configurações.

```python
from src.utils.config import Config

config = Config("config.json")
host = config.get("host", "localhost")
```

### Métodos

#### `__init__(config_file: Optional[str] = None)`
- `config_file`: Caminho do arquivo de configuração

#### `get(key: str, default: Any = None) -> Any`
Obtém valor de configuração.

#### `set(key: str, value: Any)`
Define valor de configuração.

#### `save_config()`
Salva configuração no arquivo.

## I18n

Classe para internacionalização.

```python
from src.i18n import I18n

i18n = I18n()
mensagem = i18n.get("error.not_found")
```

### Métodos

#### `__init__(lang: Optional[str] = None)`
- `lang`: Código do idioma (ex: "en_us", "pt_br")

#### `get(key: str, **kwargs) -> str`
Obtém mensagem traduzida.
- `key`: Chave da mensagem
- `kwargs`: Parâmetros de formatação

#### `set_language(lang: str)`
Altera idioma atual. 