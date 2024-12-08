#!/usr/bin/env python3
import warnings
import argparse
import sys
from typing import Optional, List
from cryptography.utils import CryptographyDeprecationWarning
import os

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
from .i18n import I18n

class DeployClient:
    def __init__(self):
        self.logger = Logger(log_file=Logger.get_default_log_file())
        self.config = Config()
        self.deployer = None
        self.file_manager = None
        self.i18n = I18n()

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
        ignore_rules = self.setup_ignore_rules(args)
        
        # Passa as regras para o deployer
        if self.deployer:
            self.deployer.ignore_rules = ignore_rules

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

    def show_banner(self):
        """Exibe o banner ASCII do NokDeploy"""
        banner = """
        ███╗   ██╗ ██████╗ ██╗  ██╗██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗
        ████╗  ██║██╔═══██╗██║ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝
        ██╔██╗ ██║██║   ██║█████╔╝ ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝ 
        ██║╚██╗██║██║   ██║██╔═██╗ ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝  
        ██║ ╚████║╚██████╔╝██║  ██╗██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║   
        ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝   
        """
        info = f"""
        {self.i18n.get('app.version')}: 0.1.0
        {self.i18n.get('app.author')}: Brendown Ferreira
        {self.i18n.get('app.repo')}: https://github.com/Br3n0k/noktech-deploy
        """
        print(banner)
        print(info)

    def interactive_mode(self) -> None:
        self.show_banner()
        print(f"\n=== {self.i18n.get('mode.interactive')} ===\n")
        
        # Protocolo
        print(self.i18n.get('protocol.select'))
        print(f"1. {self.i18n.get('protocol.ssh')}")
        print(f"2. {self.i18n.get('protocol.ftp')}")
        print(f"3. {self.i18n.get('protocol.local')}")
        protocol_choice = input(f"{self.i18n.get('input.choice')} (1-3): ").strip()
        
        protocol_map = {'1': 'ssh', '2': 'ftp', '3': 'local'}
        protocol = protocol_map.get(protocol_choice)
        
        if not protocol:
            print(self.i18n.get('error.invalid_option'))
            return
        
        # Caminhos
        files_path = input(f"\n{self.i18n.get('input.source_path')} ").strip()
        dest_path = input(f"{self.i18n.get('input.dest_path')} ").strip()
        
        # Configuração de ignore
        print(f"\n{self.i18n.get('ignore.config')}:")
        use_gitignore = input(f"{self.i18n.get('ignore.use_git')} (s/n): ").lower().startswith(
            's' if self.i18n.current_lang == 'pt_br' else 'y'
        )
        use_custom = input(f"{self.i18n.get('ignore.use_custom')} (s/n): ").lower().startswith(
            's' if self.i18n.current_lang == 'pt_br' else 'y'
        )
        
        # Criar instância de Args em vez de usar type()
        args = Args()
        args.protocol = protocol
        args.files_path = files_path
        args.dest_path = dest_path
        
        if protocol in ['ssh', 'ftp']:
            args.host = input("Host: ").strip()
            args.user = input("Usuário: ").strip()
            
            if protocol == 'ssh':
                use_key = input("Usar chave SSH? (s/n): ").lower().startswith('s')
                if use_key:
                    args.key_path = input("Caminho da chave SSH: ").strip()
                    args.password = None
                else:
                    args.password = input("Senha: ").strip()
                    args.key_path = None
            else:
                args.password = input("Senha: ").strip()
            
            port_input = input(f"Porta ({22 if protocol == 'ssh' else 21}): ").strip()
            args.port = int(port_input) if port_input else (22 if protocol == 'ssh' else 21)
        
        # Modo watch
        args.watch = input("\nAtivar modo de observação? (s/n): ").lower().startswith('s')
        
        # Pergunta sobre arquivos a ignorar
        print("\nConfiguração de arquivos ignorados:")
        args.ignore_file = '.gitignore' if use_gitignore else None
        if use_custom:
            print("Digite os padrões (um por linha, Enter vazio para terminar):")
            patterns = []
            while True:
                pattern = input().strip()
                if not pattern:
                    break
                patterns.append(pattern)
            args.ignore_patterns = patterns
        
        print("\nIniciando deploy...\n")
        
        try:
            self.setup_deployer(args)
            if not self.deployer:
                raise ValueError("Deployer não configurado")
            
            self.deployer.connect()
            self.deployer.deploy_files(args.files_path, args.dest_path)
            
            if args.watch:
                print("\nModo de observação ativado. Pressione Ctrl+C para sair.")
                self.watch_directory(args)
            
            print("\nDeploy concluído com sucesso!")
            
        except Exception as e:
            print(f"\nErro: {str(e)}")
        finally:
            if self.deployer:
                self.deployer.disconnect()

    def watch_directory(self, args):
        """Inicia o modo de observação"""
        watcher = DirectoryWatcher(
            args.files_path,
            self.handle_file_change,
            ignore_rules=None,  # Você pode adicionar regras de ignore aqui
            logger=self.logger
        )
        watcher.start()

    def setup_ignore_rules(self, args) -> IgnoreRules:
        """Configura regras de ignore para o deploy"""
        # Arquivos de ignore padrão
        ignore_files = [
            '.gitignore',
            '.deployignore'
        ]
        
        # Padrões padrão
        default_patterns = [
            '.git/',
            '__pycache__/',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.Python',
            'env/',
            'venv/',
            '.env',
            '.venv',
            'build/',
            'dist/',
            '*.egg-info/',
            '.coverage',
            'htmlcov/',
            '.pytest_cache/',
            '.idea/',
            '.vscode/',
            'node_modules/',
            '.DS_Store'
        ]
        
        # Adiciona padrões da linha de comando
        if args.ignore_patterns:
            default_patterns.extend(args.ignore_patterns)
        
        # Cria regras de ignore
        rules = IgnoreRules(
            rules=default_patterns,
            ignore_file=args.ignore_file or next((f for f in ignore_files if os.path.exists(f)), None)
        )
        
        return rules

class Args:
    def __init__(self):
        self.protocol: str = ''
        self.host: str = ''
        self.user: str = ''
        self.password: Optional[str] = None
        self.key_path: Optional[str] = None
        self.port: int = 0
        self.files_path: str = ''
        self.dest_path: str = ''
        self.watch: bool = False
        self.ignore_patterns: List[str] = []
        self.ignore_file: Optional[str] = None

def main():
    try:
        client = DeployClient()
        
        if len(sys.argv) == 1:  # Sem argumentos
            client.interactive_mode()
        else:
            client.run()
            
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 