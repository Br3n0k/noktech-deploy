import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'src/deploy_client.py',
    '--name=noktech-deploy',
    '--onefile',
    '--console',
    '--icon=assets/logo/logo.ico',
    '--add-data=assets;assets',
    '--version-file=version_info.txt',
    '--clean',
]) 