from typing import Dict
import json
import locale
import os

class I18n:
    def __init__(self):
        self.current_lang = self._detect_language()
        self.translations = self._load_translations()

    def _detect_language(self) -> str:
        """Detecta idioma do sistema"""
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang and sys_lang.lower().startswith('pt'):
                return 'pt_br'
            return 'en_us'  # fallback
        except:
            return 'en_us'

    def _load_translations(self) -> Dict:
        """Carrega arquivo de tradução"""
        lang_file = os.path.join(
            os.path.dirname(__file__), 
            'lang', 
            f'{self.current_lang}.json'
        )
        
        if not os.path.exists(lang_file):
            lang_file = os.path.join(
                os.path.dirname(__file__), 
                'lang', 
                'en_us.json'
            )
            
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get(self, key: str) -> str:
        """Retorna texto traduzido"""
        return self.translations.get(key, key) 