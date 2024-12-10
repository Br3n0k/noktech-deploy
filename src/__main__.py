#!/usr/bin/env python3
import sys
import asyncio
from src.deploy_client import DeployClient
from src.utils.cli import create_parser, validate_args
from src.utils.logger import Logger
from src.i18n import I18n

async def main():
    """Ponto de entrada principal"""
    logger = Logger(__name__)
    i18n = I18n()
    
    try:
        parser = create_parser()
        args = parser.parse_args()
        
        if args.protocol and not validate_args(args):
            return 1
            
        client = DeployClient()
        return await client.run(args if args.protocol else None)
        
    except KeyboardInterrupt:
        logger.info(i18n.get("app.error.runtime").format("Interrompido pelo usuário"))
        return 0
        
    except Exception as e:
        logger.error(i18n.get("app.error.unexpected").format(str(e)))
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 