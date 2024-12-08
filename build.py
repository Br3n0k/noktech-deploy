import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_executable():
    """Executa o build do executável"""
    if sys.platform == 'win32':
        # Build com cx_Freeze no Windows
        subprocess.run([sys.executable, 'build_config.py', 'build'], check=True)
    else:
        # Build com PyInstaller no Linux/Mac
        import PyInstaller.__main__
        
        BASE_DIR = Path(__file__).parent
        ICON_PATH = BASE_DIR / 'src' / 'assets' / 'logo.ico'
        ASSETS_PATH = BASE_DIR / 'src' / 'assets'
        
        PyInstaller.__main__.run([
            str(BASE_DIR / 'src' / 'deploy_client.py'),
            '--name=noktech-deploy',
            '--onefile',
            '--console',
            f'--icon={ICON_PATH}',
            f'--add-data={ASSETS_PATH}{os.pathsep}assets',
            '--clean',
            '--noconfirm',
        ])

def main():
    """Função principal do build"""
    try:
        print("Limpando diretórios anteriores...")
        clean_build_dirs()
        
        print("Iniciando build...")
        build_executable()
        
        print("Build concluído com sucesso!")
    except Exception as e:
        print(f"Erro durante o build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 