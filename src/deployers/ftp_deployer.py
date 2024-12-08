from typing import Optional
from ftplib import FTP
import os
from pathlib import Path
from .base_deployer import BaseDeployer
from ..core.file_manager import FileManager
import asyncio

class FTPDeployer(BaseDeployer):
    def __init__(self, host: str, user: str, password: Optional[str] = None, port: int = 21, dest_path: str = ''):
        super().__init__(host=host, user=user, password=password, port=port)
        self.ftp: Optional[FTP] = None
        self.dest_path = dest_path

    async def connect(self) -> None:
        """Conecta ao servidor FTP"""
        try:
            def _connect():
                ftp = FTP()
                ftp.connect(self.host, self.port)
                ftp.login(self.user, self.password or '')
                return ftp
                
            self.ftp = await asyncio.get_event_loop().run_in_executor(None, _connect)
        except Exception as e:
            self.ftp = None
            raise ConnectionError(f"Erro ao conectar ao FTP: {str(e)}")

    async def disconnect(self) -> None:
        if self.ftp:
            self.ftp.quit()

    async def ensure_remote_dir(self, path: str) -> None:
        if not self.ftp:
            raise ConnectionError("FTP não conectado")
            
        parts = path.split('/')
        current = ''
        
        for part in parts:
            if not part:
                continue
            current = f"{current}/{part}"
            try:
                self.ftp.mkd(current)
            except:
                pass

    async def file_exists(self, remote_path: str) -> bool:
        if not self.ftp:
            raise ConnectionError("FTP não conectado")
        try:
            self.ftp.size(remote_path)
            return True
        except:
            return False

    async def _deploy_file(self, local_path: str, remote_path: str):
        if not self.ftp:
            raise ConnectionError("FTP não conectado")
            
        remote_dir = os.path.dirname(remote_path)
        if remote_dir:
            await self.ensure_remote_dir(remote_dir)
            
        with open(local_path, 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_path}', f)

    async def handle_change(self, path: str, event_type: str) -> None:
        if not self.ftp:
            raise ConnectionError("FTP não conectado")
            
        try:
            relative_path = os.path.relpath(path)
            remote_path = os.path.join(self.dest_path, relative_path).replace('\\', '/')
            
            if event_type in ('created', 'modified'):
                await self.ensure_remote_dir(str(Path(remote_path).parent))
                await self._deploy_file(path, remote_path)
            elif event_type == 'deleted':
                self.ftp.delete(remote_path)
        except Exception as e:
            raise Exception(f"Erro ao processar mudança: {str(e)}")