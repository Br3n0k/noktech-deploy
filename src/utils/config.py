from __future__ import annotations
from pathlib import Path
import json
from typing import Dict, Any, Optional

from src.core.constants import DEFAULT_CONFIG_TEMPLATE, DEFAULT_CONFIG_FILE
from src.utils.logger import CustomLogger


class ConfigManager:
    """Classe para gerenciar configurações"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or DEFAULT_CONFIG_FILE
        self.logger = CustomLogger.get_logger(__name__)

    def load_config(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo json"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.logger.info(f"Configuração carregada de {self.config_path}")
                return config
        except FileNotFoundError:
            self.logger.warning(f"Arquivo de configuração não encontrado: {self.config_path}")
            self.logger.info("Criando configuração padrão")
            self.save_config(DEFAULT_CONFIG_TEMPLATE)
            return DEFAULT_CONFIG_TEMPLATE
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar JSON: {e}")
            raise ValueError(f"Erro ao carregar arquivo de configuração: {e}")

    def save_config(self, config: Dict[str, Any]) -> None:
        """Salva configuração em arquivo json"""
        try:
            path = Path(self.config_path)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            self.logger.info(f"Configuração salva em {self.config_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração: {e}")
            raise ValueError(f"Erro ao salvar arquivo de configuração: {e}")
