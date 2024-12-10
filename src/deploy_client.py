#!/usr/bin/env python3
"""
Cliente principal do NokTech Deploy
"""
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from src.core.constants import (
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_TEMPLATE,
    DEFAULT_LOG_DIR,
)
from src.core.deploy_manager import DeployManager
from src.core.watch_manager import WatchManager
from src.utils.logger import CustomLogger
from src.utils.config import ConfigManager
from src.deployers.local_deployer import LocalDeployer
from src.utils.log_manager import LogManager


@dataclass
class DeployClient:
    """Cliente principal de deploy"""

    def __init__(self) -> None:
        self.logger = CustomLogger.get_logger(__name__)
        self._deploy_manager = None
        self._config_manager = ConfigManager()
        self._watch_manager = None

    async def setup(self, config: Dict[str, Any]) -> None:
        """Configura o cliente de deploy"""
        try:
            retention_days = config.get("logs", {}).get("retention_days", 5)
            log_manager = LogManager(retention_days)
            log_manager.initialize()
            self._config_manager = ConfigManager(config)
            self._deploy_manager = LocalDeployer("local", config)
            self.logger.info("Deploy client setup completed")
        except Exception as e:
            self.logger.error(f"Failed to setup client: {e}")
            raise

    async def start_watching(self) -> None:
        """Inicia o monitoramento de arquivos"""
        if not self._watch_manager:
            raise RuntimeError("Client not setup. Call setup() first.")
        await self._watch_manager.start()

    async def stop_watching(self) -> None:
        """Para o monitoramento de arquivos"""
        if not self._watch_manager:
            raise RuntimeError("Client not setup. Call setup() first.")
        await self._watch_manager.stop()

    async def run(self) -> None:
        """Executa o cliente"""
        if not self._deploy_manager:
            raise RuntimeError("Client not setup. Call setup() first.")
            
        try:
            if self._watch_manager:
                await self.start_watching()
                # Mantém o programa rodando até Ctrl+C
                while True:
                    await asyncio.sleep(1)
            else:
                await self._deploy_manager.deploy_all()
        except KeyboardInterrupt:
            if self._watch_manager:
                await self.stop_watching()
        except Exception as e:
            self.logger.error(f"Error running client: {e}")
            raise
