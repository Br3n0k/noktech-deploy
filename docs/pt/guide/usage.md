# Uso

## Comandos Básicos

### Modo Interativo
```bash
noktech-deploy
```

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

### Modo Watch
```bash
noktech-deploy --watch \
               --protocol local \
               --files-path ./src \
               --dest-path ./dist
```

## Opções de Comando

- `--protocol`: Protocolo de deploy (ssh, local)
- `--host`: Host remoto
- `--user`: Usuário
- `--password`: Senha (não recomendado, use chave SSH)
- `--key-path`: Caminho da chave SSH
- `--files-path`: Diretório fonte
- `--dest-path`: Diretório destino
- `--watch`: Ativa modo de observação
- `--ignore`: Padrões de arquivos a ignorar
- `--log-level`: Nível de log (debug, info, warning, error)
- `--config`: Caminho personalizado do arquivo de configuração

## Exemplos

### Deploy com Chave SSH
```bash
noktech-deploy --protocol ssh \
               --host prod.exemplo.com \
               --user deploy \
               --key-path ~/.ssh/deploy_key \
               --files-path ./build \
               --dest-path /var/www/prod
```

### Modo Watch com Ignore Personalizado
```bash
noktech-deploy --watch \
               --protocol local \
               --files-path ./src \
               --dest-path ./dist \
               --ignore "*.tmp,*.cache"
``` 