# Referência da API de Deployers

## BaseDeployer

Classe base abstrata para todos os deployers.

```python
from src.deployers import BaseDeployer

class CustomDeployer(BaseDeployer):
    async def deploy_file(self, source: str, dest: str):
        # Implementação
        pass
```

### Métodos

#### `async deploy_file(source: str, dest: str)`
Deploy de um arquivo.
- `source`: Caminho do arquivo fonte
- `dest`: Caminho do arquivo destino

#### `async deploy_directory(source_dir: str, dest_dir: str)`
Deploy de um diretório completo.
- `source_dir`: Diretório fonte
- `dest_dir`: Diretório destino

## SSHDeployer

Deployer para protocolo SSH.

```python
from src.deployers import SSHDeployer

deployer = SSHDeployer(
    host="exemplo.com",
    user="deploy",
    password="senha"  # ou key_path="~/.ssh/id_rsa"
)
```

### Métodos

#### `__init__(host: str, user: str, password: Optional[str] = None, key_path: Optional[str] = None)`
- `host`: Host remoto
- `user`: Usuário SSH
- `password`: Senha SSH
- `key_path`: Caminho da chave SSH

## LocalDeployer

Deployer para operações locais.

```python
from src.deployers import LocalDeployer

deployer = LocalDeployer()
```

### Métodos

#### `async backup_file(path: str) -> str`
Cria backup de um arquivo.
- Retorna: Caminho do arquivo de backup

#### `async restore_backup(backup_path: str, original_path: str)`
Restaura um arquivo do backup. 