from src.core.file_manager import FileManager


class BaseDeployer:
    def __init__(self, host=None, user=None, **kwargs):
        self.host = host
        self.user = user
        self.ignore_rules = None
        self.file_manager = FileManager()

    async def connect(self):
        pass

    async def disconnect(self):
        pass
