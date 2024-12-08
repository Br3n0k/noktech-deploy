import os
import shutil
from pathlib import Path
from typing import Optional
from src.deployers.base_deployer import BaseDeployer
from src.core.file_manager import FileManager
from src.utils.logger import Logger

class LocalDeployer(BaseDeployer):
    def __init__(self, source_path: str, dest_path: str):
        super().__init__(host='localhost', user='local', password=None)
        self.source_path = source_path
        self.dest_path = dest_path
        
    async def connect(self) -> None:
        """Conecta ao sistema de arquivos local"""
        try:
            if not os.path.exists(self.dest_path):
                os.makedirs(self.dest_path)
        except Exception as e:
            raise ConnectionError(f"Erro ao acessar diretório local: {str(e)}")

    async def disconnect(self) -> None:
        """Desconecta do sistema de arquivos local"""
        # Limpa recursos se necessário
        pass

    def ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório local existe"""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                raise Exception(f"Erro ao criar diretório: {str(e)}")

    async def deploy_files(self, source_path: str, dest_path: str) -> None:
        """Deploy de arquivos localmente"""
        try:
            for root, _, files in os.walk(source_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, source_path)
                    remote_path = os.path.join(dest_path, relative_path)
                    
                    if self.ignore_rules and self.ignore_rules.should_ignore(relative_path):
                        continue
                        
                    await self._deploy_file(local_path, remote_path)
        except Exception as e:
            raise Exception(f"Erro no deploy local: {str(e)}")

    async def handle_change(self, path: str, event_type: str) -> None:
        try:
            relative_path = os.path.relpath(path, start=self.source_path)
            dest_path = os.path.join(self.dest_path, relative_path)
            
            if event_type in ('created', 'modified'):
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(path, dest_path)
            elif event_type == 'deleted' and os.path.exists(dest_path):
                os.remove(dest_path)
                self._cleanup_empty_dirs(os.path.dirname(dest_path))
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança em {path}: {str(e)}")

    def _cleanup_empty_dirs(self, directory: str) -> None:
        """Remove diretórios vazios recursivamente"""
        if directory == self.dest_path:
            return
            
        try:
            while directory != self.dest_path:
                if os.path.exists(directory) and not os.listdir(directory):
                    os.rmdir(directory)
                    directory = os.path.dirname(directory)
                else:
                    break
        except Exception as e:
            self.logger.error(f"Erro ao limpar diretórios: {str(e)}") 

    async def file_exists(self, remote_path: str) -> bool:
        return os.path.exists(remote_path)

    async def _deploy_file(self, local_path: str, remote_path: str):
        os.makedirs(os.path.dirname(remote_path), exist_ok=True)
        shutil.copy2(local_path, remote_path) 