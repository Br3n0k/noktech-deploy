# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
import sys
from src.core.constants import PROJECT_NAME

block_cipher = None

# Usando o diretório atual como base
spec_dir = os.getcwd()

# Obtendo o caminho correto do site-packages do ambiente virtual
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    # Estamos em um ambiente virtual
    site_packages = os.path.join(sys.prefix, 'Lib', 'site-packages')
else:
    # Fallback para o Python global
    site_packages = os.path.join(os.path.dirname(os.__file__), 'site-packages')

# Definindo caminhos absolutos
datas = [
    # Arquivos de tradução (copiando todo o diretório i18n)
    (os.path.join(spec_dir, 'src', 'i18n'), 'src/i18n'),
    (os.path.join(spec_dir, 'src', 'assets'), 'src/assets'),
]

# Adicione verificação explícita
lang_dir = os.path.join(spec_dir, 'src', 'i18n', 'lang')
if not os.path.exists(lang_dir):
    raise FileNotFoundError(f"Diretório de traduções não encontrado: {lang_dir}")

# Verificação de debug para os caminhos
print("Diretório do spec:", spec_dir)
print("Site-packages:", site_packages)
for src, dst in datas:
    print(f"Verificando caminho: {src} -> {dst}")
    if not os.path.exists(src):
        print(f"AVISO: Caminho não encontrado: {src}")

# Verificação do arquivo principal
main_path = os.path.join(spec_dir, 'main.py')
if not os.path.exists(main_path):
    raise FileNotFoundError(f"Arquivo principal não encontrado: {main_path}")

a = Analysis(
    [main_path],
    pathex=[spec_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # Core Python
        'importlib',
        'importlib.metadata',
        'importlib.resources',
        'typing_extensions',
        
        # Async packages
        'asyncio',
        'aiofiles',
        'aioftp',
        'aioftp.common',
        'aioftp.client',
        'aioftp.server',
        'aioftp.pathio',
    ],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=PROJECT_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/assets/logo.ico'
) 