from typing import Dict, Any, Optional, List
from pathlib import Path
from src.utils.logger import CustomLogger
from src.deployers import BaseDeployer, SSHDeployer, FTPDeployer, LocalDeployer
from src.core.constants import (
    SUPPORTED_PROTOCOLS,
    DEFAULT_PROTOCOL,
    DEPLOY_RETRY_ATTEMPTS,
    DEPLOY_RETRY_DELAY
)
import asyncio


class DeployManager:
    """Gerencia operações de deploy"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.logger = CustomLogger.get_logger(__name__)
        self.config = config
        self._deployer: Optional[BaseDeployer] = None
        self._setup_deployer()

    def _setup_deployer(self) -> None:
        """Configura o deployer baseado na configuração"""
        protocol = self.config.get("protocol", DEFAULT_PROTOCOL)
        deployers = {
            "ssh": SSHDeployer,
            "ftp": FTPDeployer,
            "local": LocalDeployer
        }

        if protocol not in SUPPORTED_PROTOCOLS:
            raise ValueError(f"Unsupported protocol: {protocol}")

        self._deployer = deployers[protocol](self.config)

    async def deploy_host(self, host_name: str, host_config: Dict) -> None:
        for attempt in range(DEPLOY_RETRY_ATTEMPTS):
            try:
                protocol = host_config.get("protocol", DEFAULT_PROTOCOL)
                if protocol not in SUPPORTED_PROTOCOLS:
                    raise ValueError(f"Protocol not supported: {protocol}")

                deployer = self._deployer
                await deployer.deploy_directory(Path(host_config["source_path"]))
                break
            except Exception as e:
                if attempt == DEPLOY_RETRY_ATTEMPTS - 1:
                    self.logger.error(f"Failed to deploy host {host_name}: {e}")
                    raise
                await asyncio.sleep(DEPLOY_RETRY_DELAY)

    async def deploy_changes(self, host_name: str, changes: List[Path]) -> None:
        try:
            deployer = self._deployer
            await deployer.deploy_files(changes)
        except Exception as e:
            self.logger.error(f"Failed to deploy changes for {host_name}: {e}")
            raise
