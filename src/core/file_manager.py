from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Awaitable, TypeAlias
from watchdog.observers.api import BaseObserver as Observer
from watchdog.observers.polling import PollingObserverVFS

from src.core.ignore_rules import IgnoreRules
from src.utils.logger import CustomLogger
from src.core.watch_manager import AsyncWatchEventHandler
from src.core.constants import WATCH_INTERVAL

OnChangeCallback: TypeAlias = Callable[[Path], Awaitable[None]]


class FileManager:
    """Gerencia operações com arquivos"""

    def __init__(self, base_path: Path) -> None:
        self.logger = CustomLogger.get_logger(__name__)
        self.base_path = base_path
        self.ignore_rules = IgnoreRules()
        self.observer: Optional[Observer] = None

    async def start_watching(
        self, on_change: "Callable[[Path], Awaitable[None]]"
    ) -> None:
        """Inicia monitoramento de arquivos"""
        if self.observer is not None:
            return

        try:
            self.observer = Observer(emitter_class=PollingObserverVFS)
            event_handler = AsyncWatchEventHandler(on_change)
            self.observer.schedule(
                event_handler, 
                str(self.base_path), 
                recursive=True
            )
            self.observer.start()
            self.logger.info(f"Watching directory: {self.base_path}")
        except Exception as e:
            self.logger.error(f"Failed to start watching: {e}")
            self.observer = None
            raise

    def stop_watching(self) -> None:
        """Para monitoramento de arquivos"""
        if not self.observer:
            return

        try:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.logger.info("Stopped watching")
        except Exception as e:
            self.logger.error(f"Failed to stop watching: {e}")
            raise

    def get_files(self) -> List[Tuple[Path, Path]]:
        """Retorna lista de arquivos para sincronização"""
        files: List[Tuple[Path, Path]] = []

        for file_path in self.base_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self.ignore_rules.should_ignore(file_path):
                continue

            rel_path = file_path.relative_to(self.base_path)
            files.append((file_path, rel_path))

        return files
