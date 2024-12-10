"""
Interface de linha de comando
"""
import sys
import asyncio
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

import inquirer  # type: ignore
from colorama import init, Fore, Style

from src.core.config import ConfigManager
from src.core.watcher import FileWatcher
from src.deployers.factory import DeployerFactory
from src.utils.logger import CustomLogger
from src.i18n import I18n


class CLI:
    """Interface de linha de comando"""

    def __init__(self):
        init()  # Inicializa colorama
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()
        self.config_manager = ConfigManager()
        self.deployer_factory = DeployerFactory()

    def print_banner(self) -> None:
        """Imprime banner do aplicativo"""
        print(Fore.CYAN + self.i18n.get("app.banner") + Style.RESET_ALL)
        print(f"\n{self.i18n.get('app.name')} v{self.i18n.get('app.version')}")
        print(self.i18n.get("app.description"))
        print(f"\n{self.i18n.get('app.author')}: Brendown Ferreira")
        print(f"{self.i18n.get('app.repo')}: {self.i18n.get('app.repository')}")
        print("\n" + self.i18n.get("text.separator") + "\n")

    def parse_args(self) -> argparse.Namespace:
        """Parse argumentos da linha de comando"""
        parser = argparse.ArgumentParser(
            description=self.i18n.get("cli.description")
        )
        
        parser.add_argument(
            "--config",
            type=Path,
            help=self.i18n.get("cli.config_help")
        )
        
        parser.add_argument(
            "--host",
            help=self.i18n.get("cli.host_help")
        )
        
        parser.add_argument(
            "--watch",
            action="store_true",
            help=self.i18n.get("cli.watch_help")
        )
        
        return parser.parse_args()

    async def interactive_mode(self, config: Dict[str, Any]) -> None:
        """Modo interativo"""
        self.print_banner()
        
        questions = [
            inquirer.List(
                "host",
                message=self.i18n.get("input.host"),
                choices=list(config["hosts"].keys())
            ),
            inquirer.Confirm(
                "watch",
                message=self.i18n.get("input.watch"),
                default=False
            )
        ]
        
        answers = inquirer.prompt(questions)
        if not answers:
            return
        
        await self.deploy(
            config,
            answers["host"],
            answers["watch"]
        )

    async def deploy(
        self,
        config: Dict[str, Any],
        host: str,
        watch: bool = False
    ) -> None:
        """Executa deploy"""
        try:
            host_config = self.config_manager.get_host_config(config, host)
            deployer = self.deployer_factory.create_deployer(
                host,
                host_config["protocol"],
                host_config
            )
            
            if watch:
                self.logger.info(self.i18n.get("mode.watch"))
                watcher = FileWatcher(deployer)
                await watcher.start(Path(host_config["source_path"]))
            else:
                self.logger.info(self.i18n.get("mode.interactive"))
                await deployer.deploy()
                
        except KeyboardInterrupt:
            self.logger.info(self.i18n.get("deploy.cancelled"))
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(1)

    async def run(self) -> None:
        """Executa aplicativo"""
        args = self.parse_args()
        
        if args.config:
            self.config_manager.config_path = args.config
        
        try:
            config = self.config_manager.load_config()
            
            if not self.config_manager.validate_config(config):
                self.logger.error(self.i18n.get("config.error.invalid"))
                sys.exit(1)
            
            if args.host:
                await self.deploy(config, args.host, args.watch)
            else:
                await self.interactive_mode(config)
                
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(1)


def main() -> None:
    """Função principal"""
    cli = CLI()
    asyncio.run(cli.run())


if __name__ == "__main__":
    main() 