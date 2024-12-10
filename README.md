# NokTech Deploy

---

![NokTech Deploy Logo](src/assets/logo.webp)

## Cliente de deploy avançado com suporte a múltiplos protocolos

![Version](https://img.shields.io/badge/version-0.1.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8.1+-yellow.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

## 📋 Índice

- [✨ Características](#-características)
- [🚀 Instalação](#-instalação)
- [💻 Uso](#-uso)
- [⚙️ Configuração](#️-configuração)
- [🛠️ Desenvolvimento](#️-desenvolvimento)
- [📊 Testes](#-testes)
- [📝 Logs](#-logs)
- [📦 Build](#-build)
- [📖 Documentação](#-documentação)
- [📄 Licença](#-licença)

## ✨ Características

- **Múltiplos Protocolos**
  - SSH/SFTP (senha ou chave SSH)
  - FTP
  - Local (cópia local/rede)
- **Monitoramento em Tempo Real**
- **Sistema de Ignore Avançado**
- **Interface Interativa**
- **Sistema de Logs Completo**
- **Verificação Automática de Versão**
  - Comparação com versão remota
  - Logs de divergência de versão
  - Alerta de versão desatualizada
- **Suporte Multi-plataforma**
  - Windows
  - Linux
  - MacOS

## 🚀 Instalação

```bash
# Via pip
pip install noktech-deploy

# Via Poetry
poetry add noktech-deploy

# Build do fonte
git clone https://github.com/Br3n0k/noktech-deploy
cd noktech-deploy
poetry install
python build_config.py build
```

## 💻 Uso

### Comandos Básicos

```bash
# Modo Interativo
noktech-deploy

# Deploy SSH
noktech-deploy --protocol ssh --host exemplo.com --user deploy

# Deploy FTP
noktech-deploy --protocol ftp --host ftp.exemplo.com --user ftpuser

# Deploy Local
noktech-deploy --protocol local --files-path ./dados --dest-path /backup
```

### Comandos Avançados

```bash
# Watch Mode
noktech-deploy --watch --files-path ./src

# Ignore Customizado
noktech-deploy --ignore-file ./custom.ignore

# Log Personalizado
noktech-deploy --log-dir ./logs --log-level debug

# Configuração Alternativa
noktech-deploy --config-file ./deploy.json
```

## ⚙️ Configuração

### Estrutura de Diretórios

```plaintext
.noktech-deploy/
├── config/           # Configurações do sistema
│   └── config.json   # Configuração principal
├── logs/            # Logs do sistema
│   ├── deploy-YYYY-MM.log
│   └─── version-YYYY-MM.log
└── .deployignore    # Regras de ignore
```

### Arquivo config.json para configuração principal

```json
{
    "default_protocol": "ssh",
    "log_level": "info",
    "log_dir": ".noktech-deploy/logs",
    "watch_delay": 1000,
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "port": 22,
            "user": "deploy",
            "password": "senha_segura",
            "key_path": null,
            "dest_path": "/var/www/app",
            "timeout": 30,
            "keep_alive": true,
            "compression": true,
            "ignore_file": ".deployignore",
            "backup": {
                "enabled": true,
                "max_backups": 5,
                "path": "/var/backups/app"
            },
            "hooks": {
                "pre_deploy": "echo 'Iniciando deploy'",
                "post_deploy": "echo 'Deploy finalizado'"
            },
            "retry": {
                "attempts": 3,
                "delay": 5
            }
        },
        "staging": {
            "protocol": "ssh",
            "host": "staging.exemplo.com",
            "port": 22,
            "user": "deploy",
            "password": "senha_staging",
            "dest_path": "/var/www/staging"
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

### Arquivo .deployignore para ignorar arquivos específicos no deploy

```plaintext
__pycache__/
.env
node_modules/
.DS_Store
.gitignore
.git/
.noktech-deploy/
```

## 🛠️ Desenvolvimento

```bash
# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell

# Executar linting
poetry run ruff check .
poetry run black .

# Atualizar versão
poetry run python scripts/update_version.py <version>
```

## 📊 Testes

```bash
# Executar todos os testes
poetry run pytest

# Testes com cobertura
poetry run pytest --cov=src

# Testes específicos
poetry run pytest tests/test_deployers.py -v

# Relatório HTML de cobertura
poetry run pytest --cov=src --cov-report=html
```

## 📝 Logs

```bash
# Visualizar logs de deploy
cat .noktech-deploy/logs/deploy-$(date +%Y-%m).log

# Visualizar logs de versão
cat .noktech-deploy/logs/version-$(date +%Y-%m).log

# Listar todos os logs
ls -l .noktech-deploy/logs/

# Limpar logs antigos (mantém últimos 30 dias)
noktech-deploy --clean-logs

# Verificar versão atual
noktech-deploy --version
```

## 📦 Build

```bash
# Build completo
poetry run python -m build

# Apenas limpeza
poetry run python -m build clean

# Build do pacote
poetry build

# Instalar localmente
pip install dist/noktech_deploy-*.whl
```

## 📖 Documentação

- [Guia de Início Rápido](docs/quickstart.md)
- [Configuração Avançada](docs/configuration.md)
- [Sistema de Ignore](docs/ignore_rules.md)
- [API de Referência](docs/api.md)
- [Changelog](CHANGELOG.md)

### Verificação de Versão

O NokTech Deploy verifica automaticamente se sua versão local está atualizada em relação à versão remota no repositório oficial. Quando uma divergência é detectada:

1. Uma mensagem de alerta é exibida
2. A divergência é registrada no arquivo de log
3. O usuário é notificado para atualizar

Os logs de versão são armazenados em:

```plaintext
.noktech-deploy/logs/version-YYYY-MM.log
```

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Brendown Ferreira

- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: [br3n0k@gmail.com](mailto:br3n0k@gmail.com)
