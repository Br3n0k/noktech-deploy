# Configuração

## Arquivo de Configuração

O arquivo de configuração fica em `~/.noktech-deploy/config.json` e segue esta estrutura:

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "log_dir": "~/.noktech-deploy/logs",
    "watch_delay": 1000,
    "hosts": {
        "local": {
            "protocol": "local",
            "dest_path": "./deploy",
            "ignore_file": ".deployignore",
            "backup": {
                "enabled": true,
                "max_backups": 5,
                "path": "./backups"
            },
            "hooks": {
                "pre_deploy": "",
                "post_deploy": ""
            },
            "retry": {
                "attempts": 3,
                "delay": 5
            }
        }
    },
    "ignore_patterns": [
        "*.pyc",
        "__pycache__/",
        "*.log",
        ".git/"
    ]
}
```

## Opções

- `default_protocol`: Protocolo padrão de deploy (ssh, local)
- `log_level`: Nível de log (debug, info, warning, error)
- `log_dir`: Diretório para arquivos de log
- `watch_delay`: Atraso entre verificações de arquivos no modo watch (milissegundos)
- `hosts`: Configuração para diferentes destinos de deploy
- `ignore_patterns`: Padrões globais para ignorar durante o deploy

## Regras de Ignore

Crie um arquivo `.deployignore` na raiz do projeto para especificar arquivos a ignorar:

```text
# Arquivos de desenvolvimento
__pycache__/
*.pyc
.git/

# Arquivos temporários
*.log
*.tmp
``` 