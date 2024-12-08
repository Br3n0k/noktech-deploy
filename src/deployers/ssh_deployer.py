from typing import Optional
import asyncssh
import os
from pathlib import Path
from src.deployers.base_deployer import BaseDeployer
from ..core.file_manager import FileManager
from ..utils.logger import Logger
import fnmatch

class SSHDeployer(BaseDeployer):
    def __init__(self, host: str, user: str, password: Optional[str] = None, key_path: Optional[str] = None, port: int = 22, dest_path: str = ''):
        super().__init__(host=host, user=user, password=password, port=port)
        self.key_path = key_path
        self.dest_path = dest_path
        self.sftp: Optional[asyncssh.SFTPClient] = None
        self.ssh: Optional[asyncssh.SSHClientConnection] = None
        self.file_manager = FileManager()
        self.logger = Logger()
        
    async def connect(self) -> None:
        """Conecta ao servidor SSH"""
        conn_params = {
            'username': self.user,
            'port': self.port
        }
        
        if self.password:
            conn_params['password'] = self.password
        elif self.key_path:
            conn_params['client_keys'] = [self.key_path]
            
        self.ssh = await asyncssh.connect(self.host, **conn_params)
        self.sftp = await self.ssh.start_sftp_client()

    async def disconnect(self) -> None:
        """Desconecta do servidor"""
        if self.sftp:
            self.sftp.exit()
        if self.ssh:
            self.ssh.close()
            await self.ssh.wait_closed()

    async def ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório remoto existe"""
        if not self.sftp:
            raise ConnectionError("SFTP não conectado")
            
        parts = path.split('/')
        current = ''
        
        for part in parts:
            if not part:
                continue
            current = f"{current}/{part}"
            try:
                await self.sftp.mkdir(current)
            except:
                pass  # Diretório já existe

    async def file_exists(self, remote_path: str) -> bool:
        if not self.sftp:
            raise ConnectionError("SFTP não conectado")
        try:
            await self.sftp.stat(remote_path)
            return True
        except FileNotFoundError:
            return False

    async def _deploy_file(self, local_path: str, remote_path: str):
        if not self.sftp:
            raise ConnectionError("SFTP não conectado")
            
        remote_dir = os.path.dirname(remote_path)
        if remote_dir:
            await self.ensure_remote_dir(remote_dir)
            
        await self.sftp.put(local_path, remote_path)

    async def create_remote_dir(self, path: str) -> None:
        """Cria diretório remoto se não existir"""
        if not self.sftp:
            raise ConnectionError("SFTP não conectado")
        try:
            await self.sftp.mkdir(path)
        except:
            pass  # Diretório já existe

    async def deploy_files(self, files_path: str, dest_path: str) -> None:
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado")
            
        try:
            files_to_deploy = self.file_manager.collect_files(files_path)
            
            for local_path, relative_path in files_to_deploy:
                remote_path = os.path.join(dest_path, relative_path).replace('\\', '/')
                await self.create_remote_dir(str(Path(remote_path).parent))
                await self.sftp.put(local_path, remote_path)
                
        except Exception as e:
            raise Exception(f"Erro no deploy: {str(e)}")

    async def handle_change(self, path: str, event_type: str) -> None:
        if not self.sftp:
            raise ConnectionError("SFTP não conectado")
            
        try:
            relative_path = os.path.relpath(path)
            remote_path = os.path.join(self.dest_path, relative_path).replace('\\', '/')
            
            if event_type in ('created', 'modified'):
                await self.ensure_remote_dir(str(Path(remote_path).parent))
                await self.sftp.put(path, remote_path)
            elif event_type == 'deleted':
                await self.sftp.remove(remote_path)
        except Exception as e:
            raise Exception(f"Erro ao processar mudança: {str(e)}") 