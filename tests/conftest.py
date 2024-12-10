import pytest
import asyncio
import shutil
from pathlib import Path
from typing import AsyncGenerator, Tuple
from src.deploy_client import DeployClient

pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(scope="function")
def event_loop_policy():
    """Define a política de event loop para os testes"""
    return asyncio.WindowsSelectorEventLoopPolicy()

@pytest.fixture(scope="function")
async def temp_project() -> AsyncGenerator[Path, None]:
    """Cria e limpa diretório temporário para testes"""
    project_dir = Path("test_project")
    if project_dir.exists():
        shutil.rmtree(project_dir, ignore_errors=True)
    project_dir.mkdir(exist_ok=True)
    (project_dir / "src").mkdir(parents=True, exist_ok=True)
    (project_dir / "deploy").mkdir(parents=True, exist_ok=True)
    try:
        yield project_dir
    finally:
        if project_dir.exists():
            shutil.rmtree(project_dir, ignore_errors=True)

@pytest.fixture(scope="function")
async def project_structure(temp_project) -> AsyncGenerator[Tuple[Path, dict], None]:
    """Fornece estrutura de projeto e configuração base para testes"""
    project_dir = await anext(temp_project)
    config = {
        "hosts": {
            "test_ssh": {
                "enabled": True,
                "protocol": "ssh",
                "host": "ssh.example.com",
                "user": "testuser",
                "source_path": str(project_dir),
                "dest_path": "/remote/ssh"
            },
            "test_ftp": {
                "enabled": True,
                "protocol": "ftp",
                "host": "ftp.example.com",
                "user": "testuser",
                "password": "testpass",
                "source_path": str(project_dir),
                "dest_path": "/remote/ftp"
            }
        }
    }
    yield project_dir, config

@pytest.fixture(scope="function")
async def configured_client(temp_project) -> AsyncGenerator[DeployClient, None]:
    """Fornece um DeployClient configurado para testes"""
    project_dir = await anext(temp_project)
    config = {
        "hosts": {
            "test_local": {
                "enabled": True,
                "protocol": "local",
                "source_path": str(project_dir),
                "dest_path": str(project_dir / "deploy")
            }
        }
    }
    client = DeployClient()
    await client.setup(config)
    yield client
