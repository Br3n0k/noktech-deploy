import os
from datetime import datetime
from pathlib import Path


class Logger:
    def __init__(self, log_file: str = None, log_level: str = "INFO"):
        self.log_file = log_file or self.get_default_log_file()
        self.log_level = log_level.upper()
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    @staticmethod
    def get_default_log_file() -> str:
        """Retorna o caminho padrão do arquivo de log"""
        log_dir = Path.home() / ".noktech-deploy" / "logs"
        return str(log_dir / f"deploy-{datetime.now():%Y-%m}.log")

    def should_log(self, level: str) -> bool:
        """Verifica se o nível deve ser logado"""
        levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        return levels.get(level.upper(), 0) >= levels.get(self.log_level, 0)

    def log(self, message: str, level: str = "INFO"):
        """Registra mensagem no log se nível permitir"""
        if not self.should_log(level):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def info(self, message: str):
        self.log(message, "INFO")

    def error(self, message: str):
        self.log(message, "ERROR")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def debug(self, message: str):
        self.log(message, "DEBUG")
