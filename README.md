# NokTech Deploy

Um cliente de deploy avançado e flexível com suporte a múltiplos protocolos e observação de mudanças em tempo real.

## Características

- Suporte a múltiplos protocolos:
  - SSH/SFTP (com suporte a senha ou chave SSH)
  - FTP
  - Local (cópia de arquivos local/rede)
- Observação de mudanças em tempo real
- Respeita regras de ignore (.gitignore e padrões personalizados)
- Mantém estrutura de diretórios
- Criação automática de diretórios remotos
- Tratamento seguro de senhas
- Logging completo
- Configurações persistentes

## Instalação

### Via pip
```bash
pip install noktech-deploy
```

### Instalação Local (Desenvolvimento)
```bash
# Clone o repositório
git clone https://github.com/Br3n0k/noktech-deploy.git
cd noktech-deploy

# Método 1: Instalação em modo desenvolvimento
pip install -e .

# Método 2: Usando poetry
poetry install

# Método 3: Instalação direta
python setup.py install
```

## Uso

### Deploy com SSH (Senha)
```bash
noktech-deploy --protocol ssh \
               --host exemplo.com \
               --user deploy \
               --password "sua_senha" \
               --dest-path /var/www/app \
               --files-path ./dist
```

### Deploy com SSH (Chave)
```bash
noktech-deploy --protocol ssh \
               --host exemplo.com \
               --user deploy \
               --key-path ~/.ssh/id_rsa \
               --dest-path /var/www/app \
               --files-path ./dist
```

### Deploy FTP
```bash
noktech-deploy --protocol ftp \
               --host ftp.exemplo.com \
               --user ftpuser \
               --password senha123 \
               --dest-path /public_html \
               --files-path ./site
```

### Deploy Local
```bash
noktech-deploy --protocol local \
               --dest-path /mnt/backup \
               --files-path ./dados
```

### Modo Observador
```bash
noktech-deploy --protocol ssh \
               --host exemplo.com \
               --user deploy \
               --password "sua_senha" \
               --dest-path /var/www/app \
               --files-path ./src \
               --watch
```

## Configuração

O NokTech Deploy armazena configurações em `~/.noktech-deploy/config.json`. 

### Acessando a Configuração

#### Windows
```powershell
# CMD
cd %USERPROFILE%\.noktech-deploy

# PowerShell
cd $env:USERPROFILE\.noktech-deploy
```

#### Linux/Mac
```bash
cd ~/.noktech-deploy
```

## Desenvolvimento

```bash
# Instalar dependências
poetry install

# Rodar testes
poetry run pytest

# Verificar estilo
poetry run flake8
poetry run black .

# Verificar tipos
poetry run mypy .
```

## Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações. 