"""
Factory para criação de deployers
"""
from typing import Dict, Optional, Type
from pathlib import Path

from src.deployers.base_deployer import BaseDeployer
from src.deployers.ssh_deployer import SSHDeployer
from src.deployers.ftp_deployer import FTPDeployer
from src.deployers.local_deployer import LocalDeployer
from src.utils.logger import CustomLogger
from src.i18n import I18n


class DeployerFactory:
    """Factory para criação de deployers"""

    DEPLOYERS: Dict[str, Type[BaseDeployer]] = {
        "ssh": SSHDeployer,
        "sftp": SSHDeployer,
        "ftp": FTPDeployer,
        "local": LocalDeployer
    }

    def __init__(self):
        self.logger = CustomLogger.get_logger(__name__)
        self.i18n = I18n()

    def create_deployer(
        self, 
        host_name: str,
        protocol: str,
        config: Dict
    ) -> BaseDeployer:
        """
        Cria uma instância do deployer apropriado
        
        Args:
            host_name: Nome do host
            protocol: Protocolo de deploy (ssh, ftp, local)
            config: Configuração do deployer
        
        Returns:
            Instância do deployer
        
        Raises:
            ValueError: Se o protocolo for inválido
        """
        protocol = protocol.lower()
        
        if protocol not in self.DEPLOYERS:
            self.logger.error(self.i18n.get("deploy.error.protocol").format(protocol))
            raise ValueError(self.i18n.get("deploy.error.protocol").format(protocol))

        deployer_class = self.DEPLOYERS[protocol]
        return deployer_class(host_name, config)

    @classmethod
    def register_deployer(
        cls,
        protocol: str,
        deployer_class: Type[BaseDeployer]
    ) -> None:
        """
        Registra um novo tipo de deployer
        
        Args:
            protocol: Nome do protocolo
            deployer_class: Classe do deployer
        """
        cls.DEPLOYERS[protocol.lower()] = deployer_class 