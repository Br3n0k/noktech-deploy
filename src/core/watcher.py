from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable, Optional, Dict
import time
import os
from .ignore_rules import IgnoreRules
from ..utils.logger import Logger
import asyncio

class AsyncEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, 'created'))
            
    def on_modified(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, 'modified'))
            
    def on_deleted(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, 'deleted'))

class DirectoryWatcher:
    def __init__(self, 
                 path: str,
                 callback: Callable,
                 ignore_rules: Optional[IgnoreRules] = None,
                 logger: Optional[Logger] = None):
        self.path = os.path.abspath(path)
        self.callback = callback
        self.ignore_rules = ignore_rules
        self.logger = logger or Logger()
        self.observer = Observer()
        self._running = False

    async def start(self):
        """Inicia a observação do diretório"""
        event_handler = AsyncEventHandler(self.callback)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

    def stop(self):
        """Para o observador"""
        self._running = False
        self.observer.stop()
        self.observer.join()
        self.logger.info("Observador finalizado") 