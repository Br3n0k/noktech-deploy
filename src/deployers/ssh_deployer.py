from typing import Optional
import asyncssh
import os
from pathlib import Path
from src.deployers.base_deployer import BaseDeployer
from ..core.file_manager import FileManager
from ..utils.logger import Logger


class SSHDeployer(BaseDeployer):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = None
        self.sftp = None
        
    async def connect(self) -> None:
        """Estabelece conexão SSH"""
        try:
            self.conn = await asyncssh.connect(
                self.config["host"],
                username=self.config["user"],
                password=self.config.get("password"),
                port=self.config.get("port", 22),
                known_hosts=None  # TODO: Implementar verificação de known_hosts
            )
            self.sftp = await self.conn.start_sftp_client()
        except Exception as e:
            raise ConnectionError(f"Falha na conexão SSH: {str(e)}")

    async def disconnect(self) -> None:
        """Encerra conexão SSH"""
        if hasattr(self, 'sftp'):
            await self.sftp.close()
        if hasattr(self, 'conn'):
            self.conn.close()
            await self.conn.wait_closed()

    async def upload_file(self, source: Path, dest: str) -> None:
        """Upload de arquivo via SSH/SFTP"""
        try:
            await self._ensure_remote_dir(str(Path(dest).parent))
            sftp_client = await self.conn.start_sftp_client()
            try:
                await sftp_client.put(str(source), dest)
            finally:
                await sftp_client.close()
        except Exception as e:
            self.logger.error(f"Erro no upload do arquivo {source}: {str(e)}")
            raise

    async def _ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório remoto existe"""
        try:
            await self.sftp.mkdir(path, parents=True)
        except asyncssh.SFTPError:
            pass  # Diretório já existe

    async def deploy_file(self, source: Path, dest: Path) -> bool:
        """Deploy de um arquivo via SFTP"""
        try:
            if not self.sftp:
                self.sftp = await self.client.start_sftp_client()

            # Normaliza caminhos
            dest_str = str(dest).replace("\\", "/")
            
            # Cria diretórios remotos
            await self._ensure_remote_dirs(dest.parent)
            
            # Upload do arquivo
            await self.sftp.put(str(source), dest_str)
            self.logger.debug(self.i18n.get("ssh.file_uploaded").format(dest_str))
            return True
            
        except Exception as e:
            self.logger.error(self.i18n.get("ssh.upload_failed").format(
                str(source), str(e)))
            return False

    async def deploy_directory(self, source: Path, dest: Path) -> bool:
        """Deploy de um diretório completo via SFTP"""
        try:
            await self.connect()
            success = True
            total_files = 0
            uploaded_files = 0

            # Processa cada arquivo no diretório fonte
            for src_file in source.rglob("*"):
                if src_file.is_file():
                    total_files += 1
                    
                    # Verifica padrões de ignore
                    if self.should_ignore(src_file):
                        self.logger.debug(self.i18n.get("deploy.file_ignored").format(
                            str(src_file), "pattern match"))
                        continue

                    # Calcula caminho relativo para destino
                    rel_path = src_file.relative_to(source)
                    dest_file = Path(dest) / rel_path

                    # Faz upload do arquivo
                    if await self.deploy_file(src_file, dest_file):
                        uploaded_files += 1
                    else:
                        success = False

            self.logger.info(self.i18n.get("ssh.upload_complete").format(
                uploaded_files, total_files))
            return success

        except Exception as e:
            self.logger.error(self.i18n.get("ssh.deploy_failed").format(str(e)))
            return False

        finally:
            if self.sftp:
                self.sftp.close()
            if self.client:
                self.client.close()

    async def ensure_remote_dir(self, path: str) -> None:
        """Cria diretório remoto"""
        try:
            await self.client.run(f'mkdir -p "{str(path)}"')
        except Exception as e:
            raise Exception(f"Erro ao criar diretório: {e}")

    async def file_exists(self, path: str) -> bool:
        """Verifica se arquivo existe"""
        try:
            await self.sftp.stat(str(path))
            return True
        except FileNotFoundError:
            return False

    async def get_remote_mtime(self, path: str) -> float:
        """Obtém data de modificação"""
        stat = await self.sftp.stat(str(path))
        return stat.mtime

    async def _deploy_file(self, src, dest):
        """Faz upload do arquivo"""
        await self.sftp.put(str(src), str(dest))

    async def handle_change(self, path: str, event_type: str) -> None:
        """Manipula mudanças em arquivos"""
        try:
            remote_path = os.path.join(self.dest_path, path).replace("\\", "/")

            if event_type in ("created", "modified"):
                await self.ensure_remote_dir(str(Path(remote_path).parent))
                await self._deploy_file(path, remote_path)
            elif event_type == "deleted":
                try:
                    await self.sftp.remove(remote_path)
                except FileNotFoundError:
                    pass
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança: {e}")
