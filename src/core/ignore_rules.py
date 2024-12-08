from typing import List, Optional, Set
import os
import fnmatch
import re

class IgnoreRules:
    def __init__(self, 
                 rules: Optional[List[str]] = None, 
                 ignore_file: Optional[str] = None,
                 default_ignores: Optional[List[str]] = None):
        self.patterns: Set[str] = set()
        self.negated_patterns: Set[str] = set()
        
        # Padrões padrão para ignorar
        if default_ignores is None:
            default_ignores = [
                '.git/',
                '.gitignore',
                '__pycache__/',
                '*.pyc',
                '.DS_Store',
                'node_modules/',
                'venv/',
                '.env'
            ]
        
        # Adiciona padrões padrão
        for pattern in default_ignores:
            self.add_pattern(pattern)
            
        # Carrega do arquivo .gitignore
        if ignore_file:
            self.load_from_file(ignore_file)
            
        # Adiciona padrões extras
        if rules:
            for rule in rules:
                self.add_pattern(rule)

    def load_from_file(self, file_path: str) -> None:
        """Carrega padrões de um arquivo de ignore"""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.add_pattern(line)

    def add_pattern(self, pattern: str) -> None:
        """Adiciona um padrão de ignore"""
        pattern = pattern.strip()
        if not pattern or pattern.startswith('#'):
            return
            
        # Trata padrões negados (começando com !)
        if pattern.startswith('!'):
            self.negated_patterns.add(pattern[1:])
        else:
            self.patterns.add(pattern)

    def should_ignore(self, path: str) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
        path = os.path.normpath(path).replace('\\', '/')
        
        # Primeiro verifica padrões negados (exceções)
        for pattern in self.negated_patterns:
            if self._matches_pattern(path, pattern):
                return False
        
        # Depois verifica padrões normais
        for pattern in self.patterns:
            if self._matches_pattern(path, pattern):
                return True
                
        return False

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Verifica se um caminho corresponde a um padrão"""
        # Remove / inicial se existir
        if pattern.startswith('/'):
            pattern = pattern[1:]
            
        # Trata padrões de diretório (terminando com /)
        if pattern.endswith('/'):
            pattern = pattern[:-1]
            if os.path.isfile(path):
                return False
                
        # Converte padrão glob para regex
        regex_pattern = fnmatch.translate(pattern)
        return bool(re.match(regex_pattern, path)) 