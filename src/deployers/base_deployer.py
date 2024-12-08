from abc import ABC, abstractmethod
from typing import Optional
from ..core.ignore_rules import IgnoreRules

class BaseDeployer(ABC):
    def __init__(self, host: str, user: str, password: str, port: int):
        self.host = host
        self.user = user 
        self.password = password
        self.port = port
        self.ignore_rules: Optional[IgnoreRules] = None

    @abstractmethod
    def connect(self) -> None:
        """Estabelece conexão com o servidor"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Encerra conexão com o servidor"""
        pass

    @abstractmethod 
    def deploy_files(self, files_path: str, dest_path: str) -> None:
        """Faz upload dos arquivos para o servidor"""
        pass

    @abstractmethod
    def ensure_remote_dir(self, path: str) -> None:
        """Garante que o diretório remoto existe"""
        pass

    @abstractmethod
    def handle_change(self, path: str, event_type: str) -> None:
        """Manipula mudanças em arquivos no modo watch"""
        pass