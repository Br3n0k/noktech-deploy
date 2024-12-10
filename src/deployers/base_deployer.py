from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
from src.utils.logger import Logger

class BaseDeployer(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = Logger(__name__)
        self.source_path = Path(config.get("source_path", "."))
        self.dest_path = config.get("dest_path", "")
        self.ignore_patterns = config.get("ignore_patterns", [])

    @abstractmethod
    async def connect(self) -> None:
        """Estabelece conexão com o destino"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Encerra a conexão com o destino"""
        pass

    @abstractmethod
    async def upload_file(self, source: Path, dest: str) -> None:
        """Faz upload de um arquivo para o destino"""
        pass

    async def deploy(self) -> None:
        """Executa o deploy completo"""
        try:
            await self.connect()
            await self._deploy_files()
            await self.disconnect()
        except Exception as e:
            self.logger.error(f"Erro durante deploy: {str(e)}")
            raise

    async def _deploy_files(self) -> None:
        """Faz deploy de todos os arquivos"""
        for file in self.source_path.rglob("*"):
            if file.is_file() and not await self.should_ignore(file):
                rel_path = file.relative_to(self.source_path)
                dest = f"{self.dest_path}/{str(rel_path).replace(chr(92), '/')}"
                await self.upload_file(file, dest)

    async def should_ignore(self, file: Path) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
        from fnmatch import fnmatch
        return any(fnmatch(str(file), pattern) for pattern in self.ignore_patterns)
