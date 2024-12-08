# Contributing Guide

## Getting Started

1. Fork the project
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/noktech-deploy.git
   ```
3. Install dependencies:
   ```bash
   cd noktech-deploy
   poetry install
   ```

## Development Environment

### Poetry Setup

```bash
poetry shell
poetry install
```

### Project Structure

```
noktech-deploy/
├── src/
│   ├── core/           # Core functionality
│   ├── protocols/      # Protocol implementations
│   ├── utils/          # Utilities
│   └── i18n/           # Internationalization
├── tests/              # Tests
├── docs/               # Documentation
└── examples/           # Usage examples
```

## Code Standards

### Style

- Follow PEP 8
- Use type hints
- Document functions and classes
- Keep lines at maximum 88 characters

### Example

```python
from typing import Optional

def process_file(path: str, options: Optional[dict] = None) -> bool:
    """
    Process a file with the specified options.

    Args:
        path: File path
        options: Processing options

    Returns:
        bool: True if processed successfully
    """
    if not options:
        options = {}
    # ... implementation ...
    return True
```

## Tests

### Running Tests

```bash
poetry run pytest
```

### Writing Tests

```python
import pytest
from noktech_deploy.core import DeployClient

def test_deploy_client_initialization():
    client = DeployClient()
    assert client is not None
    assert client.config is not None
```

## Commits

### Message Format

```
<type>: <description>

[body]

[footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc
- **refactor**: Code refactoring
- **test**: Adding/modifying tests
- **chore**: Build updates, etc

### Example

```
feat: add support for FTP over TLS

- Implements FTP client with TLS support
- Adds tests for secure connection
- Updates documentation

Closes #123
```

## Pull Requests

1. Update your fork
2. Create a feature branch
3. Commit your changes
4. Write/update tests
5. Update documentation
6. Open a Pull Request

### PR Template

```markdown
## Description
Describe your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows standards
```

## Releases

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH

### Process

1. Update CHANGELOG.md
2. Update version in pyproject.toml
3. Create a tag
4. Push to repository
5. Create a GitHub release

## Support

- Open an issue for questions
- Use discussions for ideas
- Contact via email for private matters 