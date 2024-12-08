import pytest
import os
import tempfile
import threading
import time
import shutil
from src.deploy_client import DeployClient
from src.core.watcher import DirectoryWatcher
from src.deployers import LocalDeployer

class TestIntegration:
    @pytest.fixture
    def setup_dirs(self):
        """Prepara diretórios para teste de integração"""
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        
        # Cria estrutura inicial
        os.makedirs(os.path.join(source, 'src/components'))
        os.makedirs(os.path.join(source, 'public'))
        
        with open(os.path.join(source, 'src/index.js'), 'w') as f:
            f.write('console.log("test")')
            
        yield source, dest
        
        # Cleanup
        for d in [source, dest]:
            try:
                shutil.rmtree(d)
            except:
                pass

    def test_full_deploy_cycle(self, setup_dirs):
        """Testa ciclo completo de deploy"""
        source_dir, dest_dir = setup_dirs
        
        # Configura cliente
        client = DeployClient()
        args = type('Args', (), {
            'protocol': 'local',
            'dest_path': dest_dir,
            'files_path': source_dir,
            'watch': False,
            'ignore_patterns': ['*.log']
        })()
        
        # Executa deploy
        client.setup_deployer(args)
        if not client.deployer:
            raise ValueError("Deployer não configurado")
            
        client.deployer.deploy_files(source_dir, dest_dir)
        
        # Verifica resultado
        assert os.path.exists(os.path.join(dest_dir, 'src/index.js'))
        
    def test_watch_mode(self, setup_dirs):
        """Testa modo de observação"""
        source_dir, dest_dir = setup_dirs
        events_processed = []
        
        def handle_event(path, event_type):
            events_processed.append((path, event_type))
            
        # Inicia observador
        watcher = DirectoryWatcher(
            source_dir,
            handle_event,
            None  # sem regras de ignore
        )
        
        # Executa em thread separada
        thread = threading.Thread(target=watcher.start)
        thread.daemon = True
        thread.start()
        
        # Cria novo arquivo
        test_file = os.path.join(source_dir, 'src/test.js')
        with open(test_file, 'w') as f:
            f.write('console.log("new file")')
            
        # Aguarda processamento
        time.sleep(1)
        watcher.stop()
        
        # Verifica eventos
        assert len(events_processed) > 0
        assert any(test_file in path for path, _ in events_processed) 