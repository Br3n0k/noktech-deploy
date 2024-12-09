#!/usr/bin/env python3
import warnings
import argparse
import sys
import asyncio
import json
from typing import Optional, List
from cryptography.utils import CryptographyDeprecationWarning
import os
from dataclasses import dataclass
from src.core.constants import (
    CONFIG_DIR,
    DEFAULT_CONFIG_FILE,
    DEFAULT_LOG_DIR,
    DEFAULT_IGNORE_FILE,
    DEFAULT_CONFIG_TEMPLATE,
    DEFAULT_IGNORE_TEMPLATE,
    LOG_FILE_FORMAT,
)
from src.utils.logger import Logger
from datetime import datetime
from .version_checker import VersionChecker
from src.utils.config import Config
from src.i18n import I18n
from src.deployers import SSHDeployer, LocalDeployer
from src.core.ignore_rules import IgnoreRules
from src.core.watcher import DirectoryWatcher


@dataclass
class Args:
    protocol: str = ""
    host: str = ""
    user: str = ""
    password: Optional[str] = None
    key_path: Optional[str] = None
    port: int = 0
    files_path: str = ""
    dest_path: str = ""
    watch: bool = False
    ignore_patterns: Optional[List[str]] = None
    ignore_file: Optional[str] = None

    def __post_init__(self):
        if self.ignore_patterns is None:
            self.ignore_patterns = []


# Suprimir avisos de depreciação do Paramiko
warnings.filterwarnings(
    "ignore", category=CryptographyDeprecationWarning, module="paramiko"
)


def initialize_project():
    """Inicializa a estrutura do projeto se não existir"""
    try:
        # Cria diretório de configuração
        CONFIG_DIR.mkdir(exist_ok=True)
        DEFAULT_LOG_DIR.mkdir(exist_ok=True)

        # Cria arquivo de configuração padrão completo
        if not DEFAULT_CONFIG_FILE.exists():
            config_template = {
                "default_protocol": "ssh",
                "log_level": "info",
                "log_dir": str(DEFAULT_LOG_DIR),
                "watch_delay": 1000,
                "hosts": {
                    "local": {
                        "protocol": "local",
                        "dest_path": "./deploy",
                        "ignore_file": ".deployignore",
                        "backup": {
                            "enabled": True,
                            "max_backups": 5,
                            "path": "./backups",
                        },
                        "hooks": {"pre_deploy": "", "post_deploy": ""},
                        "retry": {"attempts": 3, "delay": 5},
                    }
                },
                "ignore_patterns": DEFAULT_CONFIG_TEMPLATE["ignore_patterns"],
            }

            with open(DEFAULT_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_template, f, indent=4)

        # Cria arquivo .deployignore completo
        if not DEFAULT_IGNORE_FILE.exists():
            with open(DEFAULT_IGNORE_FILE, "w", encoding="utf-8") as f:
                f.write(DEFAULT_IGNORE_TEMPLATE)

        # Cria arquivo de log inicial
        log_file = DEFAULT_LOG_DIR / datetime.now().strftime(LOG_FILE_FORMAT)
        if not log_file.exists():
            log_file.touch()

        return True
    except Exception as e:
        print(f"Erro ao inicializar projeto: {str(e)}")
        return False


class DeployClient:
    def __init__(self):
        self.i18n = I18n()
        self.logger = Logger(log_file=Logger.get_default_log_file())
        self.config = Config()
        self.deployer = None
        self.ignore_rules = None

    async def setup_deployer(self, args):
        """Configura o deployer baseado nos argumentos"""
        if not args.protocol:
            raise ValueError("Protocolo não especificado")

        try:
            # Configura ignore rules
            ignore_file = getattr(args, "ignore_file", None)
            ignore_patterns = getattr(args, "ignore_patterns", [])
            self.ignore_rules = IgnoreRules(
                rules=ignore_patterns, ignore_file=ignore_file
            )

            if args.protocol == "ssh":
                self.deployer = SSHDeployer(
                    host=args.host,
                    user=args.user,
                    password=getattr(args, "password", None),
                    port=getattr(args, "port", 22),
                    key_path=getattr(args, "key_path", None),
                )
            elif args.protocol == "local":
                self.deployer = LocalDeployer(dest_path=args.dest_path)

            if self.deployer:
                self.deployer.ignore_rules = self.ignore_rules

        except Exception as e:
            self.logger.error(f"Erro ao configurar deployer: {str(e)}")
            raise

    async def handle_file_change(self, path: str, event_type: str):
        """Manipula mudanças nos arquivos quando em modo watch"""
        try:
            if self.deployer:
                await self.deployer.handle_change(path, event_type)
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança: {str(e)}")

    async def run(self, args):
        try:
            self.logger.info(self.i18n.get("deploy.start"))

            await self.setup_deployer(args)
            if not self.deployer:
                raise ValueError(self.i18n.get("deploy.error_no_deployer"))

            if args.protocol != "local":
                self.logger.info(
                    self.i18n.get("connection.connecting").format(args.host)
                )
            else:
                self.logger.info(
                    self.i18n.get("local.copying").format(
                        args.files_path, args.dest_path
                    )
                )

            await self.deployer.connect()

            if args.protocol != "local":
                self.logger.info(self.i18n.get("connection.connected"))

            if args.watch:
                self.logger.info(self.i18n.get("watch.start"))
                await self.watch_mode()
            else:
                await self.deployer.deploy_files(args.files_path, args.dest_path)
                self.logger.info(self.i18n.get("deploy.complete"))

        except Exception as e:
            self.logger.error(self.i18n.get("deploy.error").format(str(e)))
            raise
        finally:
            if self.deployer:
                await self.deployer.disconnect()
                if args.protocol != "local":
                    self.logger.info(self.i18n.get("connection.disconnected"))

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Cliente de Deploy Avançado")

        parser.add_argument(
            "--version", action="store_true", help="Mostra a versão do programa"
        )

        parser.add_argument(
            "--protocol", choices=["ssh", "ftp", "local"], help="Protocolo de deploy"
        )

        parser.add_argument("--host", help="Host remoto")

        parser.add_argument("--user", help="Usuário remoto")

        parser.add_argument("--password", help="Senha remota")

        parser.add_argument("--port", type=int, help="Porta remota")

        parser.add_argument("--key-path", help="Caminho para chave SSH")

        parser.add_argument("--dest-path", help="Caminho de destino")

        parser.add_argument("--files-path", help="Caminho dos arquivos fonte")

        parser.add_argument(
            "--watch", action="store_true", help="Modo de observação contínua"
        )

        parser.add_argument("--ignore-file", help="Arquivo com padrões de ignore")

        parser.add_argument(
            "--ignore-dir",
            help="Diretório que contém o arquivo .deployignore (padrão: diretório atual)",
        )

        parser.add_argument(
            "--log-dir",
            help="Diretório para armazenar logs (padrão: ~/.noktech-deploy/logs)",
        )

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

    async def interactive_mode(self, args: Optional[Args] = None):
        """Modo interativo para configurar o deploy"""
        self.show_banner()
        print(f"\n=== {self.i18n.get('mode.interactive')} ===\n")

        if args is None:
            args = Args()

        # Coleta dados do usuário
        args.protocol = input(
            f"{self.i18n.get('cli.enter_protocol')} (ssh/ftp/local): "
        ).lower()
        if args.protocol not in ["ssh", "ftp", "local"]:
            raise ValueError(
                self.i18n.get("cli.invalid_protocol").format(args.protocol)
            )

        if args.protocol != "local":
            args.host = input(f"{self.i18n.get('cli.enter_host')}: ")
            args.user = input(f"{self.i18n.get('cli.enter_user')}: ")
            args.password = (
                input(
                    f"{self.i18n.get('cli.enter_password')} ({self.i18n.get('cli.optional')}): "
                )
                or None
            )

        args.files_path = input(f"{self.i18n.get('cli.enter_source_path')}: ")
        args.dest_path = input(f"{self.i18n.get('cli.enter_dest_path')}: ")

        watch_response = input(f"{self.i18n.get('cli.watch_mode')} (y/n): ").lower()
        args.watch = watch_response.startswith("y")

        try:
            await self.run(args)
        except Exception as e:
            print(f"\n{self.i18n.get('cli.error')}: {str(e)}")

    async def watch_directory(self, args):
        """Inicia o modo de observação"""
        watcher = DirectoryWatcher(
            args.files_path,
            self.handle_file_change,
            ignore_rules=None,  # Você pode adicionar regras de ignore aqui
            logger=self.logger,
        )
        await watcher.start()

    def setup_ignore_rules(self, args) -> IgnoreRules:
        """Configura regras de ignore para o deploy"""
        # Arquivos de ignore padrão
        ignore_files = [".gitignore", ".deployignore"]

        # Padrões padrão
        default_patterns = [
            ".git/",
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".Python",
            "venv/",
            ".venv",
            "build/",
            "dist/",
            "*.egg-info/",
            ".coverage",
            "htmlcov/",
            ".pytest_cache/",
            ".idea/",
            ".vscode/",
            "node_modules/",
            ".DS_Store",
        ]

        # Adiciona padrões da linha de comando
        if args.ignore_patterns:
            default_patterns.extend(args.ignore_patterns)

        # Cria regras de ignore
        rules = IgnoreRules(
            rules=default_patterns,
            ignore_file=args.ignore_file
            or next((f for f in ignore_files if os.path.exists(f)), None),
        )

        return rules

    async def watch_mode(self):
        """Inicia o modo de observação"""
        try:
            if not self.files_path:
                raise ValueError(self.i18n.get("watch.no_path"))

            watcher = DirectoryWatcher(
                self.files_path,
                self.handle_file_change,
                ignore_rules=self.ignore_rules,
                logger=self.logger,
            )
            await watcher.start()
        except Exception as e:
            self.logger.error(self.i18n.get("watch.error").format(str(e)))
            raise


async def main():
    try:
        # Verifica versão antes de iniciar
        checker = VersionChecker()
        if not checker.check():
            sys.exit(1)

        client = DeployClient()
        parser = client.create_parser()
        args = parser.parse_args()

        if len(sys.argv) == 1:
            await client.interactive_mode(Args())
        else:
            deploy_args = Args(
                protocol=args.protocol,
                host=args.host,
                user=args.user,
                password=args.password,
                key_path=args.key_path,
                port=args.port,
                files_path=args.files_path,
                dest_path=args.dest_path,
                watch=args.watch,
                ignore_patterns=args.ignore_patterns,
                ignore_file=args.ignore_file,
            )
            await client.run(deploy_args)
            return 0
    except Exception as e:
        print(f"\nErro: {str(e)}")
        return 1


if __name__ == "__main__":
    asyncio.run(main())
