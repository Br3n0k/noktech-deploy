"""
Core do NokTech Deploy
"""

from .constants import (
    ROOT_DIR,
    CONFIG_DIR,
    LOGS_DIR,
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_TEMPLATE,
    DEFAULT_IGNORE_PATTERNS,
    SUPPORTED_PROTOCOLS,
    DEFAULT_PROTOCOL
)
from .file_manager import FileManager
from .ignore_rules import IgnoreRules
from .deploy_manager import DeployManager
from .watch_manager import WatchManager
from .watcher import FileWatcher
from .logger import Logger

__all__ = [
    # Classes principais
    "FileManager",
    "IgnoreRules",
    "DeployManager",
    "WatchManager",
    "DirectoryWatcher",
    "Logger",
    
    # Constantes importantes
    "ROOT_DIR",
    "CONFIG_DIR",
    "LOGS_DIR",
    "DEFAULT_CONFIG_FILE",
    "DEFAULT_CONFIG_TEMPLATE",
    "DEFAULT_IGNORE_PATTERNS",
    "SUPPORTED_PROTOCOLS",
    "DEFAULT_PROTOCOL"
]

__version__ = "0.1.0"
