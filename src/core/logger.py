import logging
from datetime import datetime
from pathlib import Path
from src.core.constants import (
    LOGS_DIR,
    LOG_FILE_FORMAT,
    LOG_FILE_ENCODING,
    LOG_LEVEL,
    LOG_FORMAT
)


class Logger:
    """Logger base do sistema"""
    
    def __init__(self, name: str = "noktech-deploy") -> None:
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self._setup_logger()

    def _setup_logger(self) -> None:
        """Configura handlers e formatters do logger"""
        # Garante que o diretório de logs existe
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Configura log em arquivo
        log_file = LOGS_DIR / datetime.now().strftime(LOG_FILE_FORMAT)
        file_handler = logging.FileHandler(log_file, encoding=LOG_FILE_ENCODING)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT["file"]))

        # Configura log no console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT["console"]))

        # Configura o logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    @classmethod
    def get_logger(cls, name: str) -> "Logger":
        """Retorna uma instância do logger"""
        return cls(name)
