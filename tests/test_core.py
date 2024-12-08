import pytest
import os
import tempfile
import shutil
from src.core.ignore_rules import IgnoreRules
from src.core.file_manager import FileManager
from src.core.watcher import DirectoryWatcher

class TestIgnoreRules:
    def test_default_ignores(self):
        rules = IgnoreRules()
        assert rules.should_ignore('.git/config')
        assert rules.should_ignore('__pycache__/module.pyc')
        assert not rules.should_ignore('src/main.py')
        
    def test_custom_patterns(self):
        rules = IgnoreRules(rules=['*.txt', '!important.txt'])
        assert rules.should_ignore('test.txt')
        assert not rules.should_ignore('important.txt')
        assert not rules.should_ignore('test.py')
        
class TestFileManager:
    @pytest.fixture
    def temp_dir(self):
        """Cria diretório temporário para teste"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
        
    def test_collect_files(self, temp_dir):
        # Cria arquivos de teste
        os.makedirs(os.path.join(temp_dir, 'src'))
        with open(os.path.join(temp_dir, 'src/test.py'), 'w') as f:
            f.write('print("test")')
            
        manager = FileManager()
        files = manager.collect_files(temp_dir)
        
        assert len(files) == 1
        assert files[0][1] == 'src/test.py'
        
class TestDirectoryWatcher:
    @pytest.fixture
    def temp_dir(self):
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
        
    def test_file_events(self, temp_dir):
        events = []
        def callback(path, event_type):
            events.append((path, event_type))
            
        watcher = DirectoryWatcher(temp_dir, callback)
        
        # Inicia watcher em thread separada
        import threading
        thread = threading.Thread(target=watcher.start)
        thread.daemon = True
        thread.start()
        
        # Testa eventos
        test_file = os.path.join(temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
            
        import time
        time.sleep(1)  # Aguarda processamento
        
        watcher.stop()
        assert len(events) > 0
        assert events[0][1] == 'created' 