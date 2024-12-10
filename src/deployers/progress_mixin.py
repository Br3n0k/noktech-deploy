"""
Mixin para gerenciamento de progresso
"""
from pathlib import Path
from typing import Protocol, List
from src.core.progress import ProgressManager


class ProgressMixin(Protocol):
    """Mixin para gerenciamento de progresso em deployers"""

    def __init__(self) -> None:
        self.progress = ProgressManager()

    async def calculate_transfer_size(self, files: List[Path]) -> int:
        """Calcula tamanho total dos arquivos a serem transferidos"""
        total_size = 0
        for file in files:
            if file.is_file():
                total_size += file.stat().st_size
        return total_size

    async def prepare_transfer(self, files: List[Path]) -> None:
        """Prepara transferência calculando tamanho total"""
        total_size = await self.calculate_transfer_size(files)
        self.progress.start_transfer(total_size, len(files))

    async def update_progress(self, file: Path, bytes_transferred: int) -> None:
        """Atualiza progresso da transferência"""
        self.progress.update_progress(bytes_transferred, str(file))

    async def complete_transfer(self) -> None:
        """Finaliza transferência"""
        self.progress.complete() 