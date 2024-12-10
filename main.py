#!/usr/bin/env python3
"""
Ponto de entrada principal do NokTech Deploy
"""
import argparse
import asyncio
import sys
from typing import Optional, Dict, Any
from pathlib import Path

from src.deploy_client import DeployClient
from src.utils.config import ConfigManager
from src.utils.logger import CustomLogger
from src.i18n import I18n
from src.core.constants import (
    PROJECT_NAME,
    PROJECT_VERSION,
    DEFAULT_CONFIG_FILE
)


def validate_config(config: Dict[str, Any]) -> None:
    """Valida configuração básica"""
    required_fields = ["source_path", "dest_path"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
        if not Path(config[field]).exists():
            raise ValueError(f"Path does not exist: {config[field]}")


async def main(config_file: Optional[str] = None, watch: bool = False) -> None:
    """Função principal do programa"""
    print(f"{PROJECT_NAME} v{PROJECT_VERSION}")
    logger = CustomLogger.get_logger(__name__)
    
    try:
        client = DeployClient()
        config_manager = ConfigManager(config_file or DEFAULT_CONFIG_FILE)
        config = config_manager.load_config()
        
        # Valida configuração antes de prosseguir
        validate_config(config)
        
        if watch:
            config["watch"] = {"enabled": True}
            
        await client.setup(config)
        await client.run()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


def cli():
    """Interface de linha de comando"""
    i18n = I18n()
    parser = argparse.ArgumentParser(description=i18n.get("app.description"))
    parser.add_argument("--config", "-c", help=i18n.get("input.config"))
    parser.add_argument("--watch", "-w", action="store_true", help=i18n.get("input.watch"))
    parser.add_argument("--version", "-v", action="version", version=f"{PROJECT_NAME} v{PROJECT_VERSION}")
    
    args = parser.parse_args()
    asyncio.run(main(args.config, args.watch))


if __name__ == "__main__":
    cli()
