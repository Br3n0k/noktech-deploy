# Sistema de Ignore

O NokTech Deploy oferece um sistema flexível para ignorar arquivos e diretórios durante o deploy.

## Sintaxe Básica

### Comentários
```plaintext
# Este é um comentário
```

### Ignorar Arquivo Específico
```plaintext
config.json
.env
```

### Ignorar por Extensão
```plaintext
*.log
*.tmp
*.pyc
```

### Ignorar Diretório
```plaintext
node_modules/
__pycache__/
venv/
```

### Padrões Glob
```plaintext
**/*.pyc
**/temp/
docs/**/*.pdf
```

## Ordem de Precedência

1. Padrões via linha de comando (`--ignore-patterns`)
2. Arquivo `.deployignore` no diretório do projeto
3. Arquivo global `~/.deployignore`
4. Padrões padrão do sistema

## Padrões Padrão

O sistema inclui alguns padrões padrão:

```plaintext
# Arquivos de sistema
.DS_Store
Thumbs.db

# Arquivos de desenvolvimento
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.py[cod]
*$py.class

# Ambientes virtuais
.env
.venv
env/
venv/
ENV/

# Arquivos temporários
*.log
*.tmp
*.temp
*.swp
*~

# Diretórios de build
dist/
build/
*.egg-info/
```

## Exemplos Práticos

### Projeto Python
```plaintext
# Ambiente virtual
venv/
.env

# Cache Python
__pycache__/
*.pyc

# Arquivos de build
dist/
build/
*.egg-info

# Logs e temporários
*.log
.coverage
htmlcov/
```

### Projeto Node.js
```plaintext
# Dependências
node_modules/
package-lock.json

# Build
dist/
build/

# Ambiente
.env
.env.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

### Projeto Web
```plaintext
# Dependências
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

## Dicas e Boas Práticas

1. **Seja Específico**: Use padrões específicos em vez de muito genéricos
2. **Documente**: Adicione comentários explicando por que certos arquivos são ignorados
3. **Agrupe**: Organize padrões relacionados juntos
4. **Teste**: Verifique quais arquivos estão sendo ignorados antes do deploy

## Resolução de Problemas

### Arquivo Não Está Sendo Ignorado

1. Verifique a ordem de precedência
2. Confirme a sintaxe do padrão
3. Use `--debug` para ver quais padrões estão ativos

### Arquivo Sendo Ignorado Incorretamente

1. Verifique se não há padrões muito abrangentes
2. Use `!` para incluir explicitamente arquivos específicos
3. Revise os padrões padrão do sistema