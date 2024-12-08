# Guia de Contribuição

## Começando

1. Fork o projeto
2. Clone seu fork:
   ```bash
   git clone https://github.com/seu-usuario/noktech-deploy.git
   ```
3. Instale as dependências:
   ```bash
   cd noktech-deploy
   poetry install
   ```

## Ambiente de Desenvolvimento

### Configuração do Poetry

```bash
poetry shell
poetry install
```

### Estrutura do Projeto

```
noktech-deploy/
├── src/
│   ├── core/           # Funcionalidades principais
│   ├── protocols/      # Implementações de protocolos
│   ├── utils/          # Utilitários
│   └── i18n/           # Internacionalização
├── tests/              # Testes
├── docs/               # Documentação
└── examples/           # Exemplos de uso
```

## Padrões de Código

### Estilo

- Siga o PEP 8
- Use type hints
- Documente funções e classes
- Mantenha linhas com no máximo 88 caracteres

### Exemplo

```python
from typing import Optional

def process_file(path: str, options: Optional[dict] = None) -> bool:
    """
    Processa um arquivo com as opções especificadas.

    Args:
        path: Caminho do arquivo
        options: Opções de processamento

    Returns:
        bool: True se processado com sucesso
    """
    if not options:
        options = {}
    # ... implementação ...
    return True
```

## Testes

### Executando Testes

```bash
poetry run pytest
```

### Escrevendo Testes

```python
import pytest
from noktech_deploy.core import DeployClient

def test_deploy_client_initialization():
    client = DeployClient()
    assert client is not None
    assert client.config is not None
```

## Commits

### Formato da Mensagem

```
<tipo>: <descrição>

[corpo]

[rodapé]
```

### Tipos

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Alterações na documentação
- **style**: Formatação, ponto e vírgula faltando, etc
- **refactor**: Refatoração de código
- **test**: Adição/modificação de testes
- **chore**: Atualizações de build, etc

### Exemplo

```
feat: adiciona suporte para FTP sobre TLS

- Implementa cliente FTP com suporte a TLS
- Adiciona testes para conexão segura
- Atualiza documentação

Closes #123
```

## Pull Requests

1. Atualize seu fork
2. Crie uma branch para sua feature
3. Faça commits de suas alterações
4. Escreva/atualize testes
5. Atualize a documentação
6. Abra um Pull Request

### Template de PR

```markdown
## Descrição
Descreva suas alterações

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código segue os padrões
```

## Releases

### Versionamento

Seguimos [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH

### Processo

1. Atualize CHANGELOG.md
2. Atualize versão em pyproject.toml
3. Crie uma tag
4. Push para o repositório
5. Crie um release no GitHub

## Suporte

- Abra uma issue para dúvidas
- Use as discussões para ideias
- Entre em contato via email para questões privadas 