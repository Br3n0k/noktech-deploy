import os
import shutil
from pathlib import Path
from typing import Optional
from src.deployers.base_deployer import BaseDeployer
from src.core.file_manager import FileManager
from src.utils.logger import Logger

class LocalDeployer(BaseDeployer):
    def __init__(self, dest_base: str, logger: Optional[Logger] = None):
        super().__init__(host='local', user='', password='', port=0)
        self.dest_base = os.path.abspath(dest_base)
        self.file_manager = FileManager(base_path=dest_base)
        self.logger = logger or Logger()
        
    def connect(self) -> None:
        """Verifica se o diretório de destino é acessível"""
        if not os.path.exists(self.dest_base):
            try:
                os.makedirs(self.dest_base)
            except Exception as e:
                raise ConnectionError(f"Não foi possível criar o diretório de destino: {str(e)}")
                
        if not os.access(self.dest_base, os.W_OK):
            raise ConnectionError("Sem permissão de escrita no diretório de destino")

    def disconnect(self) -> None:
        """Não necessário para deploy local"""
        pass

    def ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório local existe"""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                raise Exception(f"Erro ao criar diretório: {str(e)}")

    def deploy_files(self, files_path: str, dest_path: str) -> None:
        """Copia arquivos localmente"""
        try:
            files_to_deploy = self.file_manager.collect_files(files_path)
            
            for local_path, relative_path in files_to_deploy:
                dest_file = os.path.join(dest_path, relative_path)
                dest_dir = os.path.dirname(dest_file)
                
                self.ensure_remote_dir(dest_dir)
                
                try:
                    shutil.copy2(local_path, dest_file)
                    self.logger.info(f"Arquivo copiado: {relative_path}")
                except Exception as e:
                    self.logger.error(f"Erro ao copiar {relative_path}: {str(e)}")
                    
        except Exception as e:
            raise Exception(f"Erro no deploy local: {str(e)}")

    def handle_change(self, path: str, event_type: str) -> None:
        try:
            relative_path = os.path.relpath(path, start=self.file_manager.base_path)
            dest_path = os.path.join(self.dest_base, relative_path)
            
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
        if directory == self.dest_base:
            return
            
        try:
            while directory != self.dest_base:
                if os.path.exists(directory) and not os.listdir(directory):
                    os.rmdir(directory)
                    directory = os.path.dirname(directory)
                else:
                    break
        except Exception as e:
            self.logger.error(f"Erro ao limpar diretórios: {str(e)}") 