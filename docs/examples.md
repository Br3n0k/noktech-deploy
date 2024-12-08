# Exemplos de Uso

## Deploy Básico

### SSH com Chave
```bash
noktech-deploy --protocol ssh \
    --host prod.exemplo.com \
    --user deploy \
    --key-path ~/.ssh/deploy_key \
    --files-path ./dist \
    --dest-path /var/www/app
```

### FTP com Senha
```bash
noktech-deploy --protocol ftp \
    --host ftp.exemplo.com \
    --user ftpuser \
    --password "senha123" \
    --files-path ./public \
    --dest-path /public_html
```

## Casos de Uso Avançados

### Deploy com Observação e Ignore
```bash
noktech-deploy --protocol ssh \
    --host dev.exemplo.com \
    --user deploy \
    --files-path ./src \
    --dest-path /var/www/dev \
    --watch \
    --ignore-file .deployignore \
    --ignore-patterns "*.log" "tmp/*"
```

### Deploy Local com Backup
```bash
# Primeiro, backup
noktech-deploy --protocol local \
    --files-path /var/www/app \
    --dest-path /mnt/backup/app-$(date +%Y%m%d)

# Depois, deploy
noktech-deploy --protocol ssh \
    --host prod.exemplo.com \
    --files-path ./dist \
    --dest-path /var/www/app
```

### Deploy Multi-estágio
```bash
#!/bin/bash

# Build
npm run build

# Deploy para staging
noktech-deploy --profile staging \
    --files-path ./dist \
    --dest-path /var/www/staging

# Testes em staging
if curl -s https://staging.exemplo.com/health | grep -q "ok"; then
    # Deploy para produção
    noktech-deploy --profile production \
        --files-path ./dist \
        --dest-path /var/www/production
fi
``` 