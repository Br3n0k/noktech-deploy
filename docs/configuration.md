# Configuração

## Arquivo de Configuração Global

O arquivo de configuração principal está localizado em `~/.noktech-deploy/config.json`.

### Estrutura Básica

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy"
        }
    }
}
```

## Opções de Configuração

### Configurações Globais

| Opção | Tipo | Descrição | Padrão |
|-------|------|-----------|---------|
| default_protocol | string | Protocolo padrão | "ssh" |
| log_level | string | Nível de log | "info" |
| default_ignore_file | string | Arquivo de ignore padrão | "~/.deployignore" |
| log_file | string | Arquivo de log | "~/.noktech-deploy/deploy.log" |

### Configurações de Host

| Opção | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| protocol | string | Protocolo de deploy | Sim |
| host | string | Endereço do host | Sim* |
| user | string | Usuário | Sim* |
| password | string | Senha | Não |
| key_path | string | Caminho da chave SSH | Não |
| port | number | Porta | Não |
| dest_path | string | Caminho de destino | Sim |

*Não obrigatório para protocolo "local"

## Protocolos Suportados

### SSH/SFTP

```json
{
    "protocol": "ssh",
    "host": "exemplo.com",
    "user": "deploy",
    "key_path": "~/.ssh/id_rsa",
    "port": 22,
    "dest_path": "/var/www/app"
}
```

### FTP

```json
{
    "protocol": "ftp",
    "host": "ftp.exemplo.com",
    "user": "ftpuser",
    "password": "senha123",
    "dest_path": "/public_html"
}
```

### Local

```json
{
    "protocol": "local",
    "dest_path": "/mnt/backup"
}
```

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| NOKTECH_CONFIG | Caminho do arquivo de configuração |
| NOKTECH_LOG_LEVEL | Nível de log |
| NOKTECH_IGNORE_FILE | Arquivo de ignore |
| NOKTECH_SSH_KEY | Caminho da chave SSH |
| NOKTECH_PASSWORD | Senha para autenticação |

## Exemplos Completos

### Múltiplos Ambientes

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy",
            "key_path": "~/.ssh/id_rsa",
            "dest_path": "/var/www/app"
        },
        "staging": {
            "protocol": "ftp",
            "host": "staging.exemplo.com",
            "user": "ftpuser",
            "password": "senha123",
            "dest_path": "/public_html"
        },
        "backup": {
            "protocol": "local",
            "dest_path": "/mnt/backup"
        }
    }
}
```

### Configuração com Ignore Patterns

```json
{
    "default_protocol": "ssh",
    "default_ignore_file": "~/.deployignore",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy",
            "ignore_patterns": [
                "*.tmp",
                "*.log",
                "node_modules/"
            ]
        }
    }
}
```

## Resolução de Problemas

### Ordem de Precedência

1. Argumentos de linha de comando
2. Variáveis de ambiente
3. Arquivo de configuração do projeto
4. Arquivo de configuração global
5. Valores padrão

### Dicas

- Use variáveis de ambiente para informações sensíveis
- Mantenha senhas fora do controle de versão
- Use chaves SSH quando possível
- Configure níveis de log apropriados