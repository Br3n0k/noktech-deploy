"""
Sistema de monitoramento de arquivos
"""
import asyncio
from pathlib import Path
from typing import Set, Dict, Any, Optional
import time
from watchdog.observers import Observer  # type: ignore
from watchdog.events import FileSystemEventHandler, FileSystemEvent  # type: ignore

from src.utils.logger import CustomLogger
from src.i18n import I18n
from src.deployers.base_deployer import BaseDeployer


class DeployEventHandler(FileSystemEventHandler):
    """Handler para eventos de sistema de arquivos"""

    def __init__(self, watcher: "FileWatcher"):
        self.watcher = watcher
        self.logger = CustomLogger.get_logger(__name__)
        self._cooldown = 1.0  # segundos
        self._last_event: Dict[str, float] = {}

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Processa qualquer evento do sistema de arquivos"""
        if event.is_directory:
            return

        # Evita eventos duplicados usando cooldown
        current_time = time.time()
        if event.src_path in self._last_event:
            if current_time - self._last_event[event.src_path] < self._cooldown:
                return

        self._last_event[event.src_path] = current_time
        self.watcher.queue_change(Path(event.src_path))


class FileWatcher:
    """Gerenciador de monitoramento de arquivos"""

    def __init__(self, deployer: BaseDeployer):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.deployer = deployer
        self.observer = Observer()
        self.handler = DeployEventHandler(self)
        self._pending_changes: Set[Path] = set()
        self._running = False
        self._process_lock = asyncio.Lock()

    def queue_change(self, path: Path) -> None:
        """Adiciona arquivo à fila de mudanças"""
        self._pending_changes.add(path)

    async def start(self, path: Path) -> None:
        """Inicia monitoramento"""
        try:
            self.logger.info(self.i18n.get("watch.started").format(path))
            self.observer.schedule(self.handler, str(path), recursive=True)
            self.observer.start()
            self._running = True

            while self._running:
                await self._process_changes()
                await asyncio.sleep(1)

        except Exception as e:
            self.logger.error(self.i18n.get("watch.error").format(path, e))
            raise
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Para monitoramento"""
        self._running = False
        self.observer.stop()
        self.observer.join()
        self.logger.info(self.i18n.get("watch.stopped").format(self.deployer.source_path))

    async def _process_changes(self) -> None:
        """Processa arquivos modificados"""
        if not self._pending_changes:
            return

        async with self._process_lock:
            try:
                files = list(self._pending_changes)
                self._pending_changes.clear()

                if files:
                    self.logger.info(
                        self.i18n.get("watch.changes_detected").format(
                            len(files),
                            self.deployer.host_name
                        )
                    )
                    await self.deployer.deploy_files(files)

            except Exception as e:
                self.logger.error(
                    self.i18n.get("watch.error.monitor").format(str(e))
                )
