"""
Constantes e configurações do NokTech Deploy
"""

from pathlib import Path
from typing import Dict, Any

# Informações do Projeto
PROJECT_NAME = "noktech-deploy"
PROJECT_VERSION = "0.1.2"
PROJECT_AUTHOR = "Brendown Ferreira"
PROJECT_EMAIL = "br3n0k@gmail.com"
PROJECT_DESCRIPTION = "Advanced deployment client with multiple protocol support"
PROJECT_COPYRIGHT = "Copyright 2024 NokTech"
PROJECT_REPOSITORY = "https://github.com/Br3n0k/noktech-deploy"

# Diretórios base
ROOT_DIR = Path.cwd()  # Diretório atual onde a aplicação está rodando
CONFIG_DIR = ROOT_DIR
LOGS_DIR = ROOT_DIR / "logs"
VERSION_LOG_DIR = LOGS_DIR / "version"  # Adicionado diretório específico para logs de versão
LANG_DIR = ROOT_DIR / "lang"

# Arquivos de configuração
DEFAULT_CONFIG_FILE = CONFIG_DIR / "config.json"

# Diretório de logs padrão
LOG_FILE_FORMAT = "deploy-%Y-%m.log"
LOG_FILE_ENCODING = "utf-8"
LOG_LEVEL = "INFO"
LOG_FORMAT = {
    "file": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "console": "%(levelname)s: %(message)s"
}

# Padrões de ignore padrão
DEFAULT_IGNORE_PATTERNS = [
    "*.pyc",
    "__pycache__",
    ".git",
    ".gitignore",
    ".env",
    "*.log",
    "*.tmp",
    "*.temp",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    "dist",
    "build",
    "*.egg-info",
    ".pytest_cache",
    ".coverage",
    ".DS_Store",
]

# Template de configuração padrão
DEFAULT_CONFIG_TEMPLATE = {
    "parallel_deploy": False,
    "ignore_patterns": DEFAULT_IGNORE_PATTERNS,
    "logs": {
        "retention_days": 5,  # Dias para manter os logs
        "enabled": True
    },
    "hosts": {
        "local": {
            "enabled": True,
            "protocol": "local",
            "source_path": "./src",
            "dest_path": "./deploy",
            "ignore_patterns": [],
            "watch": {
                "enabled": False,
                "interval": 1.0
            }
        },
        "example_ssh": {
            "enabled": False,
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "port": 22,
            "key_path": "~/.ssh/id_rsa",
            "source_path": "./",
            "dest_path": "/var/www/app",
            "ignore_patterns": [],
            "watch": {
                "enabled": False,
                "interval": 1.0
            }
        },
        "example_ftp": {
            "enabled": False,
            "protocol": "ftp",
            "host": "ftp.example.com",
            "user": "ftpuser",
            "password": "",
            "port": 21,
            "source_path": "./dist",
            "dest_path": "/public_html",
            "ignore_patterns": [],
            "watch": {
                "enabled": False,
                "interval": 1.0
            }
        },
    },
}

# Configurações de Deploy
DEPLOY_PARALLEL = False
DEPLOY_RETRY_ATTEMPTS = 3
DEPLOY_RETRY_DELAY = 5.0

# Timeouts (em segundos)
CONNECTION_TIMEOUT = 30
TRANSFER_TIMEOUT = 300
WATCH_INTERVAL = 1.0

# Protocolos Suportados
SUPPORTED_PROTOCOLS: Dict[str, Any] = {
    "ssh": "SSHDeployer",
    "ftp": "FTPDeployer",
    "local": "LocalDeployer"
}
DEFAULT_PROTOCOL = "local"
