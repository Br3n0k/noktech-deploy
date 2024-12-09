import pytest
from unittest.mock import patch, MagicMock
from src.deploy_client import DeployClient, main


class TestCLI:
    def test_argument_parsing(self):
        """Testa parsing de argumentos da CLI"""
        parser = DeployClient.create_parser()

        args = parser.parse_args(
            [
                "--protocol",
                "ssh",
                "--host",
                "test.com",
                "--user",
                "testuser",
                "--dest-path",
                "/test",
                "--files-path",
                "./src",
            ]
        )

        assert args.protocol == "ssh"
        assert args.host == "test.com"
        assert args.user == "testuser"

    def test_invalid_arguments(self):
        """Testa validação de argumentos inválidos"""
        parser = DeployClient.create_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--protocol", "invalid"])

    @pytest.mark.asyncio
    @patch("src.deploy_client.SSHDeployer")
    async def test_ssh_deployer_setup(self, mock_ssh):
        """Testa configuração do deployer SSH"""
        client = DeployClient()
        args = type(
            "Args",
            (),
            {
                "protocol": "ssh",
                "host": "test.com",
                "user": "testuser",
                "password": "testpass",
                "port": 22,
                "key_path": None,
            },
        )()

        await client.setup_deployer(args)

        mock_ssh.assert_called_once_with(
            host="test.com",
            user="testuser",
            password="testpass",
            port=22,
            key_path=None,
        )

    @pytest.mark.asyncio
    async def test_main_function(self):
        """Testa função principal"""
        with patch("src.deploy_client.DeployClient") as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance

            async def mock_run(args):
                return 0

            mock_instance.run = MagicMock(side_effect=mock_run)

            with patch("sys.argv", ["noktech-deploy", "--protocol", "ssh"]):
                result = await main()
                assert result == 0
                assert mock_instance.run.call_count == 1
