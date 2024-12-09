import os
import shutil
from src.deployers.base_deployer import BaseDeployer


class LocalDeployer(BaseDeployer):
    def __init__(self, dest_path):
        super().__init__()
        self.dest_path = dest_path

    async def connect(self):
        pass  # Local não precisa conectar

    async def disconnect(self):
        pass  # Local não precisa desconectar

    async def ensure_remote_dir(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    async def file_exists(self, path):
        return os.path.exists(path)

    async def _deploy_file(self, src, dest):
        await self.ensure_remote_dir(dest)
        shutil.copy2(src, dest)

    async def handle_change(self, path, event_type):
        if event_type == "created" or event_type == "modified":
            await self._deploy_file(path, os.path.join(self.dest_path, path))
        elif event_type == "deleted":
            try:
                os.remove(os.path.join(self.dest_path, path))
            except FileNotFoundError:
                pass
