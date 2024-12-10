"""
Configuração interativa
"""
from typing import Dict, Optional
import inquirer  # type: ignore
from pathlib import Path

from src.i18n import I18n
from src.utils.logger import CustomLogger


class InteractiveConfig:
    """Classe para criar configuração interativamente"""

    def __init__(self):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()

    async def create_config(self) -> Optional[Dict]:
        """Cria configuração interativamente"""
        questions = [
            inquirer.Text("host", message=self.i18n.get("input.host")),
            inquirer.List(
                "protocol",
                message=self.i18n.get("protocol.select"),
                choices=["ssh", "ftp", "local"]
            ),
            inquirer.Text("user", message=self.i18n.get("input.user")),
            inquirer.Password("password", message=self.i18n.get("input.password")),
            inquirer.Path(
                "source",
                message=self.i18n.get("input.source_path"),
                path_type=inquirer.Path.DIRECTORY
            ),
            inquirer.Path(
                "dest",
                message=self.i18n.get("input.dest_path"),
                path_type=inquirer.Path.DIRECTORY
            ),
        ]

        answers = inquirer.prompt(questions)
        if not answers:
            self.logger.warning("Configuração interativa cancelada")
            return None

        self.logger.info("Configuração interativa criada com sucesso")
        return {
            "hosts": {
                answers["host"]: {
                    "enabled": True,
                    "protocol": answers["protocol"],
                    "host": answers["host"],
                    "user": answers["user"],
                    "password": answers["password"],
                    "source_path": str(Path(answers["source"])),
                    "dest_path": str(Path(answers["dest"])),
                }
            }
        }
