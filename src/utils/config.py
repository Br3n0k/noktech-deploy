import json
from pathlib import Path


class Config:
    def __init__(self, config_file: str = None):
        self.config_file = config_file or self.get_default_config_file()
        self.data = {}
        self.load_config()

    @staticmethod
    def get_default_config_file() -> str:
        """Retorna caminho padrão do arquivo de configuração"""
        return str(Path.home() / ".noktech-deploy" / "config.json")

    def load_config(self):
        """Carrega configurações do arquivo"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
        except json.JSONDecodeError:
            self.data = {}

    def save_config(self):
        """Salva configurações no arquivo"""
        Path(self.config_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key: str, default=None):
        """Obtém valor da configuração"""
        return self.data.get(key, default)

    def set(self, key: str, value):
        """Define valor da configuração"""
        self.data[key] = value
        self.save_config()

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save_config()
