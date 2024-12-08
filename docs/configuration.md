# Configuração

## Arquivo de Configuração

O NokTech Deploy usa um arquivo JSON para armazenar configurações em `~/.noktech-deploy/config.json`.

### Estrutura:

```json
{
    "default_protocol": "ssh",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy",
            "port": 22,
            "auth_type": "key",
            "key_path": "~/.ssh/deploy_key",
            "password": null
        },
        "staging": {
            "protocol": "ssh",
            "host": "staging.exemplo.com",
            "user": "deploy",
            "port": 22,
            "auth_type": "password",
            "password": "senha_segura",
            "key_path": null
        }
    }
}
```

## Variáveis de Ambiente

Para autenticação SSH, você pode usar:
- `NOKTECH_DEPLOY_SSH_KEY`: Caminho da chave SSH
- `NOKTECH_DEPLOY_PASSWORD`: Senha SSH (se não usar chave) 

# Diretório de Configuração

O NokTech Deploy armazena suas configurações e logs no diretório `~/.noktech-deploy/`.

## Localização por Sistema Operacional

### Linux/Mac
```bash
# Acessar diretório
cd ~/.noktech-deploy

# Listar conteúdo (incluindo arquivos ocultos)
ls -la ~/.noktech-deploy

# Estrutura
~/.noktech-deploy/
  ├── config.json     # Configurações
  └── logs/          # Logs diários
      └── noktech-deploy-2024-03-20.log
```

### Windows
```powershell
# CMD
cd %USERPROFILE%\.noktech-deploy

# PowerShell
cd $env:USERPROFILE\.noktech-deploy

# Localização típica
C:\Users\SeuUsuario\.noktech-deploy\
```

## Gerenciando Configurações

### Visualizar configuração atual
```bash
cat ~/.noktech-deploy/config.json
```

### Editar configuração
```bash
# Linux/Mac
nano ~/.noktech-deploy/config.json

# Windows
notepad %USERPROFILE%\.noktech-deploy\config.json
```

### Backup de configurações
```bash
# Linux/Mac
cp ~/.noktech-deploy/config.json ~/.noktech-deploy/config.backup.json

# Windows
copy %USERPROFILE%\.noktech-deploy\config.json %USERPROFILE%\.noktech-deploy\config.backup.json
```

## Logs

Os logs são armazenados em `~/.noktech-deploy/logs/` com rotação diária:

```bash
# Visualizar log atual
tail -f ~/.noktech-deploy/logs/noktech-deploy-$(date +%Y-%m-%d).log

# Listar todos os logs
ls -l ~/.noktech-deploy/logs/
```

## Permissões

### Linux/Mac
```bash
# Corrigir permissões
chmod 700 ~/.noktech-deploy
chmod 600 ~/.noktech-deploy/config.json
chmod 700 ~/.noktech-deploy/logs
```

### Windows
O diretório é criado com permissões padrão do usuário atual. 