import PyInstaller.__main__
import os
import sys

# Garante caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, 'src', 'assets', 'logo.ico')
VERSION_FILE = os.path.join(BASE_DIR, 'version_info.txt')
ASSETS_PATH = os.path.join(BASE_DIR, 'src', 'assets')

# Verifica se os arquivos existem
if not os.path.exists(ICON_PATH):
    print(f"Erro: Ícone não encontrado em {ICON_PATH}")
    sys.exit(1)

if not os.path.exists(VERSION_FILE):
    print(f"Erro: Arquivo de versão não encontrado em {VERSION_FILE}")
    sys.exit(1)

# Configuração do build
PyInstaller.__main__.run([
    os.path.join(BASE_DIR, 'src', 'deploy_client.py'),
    '--name=noktech-deploy',
    '--onefile',
    '--console',
    f'--icon={ICON_PATH}',
    f'--version-file={VERSION_FILE}',
    f'--add-data={ASSETS_PATH}{os.pathsep}assets',
    '--clean',
    '--noconfirm',
]) 