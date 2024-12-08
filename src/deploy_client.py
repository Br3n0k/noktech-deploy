#!/usr/bin/env python3
import warnings
import argparse
import sys
from typing import Optional
from cryptography.utils import CryptographyDeprecationWarning

# Suprimir avisos de depreciação do Paramiko
warnings.filterwarnings(
    "ignore",
    category=CryptographyDeprecationWarning,
    module="paramiko"
)

from src.deployers import SSHDeployer, FTPDeployer, LocalDeployer
from src.core.file_manager import FileManager
from src.core.ignore_rules import IgnoreRules
from src.core.watcher import DirectoryWatcher
from src.utils.logger import Logger
from src.utils.config import Config
from src.version import VERSION

class DeployClient:
    def __init__(self):
        self.logger = Logger(log_file=Logger.get_default_log_file())
        self.config = Config()
        self.deployer = None
        self.file_manager = None

    def setup_deployer(self, args):
        """Configura o deployer baseado nos argumentos"""
        try:
            if args.protocol == 'ssh':
                self.deployer = SSHDeployer(
                    host=args.host,
                    user=args.user,
                    password=args.password,
                    port=args.port or 22,
                    key_path=args.key_path,
                    dest_path=args.dest_path
                )
            elif args.protocol == 'ftp':
                self.deployer = FTPDeployer(
                    host=args.host,
                    user=args.user,
                    password=args.password,
                    port=args.port or 21,
                    dest_path=args.dest_path
                )
            elif args.protocol == 'local':
                self.deployer = LocalDeployer(
                    dest_base=args.dest_path
                )
        except Exception as e:
            self.logger.error(f"Erro ao configurar deployer: {str(e)}")
            sys.exit(1)

    def handle_file_change(self, path: str, event_type: str):
        """Manipula mudanças nos arquivos quando em modo watch"""
        try:
            if self.deployer:
                self.deployer.handle_change(path, event_type)
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança: {str(e)}")

    def run(self):
        parser = self.create_parser()
        args = parser.parse_args()

        if args.version:
            print(f"noktech-deploy versão {VERSION}")
            return

        # Configura regras de ignore
        ignore_rules = IgnoreRules(
            ignore_file=args.ignore_file,
            rules=args.ignore_patterns
        )

        # Configura deployer
        self.setup_deployer(args)

        # Modo de observação
        if args.watch:
            watcher = DirectoryWatcher(
                args.files_path,
                self.handle_file_change,
                ignore_rules,
                self.logger
            )
            watcher.start()
        else:
            # Deploy único
            if not self.deployer:
                raise ValueError("Deployer não configurado")
                
            try:
                self.deployer.connect()
                self.deployer.deploy_files(args.files_path, args.dest_path)
                self.logger.info("Deploy concluído com sucesso!")
            except Exception as e:
                self.logger.error(f"Erro no deploy: {str(e)}")
                sys.exit(1)
            finally:
                if self.deployer:
                    self.deployer.disconnect()

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Cliente de Deploy Avançado')
        
        parser.add_argument('--version',
                          action='store_true',
                          help='Mostra a versão do programa')
        
        parser.add_argument('--protocol', 
                          choices=['ssh', 'ftp', 'local'],
                          help='Protocolo de deploy')
                          
        parser.add_argument('--host',
                          help='Host remoto')
                          
        parser.add_argument('--user',
                          help='Usuário remoto')
                          
        parser.add_argument('--password',
                          help='Senha remota')
                          
        parser.add_argument('--port', 
                          type=int,
                          help='Porta remota')
                          
        parser.add_argument('--key-path',
                          help='Caminho para chave SSH')
                          
        parser.add_argument('--dest-path',
                          help='Caminho de destino')
                          
        parser.add_argument('--files-path',
                          help='Caminho dos arquivos fonte')
                          
        parser.add_argument('--watch',
                          action='store_true',
                          help='Modo de observação contínua')
                          
        parser.add_argument('--ignore-file',
                          help='Arquivo com padrões de ignore')
                          
        parser.add_argument('--ignore-patterns',
                          nargs='*',
                          help='Padrões adicionais para ignorar')

        return parser

def main():
    client = DeployClient()
    client.run()

if __name__ == '__main__':
    main() 