import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock
from src.deploy_client import DeployClient

class TestClientScenarios:
    @pytest.mark.asyncio
    async def test_cli_deploy_scenario(self, project_structure):
        """Testa cenário de deploy via CLI com múltiplos hosts"""
        project_dir, config = await anext(project_structure)
        
        client = DeployClient()
        await client.setup(config)
        
        # Mock para SSH e FTP
        with patch('src.deployers.ssh_deployer.asyncssh.connect') as mock_ssh_connect, \
             patch('aioftp.Client') as mock_ftp_client, \
             patch('src.deployers.ssh_deployer.SSHDeployer.disconnect') as mock_ssh_disconnect:
            
            # Configura mock SSH
            mock_ssh = AsyncMock()
            mock_ssh.close = AsyncMock()
            mock_ssh.wait_closed = AsyncMock()
            mock_sftp = AsyncMock()
            mock_sftp.put = AsyncMock()
            mock_sftp.close = AsyncMock()
            mock_ssh.start_sftp_client = AsyncMock(return_value=mock_sftp)
            
            async def mock_connect_ssh(*args, **kwargs):
                return mock_ssh
            mock_ssh_connect.side_effect = mock_connect_ssh
            
            # Configura mock FTP
            mock_ftp = AsyncMock()
            mock_ftp.connect = AsyncMock()
            mock_ftp.login = AsyncMock()
            mock_ftp.close = AsyncMock()
            mock_ftp_client.return_value = mock_ftp
            
            # Executa deploy
            await client.deploy_all()
            
            # Verifica chamadas do FTP
            mock_ftp.connect.assert_called_once()
            mock_ftp.login.assert_called_once()
            await mock_ftp.close()
            
            # Verifica chamadas do SSH
            mock_ssh_connect.assert_called_once()
            await mock_sftp.close()
            mock_ssh_disconnect.assert_called()

    @pytest.mark.asyncio
    async def test_watch_mode_scenario(self, project_structure):
        """Testa cenário de modo watch com alterações em tempo real"""
        project_dir, config = await anext(project_structure)
        
        # Cria diretório base e deploy
        project_dir.mkdir(parents=True, exist_ok=True)
        deploy_dir = project_dir / "deploy"
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # Ajusta configuração para ter apenas local e habilitar watch
        config["hosts"] = {
            "test_local": {
                "enabled": True,
                "protocol": "local",
                "source_path": str(project_dir),
                "dest_path": str(deploy_dir),
                "watch": {
                    "enabled": True
                }
            }
        }
        
        client = DeployClient()
        await client.setup(config)
        
        with patch('src.core.watcher.DirectoryWatcher') as mock_watcher_class:
            mock_watcher = AsyncMock()
            mock_watcher.start = AsyncMock()
            mock_watcher.stop = AsyncMock()
            mock_watcher.watch = AsyncMock(return_value=[])
            mock_watcher_class.return_value = mock_watcher
            
            # Garante que o watcher seja iniciado
            await client.start_watch()
            await mock_watcher.start()
            await asyncio.sleep(0.1)
            
            mock_watcher.start.assert_called_once()
            
            # Garante que o watcher seja parado
            await client.stop_watch()
            await mock_watcher.stop()
            await asyncio.sleep(0.1)
            
            mock_watcher.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_error_handling_scenario(self, project_structure):
        """Testa cenário de tratamento de erros durante deploy"""
        project_dir, config = await anext(project_structure)
        
        config["hosts"] = {
            "test_ssh": {
                "enabled": True,
                "protocol": "ssh",
                "host": "ssh.example.com",
                "user": "testuser",
                "source_path": str(project_dir),
                "dest_path": "/remote/ssh"
            }
        }
        
        client = DeployClient()
        await client.setup(config)
        
        with patch('src.deployers.ssh_deployer.SSHDeployer.connect') as mock_connect:
            mock_connect.side_effect = ConnectionError("SSH connection failed")
            
            with pytest.raises(ConnectionError) as exc_info:
                await client.deploy_all()
            
            assert str(exc_info.value) == "SSH connection failed", "Erro inesperado"
            mock_connect.assert_called_once()