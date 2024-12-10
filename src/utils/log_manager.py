from datetime import datetime, timedelta
from pathlib import Path
import os
from typing import Optional

from src.utils.logger import CustomLogger
from src.i18n import I18n
from src.core.constants import LOGS_DIR, VERSION_LOG_DIR


class LogManager:
    """Gerenciador de logs do sistema"""

    def __init__(self, retention_days: Optional[int] = 5):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.retention_days = retention_days
        self.log_dirs = [LOGS_DIR, VERSION_LOG_DIR]

    def cleanup_old_logs(self) -> None:
        """Remove logs mais antigos que o período de retenção"""
        self.logger.info(self.i18n.get("logs.cleanup_start"))
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        for log_dir in self.log_dirs:
            if not log_dir.exists():
                continue

            for log_file in log_dir.glob("*.log"):
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                    if file_time < cutoff_date:
                        log_file.unlink()
                        self.logger.debug(self.i18n.get("logs.file_removed").format(log_file))
                except Exception as e:
                    self.logger.error(self.i18n.get("logs.process_error").format(log_file, e))

        self.logger.info(self.i18n.get("logs.cleanup_complete"))

    def initialize(self) -> None:
        """Inicializa diretórios de log e limpa logs antigos"""
        for log_dir in self.log_dirs:
            log_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(self.i18n.get("logs.dir_create").format(log_dir))
        
        if self.retention_days > 0:
            self.logger.info(self.i18n.get("logs.retention_days").format(self.retention_days))
            self.cleanup_old_logs() 