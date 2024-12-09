import json
from pathlib import Path
from typing import Dict, List, Tuple


class LanguageValidator:
    def __init__(self):
        self.lang_dir = Path(__file__).parent / "lang"
        self.languages = {}
        self.errors = []

    def load_language_file(self, lang_code: str) -> Dict:
        """Carrega um arquivo de idioma"""
        file_path = self.lang_dir / f"{lang_code}.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.errors.append(f"Erro ao carregar {lang_code}: {str(e)}")
            return {}

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
        reference_keys = set(self.languages[reference_lang].keys())

        # Compara com outros idiomas
        for lang_code, translations in self.languages.items():
            if lang_code == reference_lang:
                continue

            current_keys = set(translations.keys())

            # Verifica chaves faltantes
            missing_keys = reference_keys - current_keys
            if missing_keys:
                self.errors.append(
                    f"Chaves faltando em {lang_code}: {', '.join(missing_keys)}"
                )

            # Verifica chaves extras
            extra_keys = current_keys - reference_keys
            if extra_keys:
                self.errors.append(
                    f"Chaves extras em {lang_code}: {', '.join(extra_keys)}"
                )

        return len(self.errors) == 0, self.errors
