# Guia de Início Rápido

## Instalação

```bash
pip install noktech-deploy
```

## Uso Básico

### Modo Interativo

A maneira mais fácil de começar é usar o modo interativo:

```bash
noktech-deploy
```

O programa irá guiá-lo através das opções necessárias.

### Deploy via SSH

```bash
noktech-deploy --protocol ssh \
               --host exemplo.com \
               --user deploy \
               --files-path ./dist \
               --dest-path /var/www/app
```

### Deploy Local

```bash
noktech-deploy --protocol local \
               --files-path ./dados \
               --dest-path /mnt/backup
```

## Configuração Básica

### Arquivo .deployignore

Crie um arquivo `.deployignore` na raiz do seu projeto:

```plaintext
# Ignorar arquivos de desenvolvimento
__pycache__/
*.pyc
venv/
node_modules/

# Ignorar arquivos temporários
*.tmp
*.log
```

### Configuração Global

Crie um arquivo `config.json` em `~/.noktech-deploy/`:

```json
{
    "default_protocol": "ssh",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy",
            "dest_path": "/var/www/app"
        },
        "staging": {
            "protocol": "ftp",
            "host": "staging.exemplo.com",
            "user": "ftpuser",
            "dest_path": "/public_html"
        }
    }
}
```

## Próximos Passos

- Leia sobre [Configuração Avançada](configuration.md)
- Aprenda sobre o [Sistema de Ignore](ignore_rules.md)
- Explore a [API de Referência](api.md) 