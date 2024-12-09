import os
import fnmatch


class IgnoreRules:
    DEFAULT_RULES = [
        ".git/*",
        "__pycache__/*",
        "*.pyc",
        ".env",
        ".venv/*",
        "node_modules/*",
    ]

    def __init__(self, rules=None, ignore_file=None):
        self.rules = list(self.DEFAULT_RULES)
        if rules:
            self.rules.extend(rules)
        if ignore_file and os.path.exists(ignore_file):
            with open(ignore_file) as f:
                self.rules.extend(line.strip() for line in f)

    def should_ignore(self, path: str) -> bool:
        path = path.replace("\\", "/")

        # Primeiro verifica regras de negação
        for rule in self.rules:
            if rule.startswith("!"):
                if fnmatch.fnmatch(path, rule[1:]):
                    return False

        # Depois verifica regras normais
        for rule in self.rules:
            if not rule.startswith("!"):
                if fnmatch.fnmatch(path, rule):
                    return True

        return False
