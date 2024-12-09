# Referência da API Core

## DirectoryWatcher

Classe responsável por monitorar mudanças em diretórios.

```python
from src.core.watcher import DirectoryWatcher

watcher = DirectoryWatcher(
    source_dir="./src",
    callback=handle_change,
    ignore_rules=ignore_rules
)
```

### Métodos

#### `__init__(source_dir: str, callback: Callable, ignore_rules: Optional[IgnoreRules] = None)`
- `source_dir`: Diretório a monitorar
- `callback`: Função chamada quando ocorrem mudanças
- `ignore_rules`: Regras para ignorar arquivos

#### `async start()`
Inicia o monitoramento de mudanças.

#### `stop()`
Para o monitoramento de mudanças.

## IgnoreRules

Classe para gerenciar padrões de arquivos a ignorar.

```python
from src.core.ignore_rules import IgnoreRules

rules = IgnoreRules(".deployignore")
```

### Métodos

#### `__init__(ignore_file: Optional[str] = None)`
- `ignore_file`: Caminho do arquivo de regras

#### `should_ignore(path: str) -> bool`
Verifica se um caminho deve ser ignorado.

#### `add_pattern(pattern: str)`
Adiciona um novo padrão de ignore.

## Constantes

```python
from src.core.constants import *

# Diretórios
PROJECT_ROOT      # Diretório atual
CONFIG_DIR        # ~/.noktech-deploy
DEFAULT_LOG_DIR   # ~/.noktech-deploy/logs

# Arquivos
DEFAULT_CONFIG_FILE  # config.json
DEFAULT_IGNORE_FILE  # .deployignore

# Templates
DEFAULT_CONFIG_TEMPLATE   # Configuração padrão
DEFAULT_IGNORE_TEMPLATE   # Regras de ignore padrão
``` 