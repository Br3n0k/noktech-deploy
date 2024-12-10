"""
Gerenciador de progresso para operações de deploy
"""
from typing import Optional, Dict, Any
import time
import sys
from dataclasses import dataclass
from datetime import datetime
from threading import Lock

from src.utils.logger import CustomLogger
from src.i18n import I18n


@dataclass
class TransferStats:
    """Estatísticas de transferência"""
    bytes_total: int = 0
    bytes_transferred: int = 0
    start_time: float = 0.0
    current_file: str = ""
    files_total: int = 0
    files_processed: int = 0

    @property
    def progress(self) -> float:
        """Retorna o progresso em porcentagem"""
        return (self.bytes_transferred / self.bytes_total * 100) if self.bytes_total > 0 else 0

    @property
    def speed(self) -> float:
        """Retorna a velocidade em bytes/segundo"""
        elapsed = time.time() - self.start_time
        return self.bytes_transferred / elapsed if elapsed > 0 else 0

    @property
    def eta(self) -> float:
        """Retorna o tempo estimado restante em segundos"""
        if self.speed == 0:
            return 0
        return (self.bytes_total - self.bytes_transferred) / self.speed


class ProgressManager:
    """Gerenciador de progresso para operações de deploy"""

    def __init__(self):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.stats = TransferStats()
        self._lock = Lock()
        self._last_update = 0
        self._update_interval = 0.1  # segundos

    def start_transfer(self, total_bytes: int, total_files: int) -> None:
        """Inicia uma nova transferência"""
        with self._lock:
            self.stats = TransferStats(
                bytes_total=total_bytes,
                files_total=total_files,
                start_time=time.time()
            )
        self._print_progress()

    def update_progress(self, bytes_transferred: int, current_file: str) -> None:
        """Atualiza o progresso da transferência"""
        with self._lock:
            self.stats.bytes_transferred += bytes_transferred
            self.stats.current_file = current_file
            self.stats.files_processed += 1

        # Limita atualizações de tela
        current_time = time.time()
        if current_time - self._last_update >= self._update_interval:
            self._print_progress()
            self._last_update = current_time

    def _format_size(self, size: float) -> str:
        """Formata tamanho em bytes para formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}TB"

    def _format_time(self, seconds: float) -> str:
        """Formata tempo em segundos para formato legível"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        minutes = seconds / 60
        if minutes < 60:
            return f"{minutes:.0f}m {seconds % 60:.0f}s"
        hours = minutes / 60
        return f"{hours:.0f}h {minutes % 60:.0f}m"

    def _print_progress(self) -> None:
        """Imprime barra de progresso no console"""
        width = 50
        progress = int(width * self.stats.progress / 100)
        
        # Formata a barra de progresso
        bar = f"[{'=' * progress}{' ' * (width - progress)}]"
        
        # Formata estatísticas
        stats = (
            f"{self.stats.progress:.1f}% "
            f"| {self._format_size(self.stats.speed)}/s "
            f"| ETA: {self._format_time(self.stats.eta)} "
            f"| {self.stats.files_processed}/{self.stats.files_total} files"
        )

        # Limpa linha anterior e imprime progresso
        sys.stdout.write("\r" + " " * 80 + "\r")  # Limpa linha
        sys.stdout.write(f"{bar} {stats}")
        sys.stdout.flush()

        # Log para arquivo
        if self.stats.progress % 10 == 0:  # Log a cada 10%
            self.logger.info(
                f"Progress: {self.stats.progress:.1f}% "
                f"| Speed: {self._format_size(self.stats.speed)}/s "
                f"| File: {self.stats.current_file}"
            )

    def complete(self) -> None:
        """Finaliza a transferência"""
        self._print_progress()
        sys.stdout.write("\n")
        sys.stdout.flush()
        
        # Log final
        elapsed = time.time() - self.stats.start_time
        self.logger.info(
            f"Transfer completed: {self._format_size(self.stats.bytes_total)} "
            f"in {self._format_time(elapsed)} "
            f"({self._format_size(self.stats.speed)}/s)"
        )
        