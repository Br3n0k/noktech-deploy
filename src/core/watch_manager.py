from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Optional, Union, Awaitable, Callable, TYPE_CHECKING
import asyncio
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, DirModifiedEvent
from watchdog.observers.api import BaseObserver as Observer
from watchdog.observers.polling import PollingObserverVFS

from src.utils.logger import CustomLogger
from src.core.constants import (
    WATCH_RECURSIVE,
    WATCH_OBSERVER_CLASS,
    WATCH_PATTERNS,
    WATCH_DELAY,
    WATCH_INTERVAL
)

if TYPE_CHECKING:
    from src.core.deploy_manager import DeployManager


class AsyncWatchEventHandler(FileSystemEventHandler):
    def __init__(self, on_change: Callable[[Path], Awaitable[None]]) -> None:
        super().__init__()
        self.on_change = on_change
        self.logger = CustomLogger.get_logger(__name__)

    async def _handle_change(self, path: Path) -> None:
        try:
            await self.on_change(path)
        except Exception as e:
            self.logger.error(f"Error processing file change: {e}")

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        if not isinstance(event, (DirModifiedEvent, FileModifiedEvent)) or event.is_directory:
            return

        asyncio.create_task(self._handle_change(Path(event.src_path)))


class WatchManager:
    def __init__(self, config: Dict[str, Any], deploy_manager: DeployManager) -> None:
        self.logger = CustomLogger.get_logger(__name__)
        self.config = config
        self.deploy_manager = deploy_manager
        self.observer: Optional[Observer] = None
        self.handler = AsyncWatchEventHandler(self.deploy_manager.sync_file)

    async def start_watch(self) -> None:
        if self.observer:
            return

        try:
            observer_class = globals().get(WATCH_OBSERVER_CLASS, PollingObserverVFS)
            self.observer = Observer(emitter_class=observer_class)
            watch_path = Path(self.config.get("source_path", "."))
            
            self.observer.schedule(
                self.handler, 
                str(watch_path), 
                recursive=WATCH_RECURSIVE
            )
            
            self.observer.start()
            await asyncio.sleep(WATCH_DELAY)  # Aguarda inicialização
            self.logger.info(f"Started watching directory: {watch_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to start watching: {e}")
            self.observer = None
            raise

    async def stop_watch(self) -> None:
        if not self.observer:
            return

        try:
            self.observer.stop()
            self.observer.join(timeout=WATCH_INTERVAL)
            self.observer = None
            self.logger.info("Stopped watching")
        except Exception as e:
            self.logger.error(f"Failed to stop watching: {e}")
            raise
