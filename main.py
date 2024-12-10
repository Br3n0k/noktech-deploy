#!/usr/bin/env python
import sys
import asyncio
import logging
import traceback
from src.deploy_client import DeployClient
from pathlib import Path
from datetime import datetime
from src.i18n import I18n
from src.core.logger import Logger
from src.utils.config import create_default_config


def handle_exception(exc_type, exc_value, exc_traceback):
    """Manipulador global de exceções não tratadas"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    i18n = I18n()
    logger = Logger()
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error(error_msg)

    print(i18n.get("app.error.fatal").format(str(exc_value)))
    print(i18n.get("app.error_details").format(error_msg))
    input(i18n.get("app.press_enter"))


def initialize_workspace():
    """Inicializa o ambiente de trabalho na raiz onde o programa foi executado"""
    try:
        current_dir = Path.cwd()
        log_dir = current_dir / "logs"
        
        # Configura logging
        log_dir.mkdir(exist_ok=True)
        
        # Configura arquivo de log inicial com encoding UTF-8
        error_log = log_dir / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(error_log, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(file_handler)
        
        # Cria config.json se não existir
        if not (current_dir / "config.json").exists():
            create_default_config(current_dir / "config.json")
            
        return True
    except Exception as e:
        logging.error(f"Erro ao inicializar workspace: {str(e)}")
        return False


def main():
    """Função principal"""
    sys.excepthook = handle_exception
    logging.basicConfig(level=logging.INFO)

    if not initialize_workspace():
        return 1

    client = DeployClient()
    parser = client.create_parser()
    args = parser.parse_args()
    return asyncio.run(client.run(args))


if __name__ == "__main__":
    sys.exit(main())
