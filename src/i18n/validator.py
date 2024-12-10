"""
Validador de arquivos de tradução
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Set
from src.utils.logger import CustomLogger


class LanguageValidator:
    """Validador de arquivos de idioma"""

    def __init__(self):
        self.logger = CustomLogger.get_logger(__name__)
        self.lang_dir = Path(__file__).parent / "lang"
        self.languages: Dict[str, Dict] = {}
        self.errors: List[str] = []

    def load_language_file(self, lang_code: str) -> dict:
        """Carrega um arquivo de idioma"""
        file_path = self.lang_dir / f"{lang_code}.json"
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"Erro ao carregar {lang_code}: {str(e)}")
            return {}

    def _get_all_keys(self, data: Dict, prefix: str = "") -> Set[str]:
        """Obtém todas as chaves de um dicionário aninhado"""
        keys = set()
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                keys.update(self._get_all_keys(value, full_key))
            else:
                keys.add(full_key)
        return keys

    def validate_languages(self) -> Tuple[bool, List[str]]:
        """Valida todos os arquivos de idioma"""
        # Carrega todos os arquivos de idioma
        for lang_file in self.lang_dir.glob("*.json"):
            lang_code = lang_file.stem
            self.languages[lang_code] = self.load_language_file(lang_code)

        if len(self.languages) < 2:
            self.errors.append("Necessário pelo menos 2 arquivos de idioma")
            return False, self.errors

        # Usa o primeiro idioma como referência
        reference_lang = next(iter(self.languages.keys()))
        reference_keys = self._get_all_keys(self.languages[reference_lang])

        # Compara com outros idiomas
        for lang_code, translations in self.languages.items():
            if lang_code == reference_lang:
                continue

            current_keys = self._get_all_keys(translations)

            # Verifica chaves faltantes
            missing_keys = reference_keys - current_keys
            if missing_keys:
                self.errors.append(
                    f"Chaves faltando em {lang_code}: {', '.join(sorted(missing_keys))}"
                )

            # Verifica chaves extras
            extra_keys = current_keys - reference_keys
            if extra_keys:
                self.errors.append(
                    f"Chaves extras em {lang_code}: {', '.join(sorted(extra_keys))}"
                )

        return len(self.errors) == 0, self.errors

    def validate_format_strings(self) -> None:
        """Valida strings de formatação entre os idiomas"""
        for lang_code, translations in self.languages.items():
            self._validate_format_strings_recursive(translations, "", lang_code)

    def _validate_format_strings_recursive(
        self, data: Dict[str, Any], prefix: str, lang_code: str
    ) -> None:
        """Valida strings de formatação recursivamente"""
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self._validate_format_strings_recursive(value, full_key, lang_code)
            elif isinstance(value, str):
                try:
                    # Tenta formatar a string com valores dummy
                    value.format(**{f"param{i}": i for i in range(10)})
                except Exception as e:
                    self.errors.append(
                        f"Erro de formatação em {lang_code}.{full_key}: {str(e)}"
                    )
