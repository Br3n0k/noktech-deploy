# API de Referência

## Deployers

### BaseDeployer
Classe base abstrata para implementações de deployers.

```python
class BaseDeployer(ABC):
    def __init__(self, host: str, user: str, password: str, port: int)
    
    @abstractmethod
    def connect(self) -> None:
        """Estabelece conexão com o servidor"""
        
    @abstractmethod
    def disconnect(self) -> None:
        """Encerra conexão com o servidor"""
        
    @abstractmethod
    def deploy_files(self, files_path: str, dest_path: str) -> None:
        """Faz upload dos arquivos"""
```

### SSHDeployer
Implementação para deploy via SSH/SFTP.

```python
class SSHDeployer(BaseDeployer):
    def __init__(self, 
                 host: str, 
                 user: str, 
                 password: str, 
                 port: int = 22,
                 key_path: Optional[str] = None)
```

### FTPDeployer
Implementação para deploy via FTP.

```python
class FTPDeployer(BaseDeployer):
    def __init__(self, 
                 host: str, 
                 user: str, 
                 password: str, 
                 port: int = 21)
```

## Core

### FileManager
Gerencia operações com arquivos.

```python
class FileManager:
    def collect_files(self, base_path: str) -> List[Tuple[str, str]]:
        """Coleta arquivos para deploy"""
        
    def watch_directory(self, path: str, callback: Callable) -> None:
        """Observa mudanças no diretório"""
```

### IgnoreRules
Processa regras de ignore.

```python
class IgnoreRules:
    def __init__(self, 
                 rules: Optional[List[str]] = None,
                 ignore_file: Optional[str] = None)
                 
    def should_ignore(self, path: str) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
```

## Utilitários

### Logger
Sistema de logging.

```python
class Logger:
    def info(self, message: str) -> None
    def error(self, message: str) -> None
    def warning(self, message: str) -> None
    def debug(self, message: str) -> None
```

### Config
Gerenciamento de configurações.

```python
class Config:
    def get(self, key: str, default: Any = None) -> Any
    def set(self, key: str, value: Any) -> None
    def delete(self, key: str) -> None
``` 