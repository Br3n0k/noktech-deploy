<div align="right">
    <a href="README.md">🇧🇷 Português</a> &nbsp;&nbsp;|&nbsp;&nbsp;
    <a href="README_en.md">🇺🇸 English</a>
</div>

# NokTech Deploy

<p align="center">
  <img src="src/assets/logo.webp" alt="NokTech Deploy Logo" width="200"/>
</p>

Um cliente de deploy avançado e flexível com suporte a múltiplos protocolos e observação de mudanças em tempo real.
Perfeito para desenvolvedores que precisam de uma solução robusta e confiável para automatizar o processo de deploy,
seja via SSH, FTP ou mesmo localmente.

## 📋 Características

- **Múltiplos Protocolos**
  - SSH/SFTP (senha ou chave SSH)
  - FTP
  - Local (cópia de arquivos local/rede)
- **Observação em Tempo Real**
  - Detecta e sincroniza mudanças automaticamente
  - Suporte a eventos de criação, modificação e deleção
- **Sistema de Ignore Avançado**
  - Compatível com padrões .gitignore
  - Suporte a múltiplos arquivos de ignore
- **Interface Interativa**
  - Modo CLI com interface amigável
  - Suporte a argumentos para automação
- **Suporte Multi-idioma**
  - Português
  - Inglês
- **Logging Completo**
  - Logs detalhados de operações
  - Suporte a diferentes níveis de log

## 🚀 Instalação

### Via pip
```bash
pip install noktech-deploy
```

### Desenvolvimento
```bash
git clone https://github.com/Br3n0k/noktech-deploy.git
cd noktech-deploy
poetry install
```

## 💻 Uso

### Modo Interativo
```bash
noktech-deploy
```

### SSH
```bash
noktech-deploy --protocol ssh --host exemplo.com --user deploy --files-path ./dist --dest-path /var/www/app
```

### FTP
```bash
noktech-deploy --protocol ftp --host ftp.exemplo.com --user ftpuser --files-path ./site --dest-path /public_html
```

### Local
```bash
noktech-deploy --protocol local --files-path ./dados --dest-path /mnt/backup
```

### Modo Observador
```bash
noktech-deploy --protocol ssh --host exemplo.com --watch
```

## 📝 Configuração

### .deployignore
```plaintext
# Arquivos de desenvolvimento
__pycache__/
*.pyc
venv/

# Build e temporários
dist/
build/
*.tmp
*.log
```

### config.json
```json
{
    "default_protocol": "ssh",
    "hosts": {
        "production": {
            "protocol": "ssh",
            "host": "exemplo.com",
            "user": "deploy"
        }
    }
}
```

## 📚 Documentação

- [Guia de Início Rápido](docs/quickstart.md)
- [Configuração Avançada](docs/configuration.md)
- [API de Referência](docs/api.md)
- [Contribuindo](docs/contributing.md)

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Brendown Ferreira**
- GitHub: [@Br3n0k](https://github.com/Br3n0k)
- Email: br3n0k@gmail.com 