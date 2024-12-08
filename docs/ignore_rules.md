# Regras de Ignore

O NokTech Deploy oferece múltiplas formas de configurar quais arquivos devem ser ignorados durante o deploy.

## Arquivos de Configuração

### .deployignore (Recomendado)
Este arquivo tem prioridade sobre o `.gitignore` e é específico para o deploy:

```plaintext
# Arquivos de desenvolvimento
__pycache__/
*.pyc
.env
venv/

# Arquivos de build
dist/
build/

# Arquivos temporários
*.tmp
*.log

# IDEs e editores
.vscode/
.idea/
*.swp
```

### .gitignore
Se não existir um `.deployignore`, o sistema usará o `.gitignore` automaticamente.

## Padrões Padrão
Os seguintes padrões são sempre ignorados:
- `.git/`
- `__pycache__/`
- `*.pyc`, `*.pyo`, `*.pyd`
- `.env`, `venv/`, `.venv`
- `build/`, `dist/`
- `*.egg-info/`
- `.coverage`, `htmlcov/`
- `.idea/`, `.vscode/`
- `node_modules/`
- `.DS_Store`

## Modo Interativo
No modo interativo, você pode:
1. Escolher usar o `.gitignore` existente
2. Adicionar padrões personalizados
```bash
$ noktech-deploy

Configuração de arquivos ignorados:
Usar .gitignore? (s/n): s
Adicionar padrões personalizados? (s/n): s
Digite os padrões (um por linha, Enter vazio para terminar):
*.temp
logs/
temp/
```

## Linha de Comando
```bash
noktech-deploy --ignore-file .deployignore \
               --ignore-patterns "*.temp" "logs/" "temp/"
```

## Sintaxe dos Padrões
- `file.txt` - Ignora arquivo específico
- `*.ext` - Ignora por extensão
- `dir/` - Ignora diretório e seu conteúdo
- `dir/*.txt` - Ignora arquivos .txt no diretório
- `!important.log` - Não ignora arquivo específico (exceção) 