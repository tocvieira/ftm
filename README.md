# FTM - Follow the Money

[![Python Version](https://img.shields.io/badge/python-3.5+-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.2.28-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/license-Open%20Source-brightgreen.svg)](LICENSE)

## 📋 Sobre o Projeto

Uma característica comum à maioria dos crimes perpetrados através da internet é a transnacionalidade. Um website de distribuição de pornografia infantil, por exemplo, pode ter o nome de domínio Sueco (.se), um provedor Russo e um CDN (Content Delivery Network) sediado nos EUA com servidores espalhados por todo o mundo.

Qual o caminho a ser percorrido pela autoridade brasileira que estiver a cargo de identificar e responsabilizar o autor do delito? Os pedidos de cooperação internacional, ainda que haja acordo entre o Brasil e o país destinatário, demanda muito tempo. Por esta razão só devem ser utilizados quando forem estritamente necessários e da forma mais eficaz, buscando sempre alcançar a prova de autoria do delito com o menor número possível de interações internacionais.

Com o fito de auxiliar as autoridades brasileiras e as vítimas, desenvolvemos o **Follow the Money – FTM**, um software livre escrito em Python, que reúne informações publicamente disponíveis que possam levar à autoria do ilícito.

### 🎯 Funcionalidades

- **Análise de Domínios**: Informações sobre registro, DNS e hospedagem
- **Extração de Links**: Coleta todos os links internos e externos do site
- **Detecção de Tecnologias**: Identifica frameworks, CMS, bibliotecas e serviços utilizados
- **Extração de Contatos**: Localiza emails e telefones disponíveis publicamente
- **Análise de IDs**: Detecta códigos de rastreamento (Google Analytics, Facebook Pixel, etc.)
- **Bypass Cloudflare**: Suporte avançado para contornar proteções anti-bot

### ⚖️ Aspectos Legais

**Importante**: Não há qualquer mecanismo intrusivo. Todas as informações estão publicamente disponíveis e poderiam ser capturadas de maneira manual. A metodologia e o licenciamento livre, além de respeitarem a lei, permitem que a parte interessada possa reproduzir cada uma das etapas, garantindo o contraditório e a ampla defesa.

## 🚀 Instalação

### Pré-requisitos

- Python 3.5 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/ftm.git
   cd ftm
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as migrações do Django**
   ```bash
   python manage.py migrate
   ```

6. **Inicie o servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acesse a aplicação**
   Abra seu navegador e vá para `http://localhost:8000`

## 📖 Como Usar

1. Acesse a interface web em `http://localhost:8000`
2. Digite a URL do site que deseja analisar
3. Clique em "Analisar"
4. Aguarde o processamento e visualize os resultados

### Exemplo de Uso via Linha de Comando

```python
from ftm.get_ids_fixed import get_ids

# Analisar um site
resultado = get_ids("https://exemplo.com")
print(f"IDs encontrados: {len(resultado['ids'])}")
print(f"Links encontrados: {len(resultado['links'])}")
print(f"Tecnologias: {len(resultado['technologies'])}")
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 2.2.28
- **Web Scraping**: BeautifulSoup4, Requests
- **Bypass Anti-bot**: Cloudscraper, Undetected Chrome Driver
- **Análise de Tecnologias**: Wappalyzer
- **DNS/WHOIS**: dnspython, pythonwhois, ipwhois

## 🤝 Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. **Commit suas mudanças**
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. **Push para a branch**
   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. **Abra um Pull Request**

### 📝 Diretrizes para Contribuição

- Mantenha o código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções de código Python (PEP 8)
- Atualize a documentação quando necessário

## 🐛 Reportar Bugs

Encontrou um bug? Por favor, abra uma [issue](https://github.com/seu-usuario/ftm/issues) com:

- Descrição detalhada do problema
- Passos para reproduzir
- Ambiente (SO, versão do Python, etc.)
- Screenshots (se aplicável)

## 📄 Licença

Este projeto é software livre e está disponível sob licença open source.

## 👥 Autores

- **Thiago Oliveira Castro Vieira** - *Desenvolvedor Principal*
- **Comunidade Welcome to The Django** - *Apoio e Contribuições*

## 🙏 Agradecimentos

- Comunidade Welcome to The Django
- Contribuidores do projeto
- Autoridades brasileiras que utilizam a ferramenta

---

**⚠️ Aviso Legal**: Esta ferramenta deve ser utilizada apenas para fins legítimos e em conformidade com as leis aplicáveis. Os desenvolvedores não se responsabilizam pelo uso inadequado da ferramenta.
