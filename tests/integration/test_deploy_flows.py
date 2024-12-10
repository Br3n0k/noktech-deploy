from typing import AsyncGenerator, Dict, Tuple
from pathlib import Path
from src.deploy_client import DeployClient


async def test_local_deploy(
    project_structure: AsyncGenerator[Tuple[Path, Dict], None]
) -> None:
    """Testa fluxo de deploy local"""
    project_dir, config = await anext(project_structure)
    client = DeployClient()
    await client.setup(config)
    await client.deploy_all()
    assert (project_dir / "deploy").exists()


async def test_watch_mode(
    project_structure: AsyncGenerator[Tuple[Path, Dict], None]
) -> None:
    """Testa modo watch"""
    project_dir, config = await anext(project_structure)
    client = DeployClient(watch=True)
    await client.setup(config)
    client.start_watching()
    client.stop_watching()
