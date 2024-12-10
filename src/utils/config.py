import json
from pathlib import Path
from typing import Dict, Any
from src.core.constants import DEFAULT_CONFIG_TEMPLATE
from src.utils.logger import Logger
from src.i18n import I18n


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

def create_default_config(config_path: Path) -> None:
    """Cria arquivo de configuração padrão"""
    logger = Logger(__name__)
    i18n = I18n()
    
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG_TEMPLATE, f, indent=4)
            
        logger.info(i18n.get("config.created").format(str(config_path)))
        
    except Exception as e:
        logger.error(i18n.get("config.error").format(str(e)))
        raise

def validate_config(config: Dict[str, Any]) -> bool:
    """Valida configuração"""
    logger = Logger(__name__)
    i18n = I18n()
    
    try:
        # Verifica campos obrigatórios
        if "hosts" not in config:
            logger.error(i18n.get("config.error").format("Campo 'hosts' não encontrado"))
            return False
            
        # Valida cada host
        for host_name, host_config in config["hosts"].items():
            if not isinstance(host_config, dict):
                logger.error(i18n.get("config.error").format(
                    f"Configuração inválida para host '{host_name}'"))
                return False
                
            # Verifica campos obrigatórios do host
            required_fields = ["protocol", "source_path", "dest_path"]
            for field in required_fields:
                if field not in host_config:
                    logger.error(i18n.get("config.error").format(
                        f"Campo '{field}' não encontrado para host '{host_name}'"))
                    return False
                    
            # Valida configuração de watch
            watch_config = host_config.get("watch", {})
            if watch_config.get("enabled", False):
                if "interval" in watch_config and not isinstance(watch_config["interval"], (int, float)):
                    logger.error(i18n.get("config.error").format(
                        f"Intervalo de watch inválido para host '{host_name}'"))
                    return False
                    
                if "patterns" in watch_config and not isinstance(watch_config["patterns"], list):
                    logger.error(i18n.get("config.error").format(
                        f"Padrões de watch inválidos para host '{host_name}'"))
                    return False
                    
                if "ignore_patterns" in watch_config and not isinstance(watch_config["ignore_patterns"], list):
                    logger.error(i18n.get("config.error").format(
                        f"Padrões de ignore inválidos para host '{host_name}'"))
                    return False
        
        return True
        
    except Exception as e:
        logger.error(i18n.get("config.error").format(str(e)))
        return False
