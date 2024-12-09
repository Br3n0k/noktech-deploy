from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable
import asyncio


class AsyncEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, "created"))

    def on_modified(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, "modified"))

    def on_deleted(self, event):
        if not event.is_directory:
            asyncio.create_task(self.callback(event.src_path, "deleted"))


class DirectoryWatcher:
    def __init__(self, path: str, callback: Callable, ignore_rules=None):
        self.path = path
        self.callback = callback
        self.ignore_rules = ignore_rules
        self.observer = Observer()
        self._running = False
        self._loop = asyncio.get_event_loop()

        def sync_callback(path: str, event_type: str):
            self._loop.create_task(self.callback(path, event_type))

        self.handler = FileSystemEventHandler()
        self.handler.on_created = lambda e: (
            sync_callback(e.src_path, "created") if not e.is_directory else None
        )
        self.handler.on_modified = lambda e: (
            sync_callback(e.src_path, "modified") if not e.is_directory else None
        )
        self.handler.on_deleted = lambda e: (
            sync_callback(e.src_path, "deleted") if not e.is_directory else None
        )

        self.observer.schedule(self.handler, path, recursive=True)

    async def start(self):
        self._running = True
        self.observer.start()
        try:
            while self._running:
                await asyncio.sleep(0.1)
        finally:
            self.stop()

    def stop(self):
        self._running = False
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
