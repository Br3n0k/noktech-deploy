import logging
from pathlib import Path
from datetime import datetime


class Logger:
    def __init__(self, name: str = "noktech-deploy"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self._setup_logger()

    def _setup_logger(self):
        # Configura log em arquivo
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"noktech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        
        # Configura log no console
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)
