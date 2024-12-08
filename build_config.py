import sys
import os
from cx_Freeze import setup, Executable

# Garante caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'src', 'assets', 'logo.ico')
ASSETS_DIR = os.path.join(BASE_DIR, 'src', 'assets')
I18N_DIR = os.path.join(BASE_DIR, 'src', 'i18n')

# Configurações do build
build_options = dict(
    packages=['asyncio', 'watchdog', 'paramiko', 'ftplib', 'asyncssh', 'typing_extensions'],
    excludes=[],
    include_files=[(ASSETS_DIR, 'assets'), (I18N_DIR, 'i18n')],
    include_msvcr=True
)

# Configuração do executável
base = 'Win32GUI' if sys.platform == 'win32' else None
exe = Executable(
    script=os.path.join(BASE_DIR, 'src', 'deploy_client.py'),
    base=base,
    target_name='noktech-deploy',
    icon=ICON_PATH,
    copyright='Copyright © 2024 NokTech',
)

# Setup
setup(
    name='NokTech Deploy',
    version='0.1.1',
    description='Advanced deployment client',
    options={'build_exe': build_options},
    executables=[exe]
) 