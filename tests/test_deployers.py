import pytest
import os
import tempfile
import shutil
from src.deployers import SSHDeployer, FTPDeployer, LocalDeployer
from src.core.ignore_rules import IgnoreRules

class TestLocalDeployer:
    @pytest.fixture
    def temp_dirs(self):
        """Cria diretórios temporários para teste"""
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        
        # Cria alguns arquivos de teste
        test_files = {
            'file1.txt': 'conteúdo 1',
            'dir1/file2.txt': 'conteúdo 2',
            'dir1/dir2/file3.txt': 'conteúdo 3'
        }
        
        for path, content in test_files.items():
            full_path = os.path.join(source, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
                
        yield source, dest
        
        # Cleanup
        shutil.rmtree(source)
        shutil.rmtree(dest)
        
    def test_local_deploy(self, temp_dirs):
        source_dir, dest_dir = temp_dirs
        deployer = LocalDeployer(dest_dir)
        
        # Testa deploy
        deployer.connect()
        deployer.deploy_files(source_dir, dest_dir)
        
        # Verifica se arquivos foram copiados
        assert os.path.exists(os.path.join(dest_dir, 'file1.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'dir1/file2.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'dir1/dir2/file3.txt'))
        
    def test_ignore_patterns(self, temp_dirs):
        source_dir, dest_dir = temp_dirs
        
        # Cria arquivo para ignorar
        ignore_file = os.path.join(source_dir, '.deployignore')
        with open(ignore_file, 'w') as f:
            f.write('*.txt\n')
            
        ignore_rules = IgnoreRules(ignore_file=ignore_file)
        deployer = LocalDeployer(dest_dir)
        deployer.file_manager.ignore_rules = ignore_rules
        
        # Testa deploy com ignore
        deployer.connect()
        deployer.deploy_files(source_dir, dest_dir)
        
        # Verifica se arquivos foram ignorados
        assert not os.path.exists(os.path.join(dest_dir, 'file1.txt')) 