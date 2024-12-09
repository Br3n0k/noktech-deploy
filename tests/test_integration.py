import pytest
import os
import shutil
import asyncio
from src.deploy_client import DeployClient
from src.core.watcher import DirectoryWatcher


class TestIntegration:
    @pytest.fixture
    def setup_dirs(self):
        """Configura diretórios para teste"""
        test_dirs = ["test_src", "test_dest"]
        for d in test_dirs:
            try:
                os.makedirs(d, exist_ok=True)
            except (OSError, PermissionError) as e:
                pytest.fail(f"Falha ao criar diretório {d}: {e}")
        return test_dirs

    @pytest.mark.asyncio
    async def test_full_deploy_cycle(self, setup_dirs):
        """Testa ciclo completo de deploy"""
        try:
            source_dir, dest_dir = setup_dirs

            # Cria estrutura de arquivos para teste
            src_dir = os.path.join(source_dir, "src")
            os.makedirs(src_dir, exist_ok=True)
            with open(os.path.join(src_dir, "index.js"), "w") as f:
                f.write('console.log("test")')

            client = DeployClient()
            args = type(
                "Args",
                (),
                {
                    "protocol": "local",
                    "dest_path": dest_dir,
                    "files_path": source_dir,
                    "watch": False,
                    "ignore_patterns": ["*.log"],
                },
            )()

            await client.setup_deployer(args)
            assert client.deployer is not None

            await client.deployer.deploy_files(source_dir, dest_dir)
            assert os.path.exists(os.path.join(dest_dir, "src", "index.js"))
        finally:
            self.cleanup_dirs(setup_dirs)

    @pytest.mark.asyncio
    async def test_watch_mode(self, setup_dirs):
        """Testa modo de observação"""
        source_dir, dest_dir = setup_dirs
        events_processed = []

        async def handle_event(path, event_type):
            normalized_path = os.path.normpath(path)
            events_processed.append((normalized_path, event_type))

        # Inicia observador
        watcher = DirectoryWatcher(source_dir, handle_event)
        watch_task = asyncio.create_task(watcher.start())

        await asyncio.sleep(1)  # Aumentado tempo de espera

        # Cria novo arquivo
        src_dir = os.path.join(source_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        test_file = os.path.join(src_dir, "test.js")
        test_file = os.path.normpath(test_file)

        with open(test_file, "w") as f:
            f.write('console.log("new file")')

        await asyncio.sleep(2)  # Aumentado tempo de espera
        watcher.stop()
        await watch_task

        assert len(events_processed) > 0
        assert any(
            test_file == path for path, _ in events_processed
        ), f"Expected {test_file} in {events_processed}"

    def cleanup_dirs(self, dirs):
        """Limpa diretórios de teste"""
        for d in dirs:
            try:
                shutil.rmtree(d)
            except (FileNotFoundError, PermissionError, OSError) as e:
                print(f"Erro ao remover diretório {d}: {e}")
