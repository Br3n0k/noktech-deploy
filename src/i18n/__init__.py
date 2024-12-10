"""
Sistema de internacionalização
"""
import json
from pathlib import Path
from typing import Dict, Any

from src.core.constants import LANG_DIR


class I18n:
    """Gerenciador de internacionalização"""

    def __init__(self, lang: str = "pt_br"):
        self.lang = lang
        self.translations = self.load_translations()

    def load_translations(self) -> Dict[str, Any]:
        """Carrega traduções do arquivo JSON"""
        lang_file = LANG_DIR / f"{self.lang}.json"
        if not lang_file.exists():
            raise FileNotFoundError(f"Translation file not found: {lang_file}")

        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key: str) -> str:
        """Retorna a tradução para a chave especificada"""
        return self.translations.get(key, f"Missing translation for {key}")
