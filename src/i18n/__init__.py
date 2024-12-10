import json
import os
from pathlib import Path
from typing import Dict, Any

class I18n:
    _instance = None
    _strings: Dict[str, str] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_strings()
        return cls._instance
        
    def _load_strings(self):
        """Carrega strings de tradução"""
        try:
            lang = os.getenv("LANG", "pt_BR").lower()[:5]
            lang_file = Path(__file__).parent / "lang" / f"{lang}.json"
            
            if not lang_file.exists():
                lang_file = Path(__file__).parent / "lang" / "pt_br.json"
                
            with open(lang_file, 'r', encoding='utf-8') as f:
                self._strings = json.load(f)
                
        except Exception as e:
            print(f"Erro ao carregar traduções: {str(e)}")
            self._strings = {}
            
    def get(self, key: str, default: str = "") -> str:
        """Obtém string traduzida"""
        return self._strings.get(key, default)
        
    def format(self, key: str, *args: Any, **kwargs: Any) -> str:
        """Formata string traduzida com argumentos"""
        text = self.get(key)
        if not text:
            return key
            
        try:
            return text.format(*args, **kwargs)
        except Exception:
            return text
