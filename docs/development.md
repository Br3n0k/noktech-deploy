# Guia de Desenvolvimento

## Ambiente de Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/noktech-deploy.git
cd noktech-deploy
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Instale dependências de desenvolvimento:
```bash
poetry install
```

## Estrutura do Projeto

```
noktech-deploy/
├── src/
│   ├── deployers/      # Implementações de protocolos
│   ├── core/           # Funcionalidades principais
│   └── utils/          # Utilitários
├── tests/              # Testes unitários e integração
├── docs/               # Documentação
└── examples/           # Exemplos de uso
```

## Testes

```bash
# Roda todos os testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=src

# Testes específicos
poetry run pytest tests/test_deployers.py
```

## Estilo de Código

Seguimos PEP 8 e usamos black para formatação:

```bash
# Verifica estilo
poetry run flake8

# Formata código
poetry run black .

# Verifica tipos
poetry run mypy .
```

## Criando um Novo Deployer

1. Crie uma nova classe em `src/deployers/`:
```python
from .base_deployer import BaseDeployer

class NewDeployer(BaseDeployer):
    def __init__(self, host: str, user: str, password: str, port: int):
        super().__init__(host, user, password, port)
        
    def connect(self) -> None:
        # Implementação
        pass
        
    def disconnect(self) -> None:
        # Implementação
        pass
        
    def deploy_files(self, files_path: str, dest_path: str) -> None:
        # Implementação
        pass
```

2. Adicione testes em `tests/test_deployers.py`
3. Atualize a documentação em `docs/`
4. Envie um Pull Request 