"""
Mixin para funcionalidades de sincronização
"""
from pathlib import Path
from typing import Protocol, TypeVar

T = TypeVar("T", bound="SyncMixin")


class SyncMixin(Protocol):
    """Mixin para sincronização de arquivos"""

    async def ensure_remote_dir(self, path: Path) -> None:
        """Garante existência de diretório remoto"""
        ...

    async def sync_file(self, source: Path, dest: Path) -> None:
        """Sincroniza um arquivo"""
        ...

    async def sync_directory(self: T, source: Path, dest: Path) -> None:
        """Sincroniza um diretório inteiro"""
        await self.ensure_remote_dir(dest)
        for item in source.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(source)
                dest_path = dest / rel_path
                await self.sync_file(item, dest_path)
