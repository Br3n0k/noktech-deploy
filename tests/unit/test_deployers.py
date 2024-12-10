import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from src.deployers.ssh_deployer import SSHDeployer
from src.deployers.ftp_deployer import FTPDeployer
from src.deployers.local_deployer import LocalDeployer

@pytest.mark.asyncio
class TestSSHDeployer:
    @pytest.fixture
    async def ssh_deployer(self):
        """Fixture que fornece um SSHDeployer configurado"""
        config = {
            "host": "test.example.com",
            "user": "testuser",
            "dest_path": "/remote/path"
        }
        return SSHDeployer(config)

    @pytest.mark.asyncio
    async def test_ssh_file_transfer(self, ssh_deployer, temp_project):
        """Testa transferência de arquivo via SSH"""
        deployer = await ssh_deployer
        project_dir = await anext(temp_project)
        
        # Cria estrutura de diretórios
        source_file = project_dir / "src/test.py"
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.write_text("print('test')")
        
        with patch('asyncssh.connect') as mock_connect:
            mock_ssh = AsyncMock()
            mock_sftp = AsyncMock()
            mock_sftp.mkdir = AsyncMock()
            mock_sftp.put = AsyncMock()
            mock_ssh.start_sftp_client = AsyncMock(return_value=mock_sftp)
            
            # Configura o mock_connect para retornar uma coroutine
            async def mock_connect_coro(*args, **kwargs):
                return mock_ssh
            mock_connect.side_effect = mock_connect_coro
            
            # Conecta e configura SFTP
            await deployer.connect()
            
            await deployer.upload_file(source_file, "/remote/test.py")
            mock_sftp.put.assert_called_once()

@pytest.mark.asyncio
class TestFTPDeployer:
    @pytest.fixture
    async def ftp_deployer(self):
        """Fixture que fornece um FTPDeployer configurado"""
        config = {
            "host": "ftp.example.com",
            "user": "ftpuser",
            "dest_path": "/remote/path"
        }
        return FTPDeployer(config)

    @pytest.mark.asyncio
    async def test_ftp_file_upload(self, ftp_deployer, temp_project):
        """Testa upload de arquivo via FTP"""
        deployer = await ftp_deployer
        project_dir = await anext(temp_project)
        
        # Cria estrutura de diretórios
        source_file = project_dir / "src/test.py"
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.write_text("print('test')")
        
        with patch('aioftp.Client') as mock_client:
            mock_ftp = AsyncMock()
            mock_ftp.upload = AsyncMock()
            mock_ftp.make_directory = AsyncMock()
            mock_client.return_value = mock_ftp
            
            # Conecta e configura cliente FTP
            await deployer.connect()
            deployer.client = mock_ftp
            
            await deployer.upload_file(source_file, "/remote/test.py")
            mock_ftp.upload.assert_called_once()

@pytest.mark.asyncio
class TestLocalDeployer:
    @pytest.fixture
    async def local_deployer(self):
        """Fixture que fornece um LocalDeployer configurado"""
        config = {
            "dest_path": "/local/deploy/path",
            "ignore_patterns": ["*.log", "temp/"]
        }
        return LocalDeployer(config)

    @pytest.mark.asyncio
    async def test_local_file_copy(self, local_deployer, temp_project, tmp_path):
        """Testa cópia local de arquivos"""
        deployer = await local_deployer
        project_dir = await anext(temp_project)
        
        # Cria estrutura de diretórios
        source_file = project_dir / "config/settings.json"
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.write_text('{"test": true}')
        
        dest_file = str(tmp_path / "settings.json")
        Path(dest_file).parent.mkdir(parents=True, exist_ok=True)
        
        await deployer.upload_file(source_file, dest_file)
        assert Path(dest_file).exists()

    @pytest.mark.asyncio
    async def test_ignore_patterns(self, local_deployer, temp_project):
        """Testa padrões de ignore na cópia local"""
        deployer = await local_deployer
        project_dir = await anext(temp_project)
        
        # Cria estrutura de diretórios
        ignore_file = project_dir / "temp/ignored.log"
        ignore_file.parent.mkdir(parents=True, exist_ok=True)
        ignore_file.write_text("test")

        assert await deployer.should_ignore(ignore_file) 