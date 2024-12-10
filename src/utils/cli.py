import argparse
from src.i18n import I18n

def create_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos"""
    i18n = I18n()
    
    parser = argparse.ArgumentParser(
        description=i18n.get("app.description")
    )
    
    parser.add_argument(
        '--protocol',
        choices=['ssh', 'ftp', 'local'],
        help=i18n.get("protocol.select")
    )
    
    parser.add_argument(
        '--host',
        help=i18n.get("input.host")
    )
    
    parser.add_argument(
        '--user',
        help=i18n.get("input.user")
    )
    
    parser.add_argument(
        '--password',
        help=i18n.get("input.password")
    )
    
    parser.add_argument(
        '--key-path',
        help=i18n.get("input.key_path")
    )
    
    parser.add_argument(
        '--port',
        type=int,
        help=i18n.get("input.port").format("22 para SSH, 21 para FTP")
    )
    
    parser.add_argument(
        '--source',
        help=i18n.get("input.source_path")
    )
    
    parser.add_argument(
        '--dest',
        help=i18n.get("input.dest_path")
    )
    
    parser.add_argument(
        '--watch',
        action='store_true',
        help=i18n.get("input.watch")
    )
    
    parser.add_argument(
        '--ignore-patterns',
        nargs='+',
        help=i18n.get("deploy.file_ignored")
    )
    
    return parser

def validate_args(args: argparse.Namespace) -> bool:
    """Valida argumentos da linha de comando"""
    i18n = I18n()
    
    if args.protocol == 'ssh':
        if not args.host or not args.user:
            print(i18n.get("deploy.error.config").format(
                "Host e usuário são obrigatórios para SSH"))
            return False
            
        if not args.password and not args.key_path:
            print(i18n.get("deploy.error.auth").format(
                "Senha ou chave SSH são obrigatórios"))
            return False
            
    elif args.protocol == 'ftp':
        if not args.host or not args.user or not args.password:
            print(i18n.get("deploy.error.config").format(
                "Host, usuário e senha são obrigatórios para FTP"))
            return False
            
    if not args.source:
        print(i18n.get("deploy.error.path").format(
            "Caminho fonte não especificado"))
        return False
        
    if not args.dest:
        print(i18n.get("deploy.error.path").format(
            "Caminho destino não especificado"))
        return False
        
    return True 