from typing import Dict
import json
import locale
import logging
from pathlib import Path
from .validator import LanguageValidator
import os

logger = logging.getLogger(__name__)


class I18n:
    SUPPORTED_LANGUAGES = {"en_us": "English", "pt_br": "Português"}

    def __init__(self):
        self._validate_languages()
        self.current_lang = self._detect_system_language()
        self.translations = self._load_translations()

    def _validate_languages(self):
        """Valida arquivos de idioma"""
        validator = LanguageValidator()
        is_valid, errors = validator.validate_languages()

        if not is_valid:
            error_msg = "\n".join(errors)
            logger.error(f"Erro na validação de idiomas:\n{error_msg}")
            raise ValueError(f"Arquivos de idioma inválidos:\n{error_msg}")

    def _detect_system_language(self) -> str:
        """Detecta idioma do sistema"""
        try:
            locale.setlocale(locale.LC_ALL, "")
            sys_lang = locale.getlocale()[0]
            if sys_lang:
                if sys_lang.lower().startswith("pt"):
                    return "pt_br"
                return "en_us"  # fallback
        except (locale.Error, TypeError) as e:
            self.logger.warning(f"Erro ao detectar idioma do sistema: {e}")
            return "en_us"

    def _load_translations(self) -> Dict:
        """Carrega arquivo de tradução"""
        lang_file = Path(__file__).parent / "lang" / f"{self.current_lang}.json"

        if not lang_file.exists():
            lang_file = Path(__file__).parent / "lang" / "en_us.json"

        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def get(self, key: str) -> str:
        """Retorna texto traduzido"""
        return self.translations.get(key, key)

    def change_language(self, lang_code: str) -> bool:
        """Muda o idioma do sistema"""
        if lang_code in self.SUPPORTED_LANGUAGES:
            self.current_lang = lang_code
            self.translations = self._load_translations()
            return True
        return False

    def show_language_menu(self):
        """Mostra menu de seleção de idioma"""
        print(
            self.get("language.current").format(
                self.SUPPORTED_LANGUAGES[self.current_lang]
            )
        )
        print(self.get("language.select"))
        for code, name in self.SUPPORTED_LANGUAGES.items():
            print(f"  {code} - {name}")

    def _load_language_file(self, lang: str) -> dict:
        """Carrega arquivo de idioma"""
        try:
            lang_file = os.path.join(os.path.dirname(__file__), "lang", f"{lang}.json")

            with open(lang_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Language file not found: {lang}")
            return self._load_language_file("en_us")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in language file: {lang}")
            return self._load_language_file("en_us")
