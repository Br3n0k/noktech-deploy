"""Script para atualização de versão"""

import re
from pathlib import Path
from typing import Dict


def parse_version(version: str) -> Dict[str, int]:
    """Converte string de versão em dicionário"""
    try:
        major, minor, micro = map(int, version.split("."))
        return {"major": major, "minor": minor, "micro": micro}
    except ValueError as e:
        raise ValueError("Formato de versão inválido. Use: X.Y.Z") from e


def update_version(new_version: str) -> None:
    """Atualiza a versão em todos os arquivos do projeto"""
    try:
        version_info = parse_version(new_version)
        root_dir = Path(__file__).parent.parent.parent

        # Atualiza constants.py
        constants_file = root_dir / "src" / "core" / "constants.py"
        content = constants_file.read_text(encoding="utf-8")

        # Atualiza PROJECT_VERSION
        content = re.sub(
            r'PROJECT_VERSION = "[^"]*"',
            f'PROJECT_VERSION = "{new_version}"',
            content
        )

        # Atualiza VERSION_INFO
        for key, value in version_info.items():
            content = re.sub(
                f'"{key}": \\d+',
                f'"{key}": {value}',
                content
            )

        constants_file.write_text(content, encoding="utf-8")

        # Atualiza pyproject.toml
        pyproject_file = root_dir / "pyproject.toml"
        content = pyproject_file.read_text(encoding="utf-8")
        content = re.sub(
            r'version = "[^"]*"',
            f'version = "{new_version}"',
            content
        )
        pyproject_file.write_text(content, encoding="utf-8")

        print(f"✅ Versão atualizada para {new_version} em todos os arquivos")

    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar versão: {str(e)}") from e


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python update_version.py <nova_versão>")
        sys.exit(1)
    update_version(sys.argv[1])
