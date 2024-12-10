"""
Implementação do deployer SSH/SFTP
"""
from typing import List, Optional
from pathlib import Path
import asyncssh  # type: ignore

from src.deployers.base_deployer import BaseDeployer
from src.deployers.sync_mixin import SyncMixin
from src.deployers.progress_mixin import ProgressMixin
from src.core.constants import CONNECTION_TIMEOUT


class SSHDeployer(BaseDeployer, SyncMixin, ProgressMixin):
    """Implementação de deployer via SSH"""

    def __init__(self, host_name: str, config: dict) -> None:
        super().__init__(host_name, config)
        ProgressMixin.__init__(self)
        self.host = config["host"]
        self.user = config["user"]
        self.password = config.get("password")
        self.key_path = config.get("key_path")
        self.port = config.get("port", 22)
        self.conn: Optional[asyncssh.SSHClientConnection] = None

    async def connect(self) -> None:
        """Estabelece conexão SSH"""
        try:
            if self.key_path:
                self.conn = await asyncssh.connect(
                    self.host,
                    username=self.user,
                    client_keys=[self.key_path],
                    port=self.port,
                    timeout=CONNECTION_TIMEOUT
                )
            else:
                self.conn = await asyncssh.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                    port=self.port,
                    timeout=CONNECTION_TIMEOUT
                )
            self.logger.info(f"Connected to {self.host} via SSH")
        except Exception as e:
            self.logger.error(f"SSH connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Encerra conexão SSH"""
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()
            self.logger.info(f"Disconnected from {self.host}")

    async def ensure_remote_dir(self, path: Path) -> None:
        """Garante que o diretório remoto existe"""
        if not self.conn:
            raise RuntimeError("SSH connection not established")
        await self.conn.run(f'mkdir -p "{path}"')

    async def deploy_directory(self, path: Path) -> None:
        """Deploy de diretório via SSH"""
        try:
            await self.connect()
            if self.conn:
                # Lista todos os arquivos antes de iniciar
                files = [f for f in path.rglob("*") if f.is_file()]
                await self.prepare_transfer(files)
                
                async with self.conn.start_sftp_client() as sftp:
                    for file in files:
                        dest = Path(self.dest_path) / file.relative_to(path)
                        await self.sync_file(file, dest)
                
                await self.complete_transfer()
        finally:
            await self.disconnect()

    async def deploy_files(self, files: List[Path]) -> None:
        """Deploy de arquivos específicos via SSH"""
        try:
            await self.connect()
            if self.conn:
                await self.prepare_transfer(files)
                
                async with self.conn.start_sftp_client() as sftp:
                    for file in files:
                        if file.is_file():
                            dest = Path(self.dest_path) / file.relative_to(self.source_path)
                            await self.sync_file(file, dest)
                
                await self.complete_transfer()
        finally:
            await self.disconnect()

    async def sync_file(self, source: Path, dest: Path) -> None:
        """Sincroniza um arquivo via SSH com progresso"""
        if not self.conn:
            raise RuntimeError("SSH connection not established")
        
        try:
            await self.ensure_remote_dir(dest.parent)
            
            # Implementa transferência com progresso
            async with self.conn.start_sftp_client() as sftp:
                # Cria callback para progresso
                async def progress_callback(bytes_transferred: int, _: int) -> None:
                    await self.update_progress(source, bytes_transferred)
                
                # Inicia transferência com callback
                await sftp.put(
                    str(source),
                    str(dest),
                    progress_handler=progress_callback
                )
                
            self.logger.debug(f"Synced {source} -> {dest}")
        except Exception as e:
            self.logger.error(f"Failed to sync file {source}: {e}")
            raise
