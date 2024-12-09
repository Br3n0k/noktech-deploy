"""
Constantes e configurações do NokTech Deploy
"""

import os
from pathlib import Path

# Diretórios base
PROJECT_ROOT = Path(os.getcwd())
CONFIG_DIR = PROJECT_ROOT / ".noktech-deploy"
DEFAULT_CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_LOG_DIR = CONFIG_DIR / "logs"
DEFAULT_IGNORE_FILE = PROJECT_ROOT / ".deployignore"

# Templates de arquivos
DEFAULT_CONFIG_TEMPLATE = {
    "default_protocol": "local",
    "hosts": {"local": {"protocol": "local", "dest_path": "./deploy"}},
    "ignore_patterns": ["*.pyc", "__pycache__/", "*.log", ".git/", "node_modules/"],
}

DEFAULT_IGNORE_TEMPLATE = """# Arquivos de desenvolvimento
__pycache__/
*.pyc
.git/
.vscode/
.idea/
node_modules/

# Arquivos temporários
*.log
*.tmp
.DS_Store

# Arquivos de configuração local
.env
*.local.json
"""

# Configurações de log
LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_FORMAT = "deploy-%Y-%m.log"
