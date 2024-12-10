import os
import shutil
import asyncio
from pathlib import Path
from src.deployers.base_deployer import BaseDeployer


class LocalDeployer(BaseDeployer):
    def __init__(self, config: dict = None):
        super().__init__(config or {"protocol": "local"})

    async def deploy_file(self, source: Path, dest: Path) -> bool:
        """
        Deploy de um arquivo local
        """
        try:
            # Garante que o diretório de destino existe
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Copia o arquivo preservando metadados
            shutil.copy2(source, dest)
            self.logger.debug(self.i18n.get("local.copying").format(
                str(source), str(dest)))
            return True
            
        except Exception as e:
            self.logger.error(self.i18n.get("local.error.copy").format(str(e)))
            return False

    async def deploy_directory(self, source: Path, dest: Path) -> bool:
        """
        Deploy de um diretório local completo
        """
        try:
            source = Path(source).resolve()
            dest = Path(dest).resolve()
            
            self.logger.info(self.i18n.get("local.copying_dir").format(
                str(source), str(dest)))
            
            # Garante que o diretório de destino existe
            dest.mkdir(parents=True, exist_ok=True)
            
            success = True
            total_files = 0
            copied_files = 0
            
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
                    try:
                        rel_path = src_file.relative_to(source)
                        dest_file = dest / rel_path
                        
                        # Faz a cópia do arquivo
                        if await self.deploy_file(src_file, dest_file):
                            copied_files += 1
                        else:
                            success = False
                            
                    except Exception as e:
                        self.logger.error(self.i18n.get("local.path_error").format(
                            str(src_file), str(e)))
                        success = False
            
            # Log do resultado
            self.logger.info(self.i18n.get("local.copy_complete").format(
                copied_files, total_files))
            
            return success
            
        except Exception as e:
            self.logger.error(self.i18n.get("local.deploy_failed").format(str(e)))
            return False

    async def _ensure_dest_dir(self, path: Path) -> None:
        """
        Garante que o diretório de destino existe
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception(self.i18n.get("local.mkdir_failed").format(
                str(path), str(e)))

    async def connect(self) -> None:
        """Não é necessário conectar para deploy local"""
        pass

    async def disconnect(self) -> None:
        """Não é necessário desconectar para deploy local"""
        pass

    async def ensure_remote_dir(self, path):
        """Garante que diretório existe"""
        os.makedirs(str(path), exist_ok=True)

    async def file_exists(self, path):
        """Verifica se arquivo existe"""
        return os.path.exists(str(path))

    async def get_remote_mtime(self, path):
        """Obtém data de modificação"""
        return os.path.getmtime(str(path))

    async def _deploy_file(self, src, dest):
        """Copia um arquivo"""
        shutil.copy2(str(src), str(dest))

    async def handle_change(self, path, event_type):
        """Manipula mudanças em arquivos"""
        try:
            if event_type in ("created", "modified"):
                await self._deploy_file(path, os.path.join(self.dest_path, path))
            elif event_type == "deleted":
                try:
                    os.remove(os.path.join(self.dest_path, path))
                except FileNotFoundError:
                    pass
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança: {e}")

    async def upload_file(self, source: Path, dest: str) -> None:
        """Copia arquivo localmente"""
        try:
            source_path = Path(source)
            dest_path = Path(dest)
            
            # Garante que o diretório fonte existe
            if not source_path.exists():
                source_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.touch()
            
            # Garante que o diretório destino existe
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copia o arquivo
            shutil.copy2(str(source_path), str(dest_path))
        except Exception as e:
            self.logger.error(f"Erro na cópia do arquivo {source}: {str(e)}")
            raise
