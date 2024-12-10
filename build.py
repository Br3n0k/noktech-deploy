#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from src.i18n import I18n

class BuildManager:
    def __init__(self):
        self.i18n = I18n()
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        self.release_dir = self.root_dir / "release"
        
        # Diretórios para limpar
        self.clean_dirs = [
            "dist", 
            "build", 
            "*.egg-info",
            ".pytest_cache", 
            ".ruff_cache", 
            ".mypy_cache",
            "htmlcov", 
            "__pycache__",
            "*/__pycache__",
            "*/*/__pycache__",
            "*/*/*/__pycache__",
            "*.pyc",
            ".coverage", 
            ".DS_Store",
            "*.log",
            "logs/*",
            "poetry.lock"
        ]
        
        # Configurações de build
        self.package_name = "noktech-deploy"
        self.pypi_repo = "https://upload.pypi.org/legacy/"
        self.test_pypi_repo = "https://test.pypi.org/legacy/"

    def _run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Executa comando com output em tempo real"""
        return subprocess.run(cmd, check=check, text=True)

    def clean(self) -> bool:
        """Limpa diretórios de build"""
        print(self.i18n.get("build.clean"))
        try:
            for pattern in self.clean_dirs:
                for path in self.root_dir.glob(pattern):
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def check_dependencies(self) -> bool:
        """Verifica e instala dependências"""
        print(self.i18n.get("build.deps"))
        try:
            self._run_command(["poetry", "--version"])
            self._run_command(["poetry", "install"])
            self._run_command(["poetry", "run", "pip", "install", "build", "twine"])
            return True
        except Exception as e:
            print(self.i18n.get("build.error.deps").format(str(e)))
            return False

    def run_tests(self) -> bool:
        """Executa suite de testes"""
        print(self.i18n.get("build.test"))
        try:
            self._run_command(["poetry", "run", "pytest", "--cov", "--cov-report=html"])
            return True
        except Exception as e:
            print(self.i18n.get("build.error.test").format(str(e)))
            return False

    def lint(self) -> bool:
        """Executa verificações de código"""
        print(self.i18n.get("build.lint"))
        try:
            self._run_command(["poetry", "run", "ruff", "check", "."])
            self._run_command(["poetry", "run", "black", "."])
            self._run_command(["poetry", "run", "mypy", "."])
            return True
        except Exception as e:
            print(self.i18n.get("build.error.lint").format(str(e)))
            return False

    def build_package(self) -> bool:
        """Gera pacote para PyPI"""
        print(self.i18n.get("build.package"))
        try:
            self._run_command(["poetry", "build"])
            return True
        except Exception as e:
            print(self.i18n.get("build.error.package").format(str(e)))
            return False

    def build_executable(self) -> bool:
        """Gera executável"""
        print(self.i18n.get("build.exe"))
        try:
            self._run_command([
                "poetry", "run", "pyinstaller",
                "--name", self.package_name,
                "--onefile",
                "--clean",
                "src/main.py"
            ])
            return True
        except Exception as e:
            print(self.i18n.get("build.error.exe").format(str(e)))
            return False

    def prepare_release(self, version: Optional[str] = None) -> bool:
        """Prepara release para GitHub e PyPI"""
        print(self.i18n.get("build.release"))
        try:
            if version:
                self._run_command(["poetry", "version", version])
            
            # Cria diretório de release
            release_dir = self.release_dir / datetime.now().strftime("%Y%m%d_%H%M%S")
            release_dir.mkdir(parents=True, exist_ok=True)
            
            # Copia artefatos
            if (self.dist_dir / f"{self.package_name}.exe").exists():
                shutil.copy2(
                    self.dist_dir / f"{self.package_name}.exe",
                    release_dir / f"{self.package_name}.exe"
                )
            
            for wheel in self.dist_dir.glob("*.whl"):
                shutil.copy2(wheel, release_dir)
            
            for tar in self.dist_dir.glob("*.tar.gz"):
                shutil.copy2(tar, release_dir)
            
            return True
        except Exception as e:
            print(self.i18n.get("build.error.release").format(str(e)))
            return False

    def build_all(self, version: Optional[str] = None) -> bool:
        """Executa processo completo de build"""
        steps = [
            self.clean,
            self.check_dependencies,
            self.lint,
            self.run_tests,
            self.build_package,
            self.build_executable,
            lambda: self.prepare_release(version)
        ]
        
        for step in steps:
            if not step():
                return False
        
        print(self.i18n.get("build.complete"))
        return True

def main():
    builder = BuildManager()
    
    if len(sys.argv) < 2:
        print("Usage: python build.py [clean|deps|test|lint|package|exe|release|all] [version]")
        sys.exit(1)
    
    command = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None
    
    commands = {
        "clean": builder.clean,
        "deps": builder.check_dependencies,
        "test": builder.run_tests,
        "lint": builder.lint,
        "package": builder.build_package,
        "exe": builder.build_executable,
        "release": lambda: builder.prepare_release(version),
        "all": lambda: builder.build_all(version)
    }
    
    if command not in commands:
        print(f"Invalid command: {command}")
        sys.exit(1)
    
    success = commands[command]()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
