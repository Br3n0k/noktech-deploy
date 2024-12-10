from typing import Dict, List, Optional
from pathlib import Path
import aioftp  # type: ignore
from src.deployers.base_deployer import BaseDeployer
from src.deployers.sync_mixin import SyncMixin
from src.deployers.progress_mixin import ProgressMixin
from src.core.constants import CONNECTION_TIMEOUT, TRANSFER_TIMEOUT


class FTPDeployer(BaseDeployer, SyncMixin, ProgressMixin):
    """Implementação de deployer via FTP"""

    def __init__(self, host_name: str, config: Dict) -> None:
        super().__init__(host_name, config)
        ProgressMixin.__init__(self)
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.port = config.get("port", 21)
        self.client: Optional[aioftp.Client] = None

    async def connect(self) -> None:
        """Estabelece conexão FTP"""
        try:
            self.client = await aioftp.Client.context(
                self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                timeout=CONNECTION_TIMEOUT
            )
            self.logger.info(f"Connected to {self.host} via FTP")
        except Exception as e:
            self.logger.error(f"FTP connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Encerra conexão FTP"""
        if self.client:
            await self.client.quit()
            self.client = None
            self.logger.debug("FTP connection closed")

    async def ensure_remote_dir(self, path: Path) -> None:
        """Garante existência de diretório remoto"""
        if not self.client:
            raise RuntimeError("FTP connection not established")
        try:
            await self.client.make_directory(str(path), parents=True)
            self.logger.debug(f"Created remote directory: {path}")
        except Exception as e:
            self.logger.error(f"Failed to create remote directory {path}: {e}")
            raise

    async def deploy_directory(self, path: Path) -> None:
        """Deploy de diretório via FTP"""
        try:
            await self.connect()
            if self.client:
                # Lista todos os arquivos antes de iniciar
                files = [f for f in path.rglob("*") if f.is_file()]
                await self.prepare_transfer(files)
                
                for file in files:
                    dest = Path(self.dest_path) / file.relative_to(path)
                    await self.sync_file(file, dest)
                
                await self.complete_transfer()
        finally:
            await self.disconnect()

    async def deploy_files(self, files: List[Path]) -> None:
        """Deploy de arquivos específicos via FTP"""
        try:
            await self.connect()
            if self.client:
                await self.prepare_transfer(files)
                
                for file in files:
                    if file.is_file():
                        dest = Path(self.dest_path) / file.relative_to(self.source_path)
                        await self.sync_file(file, dest)
                
                await self.complete_transfer()
        finally:
            await self.disconnect()

    async def sync_file(self, source: Path, dest: Path) -> None:
        """Sincroniza um arquivo via FTP com progresso"""
        if not self.client:
            raise RuntimeError("FTP connection not established")
        
        try:
            await self.ensure_remote_dir(dest.parent)
            
            # Implementa transferência com progresso
            total_size = source.stat().st_size
            bytes_transferred = 0
            
            async with source.open('rb') as local_file:
                stream = await self.client.upload_stream(str(dest))
                
                while chunk := await local_file.read(8192):
                    await stream.write(chunk)
                    bytes_transferred += len(chunk)
                    await self.update_progress(source, len(chunk))
                
                await stream.finish()
            
            self.logger.debug(f"Synced {source} -> {dest}")
        except Exception as e:
            self.logger.error(f"Failed to sync file {source}: {e}")
            raise
