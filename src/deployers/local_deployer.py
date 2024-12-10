"""
Implementação do deployer local
"""
from typing import Dict, List
import shutil
from pathlib import Path
import aiofiles  # type: ignore

from src.deployers.base_deployer import BaseDeployer
from src.deployers.sync_mixin import SyncMixin
from src.deployers.progress_mixin import ProgressMixin


class LocalDeployer(BaseDeployer, SyncMixin, ProgressMixin):
    """Implementação de deployer para deploy local"""

    def __init__(self, host_name: str, config: Dict) -> None:
        super().__init__(host_name, config)
        ProgressMixin.__init__(self)

    async def connect(self) -> None:
        """Não necessário para deploy local"""
        pass

    async def disconnect(self) -> None:
        """Não necessário para deploy local"""
        pass

    async def ensure_remote_dir(self, path: Path) -> None:
        """Garante existência de diretório local"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created directory: {path}")
        except Exception as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            raise

    async def deploy_directory(self, path: Path) -> None:
        """Deploy de diretório local"""
        # Lista todos os arquivos antes de iniciar
        files = [f for f in path.rglob("*") if f.is_file()]
        await self.prepare_transfer(files)
        
        for file in files:
            dest = Path(self.dest_path) / file.relative_to(path)
            await self.sync_file(file, dest)
        
        await self.complete_transfer()

    async def deploy_files(self, files: List[Path]) -> None:
        """Deploy de arquivos específicos local"""
        await self.prepare_transfer(files)
        
        for file in files:
            if file.is_file():
                dest = Path(self.dest_path) / file.relative_to(self.source_path)
                await self.sync_file(file, dest)
        
        await self.complete_transfer()

    async def sync_file(self, source: Path, dest: Path) -> None:
        """Sincroniza um arquivo localmente com progresso"""
        try:
            await self.ensure_remote_dir(dest.parent)
            
            # Implementa cópia com progresso
            total_size = source.stat().st_size
            bytes_transferred = 0
            
            async with aiofiles.open(source, 'rb') as src_file:
                async with aiofiles.open(dest, 'wb') as dst_file:
                    while chunk := await src_file.read(8192):
                        await dst_file.write(chunk)
                        bytes_transferred += len(chunk)
                        await self.update_progress(source, len(chunk))
            
            # Preserva metadados
            shutil.copystat(source, dest)
            
            self.logger.debug(f"Synced {source} -> {dest}")
        except Exception as e:
            self.logger.error(f"Failed to sync file {source}: {e}")
            raise

    def file_exists(self, path: Path) -> bool:
        """Verifica se arquivo existe"""
        return path.exists()

    def get_remote_mtime(self, path: Path) -> float:
        """Obtém timestamp de modificação"""
        return path.stat().st_mtime
