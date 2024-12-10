import os
import aioftp
from pathlib import Path
from .base_deployer import BaseDeployer


class FTPDeployer(BaseDeployer):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = None

    async def connect(self) -> None:
        """Estabelece conexão FTP"""
        try:
            self.client = aioftp.Client()
            await self.client.connect(
                self.config["host"],
                port=self.config.get("port", 21)
            )
            await self.client.login(
                self.config["user"],
                self.config.get("password", "")
            )
        except Exception as e:
            raise ConnectionError(f"Falha na conexão FTP: {str(e)}")

    async def disconnect(self) -> None:
        """Fecha conexão FTP"""
        if hasattr(self, 'client'):
            await self.client.quit()

    async def upload_file(self, source: Path, dest: str) -> None:
        """Upload de arquivo via FTP"""
        try:
            await self._ensure_remote_dir(str(Path(dest).parent))
            await self.client.upload(str(source), dest)
        except Exception as e:
            self.logger.error(f"Erro no upload do arquivo {source}: {str(e)}")
            raise

    async def _ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório remoto existe"""
        try:
            await self.client.make_directory(path, parents=True)
        except Exception:
            pass  # Diretório já existe
