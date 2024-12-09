# Deployers API Reference

## BaseDeployer

Abstract base class for all deployers.

```python
from src.deployers import BaseDeployer

class CustomDeployer(BaseDeployer):
    async def deploy_file(self, source: str, dest: str):
        # Implementation
        pass
```

### Methods

#### `async deploy_file(source: str, dest: str)`
Deploy a single file.
- `source`: Source file path
- `dest`: Destination file path

#### `async deploy_directory(source_dir: str, dest_dir: str)`
Deploy an entire directory.
- `source_dir`: Source directory
- `dest_dir`: Destination directory

## SSHDeployer

Deployer for SSH protocol.

```python
from src.deployers import SSHDeployer

deployer = SSHDeployer(
    host="example.com",
    user="deploy",
    password="secret"  # or key_path="~/.ssh/id_rsa"
)
```

### Methods

#### `__init__(host: str, user: str, password: Optional[str] = None, key_path: Optional[str] = None)`
- `host`: Remote host
- `user`: SSH username
- `password`: SSH password
- `key_path`: Path to SSH key file

## LocalDeployer

Deployer for local file operations.

```python
from src.deployers import LocalDeployer

deployer = LocalDeployer()
```

### Methods

#### `async backup_file(path: str) -> str`
Creates a backup of a file.
- Returns: Backup file path

#### `async restore_backup(backup_path: str, original_path: str)`
Restores a file from backup. 