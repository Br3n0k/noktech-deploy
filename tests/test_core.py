import pytest
import os
import tempfile
import shutil
from src.core.ignore_rules import IgnoreRules
from src.core.file_manager import FileManager
from src.core.watcher import DirectoryWatcher
import asyncio


class TestIgnoreRules:
    def test_default_ignores(self):
        rules = IgnoreRules()
        assert rules.should_ignore(".git/config")
        assert rules.should_ignore("__pycache__/module.pyc")
        assert not rules.should_ignore("src/main.py")

    def test_custom_patterns(self):
        rules = IgnoreRules(rules=["*.txt", "!important.txt"])
        assert rules.should_ignore("test.txt")
        assert not rules.should_ignore("important.txt")
        assert not rules.should_ignore("test.py")


class TestFileManager:
    @pytest.fixture
    def temp_dir(self):
        """Cria diretório temporário para teste"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)

    def test_collect_files(self, temp_dir):
        # Cria arquivos de teste
        os.makedirs(os.path.join(temp_dir, "src"))
        with open(os.path.join(temp_dir, "src/test.py"), "w") as f:
            f.write('print("test")')

        manager = FileManager()
        files = manager.collect_files(temp_dir)

        assert len(files) == 1
        assert files[0][1] == "src/test.py"


class TestDirectoryWatcher:
    @pytest.fixture
    def temp_dir(self, tmp_path):
        return str(tmp_path)

    @pytest.mark.asyncio
    async def test_file_events(self, temp_dir):
        events = []

        async def callback(path, event_type):
            events.append((path, event_type))

        # Cria e inicia o watcher
        watcher = DirectoryWatcher(temp_dir, callback)
        watch_task = asyncio.create_task(watcher.start())

        # Aguarda o observer iniciar
        await asyncio.sleep(0.1)

        # Cria arquivo de teste
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        # Aguarda os eventos serem processados
        await asyncio.sleep(0.5)

        # Para o watcher
        watcher.stop()
        await watch_task

        # Verifica se eventos foram capturados
        assert len(events) > 0
        assert any(event[1] == "created" for event in events)
