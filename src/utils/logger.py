"""
Logger customizado
"""
import logging
from logging import Logger, getLogger, FileHandler, Formatter
from datetime import datetime
from pathlib import Path

from src.core.constants import (
    LOGS_DIR,
    LOG_FILE_FORMAT,
    LOG_LEVEL,
    LOG_FORMAT,
    VERSION_LOG_DIR
)
from src.i18n import I18n


class CustomLogger(Logger):
    """Logger customizado com métodos adicionais"""

    @classmethod
    def get_logger(cls, name: str) -> "CustomLogger":
        """Retorna uma instância do logger"""
        logger = getLogger(name)
        if not isinstance(logger, cls):
            logger = cls(name)
        return logger

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.i18n = I18n()
        self.setup_logger()

    def setup_logger(self) -> None:
        """Configura o logger com handlers e formatters"""
        self.setLevel(LOG_LEVEL)

        # Garante que o diretório de logs existe
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOGS_DIR / datetime.now().strftime(LOG_FILE_FORMAT)

        # Configura handler de arquivo
        file_handler = FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(Formatter(LOG_FORMAT["file"]))
        self.addHandler(file_handler)

        # Configura handler de console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter(LOG_FORMAT["console"]))
        self.addHandler(console_handler)

        # Log de inicialização
        self.info(self.i18n.get("logger.initialized").format(log_file))

    def log_version_info(self) -> None:
        """Loga informações de versão"""
        version_log_file = VERSION_LOG_DIR / datetime.now().strftime(LOG_FILE_FORMAT)
        version_log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(version_log_file, "a", encoding="utf-8") as f:
            f.write(self.i18n.get("logger.version_info").format(datetime.now()))

    def log_error(self, message: str) -> None:
        """Loga uma mensagem de erro"""
        self.error(self.i18n.get("logger.error").format(message))

    def log_warning(self, message: str) -> None:
        """Loga uma mensagem de aviso"""
        self.warning(self.i18n.get("logger.warning").format(message))

    def log_info(self, message: str) -> None:
        """Loga uma mensagem de informação"""
        self.info(self.i18n.get("logger.info").format(message))
