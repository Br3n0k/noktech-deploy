# Uso

## Modo Interativo

```bash
noktech-deploy
```

## Deploy via SSH

```bash
noktech-deploy --protocol ssh \
               --host exemplo.com \
               --user deploy \
               --files-path ./dist \
               --dest-path /var/www/app
```

## Deploy Local

```bash
noktech-deploy --protocol local \
               --files-path ./dados \
               --dest-path /mnt/backup
```

## Modo Watch

```bash
noktech-deploy --watch \
               --protocol local \
               --files-path ./src \
               --dest-path ./dist
```

## Opções Disponíveis

- `--protocol`: Protocolo de deploy (ssh, ftp, local)
- `--host`: Host remoto
- `--user`: Usuário
- `--password`: Senha (não recomendado, use chave SSH)
- `--key-path`: Caminho da chave SSH
- `--files-path`: Diretório fonte
- `--dest-path`: Diretório destino
- `--watch`: Ativa modo de observação
- `--ignore`: Padrões de arquivos a ignorar 