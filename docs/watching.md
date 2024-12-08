# Modo de Observação

O modo de observação permite monitorar mudanças em tempo real e fazer deploy automático.

## Funcionamento

- Monitora criação, modificação e remoção de arquivos
- Respeita regras de ignore
- Debouncing para evitar múltiplos deploys
- Logging de todas as operações

## Uso

```bash
noktech-deploy --watch \
    --protocol ssh \
    --host exemplo.com \
    --files-path ./src \
    --dest-path /var/www/app
```

## Configurações Avançadas

### Debouncing

O tempo de espera entre detecção de mudança e deploy pode ser configurado:

```bash
noktech-deploy --watch \
    --watch-delay 2.0  # Espera 2 segundos
```

### Eventos

Você pode escolher quais eventos observar:

```bash
noktech-deploy --watch \
    --watch-events create,modify  # Ignora deleções
```

### Filtros

Filtrar arquivos específicos durante observação:

```bash
noktech-deploy --watch \
    --watch-pattern "*.js,*.css"  # Apenas JS e CSS
``` 