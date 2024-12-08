# API Reference

## DeployClient Class

The main class that manages all deployment operations.

### Methods

#### `__init__(self, config_path: Optional[str] = None)`
Initializes a new deploy client.
- **config_path**: Optional path to configuration file

#### `async def run(self, args: Args)`
Executes the deployment process with the provided arguments.
- **args**: Args object with deployment settings

#### `async def interactive_mode(self)`
Starts the interactive mode for deployment configuration.

#### `async def watch_mode(self)`
Starts the change observation mode.

## Args Class

Class that encapsulates command line arguments.

### Attributes

- **protocol**: Deployment protocol (`ssh`, `ftp`, `local`)
- **host**: Target host
- **user**: Authentication username
- **password**: Authentication password
- **key_path**: Path to SSH key
- **files_path**: Source files path
- **dest_path**: Destination path
- **watch**: Watch mode flag
- **ignore_patterns**: List of patterns to ignore

## Protocols

### SSHDeployer

Implements deployment via SSH/SFTP.

#### Main Methods

```python
async def connect(self)
async def disconnect(self)
async def upload_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

### FTPDeployer

Implements deployment via FTP.

#### Main Methods

```python
async def connect(self)
async def disconnect(self)
async def upload_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

### LocalDeployer

Implements local deployment.

#### Main Methods

```python
async def connect(self)
async def disconnect(self)
async def copy_file(self, source: str, dest: str)
async def delete_file(self, path: str)
```

## Event System

### FileEvent Class

Represents a file change event.

#### Attributes

- **event_type**: Event type (`created`, `modified`, `deleted`)
- **src_path**: Source file path
- **is_directory**: Flag indicating if it's a directory

## Logging

### Logger Class

Manages the logging system.

#### Methods

```python
def info(self, message: str)
def error(self, message: str)
def debug(self, message: str)
def warning(self, message: str)
```

## Usage Examples

### Basic Deployment

```python
from noktech_deploy import DeployClient, Args

async def main():
    client = DeployClient()
    args = Args(
        protocol="ssh",
        host="example.com",
        user="deploy",
        files_path="./dist",
        dest_path="/var/www/app"
    )
    await client.run(args)
```

### Custom Watch Mode

```python
from noktech_deploy import DeployClient, Args

async def main():
    client = DeployClient()
    args = Args(
        protocol="local",
        files_path="./src",
        dest_path="./dist",
        watch=True,
        ignore_patterns=["*.tmp", "*.log"]
    )
    await client.watch_mode(args)
``` 