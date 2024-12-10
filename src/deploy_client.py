#!/usr/bin/env python3
import warnings
import argparse
import json
import sys
import asyncio
import inquirer
from pathlib import Path
from typing import Optional, List, Dict, Any
from cryptography.utils import CryptographyDeprecationWarning
import os
from dataclasses import dataclass
from src.core.constants import (
    CONFIG_DIR,
    DEFAULT_CONFIG_FILE,
    DEFAULT_LOG_DIR,
    DEFAULT_CONFIG_TEMPLATE,
    LOG_FILE_FORMAT,
    DEFAULT_CONFIG,
)
from src.utils.logger import Logger
from datetime import datetime
from src.utils.config import create_default_config
from src.i18n import I18n
from src.deployers import SSHDeployer, FTPDeployer, LocalDeployer
from src.core.watcher import DirectoryWatcher
import logging
import fnmatch
from src.core.deploy_manager import DeployManager
from src.core.watch_manager import WatchManager


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

        return True
    except Exception as e:
        print(f"Erro ao inicializar projeto: {str(e)}")
        return False


@dataclass
class IgnoreRules:
    """Classe simplificada para gerenciar regras de ignore"""
    rules: List[str]

    def should_ignore(self, file_path: str) -> bool:
        """Verifica se um arquivo deve ser ignorado"""
        for pattern in self.rules:
            if fnmatch.fnmatch(str(file_path), pattern):
                return True
        return False


class DeployClient:
    def __init__(self):
        self.config = {}
        self.deployers = {}
        self.watcher = None
        self.logger = Logger(__name__)

    async def setup(self, config: Dict[str, Any]) -> None:
        """Configura o cliente com as configurações fornecidas"""
        self.config = config
        self.deployers = {}

        for host_name, host_config in config.get("hosts", {}).items():
            if not host_config.get("enabled", True):
                continue

            deployer = self._create_deployer(host_name, host_config)
            if deployer:
                self.deployers[host_name] = deployer

    async def deploy_all(self) -> None:
        """Executa deploy para todos os hosts configurados"""
        if self.config.get("parallel_deploy", False):
            tasks = [deployer.deploy() for deployer in self.deployers.values()]
            await asyncio.gather(*tasks)
        else:
            for deployer in self.deployers.values():
                await deployer.deploy()

    async def start_watch(self) -> None:
        """Inicia modo watch"""
        if not self.config.get("hosts"):
            raise ValueError("Nenhum host configurado para watch")
        
        # Pega o primeiro host habilitado
        for host in self.config["hosts"].values():
            if host.get("enabled", True):
                source_path = Path(host["source_path"])
                self.watcher = DirectoryWatcher(str(source_path))
                await self.watcher.start()
                return
            
        raise ValueError("Nenhum host habilitado para watch")

    async def stop_watch(self) -> None:
        """Para o modo watch"""
        if self.watcher:
            await self.watcher.stop()
            self.watcher = None

    def _create_deployer(self, host_name: str, config: Dict[str, Any]):
        """Cria o deployer apropriado baseado no protocolo"""
        protocol = config.get("protocol", "").lower()
        
        if protocol == "ssh":
            return SSHDeployer(config)
        elif protocol == "ftp":
            return FTPDeployer(config)
        elif protocol == "local":
            return LocalDeployer(config)
        else:
            self.logger.warning(f"Protocolo desconhecido para host {host_name}: {protocol}")
            return None

    def create_parser(self) -> argparse.ArgumentParser:
        """Cria e configura o parser de argumentos da linha de comando"""
        parser = argparse.ArgumentParser(
            description="Cliente de deploy com suporte a múltiplos protocolos"
        )
        
        parser.add_argument(
            "-c", "--config",
            help="Caminho para o arquivo de configuração",
            default=str(DEFAULT_CONFIG_FILE)
        )
        
        parser.add_argument(
            "-w", "--watch",
            help="Ativa o modo de monitoramento",
            action="store_true"
        )
        
        parser.add_argument(
            "--host",
            help="Host específico para deploy (opcional)",
            default=None
        )
        
        parser.add_argument(
            "--verbose", "-v",
            help="Ativa logs detalhados",
            action="store_true"
        )
        
        return parser

    async def run(self, args):
        """Executa o cliente com os argumentos fornecidos"""
        config = self.load_config(args.config)
        await self.setup(config)
        
        # Se não houver argumentos específicos, mostra menu interativo
        if not any([args.host, args.watch]):
            return await self.show_interactive_menu()
            
        if args.host:
            await self.deploy_host(args.host)
        else:
            await self.deploy_all()
            
        if args.watch:
            await self.start_watch()
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                await self.stop_watch()
    
    async def show_interactive_menu(self) -> None:
        """Mostra menu interativo de opções"""
        questions = [
            inquirer.List('action',
                message="Escolha uma ação",
                choices=[
                    ('Deploy completo', 'deploy_all'),
                    ('Deploy específico', 'deploy_host'),
                    ('Modo Watch', 'watch'),
                    ('Sair', 'exit')
                ]
            )
        ]
        
        while True:
            answers = inquirer.prompt(questions)
            
            if answers['action'] == 'exit':
                break
            elif answers['action'] == 'deploy_all':
                await self.deploy_all()
            elif answers['action'] == 'deploy_host':
                # Submenu para escolher host
                host_choices = [(h, h) for h in self.config['hosts'].keys()]
                host = inquirer.prompt([
                    inquirer.List('host',
                        message="Escolha um host",
                        choices=host_choices
                    )
                ])
                if host:
                    await self.deploy_host(host['host'])
            elif answers['action'] == 'watch':
                await self.start_watch()
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    await self.stop_watch()

    def load_config(self, config_path: str) -> dict:
        """Carrega a configuração do arquivo JSON"""
        try:
            config_file = Path(config_path)
            
            # Se não existir, cria diretório e arquivo de configuração padrão
            if not config_file.exists():
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                config_file.parent.mkdir(parents=True, exist_ok=True)
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(DEFAULT_CONFIG_TEMPLATE, f, indent=4)
                    
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Mescla com configurações padrão
            merged_config = DEFAULT_CONFIG.copy()
            merged_config.update(config)
                
            return merged_config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao decodificar JSON: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar configuração: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description=I18n().get("app.description"))
    parser.add_argument('--protocol', help=I18n().get("protocol.select"))
    parser.add_argument('--host', help=I18n().get("input.host"))
    parser.add_argument('--user', help=I18n().get("input.user"))
    parser.add_argument('--password', help=I18n().get("input.password"))
    parser.add_argument('--key-path', help=I18n().get("input.key_path"))
    parser.add_argument('--port', type=int, help=I18n().get("input.port"))
    parser.add_argument('--source', help=I18n().get("input.source_path"))
    parser.add_argument('--dest', help=I18n().get("input.dest_path"))
    parser.add_argument('--watch', action='store_true', help=I18n().get("input.watch"))
    
    args = parser.parse_args()
    client = DeployClient()
    sys.exit(asyncio.run(client.run(args)))

if __name__ == '__main__':
    main()