import logging
from typing import Optional

class Logger:
    def __init__(self, name: str = 'noktech-deploy'):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self._setup_logger()
            
    def _setup_logger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def info(self, message: str):
        self.logger.info(message)
        
    def error(self, message: str):
        self.logger.error(message)
        
    def debug(self, message: str):
        self.logger.debug(message)
        
    def warning(self, message: str):
        self.logger.warning(message) 