"""
Gerenciamento de configuração
"""
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime

from src.utils.logger import CustomLogger
from src.i18n import I18n
from src.core.constants import (
    CONFIG_DIR,
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_TEMPLATE,
    PROJECT_VERSION,
    VERSION_LOG_DIR
)


class ConfigManager:
    """Gerenciador de configuração"""

    def __init__(self, config_path: Optional[Path] = None):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.config_path = config_path or DEFAULT_CONFIG_FILE

    def load_config(self) -> Dict[str, Any]:
        """
        Carrega configuração do arquivo JSON
        
        Returns:
            Dict com configuração
            
        Raises:
            ValueError: Se o arquivo estiver mal formatado
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Verifica se é igual ao template padrão
                if config == DEFAULT_CONFIG_TEMPLATE:
                    self.logger.warning(self.i18n.get("config.using_default"))
                    return self._handle_default_config()
                
                self.logger.info(self.i18n.get("config.loaded").format(self.config_path))
                return config
            
            self.logger.warning(self.i18n.get("config.not_found").format(self.config_path))
            return self._handle_default_config()
            
        except json.JSONDecodeError as e:
            self.logger.error(self.i18n.get("config.error.decode").format(str(e)))
            raise ValueError(f"Invalid config file: {e}")

    def _handle_default_config(self) -> Dict[str, Any]:
        """Cria e retorna configuração padrão"""
        self.logger.info(self.i18n.get("config.creating_default"))
        self.save_config(DEFAULT_CONFIG_TEMPLATE)
        return DEFAULT_CONFIG_TEMPLATE

    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Salva configuração em arquivo JSON
        
        Args:
            config: Configuração a ser salva
        """
        try:
            # Garante que o diretório existe
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Cria backup do arquivo existente
            if self.config_path.exists():
                backup_dir = VERSION_LOG_DIR / "backups"
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                backup_path = backup_dir / f"config_{datetime.now():%Y%m%d_%H%M%S}.json"
                self.config_path.rename(backup_path)
            
            # Adiciona versão atual
            config["version"] = PROJECT_VERSION
            
            # Salva nova configuração
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            self.logger.info(self.i18n.get("config.saved").format(self.config_path))
            
        except Exception as e:
            self.logger.error(self.i18n.get("config.error.save").format(str(e)))
            raise

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Valida estrutura da configuração
        
        Args:
            config: Configuração a ser validada
            
        Returns:
            True se válida, False caso contrário
        """
        # Verifica campos obrigatórios
        if not all(key in config for key in DEFAULT_CONFIG_TEMPLATE.keys()):
            return False

        # Verifica hosts
        for host, host_config in config.get("hosts", {}).items():
            if not self._validate_host_config(host_config):
                return False

        return True

    def _validate_host_config(self, host_config: Dict[str, Any]) -> bool:
        """Valida configuração de um host específico"""
        # Verifica protocolo
        if "protocol" not in host_config:
            return False
            
        # Verifica caminhos obrigatórios
        if "source_path" not in host_config or "dest_path" not in host_config:
            return False
            
        # Verifica campos específicos por protocolo
        protocol = host_config["protocol"]
        if protocol in ["ssh", "ftp"]:
            if "host" not in host_config or "user" not in host_config:
                return False
                
            if protocol == "ssh" and not ("password" in host_config or "key_path" in host_config):
                return False
                
            if protocol == "ftp" and "password" not in host_config:
                return False

        return True

    def get_host_config(self, config: Dict[str, Any], host: str) -> Dict[str, Any]:
        """Retorna configuração de um host específico"""
        if host not in config["hosts"]:
            raise ValueError(self.i18n.get("config.error.host_not_found").format(host))
        return config["hosts"][host]

    def update_host_config(
        self,
        config: Dict[str, Any],
        host: str,
        host_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Atualiza configuração de um host"""
        if not self._validate_host_config(host_config):
            raise ValueError(self.i18n.get("config.error.invalid_host"))
            
        config["hosts"][host] = host_config
        self.save_config(config)
        return config 