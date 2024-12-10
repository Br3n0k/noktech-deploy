"""
Constantes e configurações do NokTech Deploy
"""

from pathlib import Path

# Diretórios base
ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
CONFIG_DIR = ROOT_DIR / ".noktech-deploy"
LOGS_DIR = CONFIG_DIR / "logs"

# Diretório de logs padrão
DEFAULT_LOG_DIR = LOGS_DIR
LOG_FILE_FORMAT = "deploy-%Y-%m.log"

# Arquivos de configuração
DEFAULT_CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_FILE = DEFAULT_CONFIG_FILE  # Para compatibilidade
VERSION_FILE = CONFIG_DIR / "version.txt"

# Template de configuração padrão
DEFAULT_CONFIG_TEMPLATE = {
    "parallel_deploy": False,
    "ignore_patterns": [
        "*.pyc",
        "__pycache__",
        ".git",
        ".env",
        "*.log",
        "node_modules",
        "venv",
        ".venv"
    ],
    "hosts": {
        "example_ssh": {
            "enabled": False,
            "protocol": "ssh",
            "host": "example.com",
            "user": "deploy",
            "port": 22,
            "key_path": "~/.ssh/id_rsa",
            "source_path": "./",
            "dest_path": "/var/www/app",
            "ignore_patterns": []
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
            "ignore_patterns": []
        },
        "example_local": {
            "enabled": False,
            "protocol": "local",
            "source_path": "./src",
            "dest_path": "./deploy",
            "ignore_patterns": []
        }
    }
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
    "htmlcov",
    ".DS_Store"
]

# Configurações padrão
DEFAULT_CONFIG = {
    "parallel_deploy": False,
    "ignore_patterns": DEFAULT_IGNORE_PATTERNS,
    "hosts": {}
}

# Portas padrão
DEFAULT_PORTS = {
    "ssh": 22,
    "ftp": 21
}

# Timeouts (em segundos)
CONNECTION_TIMEOUT = 30
TRANSFER_TIMEOUT = 300
WATCH_INTERVAL = 1.0

# Versão mínima suportada
MIN_PYTHON_VERSION = (3, 7, 0)
