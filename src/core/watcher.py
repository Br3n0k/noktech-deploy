from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable, Optional, Dict
import time
import os
from .ignore_rules import IgnoreRules
from ..utils.logger import Logger

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, 
                 callback: Callable, 
                 ignore_rules: Optional[IgnoreRules] = None,
                 logger: Optional[Logger] = None):
        self.callback = callback
        self.ignore_rules = ignore_rules
        self.logger = logger or Logger()
        self._processing = False
        self._pending_events: Dict[str, str] = {}

    def on_any_event(self, event):
        if event.is_directory:
            return
            
        if self.ignore_rules and self.ignore_rules.should_ignore(event.src_path):
            return
            
        # Armazena o evento mais recente para cada arquivo
        self._pending_events[event.src_path] = event.event_type
        
        # Processa eventos pendentes se não estiver processando
        if not self._processing:
            self._process_pending_events()

    def _process_pending_events(self):
        """Processa eventos pendentes com debounce"""
        self._processing = True
        
        try:
            # Pequeno delay para agrupar eventos
            time.sleep(0.1)
            
            # Processa eventos acumulados
            for path, event_type in self._pending_events.items():
                try:
                    self.callback(path, event_type)
                except Exception as e:
                    self.logger.error(f"Erro ao processar evento {event_type} para {path}: {str(e)}")
                    
            self._pending_events.clear()
            
        finally:
            self._processing = False

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

    def start(self):
        """Inicia o observador de diretório"""
        if self._running:
            return
            
        handler = FileEventHandler(
            self.callback,
            self.ignore_rules,
            self.logger
        )
        
        self.observer.schedule(handler, self.path, recursive=True)
        self.observer.start()
        self._running = True
        
        self.logger.info(f"Iniciando observação do diretório: {self.path}")
        
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            self.logger.error(f"Erro no observador: {str(e)}")
            self.stop()

    def stop(self):
        """Para o observador"""
        self._running = False
        self.observer.stop()
        self.observer.join()
        self.logger.info("Observador finalizado") 