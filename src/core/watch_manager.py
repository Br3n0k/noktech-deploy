import asyncio
from typing import Dict
from pathlib import Path
from src.core.watcher import DirectoryWatcher
from src.utils.logger import Logger
from src.i18n import I18n
from src.core.deploy_manager import DeployManager

class WatchManager:
    def __init__(self, deploy_manager: DeployManager):
        self.logger = Logger(__name__)
        self.i18n = I18n()
        self.deploy_manager = deploy_manager
        self.watchers: Dict[str, DirectoryWatcher] = {}
        self.running = False
        
    async def start_watchers(self, config: dict) -> None:
        """Inicia observadores para hosts habilitados"""
        self.running = True
        
        for host_name, host_config in config["hosts"].items():
            if not host_config.get("enabled", False):
                continue
                
            watch_config = host_config.get("watch", {})
            if not watch_config.get("enabled", False):
                continue

            try:
                self.logger.info(self.i18n.get("watch.starting").format(host_name))
                
                watcher = DirectoryWatcher(
                    path=Path(host_config["source_path"]),
                    patterns=watch_config.get("patterns", ["*"]),
                    ignore_patterns=watch_config.get("ignore_patterns", []),
                    interval=watch_config.get("interval", 1.0)
                )
                
                self.watchers[host_name] = watcher
                asyncio.create_task(self._watch_host(host_name, watcher))
                
            except Exception as e:
                self.logger.error(self.i18n.get("watch.error.config").format(str(e)))

    async def _watch_host(self, host_name: str, watcher: DirectoryWatcher) -> None:
        """Processa alterações para um host específico"""
        try:
            async for changes in watcher.watch():
                if not self.running:
                    break
                    
                if changes:
                    self.logger.info(self.i18n.get("watch.changes_detected").format(
                        len(changes), host_name))
                    await self.deploy_manager.deploy_changes(host_name, changes)
                    
        except Exception as e:
            self.logger.error(self.i18n.get("watch.error.monitor").format(str(e)))

    async def stop_watchers(self) -> None:
        """Para todos os watchers ativos"""
        self.running = False
        for host_name, watcher in self.watchers.items():
            await watcher.stop()
            self.logger.info(self.i18n.get("watch.stopped").format(host_name)) 