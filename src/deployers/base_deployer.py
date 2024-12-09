from abc import ABC, abstractmethod
from typing import Optional
import os
from src.core.ignore_rules import IgnoreRules
from src.core.logger import Logger


class BaseDeployer(ABC):
    def __init__(
        self,
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 22,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ignore_rules: Optional[IgnoreRules] = None
        self.logger = Logger()
        self.overwrite_existing = True

    def set_overwrite_mode(self, overwrite: bool):
        """Define se arquivos existentes devem ser sobrescritos"""
        self.overwrite_existing = overwrite

    async def deploy_file(self, local_path: str, remote_path: str):
        """Verifica existência antes de fazer upload"""
        if not self.overwrite_existing:
            if await self.file_exists(remote_path):
                return  # Pula arquivo existente

        await self._deploy_file(local_path, remote_path)

    @abstractmethod
    async def file_exists(self, remote_path: str) -> bool:
        """Verifica se arquivo existe no destino"""
        pass

    @abstractmethod
    async def _deploy_file(self, local_path: str, remote_path: str) -> None:
        """Implementação específica do deploy de um arquivo"""
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Estabelece conexão com o servidor"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Encerra conexão com o servidor"""
        pass

    @abstractmethod
    async def ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório remoto existe"""
        pass

    @abstractmethod
    async def handle_change(self, path: str, event_type: str) -> None:
        """Manipula mudanças em arquivos no modo watch"""
        pass

    async def deploy_files(self, source_path: str, dest_path: str) -> None:
        """Deploy de múltiplos arquivos"""
        for root, _, files in os.walk(source_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, source_path)
                remote_path = os.path.join(dest_path, relative_path).replace("\\", "/")

                if self.ignore_rules and self.ignore_rules.should_ignore(relative_path):
                    continue

                await self._deploy_file(local_path, remote_path)
