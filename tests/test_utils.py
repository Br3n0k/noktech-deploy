import pytest
import os
import tempfile
from src.utils.logger import Logger
from src.utils.config import Config


class TestLogger:
    def test_log_levels(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file = os.path.join(tmp_dir, "test.log")
            logger = Logger(log_file=log_file, log_level="DEBUG")

            # Testa diferentes níveis
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # Verifica se o arquivo foi criado
            assert os.path.exists(log_file)

            # Lê o conteúdo do log
            with open(log_file, "r") as f:
                content = f.read()

            # Verifica se todas as mensagens foram registradas
            assert "Debug message" in content
            assert "Info message" in content
            assert "Warning message" in content
            assert "Error message" in content


class TestConfig:
    @pytest.fixture
    def temp_config(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name

        config = Config(tmp_name)
        yield config

        try:
            # Remove o arquivo temporário ao invés de fechar
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
        except OSError:
            pass  # Ignora erros ao tentar remover arquivo temporário

    def test_save_load(self, temp_config):
        temp_config.set("test_key", "test_value")

        # Cria nova instância para testar load
        new_config = Config(temp_config.config_file)
        assert new_config.get("test_key") == "test_value"

    def test_delete(self, temp_config):
        temp_config.set("test_key", "test_value")
        temp_config.delete("test_key")
        assert temp_config.get("test_key") is None
