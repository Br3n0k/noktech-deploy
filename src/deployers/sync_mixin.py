from pathlib import Path


class SyncMixin:
    """Mixin para sincronização de arquivos entre fonte e destino"""

    async def sync_files(self, source_path: str, dest_path: str):
        """
        Sincroniza arquivos da fonte para o destino

        Args:
            source_path: Caminho do diretório fonte
            dest_path: Caminho do diretório destino
        """
        source = Path(source_path)
        dest = Path(dest_path)

        if not source.exists():
            raise FileNotFoundError(f"Diretório fonte não encontrado: {source}")

        # Cria diretório de destino se não existir
        await self.ensure_remote_dir(dest)

        # Sincroniza arquivos recursivamente
        for src_file in source.rglob("*"):
            if src_file.is_file() and not self._should_ignore(src_file):
                try:
                    rel_path = src_file.relative_to(source)
                    dst_file = dest / rel_path

                    # Verifica se precisa atualizar
                    should_update = True
                    if await self.file_exists(dst_file):
                        src_mtime = src_file.stat().st_mtime
                        dst_mtime = await self.get_remote_mtime(dst_file)
                        should_update = src_mtime > dst_mtime

                    if should_update:
                        await self.ensure_remote_dir(dst_file.parent)
                        await self._deploy_file(src_file, dst_file)
                        self.logger.debug(f"Atualizado: {rel_path}")

                except Exception as e:
                    self.logger.warning(f"Erro ao sincronizar {src_file}: {e}")
                    continue
