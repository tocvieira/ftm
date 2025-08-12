# Contribuindo para o FTM - Follow the Money

Obrigado por considerar contribuir para o FTM! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e inclusivo para todos os contribuidores.

## 🚀 Como Contribuir

### Reportando Bugs

Antes de reportar um bug, verifique se ele já não foi reportado nas [issues existentes](https://github.com/seu-usuario/ftm/issues).

Para reportar um bug:

1. Use um título claro e descritivo
2. Descreva os passos exatos para reproduzir o problema
3. Inclua informações sobre seu ambiente:
   - Sistema operacional
   - Versão do Python
   - Versão do Django
   - Outras dependências relevantes
4. Inclua screenshots ou logs de erro, se aplicável
5. Descreva o comportamento esperado vs. o comportamento atual

### Sugerindo Melhorias

Para sugerir uma nova funcionalidade ou melhoria:

1. Verifique se a sugestão já não existe nas issues
2. Crie uma nova issue com o label "enhancement"
3. Descreva claramente a funcionalidade proposta
4. Explique por que essa funcionalidade seria útil
5. Forneça exemplos de uso, se possível

### Contribuindo com Código

#### Configuração do Ambiente de Desenvolvimento

1. **Fork o repositório**
   ```bash
   git clone https://github.com/seu-usuario/ftm.git
   cd ftm
   ```

2. **Configure o ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**
   ```bash
   python manage.py migrate
   ```

#### Processo de Desenvolvimento

1. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nome-da-funcionalidade
   ```

2. **Faça suas alterações**
   - Mantenha o código limpo e bem documentado
   - Siga as convenções de código Python (PEP 8)
   - Adicione comentários quando necessário

3. **Teste suas alterações**
   ```bash
   python test_get_ids.py
   python manage.py runserver
   ```

4. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

5. **Push para sua branch**
   ```bash
   git push origin feature/nome-da-funcionalidade
   ```

6. **Abra um Pull Request**

#### Convenções de Commit

Use mensagens de commit claras e descritivas:

- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para mudanças na documentação
- `style:` para mudanças de formatação
- `refactor:` para refatoração de código
- `test:` para adição ou modificação de testes
- `chore:` para tarefas de manutenção

Exemplos:
```
feat: adiciona suporte para bypass de Cloudflare
fix: corrige erro de encoding em páginas UTF-8
docs: atualiza README com instruções de instalação
```

## 🧪 Testes

Antes de submeter um Pull Request:

1. Execute os testes existentes:
   ```bash
   python test_get_ids.py
   ```

2. Teste manualmente a interface web:
   ```bash
   python manage.py runserver
   ```

3. Verifique se não há erros no console

## 📝 Diretrizes de Código

### Python

- Siga o PEP 8 para estilo de código
- Use nomes descritivos para variáveis e funções
- Adicione docstrings para funções complexas
- Mantenha funções pequenas e focadas
- Use type hints quando apropriado

### Django

- Siga as convenções do Django
- Use templates para renderização HTML
- Mantenha views simples e lógica no modelo
- Use formulários Django quando possível

### Frontend

- Use HTML semântico
- Mantenha CSS organizado
- Teste em diferentes navegadores
- Garanta responsividade

## 🔒 Segurança

- Nunca commite credenciais ou chaves de API
- Use variáveis de ambiente para configurações sensíveis
- Valide todas as entradas do usuário
- Siga práticas de segurança web

## 📚 Documentação

- Atualize o README.md se necessário
- Documente novas funcionalidades
- Inclua exemplos de uso
- Mantenha comentários atualizados

## ❓ Dúvidas

Se você tiver dúvidas sobre como contribuir:

1. Verifique a documentação existente
2. Procure em issues fechadas
3. Abra uma nova issue com a tag "question"
4. Entre em contato com os mantenedores

## 🙏 Reconhecimento

Todos os contribuidores serão reconhecidos no README.md do projeto.

Obrigado por contribuir para o FTM! 🚀