import pytest
import os
import tempfile
import shutil
from src.deployers import LocalDeployer
from src.core.ignore_rules import IgnoreRules


@pytest.mark.asyncio
class TestLocalDeployer:
    @pytest.fixture
    def temp_dirs(self):
        """Cria diretórios temporários para teste"""
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        try:
            yield source, dest
        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)

    @pytest.fixture
    async def deployer(self, temp_dirs):
        """Cria e configura o deployer"""
        source_dir, dest_dir = temp_dirs
        deployer = LocalDeployer(dest_dir)
        await deployer.connect()

        try:
            yield deployer
        finally:
            await deployer.disconnect()

    async def test_local_deploy(self, temp_dirs):
        """Testa deploy local básico"""
        source_dir, dest_dir = temp_dirs

        # Cria arquivo de teste
        test_file = os.path.join(source_dir, "file1.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        deployer = LocalDeployer(dest_dir)
        await deployer.connect()
        try:
            await deployer.deploy_files(source_dir, dest_dir)
            assert os.path.exists(os.path.join(dest_dir, "file1.txt"))
        finally:
            await deployer.disconnect()

    async def test_ignore_patterns(self, deployer, temp_dirs):
        """Testa regras de ignore"""
        source_dir, dest_dir = temp_dirs

        # Cria arquivo de teste
        test_file = os.path.join(source_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("should be ignored")

        async for d in deployer:
            d.ignore_rules = IgnoreRules(rules=["*.txt"])
            await d.deploy_files(source_dir, dest_dir)
            assert not os.path.exists(os.path.join(dest_dir, "test.txt"))
            break
