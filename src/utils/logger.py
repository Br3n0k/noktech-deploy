import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from src.core.constants import DEFAULT_LOG_DIR, LOG_FILE_FORMAT
from src.i18n import I18n

class Logger:
    _instances = {}
    _initialized = False
    _i18n = I18n()

    def __new__(cls, name: str):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(self, name: str):
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger(name)
            
            if not Logger._initialized:
                self._setup_logging()
                Logger._initialized = True

    def _setup_logging(self):
        """Configura o sistema de logging"""
        try:
            # Cria diretório de logs
            DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Nome do arquivo de log
            log_file = DEFAULT_LOG_DIR / LOG_FILE_FORMAT.format(
                datetime.now().strftime("%Y%m%d_%H%M%S"))
            
            # Configura formato
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Handler para arquivo
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            
            # Handler para console
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            
            # Configura root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)
            
        except Exception as e:
            print(self._i18n.get("app.error.fatal").format(
                f"Erro ao configurar logging: {str(e)}"))
            sys.exit(1)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)
