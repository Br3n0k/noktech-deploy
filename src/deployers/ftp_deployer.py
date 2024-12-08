from typing import Optional
from ftplib import FTP
import os
from pathlib import Path
from .base_deployer import BaseDeployer
from ..core.file_manager import FileManager

class FTPDeployer(BaseDeployer):
    def __init__(self, host: str, user: str, password: str, port: int = 21, dest_path: Optional[str] = None):
        super().__init__(host, user, password, port)
        self.ftp: Optional[FTP] = None
        self.dest_path = dest_path
        self.file_manager = FileManager()

    def connect(self) -> None:
        try:
            self.ftp = FTP()
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.password)
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar via FTP: {str(e)}")

    def ensure_remote_dir(self, path: str) -> None:
        if not self.ftp:
            raise ConnectionError("FTP não inicializado")
            
        current = ''
        for part in path.split('/'):
            if not part:
                continue
            current += '/' + part
            try:
                self.ftp.cwd(current)
            except:
                self.ftp.mkd(current)

    def deploy_files(self, files_path: str, dest_path: str) -> None:
        if not self.ftp:
            raise ConnectionError("FTP não inicializado")
            
        try:
            files_to_deploy = self.file_manager.collect_files(files_path)
            
            for local_path, relative_path in files_to_deploy:
                remote_path = os.path.join(dest_path, relative_path).replace('\\', '/')
                self.ensure_remote_dir(str(Path(remote_path).parent))
                
                with open(local_path, 'rb') as f:
                    self.ftp.storbinary(f'STOR {remote_path}', f)
                    
        except Exception as e:
            raise Exception(f"Erro no deploy: {str(e)}")

    def disconnect(self) -> None:
        if self.ftp:
            self.ftp.quit() 

    def handle_change(self, path: str, event_type: str) -> None:
        if not self.ftp:
            raise ConnectionError("FTP não inicializado")
        if not self.dest_path:
            raise ValueError("Caminho de destino não definido")
            
        try:
            relative_path = os.path.relpath(path, start=self.file_manager.base_path)
            remote_path = os.path.join(self.dest_path, relative_path).replace('\\', '/')
            
            if event_type in ('created', 'modified'):
                self.ensure_remote_dir(str(Path(remote_path).parent))
                with open(path, 'rb') as f:
                    self.ftp.storbinary(f'STOR {remote_path}', f)
            elif event_type == 'deleted':
                self.ftp.delete(remote_path)
        except Exception as e:
            raise Exception(f"Erro ao processar mudança via FTP: {str(e)}")