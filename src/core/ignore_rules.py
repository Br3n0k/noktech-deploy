from pathlib import Path
from typing import List, Optional
import fnmatch
from src.core.constants import DEFAULT_IGNORE_PATTERNS


class IgnoreRules:
    """Gerencia regras de ignorar arquivos"""

    def __init__(self, patterns: Optional[List[str]] = None) -> None:
        self.patterns = patterns or DEFAULT_IGNORE_PATTERNS
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compila os padrões de ignore"""
        # Mantém os padrões originais para referência
        self._original_patterns = self.patterns
        
        # Converte padrões para lowercase para comparação case-insensitive
        self._compiled_patterns = [pattern.lower() for pattern in self.patterns]

    def should_ignore(self, path: Path) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
        path_str = str(path).lower()
        
        for pattern in self._compiled_patterns:
            if fnmatch.fnmatch(path_str, pattern):
                return True
                
        return False
