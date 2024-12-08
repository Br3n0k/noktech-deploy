# Supported Protocols

## SSH/SFTP

The SSH/SFTP protocol is recommended for secure deployments. It supports two authentication methods:

### Password Authentication
```bash
noktech-deploy --protocol ssh \
               --host server.com \
               --user deploy \
               --password "your_password" \
               --dest-path /var/www/app
```

### SSH Key Authentication (Recommended)
```bash
noktech-deploy --protocol ssh \
               --host server.com \
               --user deploy \
               --key-path ~/.ssh/id_rsa \
               --dest-path /var/www/app
```

### Features
- Encrypted transfer
- File permissions preservation
- Support for SSH keys and passwords
- Secure and reliable connection
- Ideal for production environments

### Security Considerations
- SSH key authentication is more secure than password
- Use strong passwords if opting for password authentication
- Keep your SSH keys protected
- Consider using `ssh-agent` for key management

## FTP

Traditional FTP protocol. Suitable for:
- Shared hosting
- Simple web servers
- Situations where SSH is not available

### Example:
```bash
noktech-deploy --protocol ftp \
               --host ftp.site.com \
               --user ftpuser \
               --password pass123 \
               --dest-path /public_html
```

## Local

Deploy to local directory or network share. Useful for:
- Backups
- Folder synchronization
- Local testing
- Network shares

### Example:
```bash
noktech-deploy --protocol local \
               --dest-path /mnt/backup \
               --files-path ./data
``` 