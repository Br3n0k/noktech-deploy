# Protocolos Suportados

## SSH/SFTP

O protocolo SSH/SFTP é recomendado para deployments seguros. Suporta dois métodos de autenticação:

### Autenticação por Senha
```bash
noktech-deploy --protocol ssh \
               --host servidor.com \
               --user deploy \
               --password "sua_senha" \
               --dest-path /var/www/app
```

### Autenticação por Chave SSH (Recomendado)
```bash
noktech-deploy --protocol ssh \
               --host servidor.com \
               --user deploy \
               --key-path ~/.ssh/id_rsa \
               --dest-path /var/www/app
```

### Características
- Transferência criptografada
- Preservação de permissões de arquivos
- Suporte a chaves SSH e senhas
- Conexão segura e confiável
- Ideal para ambientes de produção

### Considerações de Segurança
- A autenticação por chave SSH é mais segura que por senha
- Use senhas fortes se optar por autenticação por senha
- Mantenha suas chaves SSH protegidas
- Considere usar `ssh-agent` para gerenciar chaves

## FTP

Protocolo FTP tradicional. Adequado para:
- Hospedagens compartilhadas
- Servidores web simples
- Situações onde SSH não está disponível

### Exemplo:
```bash
noktech-deploy --protocol ftp \
               --host ftp.site.com \
               --user ftpuser \
               --password senha123 \
               --dest-path /public_html
```

## Local

Deploy para diretório local ou compartilhamento de rede. Útil para:
- Backups
- Sincronização de pastas
- Testes locais
- Compartilhamentos de rede

### Exemplo:
```bash
noktech-deploy --protocol local \
               --dest-path /mnt/backup \
               --files-path ./dados
``` 