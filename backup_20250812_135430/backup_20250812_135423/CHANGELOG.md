# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Adicionado
- Documentação completa do projeto (README.md, CONTRIBUTING.md, LICENSE)
- Arquivo .gitignore abrangente seguindo melhores práticas
- Suporte para bypass avançado de Cloudflare com múltiplas estratégias
- Detecção automática de tecnologias usando Wappalyzer
- Extração de informações de contato (emails e telefones)
- Sistema de análise de IDs de rastreamento
- Interface web moderna e responsiva

### Corrigido
- Problema de descompressão de conteúdo HTML corrompido
- Erro "TypeError: 'set' object is not subscriptable" na extração de dados
- Problemas de encoding em páginas com diferentes codificações
- Tratamento adequado de headers de compressão (gzip, deflate)

### Melhorado
- Performance na extração de links e análise de páginas
- Tratamento de erros mais robusto
- Logging e debug mais informativos
- Estrutura de código mais limpa e modular

### Removido
- Prints de debug desnecessários do código de produção
- Arquivos temporários e de teste do repositório

## [1.0.0] - Data do primeiro release

### Adicionado
- Versão inicial do FTM (Follow the Money)
- Funcionalidade básica de análise de domínios
- Extração de informações WHOIS
- Interface web básica com Django
- Análise de DNS e hospedagem

---

### Tipos de Mudanças

- `Adicionado` para novas funcionalidades
- `Alterado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas