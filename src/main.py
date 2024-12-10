import sys
import asyncio
import logging
from src.deploy_client import DeployClient
from src.utils.config import setup_logging

async def async_main():
    """Função principal assíncrona"""
    setup_logging()
    client = DeployClient()
    
    parser = client.create_parser()
    args = parser.parse_args()
    
    try:
        await client.run(args)
    except Exception as e:
        logging.error(f"Fatal application error: {str(e)}")
        logging.error("Error details:", exc_info=True)
        return 1
    return 0

def main():
    """Ponto de entrada principal"""
    try:
        if sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(async_main())
    except KeyboardInterrupt:
        logging.info("Operação cancelada pelo usuário")
        return 0
    except Exception as e:
        logging.error(f"Fatal application error: {str(e)}")
        logging.error("Error details:", exc_info=True)
        input("Press ENTER to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
