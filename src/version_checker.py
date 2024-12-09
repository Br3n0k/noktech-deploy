#!/usr/bin/env python
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
from .i18n import I18n
import webbrowser


class VersionChecker:
    def __init__(self):
        self.i18n = I18n()
        self.log_dir = Path(".noktech-deploy/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.repo_url = "https://github.com/Br3n0k/noktech-deploy"

    def get_local_version(self) -> str:
        """Obtém versão local do arquivo version.py"""
        from .version import __version__

        return __version__

    def get_remote_version(self) -> Optional[str]:
        """Obtém versão do repositório remoto"""
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/Br3n0k/noktech-deploy/main/src/version.py"
            )

            if response.status_code != 200:
                return None

            for line in response.text.split("\n"):
                if line.startswith("__version__"):
                    return line.split('"')[1]
            return None

        except Exception:
            return None

    def log_version_mismatch(self, local: str, remote: str):
        """Registra diferença de versão no log"""
        log_file = self.log_dir / f"version-{datetime.now():%Y-%m}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
                f"Version mismatch - Local: {local}, Remote: {remote}\n"
            )

    def check(self) -> bool:
        """Verifica se versão local está atualizada"""
        print(self.i18n.get("version.checking"))

        local_version = self.get_local_version()
        remote_version = self.get_remote_version()

        if not remote_version:
            print(self.i18n.get("version.error.fetch"))
            return True  # Continua execução em caso de erro

        if local_version != remote_version:
            print(
                self.i18n.get("version.mismatch").format(local_version, remote_version)
            )
            self.log_version_mismatch(local_version, remote_version)
            return False

        return True

    def open_releases_page(self):
        """Abre a página de releases no navegador"""
        releases_url = f"{self.repo_url}/releases"
        try:
            webbrowser.open(releases_url)
        except Exception as e:
            print(self.i18n.get("version.error.browser").format(str(e)))
