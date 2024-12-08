# API de Referência

## Classe DeployClient

A classe principal que gerencia todas as operações de deploy.

### Métodos

#### `__init__(self, config_path: Optional[str] = None)`
Inicializa um novo cliente de deploy.
- **config_path**: Caminho opcional para arquivo de configuração

#### `async def run(self, args: Args)`
Executa o processo de deploy com os argumentos fornecidos.
- **args**: Objeto Args com as configurações do deploy

#### `async def interactive_mode(self)`
Inicia o modo interativo para configuração do deploy.

#### `async def watch_mode(self)`
Inicia o modo de observação de mudanças.

## Classe Args

Classe que encapsula os argumentos de linha de comando.

### Atributos

- **protocol**: Protocolo de deploy (`ssh`, `ftp`, `local`)
- **host**: Host de destino
- **user**: Usuário para autenticação
- **password**: Senha para autenticação
- **key_path**: Caminho para chave SSH
- **files_path**: Caminho dos arquivos fonte
- **dest_path**: Caminho de destino
- **watch**: Flag para modo de observação
- **ignore_patterns**: Lista de padrões para ignorar

## Protocolos

### SSHDeployer

Implementa deploy via SSH/SFTP.

#### Métodos Principais

```python
async def connect(self)
async def disconnect(self)
async def upload_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

### FTPDeployer

Implementa deploy via FTP.

#### Métodos Principais

```python
async def connect(self)
async def disconnect(self)
async def upload_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

### LocalDeployer

Implementa deploy local.

#### Métodos Principais

```python
async def connect(self)
async def disconnect(self)
async def copy_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

## Sistema de Eventos

### Classe FileEvent

Representa um evento de mudança de arquivo.

#### Atributos

- **event_type**: Tipo do evento (`created`, `modified`, `deleted`)
- **src_path**: Caminho do arquivo fonte
- **is_directory**: Flag indicando se é diretório

## Logging

### Classe Logger

Gerencia o sistema de logging.

#### Métodos

```python
def info(self, message: str)
def error(self, message: str)
def debug(self, message: str)
def warning(self, message: str)
```

## Exemplos de Uso

### Deploy Básico

```python
from noktech_deploy import DeployClient, Args

async def main():
    client = DeployClient()
    args = Args(
        protocol="ssh",
        host="exemplo.com",
        user="deploy",
        files_path="./dist",
        dest_path="/var/www/app"
    )
    await client.run(args)
```

### Modo Watch Customizado

```python
from noktech_deploy import DeployClient, Args

async def main():
    client = DeployClient()
    args = Args(
        protocol="local",
        files_path="./src",
        dest_path="./dist",
        watch=True,
        ignore_patterns=["*.tmp", "*.log"]
    )
    await client.watch_mode(args)
``` 