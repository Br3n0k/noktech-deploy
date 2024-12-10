from pathlib import Path
from typing import Dict, List
from src.utils.logger import Logger
from src.i18n import I18n
from src.deployers.base_deployer import BaseDeployer
from src.deployers.local_deployer import LocalDeployer
from src.deployers.ssh_deployer import SSHDeployer
from src.deployers.ftp_deployer import FTPDeployer

class DeployManager:
    def __init__(self):
        self.logger = Logger(__name__)
        self.i18n = I18n()
        self.deployers: Dict[str, BaseDeployer] = {}

    async def initialize_deployers(self, config: dict) -> None:
        """Inicializa os deployers baseado na configuração"""
        self.logger.info(self.i18n.get("deploy.manager.init"))
        
        for host_name, host_config in config.get("hosts", {}).items():
            if not host_config.get("enabled", False):
                continue

            try:
                deployer = self._create_deployer(host_config)
                if deployer:
                    self.deployers[host_name] = deployer
                    self.logger.info(self.i18n.get("deploy.manager.host_enabled").format(host_name))
            except Exception as e:
                self.logger.error(self.i18n.get("deploy.manager.host_error").format(host_name, str(e)))

    def _create_deployer(self, config: dict) -> BaseDeployer:
        """Cria instância do deployer apropriado"""
        protocol = config.get("protocol", "").lower()
        
        if protocol == "local":
            return LocalDeployer(config)
        elif protocol == "ssh":
            return SSHDeployer(config)
        elif protocol == "ftp":
            return FTPDeployer(config)
        else:
            raise ValueError(self.i18n.get("error.invalid_protocol").format(protocol))

    async def deploy_all(self, source_path: Path) -> bool:
        """Executa deploy para todos os hosts configurados"""
        if not self.deployers:
            raise ValueError(self.i18n.get("error.no_hosts_enabled"))

        success = True
        for host_name, deployer in self.deployers.items():
            success &= await self._deploy_host(host_name, deployer, source_path)
        return success

    async def _deploy_host(self, host_name: str, deployer: BaseDeployer, source_path: Path) -> bool:
        """Executa deploy para um host específico"""
        try:
            self.logger.info(self.i18n.get("deploy.progress.start_host").format(host_name))
            await deployer.deploy_directory(source_path, Path(deployer.config["dest_path"]))
            self.logger.info(self.i18n.get("deploy.progress.complete_host").format(host_name))
            return True
        except Exception as e:
            self.logger.error(self.i18n.get("deploy.progress.error_host").format(host_name, str(e)))
            return False

    async def deploy_changes(self, host_name: str, changes: List[Path]) -> bool:
        """Deploy de arquivos específicos para um host"""
        if host_name not in self.deployers:
            self.logger.error(self.i18n.get("deploy.error.config").format(
                f"Host não encontrado: {host_name}"))
            return False
            
        deployer = self.deployers[host_name]
        success = True
        
        try:
            self.logger.info(self.i18n.get("deploy.progress.start"))
            self.logger.info(self.i18n.get("deploy.progress.files"))
                
            for source in changes:
                if not source.is_file():
                    continue
                    
                try:
                    rel_path = source.relative_to(Path(deployer.config["source_path"]))
                    dest = Path(deployer.config["dest_path"]) / rel_path
                    
                    if await deployer.deploy_file(source, dest):
                        self.logger.debug(self.i18n.get("deploy.success"))
                    else:
                        success = False
                        
                except Exception as e:
                    self.logger.error(self.i18n.get("deploy.error.transfer").format(str(e)))
                    success = False
            
            if success:
                self.logger.info(self.i18n.get("deploy.progress.complete"))
            return success
            
        except Exception as e:
            self.logger.error(self.i18n.get("deploy.progress.error").format(str(e)))
            return False