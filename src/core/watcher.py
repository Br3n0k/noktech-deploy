import asyncio
from pathlib import Path
from typing import List, AsyncGenerator
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class DirectoryWatcher:
    def __init__(self, path: Path, patterns: List[str] = None, 
                 ignore_patterns: List[str] = None, interval: float = 1.0):
        self.path = str(path)
        self.patterns = patterns or ["*"]
        self.ignore_patterns = ignore_patterns or []
        self.interval = interval
        self.observer = None
        self.running = False
        self.changes: List[str] = []
        self._change_event = asyncio.Event()

    def _on_change(self, event: FileSystemEvent):
        """Callback para eventos de alteração"""
        if event.is_directory:
            return
            
        # Verifica se o arquivo corresponde aos padrões
        file_path = event.src_path
        if any(p in file_path for p in self.ignore_patterns):
            return
            
        if file_path not in self.changes:
            self.changes.append(file_path)
            self._change_event.set()

    async def watch(self) -> AsyncGenerator[List[str], None]:
        """Gera lista de arquivos alterados"""
        if not self.running:
            await self.start()
            
        while self.running:
            await self._change_event.wait()
            changes = self.changes.copy()
            self.changes.clear()
            self._change_event.clear()
            yield changes
            await asyncio.sleep(self.interval)

    async def start(self):
        """Inicia o monitoramento do diretório"""
        if self.running:
            return
        
        self.observer = Observer()
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = self._on_change
        event_handler.on_created = self._on_change
        
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        self.running = True

    async def stop(self):
        """Para o monitoramento do diretório"""
        if not self.running:
            return
        
        self.observer.stop()
        self.observer.join()
        self.running = False
        self._change_event.set()  # Libera qualquer wait pendente
