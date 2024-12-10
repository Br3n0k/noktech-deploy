"""
Classe base para implementações de deployers
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Set
import fnmatch
import yaml

from src.utils.logger import CustomLogger
from src.i18n import I18n


class BaseDeployer(ABC):
    """Classe base abstrata para deployers"""

    def __init__(self, host_name: str, config: Dict) -> None:
        self.host_name = host_name
        self.source_path = Path(config["source_path"])
        self.dest_path = Path(config["dest_path"])
        self.ignore_patterns: Set[str] = self._load_ignore_patterns()
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()

    def _load_ignore_patterns(self) -> Set[str]:
        """Carrega padrões de ignore do .deployignore"""
        ignore_file = self.source_path / ".deployignore"
        patterns = {
            "*.pyc", "__pycache__", "*.pyo", "*.pyd",  # Python
            ".git", ".gitignore", ".gitattributes",    # Git
            ".env", ".venv", "venv", "env",            # Virtualenv
            ".idea", ".vscode", "*.swp", "*.swo",      # IDEs
            "*.log", "logs", "*.tmp", "*.temp",        # Logs e temporários
            ".deployignore", "*.bak", "~*"             # Deploy específicos
        }

        if ignore_file.exists():
            try:
                with open(ignore_file, 'r', encoding='utf-8') as f:
                    custom_patterns = {
                        line.strip() for line in f
                        if line.strip() and not line.startswith('#')
                    }
                    patterns.update(custom_patterns)
            except Exception as e:
                self.logger.warning(f"Error loading .deployignore: {e}")

        return patterns

    def should_ignore(self, path: Path) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
        rel_path = str(path.relative_to(self.source_path))
        
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                self.logger.debug(
                    self.i18n.get("deploy.file_ignored").format(rel_path, pattern)
                )
                return True
        return False

    @abstractmethod
    async def connect(self) -> None:
        """Estabelece conexão com o destino"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Encerra conexão com o destino"""
        pass

    @abstractmethod
    async def deploy_directory(self, path: Path) -> None:
        """Realiza deploy de um diretório completo"""
        pass

    @abstractmethod
    async def deploy_files(self, files: List[Path]) -> None:
        """Realiza deploy de arquivos específicos"""
        pass

    @abstractmethod
    async def ensure_remote_dir(self, path: Path) -> None:
        """Garante existência de diretório no destino"""
        pass

    async def validate_paths(self) -> None:
        """Valida caminhos de origem e destino"""
        if not self.source_path.exists():
            raise FileNotFoundError(
                self.i18n.get("deploy.error.path").format(self.source_path)
            )

    async def prepare_deploy(self) -> None:
        """Prepara ambiente para deploy"""
        self.logger.info(self.i18n.get("deploy.progress.setup"))
        await self.validate_paths()
        await self.connect()

    async def deploy(self) -> None:
        """Executa processo de deploy completo"""
        try:
            self.logger.info(self.i18n.get("deploy.progress.start"))
            await self.prepare_deploy()
            await self.deploy_directory(self.source_path)
            self.logger.info(self.i18n.get("deploy.progress.complete"))
        except Exception as e:
            self.logger.error(self.i18n.get("deploy.progress.error").format(str(e)))
            raise
        finally:
            await self.disconnect()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(host={self.host_name})"
