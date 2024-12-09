#!/usr/bin/env python
import subprocess
import sys
from pathlib import Path
from src.i18n import I18n

i18n = I18n()


def setup_docs():
    """Configura ambiente inicial de documentação"""
    try:
        # Instala dependências
        subprocess.run(
            [
                "poetry",
                "add",
                "--dev",
                "mkdocs",
                "mkdocs-material",
                "mkdocs-i18n",
                "mkdocstrings[python]",
            ],
            check=True,
        )

        # Cria estrutura de diretórios
        docs_dir = Path("docs")
        docs_dir.mkdir(exist_ok=True)

        for lang in ["pt", "en"]:
            lang_dir = docs_dir / lang
            lang_dir.mkdir(exist_ok=True)

            # Cria estrutura básica para cada idioma
            (lang_dir / "guide").mkdir(exist_ok=True)
            (lang_dir / "api").mkdir(exist_ok=True)

        return True
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False


def build_docs():
    """Gera a documentação"""
    try:
        subprocess.run(["mkdocs", "build"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao gerar documentação: {str(e)}")
        return False


def serve_docs():
    """Inicia servidor local de documentação"""
    try:
        subprocess.run(["mkdocs", "serve"], check=True)
    except KeyboardInterrupt:
        print("\nServidor interrompido")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar servidor: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "setup":
            setup_docs()
        elif command == "build":
            build_docs()
        elif command == "serve":
            serve_docs()
        else:
            print("Comando inválido. Use: setup, build ou serve")
    else:
        print("Uso: python scripts/docs.py [setup|build|serve]")
