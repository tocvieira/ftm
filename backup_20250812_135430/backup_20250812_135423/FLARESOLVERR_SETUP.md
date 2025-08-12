# Guia de Instalação do FlareSolverr

## O que é o FlareSolverr?

O FlareSolverr é uma solução premium para bypass do Cloudflare em 2025, baseada nas pesquisas mais recentes. Ele funciona como um proxy reverso que usa Selenium com undetected-chromedriver para simular um navegador real e contornar as proteções do Cloudflare.

## Instalação via Docker (Recomendado)

### 1. Instalar Docker

Baixe e instale o Docker Desktop para Windows:
- Acesse: https://www.docker.com/get-started
- Baixe o Docker Desktop para Windows
- Execute o instalador e siga as instruções
- Reinicie o computador se necessário

### 2. Verificar Instalação do Docker

Abra o PowerShell e execute:
```powershell
docker --version
```

### 3. Baixar e Executar FlareSolverr

No PowerShell, execute os seguintes comandos:

```powershell
# Baixar a imagem do FlareSolverr
docker pull flaresolverr/flaresolverr

# Executar o container
docker run -d --name=flaresolverr -p 8191:8191 -e LOG_LEVEL=info --restart unless-stopped flaresolverr/flaresolverr
```

### 4. Verificar se está Funcionando

Abra seu navegador e acesse:
```
http://localhost:8191
```

Você deve ver uma mensagem confirmando que o FlareSolverr está rodando.

## Comandos Úteis

### Verificar Status do Container
```powershell
docker ps
```

### Parar o FlareSolverr
```powershell
docker stop flaresolverr
```

### Iniciar o FlareSolverr
```powershell
docker start flaresolverr
```

### Ver Logs do FlareSolverr
```powershell
docker logs flaresolverr
```

### Remover o Container (se necessário)
```powershell
docker stop flaresolverr
docker rm flaresolverr
```

## Configuração no FTM

Após instalar o FlareSolverr, reinicie o servidor Django:

1. Pare o servidor atual (Ctrl+C no terminal)
2. Execute novamente:
   ```
   venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
   ```

Você deve ver a mensagem:
```
✓ FlareSolverr detectado - bypass premium do Cloudflare ativado
```

## Vantagens do FlareSolverr

- ✅ **Mais Eficaz**: Taxa de sucesso superior ao cloudscraper
- ✅ **Atualizado**: Solução de 2025 com as técnicas mais recentes
- ✅ **Robusto**: Usa navegador real para contornar detecções avançadas
- ✅ **Automático**: Funciona sem configuração adicional
- ✅ **Suporte a CAPTCHA**: Pode resolver alguns tipos de CAPTCHA

## Solução de Problemas

### Erro "Docker não encontrado"
- Certifique-se de que o Docker Desktop está instalado e rodando
- Reinicie o computador após a instalação

### Porta 8191 em uso
- Mude a porta no comando docker:
  ```powershell
  docker run -d --name=flaresolverr -p 8192:8191 -e LOG_LEVEL=info --restart unless-stopped flaresolverr/flaresolverr
  ```
- Atualize a URL no código para `http://localhost:8192/v1`

### FlareSolverr não detectado
- Verifique se o container está rodando: `docker ps`
- Teste o acesso: `http://localhost:8191`
- Reinicie o servidor Django

## Recursos Adicionais

- **Documentação Oficial**: https://github.com/FlareSolverr/FlareSolverr
- **Docker Hub**: https://hub.docker.com/r/flaresolverr/flaresolverr
- **Guias Avançados**: https://www.zenrows.com/blog/flaresolverr