import logging
from typing import Optional
import sys
import os
from datetime import datetime

class Logger:
    def __init__(self, 
                 name: str = 'noktech-deploy',
                 log_file: Optional[str] = None,
                 level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove handlers existentes
        self.logger.handlers.clear()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler (opcional)
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def debug(self, message: str):
        self.logger.debug(message)

    @staticmethod
    def get_default_log_file() -> str:
        """Retorna o caminho padrão para o arquivo de log"""
        log_dir = os.path.expanduser('~/.noktech-deploy/logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        date_str = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(log_dir, f'noktech-deploy-{date_str}.log') 