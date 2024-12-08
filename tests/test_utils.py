import pytest
import os
import tempfile
from src.utils.logger import Logger
from src.utils.config import Config

class TestLogger:
    def test_log_levels(self):
        with tempfile.NamedTemporaryFile() as tmp:
            logger = Logger(log_file=tmp.name)
            
            logger.info("test info")
            logger.error("test error")
            
            content = tmp.read().decode()
            assert "INFO" in content
            assert "ERROR" in content
            
class TestConfig:
    @pytest.fixture
    def temp_config(self):
        with tempfile.NamedTemporaryFile() as tmp:
            config = Config(tmp.name)
            yield config
            
    def test_save_load(self, temp_config):
        temp_config.set('test_key', 'test_value')
        
        # Cria nova instância para testar load
        new_config = Config(temp_config.config_file)
        assert new_config.get('test_key') == 'test_value'
        
    def test_delete(self, temp_config):
        temp_config.set('test_key', 'test_value')
        temp_config.delete('test_key')
        assert temp_config.get('test_key') is None 