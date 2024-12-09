#!/usr/bin/env python
import os
import sys
import subprocess
from pathlib import Path
from src.i18n import I18n
import re


class BuildError(Exception):
    """Erro durante o processo de build"""

    pass


class BuildManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.version_file = self.root_dir / "src" / "version.py"
        self.i18n = I18n()
        self.build_files = [
            "*.spec",
            "build.spec",
            "noktech-deploy.spec",
            "setup.py",
            "requirements.txt",
        ]

    def get_current_version(self) -> str:
        """Obtém versão atual do projeto"""
        return subprocess.check_output(["poetry", "version", "-s"], text=True).strip()

    def _update_version_info(self, new_version: str):
        """Atualiza version_info.txt com nova versão"""
        version_parts = [int(x) for x in new_version.split(".")]
        while len(version_parts) < 4:
            version_parts.append(0)

        version_info = Path("version_info.txt")
        content = version_info.read_text()

        # Atualiza filevers e prodvers
        content = re.sub(
            r"filevers=\([^)]+\)",
            f'filevers=({", ".join(map(str, version_parts))})',
            content,
        )
        content = re.sub(
            r"prodvers=\([^)]+\)",
            f'prodvers=({", ".join(map(str, version_parts))})',
            content,
        )

        # Atualiza FileVersion e ProductVersion
        content = re.sub(
            r"FileVersion\', u\'[^\']+\'", f"FileVersion', u'{new_version}'", content
        )
        content = re.sub(
            r"ProductVersion\', u\'[^\']+\'",
            f"ProductVersion', u'{new_version}'",
            content,
        )

        version_info.write_text(content)

    def update_all_versions(self, new_version: str):
        """Atualiza versão em todos os arquivos necessários"""
        # Atualiza pyproject.toml
        subprocess.run(["poetry", "version", new_version], check=True)

        # Atualiza version.py
        version_content = self.version_file.read_text()
        version_content = re.sub(
            r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', version_content
        )
        self.version_file.write_text(version_content)

        # Atualiza version_info.txt
        if Path("version_info.txt").exists():
            self._update_version_info(new_version)

        print(self.i18n.get("release.version_updated").format(new_version))

    def check_dependencies(self) -> bool:
        """Verifica e instala dependências"""
        print(self.i18n.get("release.checking_deps"))
        try:
            subprocess.run(
                ["poetry", "add", "--dev", "ruff", "black", "pytest", "pytest-cov"],
                check=True,
            )
            subprocess.run(["poetry", "install"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(self.i18n.get("build.error.deps").format(str(e)))
            return False

    def clean(self, include_generated=False):
        """Limpa diretórios de build e cache"""
        print(self.i18n.get("build.cleaning"))
        dirs_to_clean = [
            "dist",
            "build",
            ".pytest_cache",
            ".ruff_cache",
            ".mypy_cache",
            "htmlcov",
            "**/__pycache__",
            "site",
        ]

        if include_generated:
            for pattern in self.build_files:
                for f in self.root_dir.glob(pattern):
                    f.unlink(missing_ok=True)

        for dir_pattern in dirs_to_clean:
            try:
                subprocess.run(
                    ["rm", "-rf", dir_pattern],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except subprocess.CalledProcessError:
                os.system(f"rd /s /q {dir_pattern} 2>nul")
        print(self.i18n.get("build.clean_complete"))

    def _build_executable(self):
        """Build do executável usando PyInstaller"""
        print(self.i18n.get("build.executable"))
        subprocess.run(
            [
                "poetry",
                "run",
                "pyinstaller",
                "--name=noktech-deploy",
                "--icon=src/assets/logo.ico",
                "--add-data=src/assets:assets",
                "--onefile",
                "src/deploy_client.py",
            ],
            check=True,
        )

    def _build_docs(self):
        """Build da documentação usando MkDocs"""
        print(self.i18n.get("build.docs"))
        subprocess.run(["poetry", "run", "mkdocs", "build"], check=True)

    def build_all(self):
        """Executa todos os passos do build em sequência"""
        try:
            if not self.check_dependencies():
                sys.exit(1)

            self.clean(include_generated=True)

            print(self.i18n.get("build.formatting"))
            subprocess.run(["poetry", "run", "black", "."], check=False)
            subprocess.run(
                ["poetry", "run", "ruff", "check", ".", "--fix"], check=False
            )

            print(self.i18n.get("build.testing"))
            subprocess.run(["poetry", "run", "pytest", "--cov=src"], check=True)

            print(self.i18n.get("build.packaging"))
            subprocess.run(["poetry", "build"], check=True)

            self._build_executable()
            self._build_docs()

            print(self.i18n.get("build.complete"))

        except subprocess.CalledProcessError as e:
            print(self.i18n.get("build.error.build").format(str(e)))
            sys.exit(1)

    def release(self):
        """Executa processo completo de release"""
        try:
            if not all(Path(f).exists() for f in ["CHANGELOG.md", "README.md"]):
                raise Exception(self.i18n.get("release.missing_files"))

            print(
                self.i18n.get("release.current_version").format(
                    self.get_current_version()
                )
            )
            new_version = input(self.i18n.get("release.new_version"))

            if new_version.strip():
                self.update_all_versions(new_version)
            else:
                self.update_all_versions(self.get_current_version())

            print(self.i18n.get("release.starting").format(self.get_current_version()))
            self.build_all()

            version = self.get_current_version()
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"release: version {version}"], check=True
            )
            subprocess.run(["git", "tag", f"v{version}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            subprocess.run(["git", "push", "origin", f"v{version}"], check=True)

            print(self.i18n.get("release.complete").format(version))

        except Exception as e:
            print(self.i18n.get("release.error").format(str(e)))
            sys.exit(1)

    def show_usage(self):
        print(self.i18n.get("build.usage"))
        print(self.i18n.get("build.commands"))
        for cmd in ["clean", "release", "exe", "package", "test", "docs", "all"]:
            print(self.i18n.get(f"build.cmd.{cmd}"))
        sys.exit(1)

    def docs(self):
        """Gera documentação"""
        print("\n📚 Gerando documentação...")
        try:
            subprocess.run(["mkdocs", "build"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar documentação: {str(e)}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            return False

    def all(self):
        """Executa todos os processos"""
        steps = [
            self.check_dependencies,
            self.clean,
            self.format,
            self.test,
            self.package,
            self.executable,
            self.docs,
        ]

        for step in steps:
            if not step():
                raise BuildError(f"Erro no build: {step.__name__}")

        print("\n✨ Build completo!")
        return True


def main():
    builder = BuildManager()

    if len(sys.argv) < 2:
        builder.show_usage()

    command = sys.argv[1]

    try:
        if command == "clean":
            builder.clean("--all" in sys.argv)
        elif command in ["release", "exe", "package", "docs"]:
            if command == "release":
                builder.release()
            else:
                builder.build(command)
        elif command == "test":
            subprocess.run(["poetry", "run", "pytest"], check=True)
        elif command == "all":
            builder.build_all()
        else:
            builder.show_usage()

    except KeyboardInterrupt:
        print(builder.i18n.get("build.error.interrupted"))
        sys.exit(1)
    except Exception as e:
        print(builder.i18n.get("build.error.build").format(str(e)))
        sys.exit(1)


if __name__ == "__main__":
    main()
