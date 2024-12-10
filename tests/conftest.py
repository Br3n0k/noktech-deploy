import asyncio
import shutil
from collections.abc import AsyncGenerator
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Any, Dict, Tuple

import pytest

from src.deploy_client import DeployClient

pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="function")
def event_loop_policy():
    """Define a política de event loop para os testes"""
    return asyncio.WindowsSelectorEventLoopPolicy()


@asynccontextmanager
async def deploy_context() -> AsyncGenerator[Path, None]:
    """Contexto para testes de deploy"""
    deploy_dir = Path("test_project")
    try:
        deploy_dir.mkdir(exist_ok=True)
        yield deploy_dir
    finally:
        if deploy_dir.exists():
            shutil.rmtree(deploy_dir)


async def aiter_next(ait: AsyncGenerator) -> Tuple[bool, Any]:
    """Helper para substituir anext em versões antigas do Python"""
    try:
        value = await ait.__anext__()
        return True, value
    except StopAsyncIteration:
        return False, None


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
async def project_structure(
    temp_project: AsyncGenerator[Path, None]
) -> AsyncGenerator[Tuple[Path, Dict], None]:
    """Fornece estrutura de projeto e configuração base para testes"""
    has_next, project_dir = await aiter_next(temp_project)
    if not has_next or not project_dir:
        raise RuntimeError("Falha ao obter diretório temporário")

    config = {
        "hosts": {
            "test_ssh": {
                "enabled": True,
                "protocol": "ssh",
                "host": "ssh.example.com",
                "user": "testuser",
                "source_path": str(project_dir),
                "dest_path": "/remote/ssh",
            },
            "test_ftp": {
                "enabled": True,
                "protocol": "ftp",
                "host": "ftp.example.com",
                "user": "testuser",
                "password": "testpass",
                "source_path": str(project_dir),
                "dest_path": "/remote/ftp",
            },
        }
    }
    yield project_dir, config


@pytest.fixture(scope="function")
async def configured_client(
    temp_project: AsyncGenerator[Path, None]
) -> AsyncGenerator[DeployClient, None]:
    """Fornece um DeployClient configurado para testes"""
    has_next, project_dir = await aiter_next(temp_project)
    if not has_next or not project_dir:
        raise RuntimeError("Falha ao obter diretório temporário")

    config = {
        "hosts": {
            "test_local": {
                "enabled": True,
                "protocol": "local",
                "source_path": str(project_dir),
                "dest_path": str(project_dir / "deploy"),
            }
        }
    }
    client = DeployClient()
    await client.setup(config)
    yield client
