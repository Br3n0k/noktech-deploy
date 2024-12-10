import pytest
from pathlib import Path
from unittest.mock import patch
from src.deploy_client import DeployClient

class TestDeployFlows:
    @pytest.mark.asyncio
    async def test_full_project_deploy(self, configured_client, temp_project):
        """Testa deploy completo de um projeto"""
        client = await anext(configured_client)
        
        deploy_dir = Path("test_project/deploy")
        deploy_dir.mkdir(parents=True, exist_ok=True)
        (deploy_dir / "src/lib").mkdir(parents=True, exist_ok=True)
        (Path("test_project") / "src/lib").mkdir(parents=True, exist_ok=True)
        
        (Path("test_project") / "src/lib/utils.py").write_text("def test(): pass")
        
        with patch('src.deployers.local_deployer.shutil.copy2') as mock_copy:
            def copy_file(src, dst):
                Path(dst).parent.mkdir(parents=True, exist_ok=True)
                Path(dst).write_text(Path(src).read_text())
                return True
            
            mock_copy.side_effect = copy_file
            await client.deploy_all()
            
            # Validações
            assert (deploy_dir / "src/lib/utils.py").exists(), "Arquivo não foi copiado"
            assert mock_copy.called, "Função de cópia não foi chamada"

    @pytest.mark.asyncio
    async def test_deploy_with_file_changes(self, temp_project):
        """Testa deploy após alterações em arquivos"""
        project_dir = await anext(temp_project)
        
        (project_dir / "src").mkdir(parents=True, exist_ok=True)
        (project_dir / "deploy").mkdir(parents=True, exist_ok=True)
        
        client = DeployClient()
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
        
        await client.setup(config)
        await client.deploy_all()

        # Simula alterações
        new_file = project_dir / "src/new_module.py"
        new_file.parent.mkdir(parents=True, exist_ok=True)
        new_file.write_text("print('New module')\n") 