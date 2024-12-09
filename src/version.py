"""Versão centralizada do NokTech Deploy"""

__version__ = "0.1.2"
__author__ = "Brendown Ferreira"
__email__ = "br3n0k@gmail.com"
__description__ = "Advanced deployment client with multi-protocol support"
__copyright__ = "Copyright © 2024 NokTech"

# Alias para compatibilidade
VERSION = __version__


def get_version():
    return __version__


def get_full_version():
    return {
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "description": __description__,
        "copyright": __copyright__,
    }
