# Ignore System

NokTech Deploy offers a flexible system for ignoring files and directories during deployment.

## Basic Syntax

### Comments
```plaintext
# This is a comment
```

### Ignore Specific File
```plaintext
config.json
.env
```

### Ignore by Extension
```plaintext
*.log
*.tmp
*.pyc
```

### Ignore Directory
```plaintext
node_modules/
__pycache__/
venv/
```

### Glob Patterns
```plaintext
**/*.pyc
**/temp/
docs/**/*.pdf
```

## Order of Precedence

1. Patterns via command line (`--ignore-patterns`)
2. `.deployignore` file in project directory
3. Global `~/.deployignore` file
4. System default patterns

## Default Patterns

The system includes some default patterns:

```plaintext
# System files
.DS_Store
Thumbs.db

# Development files
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.py[cod]
*$py.class

# Virtual environments
.env
.venv
env/
venv/
ENV/

# Temporary files
*.log
*.tmp
*.temp
*.swp
*~

# Build directories
dist/
build/
*.egg-info/
```

## Practical Examples

### Python Project
```plaintext
# Virtual environment
venv/
.env

# Python cache
__pycache__/
*.pyc

# Build files
dist/
build/
*.egg-info

# Logs and temporary
*.log
.coverage
htmlcov/
```

### Node.js Project
```plaintext
# Dependencies
node_modules/
package-lock.json

# Build
dist/
build/

# Environment
.env
.env.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

### Web Project
```plaintext
# Dependencies
node_modules/
vendor/

# Build
dist/
build/
*.min.js
*.min.css

# Cache
.cache/
.temp/

# IDE
.vscode/
.idea/
```

## Tips and Best Practices

1. **Be Specific**: Use specific patterns instead of overly generic ones
2. **Document**: Add comments explaining why certain files are ignored
3. **Group**: Organize related patterns together
4. **Test**: Verify which files are being ignored before deployment

## Troubleshooting

### File Not Being Ignored

1. Check the order of precedence
2. Confirm pattern syntax
3. Use `--debug` to see which patterns are active

### File Being Incorrectly Ignored

1. Check for overly broad patterns
2. Use `!` to explicitly include specific files
3. Review system default patterns
 