#!/usr/bin/env python
import webbrowser
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from src.utils.logger import CustomLogger
from src.i18n import I18n
from src.core.constants import (
    PROJECT_VERSION,
    PROJECT_REPOSITORY,
    VERSION_CHECK_TIMEOUT,
    VERSION_LOG_FORMAT,
    VERSION_LOG_DIR,
)


class VersionChecker:
    """Verifica atualizações de versão"""

    def __init__(self) -> None:
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.log_dir = VERSION_LOG_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.repo_url = PROJECT_REPOSITORY

    async def check_for_updates(self) -> Optional[str]:
        """Verifica se há atualizações disponíveis"""
        self.logger.info(self.i18n.get("version.check_start"))
        local = PROJECT_VERSION
        remote = self.get_remote_version()

        if remote and remote != local:
            self.logger.warning(self.i18n.get("version.new_available").format(remote, local))
            self.log_version_mismatch(local, remote)
            self.open_releases_page()
            self.logger.info(self.i18n.get("version.update_required"))
            sys.exit(1)
        return None

    def get_remote_version(self) -> Optional[str]:
        """Obtém versão remota do repositório"""
        try:
            response = requests.get(
                f"{self.repo_url}/raw/main/src/core/constants.py",
                timeout=VERSION_CHECK_TIMEOUT
            )
            if response.status_code != 200:
                return None

            for line in response.text.split("\n"):
                if line.startswith("PROJECT_VERSION"):
                    return line.split('"')[1]
            return None
        except Exception as e:
            self.logger.error(self.i18n.get("version.check_error").format(e))
            return None

    def log_version_mismatch(self, local: str, remote: str):
        """Registra diferença de versão no log"""
        log_file = self.log_dir / datetime.now().strftime(VERSION_LOG_FORMAT)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
                f"Version mismatch - Local: {local}, Remote: {remote}\n"
            )

    def open_releases_page(self):
        """Abre a página de releases no navegador"""
        releases_url = f"{self.repo_url}/releases"
        try:
            self.logger.info(self.i18n.get("version.browser_open"))
            webbrowser.open(releases_url)
        except Exception as e:
            self.logger.error(self.i18n.get("version.browser_error").format(releases_url))
