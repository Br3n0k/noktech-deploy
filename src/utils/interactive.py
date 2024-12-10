import getpass
from typing import Dict, Any
from src.utils.logger import Logger
from src.i18n import I18n

class InteractiveConfig:
    def __init__(self):
        self.logger = Logger(__name__)
        self.i18n = I18n()
        
    def get_config(self) -> dict[str, Any]:
        """Obtém configuração via modo interativo"""
        print("\n" + self.i18n.get("mode.interactive"))
        
        # Protocolo
        print("\n" + self.i18n.get("protocol.select"))
        print("1. " + self.i18n.get("protocol.ssh"))
        print("2. " + self.i18n.get("protocol.ftp"))
        print("3. " + self.i18n.get("protocol.local"))
        print("0. " + self.i18n.get("menu.exit"))
        
        choice = input(f"\n{self.i18n.get('input.choice')}: ")
        
        if choice == "0":
            return None
            
        protocol = {
            "1": "ssh",
            "2": "ftp",
            "3": "local"
        }.get(choice)
        
        if not protocol:
            self.logger.error(self.i18n.get("deploy.error.protocol").format(choice))
            return None
            
        # Caminhos
        source_path = input(f"\n{self.i18n.get('input.source_path')} ")
        dest_path = input(f"{self.i18n.get('input.dest_path')} ")
        
        config = {
            "protocol": protocol,
            "source_path": source_path,
            "dest_path": dest_path,
            "enabled": True
        }
        
        # Configurações específicas do protocolo
        if protocol in ["ssh", "ftp"]:
            config.update({
                "host": input(f"{self.i18n.get('input.host')} "),
                "user": input(f"{self.i18n.get('input.user')} "),
                "password": getpass.getpass(f"{self.i18n.get('input.password')} ")
            })
            
            if protocol == "ssh":
                key_path = input(f"{self.i18n.get('input.key_path')} ")
                if key_path:
                    config["key_path"] = key_path
                    
            port_default = "22" if protocol == "ssh" else "21"
            port = input(f"{self.i18n.get('input.port').format(port_default)} ")
            if port:
                config["port"] = int(port)
                
        # Configuração de watch
        watch = input(f"\n{self.i18n.get('input.watch')} ").lower()
        if watch in ["s", "y", "sim", "yes"]:
            config["watch"] = {
                "enabled": True,
                "ignore_patterns": []
            }
            
        return {
            "hosts": {
                "interactive": config
            }
        } 