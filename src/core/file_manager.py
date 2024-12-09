import os
from typing import List, Tuple, Optional
from .ignore_rules import IgnoreRules
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import asyncio


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback, ignore_rules=None):
        self.callback = callback
        self.ignore_rules = ignore_rules
        self.loop = None

    def _get_loop(self):
        if self.loop is None:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
        return self.loop

    async def _handle_event(self, event, event_type):
        if not event.is_directory:
            rel_path = os.path.relpath(event.src_path)
            if not self.ignore_rules or not self.ignore_rules.should_ignore(rel_path):
                await self.callback(event.src_path, event_type)

    def on_created(self, event):
        loop = self._get_loop()
        loop.create_task(self._handle_event(event, "created"))

    def on_modified(self, event):
        loop = self._get_loop()
        loop.create_task(self._handle_event(event, "modified"))

    def on_deleted(self, event):
        loop = self._get_loop()
        loop.create_task(self._handle_event(event, "deleted"))


class FileManager:
    def __init__(
        self,
        base_path: Optional[str] = None,
        ignore_rules: Optional[IgnoreRules] = None,
    ):
        self.ignore_rules = ignore_rules
        self.observer = None
        self.base_path = os.path.abspath(base_path) if base_path else None

    def collect_files(self, path: str) -> List[Tuple[str, str]]:
        files = []
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                abs_path = os.path.join(root, filename)
                rel_path = os.path.relpath(abs_path, path)
                # Normaliza separadores para forward slash
                rel_path = rel_path.replace(os.sep, "/")
                files.append((abs_path, rel_path))
        return files

    def watch_directory(self, path: str, callback) -> None:
        """Observa mudanças no diretório"""
        self.observer = Observer()
        handler = FileChangeHandler(callback, self.ignore_rules)
        self.observer.schedule(handler, path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_watching()

    def stop_watching(self) -> None:
        """Para de observar o diretório"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
