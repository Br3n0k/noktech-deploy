#!/usr/bin/env python
from typing import Dict, List, Optional
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from src.i18n import I18n
from src.scripts.update_version import update_version
from src.core.constants import PROJECT_NAME


class BuildManager:
    def __init__(self) -> None:
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
            "poetry.lock",
            "test_project",
        ]

        # Configurações de build
        self.package_name = PROJECT_NAME
        self.pypi_repo = "https://upload.pypi.org/legacy/"
        self.test_pypi_repo = "https://test.pypi.org/legacy/"

    def _validate_command(
        self, cmd: List[str], allowed_commands: Dict[str, List[str]]
    ) -> None:
        """Valida comando e argumentos"""
        if not cmd:
            raise ValueError("Comando vazio")
        base_cmd = cmd[0]
        if base_cmd not in allowed_commands:
            raise ValueError(f"Comando não permitido: {base_cmd}")
        for arg in cmd[1:]:
            if arg.startswith("-"):
                if not any(
                    allowed_arg in arg for allowed_arg in allowed_commands[base_cmd]
                ):
                    raise ValueError(f"Argumento não permitido: {arg}")

    def _execute_process(
        self, cmd: List[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Executa processo e captura output"""
        if not isinstance(cmd, list) or not all(isinstance(x, str) for x in cmd):
            raise ValueError("Comando deve ser uma lista de strings")
        allowed_commands = {
            "pip": ["install", "uninstall", "--version"],
            "pytest": ["--cov", "--cov-report", "term-missing", "-v", "--verbose"],
            "python": [
                "-m",
                "-V",
                "--version",
                "pytest",
                "--cov",
                "--cov-report",
                "term-missing",
            ],
            "poetry": [
                "install",
                "update",
                "add",
                "remove",
                "--version",
                "--no-dev",
                "-v",
                "--verbose",
                "build",
                "version",
            ],
            "ruff": ["check", "--fix", "--unsafe-fixes"],
            "black": ["."],
            "mypy": ["."],
            "pyinstaller": [
                "--onefile",
                "--name",
                "--distpath",
                "--workpath",
                "--specpath",
                "--clean",
            ],
        }
        self._validate_command(cmd, allowed_commands)
        sanitized_cmd = [str(arg).strip() for arg in cmd]
        try:
            process = subprocess.Popen(  # noqa: S603
                sanitized_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=False,
            )
            output: List[str] = []
            if process.stdout:
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        print(line.rstrip())
                        output.append(line)
            return_code = process.wait()
            if check and return_code != 0:
                raise subprocess.CalledProcessError(
                    return_code, sanitized_cmd, "".join(output)
                )
            return subprocess.CompletedProcess(
                sanitized_cmd, return_code, "".join(output)
            )
        except Exception as e:
            msg = f"Erro ao executar comando {' '.join(sanitized_cmd)}: {str(e)}"
            raise RuntimeError(msg) from e

    def prepare_release(self, version: Optional[str] = None) -> bool:
        """Prepara release para GitHub e PyPI"""
        print(self.i18n.get("build.release"))
        try:
            if version:
                self._run_command(["poetry", "version", version])

            release_dir = self.release_dir / datetime.now().strftime("%Y%m%d_%H%M%S")
            release_dir.mkdir(parents=True, exist_ok=True)

            if (self.dist_dir / f"{self.package_name}.exe").exists():
                shutil.copy2(
                    self.dist_dir / f"{self.package_name}.exe",
                    release_dir / f"{self.package_name}.exe",
                )

            for wheel in self.dist_dir.glob("*.whl"):
                shutil.copy2(wheel, release_dir)

            for tar in self.dist_dir.glob("*.tar.gz"):
                shutil.copy2(tar, release_dir)

            return True
        except Exception as e:
            print(self.i18n.get("build.error.release").format(str(e)))
            return False

    def _run_command(
        self, cmd: list[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Executa comando com output em tempo real"""
        allowed_commands = {
            "pip": ["install", "uninstall", "--version"],
            "pytest": ["--cov", "--cov-report", "term-missing", "-v", "--verbose"],
            "python": [
                "-m",
                "-V",
                "--version",
                "pytest",
                "--cov",
                "--cov-report",
                "term-missing",
            ],
            "poetry": [
                "install",
                "update",
                "add",
                "remove",
                "--version",
                "--no-dev",
                "-v",
                "--verbose",
                "build",
                "version",
            ],
            "ruff": ["check", "--fix", "--unsafe-fixes"],
            "black": ["."],
            "mypy": ["."],
            "pyinstaller": [
                "--onefile",
                "--name",
                "--distpath",
                "--workpath",
                "--specpath",
                "--clean",
            ],
        }
        try:
            self._validate_command(cmd, allowed_commands)
            return self._execute_process(cmd, check)
        except Exception as e:
            raise RuntimeError(
                f"Erro ao executar comando {' '.join(cmd)}: {str(e)}"
            ) from e

    def clean(self) -> bool:
        """Limpa diretórios de build e teste"""
        for dir_name in self.clean_dirs:
            path = Path(dir_name)
            if path.exists():
                try:
                    if path.is_file():
                        path.unlink()
                    else:
                        shutil.rmtree(path)
                except Exception as e:
                    print(f"Erro ao remover {dir_name}: {e}")
                    return False
        return True

    def test(self) -> bool:
        """Executa testes"""
        try:
            self._run_command(
                ["python", "-m", "pytest", "--cov", "--cov-report", "term-missing"]
            )
            return True
        except Exception as e:
            print(self.i18n.get("build.error.test").format(str(e)))
            return False

    def lint(self) -> bool:
        """Executa linters"""
        print(self.i18n.get("build.lint"))
        try:
            # Roda ruff com --fix primeiro
            self._run_command(["ruff", "check", "--fix", "."])

            # Depois os outros linters
            self._run_command(["black", "."])
            self._run_command(["mypy", "."])
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
            self._run_command(
                [
                    "pyinstaller",
                    "--name",
                    self.package_name,
                    "--onefile",
                    "--clean",
                    "src/main.py",
                ]
            )
            return True
        except Exception as e:
            print(self.i18n.get("build.error.exe").format(str(e)))
            return False

    def check_dependencies(self) -> bool:
        """Verifica e instala dependências"""
        try:
            self._run_command(["poetry", "install"])
            return True
        except Exception as e:
            print(f"Error checking dependencies: {e}")
            return False

    def cmd_version(self, new_version: str):
        """Atualiza a versão do projeto"""
        update_version(new_version)
        print(f"✅ Versão atualizada para {new_version}")

    def build_all(self, version: str | None = None) -> bool:
        """Executa processo completo de build"""
        if version:
            self.cmd_version(version)

        steps = [
            self.clean,
            self.check_dependencies,
            self.lint,
            self.test,
            self.build_package,
            self.build_executable,
            lambda: self.prepare_release(version),
        ]

        for step in steps:
            if not step():
                return False

        print(self.i18n.get("build.complete"))
        return True


def main():
    builder = BuildManager()

    if len(sys.argv) < 2:
        print(
            "Usage: python build.py "
            "[clean|deps|test|lint|package|exe|release|version|all] [version]"
        )
        sys.exit(1)

    command = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None

    commands = {
        "clean": builder.clean,
        "deps": builder.check_dependencies,
        "test": builder.test,
        "lint": builder.lint,
        "package": builder.build_package,
        "exe": builder.build_executable,
        "release": lambda: builder.prepare_release(version),
        "version": lambda: (
            builder.cmd_version(version)
            if version
            else print("Erro: Informe a nova versão")
        ),
        "all": lambda: builder.build_all(version),
    }

    if command not in commands:
        print(f"Invalid command: {command}")
        sys.exit(1)

    success = commands[command]()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
