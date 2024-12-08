"""Versão centralizada do NokTech Deploy"""
import importlib.metadata

try:
    VERSION = importlib.metadata.version("noktech-deploy")
except importlib.metadata.PackageNotFoundError:
    VERSION = "0.1.0"  # Versão padrão para desenvolvimento 