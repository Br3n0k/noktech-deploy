import os
from typing import List, Tuple, Optional
from pathlib import Path
from .ignore_rules import IgnoreRules
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback, ignore_rules: Optional[IgnoreRules] = None):
        self.callback = callback
        self.ignore_rules = ignore_rules

    def on_modified(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.callback(event.src_path, 'modified')

    def on_created(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.callback(event.src_path, 'created')

    def on_deleted(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            self.callback(event.src_path, 'deleted')

    def _should_ignore(self, path: str) -> bool:
        return bool(self.ignore_rules and self.ignore_rules.should_ignore(path))

class FileManager:
    def __init__(self, base_path: Optional[str] = None, ignore_rules: Optional[IgnoreRules] = None):
        self.ignore_rules = ignore_rules
        self.observer = None
        self.base_path = os.path.abspath(base_path) if base_path else None

    def collect_files(self, base_path: str) -> List[Tuple[str, str]]:
        """Coleta arquivos para deploy respeitando regras de ignore"""
        self.base_path = os.path.abspath(base_path)
        files_to_deploy = []
        
        for root, _, files in os.walk(self.base_path):
            for file in files:
                full_path = os.path.join(root, file)
                if not self.ignore_rules or not self.ignore_rules.should_ignore(full_path):
                    relative_path = os.path.relpath(full_path, self.base_path)
                    files_to_deploy.append((full_path, relative_path))
                    
        return files_to_deploy

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