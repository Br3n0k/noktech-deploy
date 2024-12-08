import os
import json
from typing import Dict, Any, Optional

class Config:
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self.get_default_config_file()
        self.config: Dict[str, Any] = {}
        self.load()

    @staticmethod
    def get_default_config_file() -> str:
        """Retorna o caminho padrão para o arquivo de configuração"""
        config_dir = os.path.expanduser('~/.noktech-deploy')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'config.json')

    def load(self) -> None:
        """Carrega configurações do arquivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Erro ao carregar configurações: {str(e)}")
                self.config = {}

    def save(self) -> None:
        """Salva configurações no arquivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor de configuração"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Define um valor de configuração"""
        self.config[key] = value
        self.save()

    def delete(self, key: str) -> None:
        """Remove uma configuração"""
        if key in self.config:
            del self.config[key]
            self.save() 