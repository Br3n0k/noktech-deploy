from paramiko import SSHClient, AutoAddPolicy, SFTPClient
from typing import Optional
import os
from pathlib import Path
from src.deployers.base_deployer import BaseDeployer
from ..core.file_manager import FileManager
from ..utils.logger import Logger
import fnmatch

class SSHDeployer(BaseDeployer):
    def __init__(self, 
                 host: str, 
                 user: str, 
                 password: Optional[str] = None, 
                 port: int = 22,
                 key_path: Optional[str] = None,
                 dest_path: Optional[str] = None,
                 logger: Optional[Logger] = None):
        super().__init__(host, user, password or '', port)
        self.key_path = key_path
        self.dest_path = dest_path
        self.client: Optional[SSHClient] = None
        self.sftp: Optional[SFTPClient] = None
        self.file_manager = FileManager()
        self.logger = logger or Logger()
        
        # Valida se pelo menos um método de autenticação foi fornecido
        if not password and not key_path:
            raise ValueError("É necessário fornecer senha ou caminho da chave SSH")
        
    def connect(self) -> None:
        try:
            self.client = SSHClient()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            
            connect_kwargs = {
                'hostname': self.host,
                'port': self.port,
                'username': self.user,
                'timeout': 10
            }
            
            # Prioriza autenticação por chave se disponível
            if self.key_path and os.path.exists(os.path.expanduser(self.key_path)):
                self.logger.info(f"Conectando via SSH usando chave: {self.key_path}")
                connect_kwargs['key_filename'] = os.path.expanduser(self.key_path)
            elif self.password:
                self.logger.info("Conectando via SSH usando senha")
                connect_kwargs['password'] = self.password
            
            self.client.connect(**connect_kwargs)
            self.sftp = self.client.open_sftp()
            self.logger.info("Conexão SSH estabelecida com sucesso")
            
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar via SSH: {str(e)}")

    def ensure_remote_dir(self, path: str) -> None:
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado")
            
        path = path.replace('\\', '/').rstrip('/')
        if not path:
            return
            
        try:
            self.sftp.stat(path)
        except:
            parent = str(Path(path).parent).replace('\\', '/')
            if parent and parent != '/':
                self.ensure_remote_dir(parent)
            self.sftp.mkdir(path)

    def deploy_files(self, files_path: str, dest_path: str) -> None:
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado")
            
        try:
            files_to_deploy = self.file_manager.collect_files(files_path)
            
            for local_path, relative_path in files_to_deploy:
                remote_path = os.path.join(dest_path, relative_path).replace('\\', '/')
                self.ensure_remote_dir(str(Path(remote_path).parent))
                self.sftp.put(local_path, remote_path)
                
        except Exception as e:
            raise Exception(f"Erro no deploy: {str(e)}")

    def disconnect(self) -> None:
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close() 

    def handle_change(self, path: str, event_type: str) -> None:
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado")
        if not self.dest_path:
            raise ValueError("Caminho de destino não definido")
            
        try:
            relative_path = os.path.relpath(path, start=self.file_manager.base_path)
            remote_path = os.path.join(self.dest_path, relative_path).replace('\\', '/')
            
            if event_type in ('created', 'modified'):
                self.ensure_remote_dir(str(Path(remote_path).parent))
                self.sftp.put(path, remote_path)
            elif event_type == 'deleted':
                self.sftp.remove(remote_path)
        except Exception as e:
            raise Exception(f"Erro ao processar mudança via SSH: {str(e)}") 