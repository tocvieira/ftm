import random
import time
import urllib.request
import gzip
import re
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Importa cloudscraper se disponível (solução mais eficaz para Cloudflare)
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
    print("✓ Cloudscraper disponível - bypass avançado do Cloudflare ativado")
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    print("⚠ Cloudscraper não instalado. Para melhor bypass do Cloudflare, instale com: pip install cloudscraper")

# Importa undetected-chromedriver se disponível (solução robusta para Cloudflare 2025)
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    UNDETECTED_CHROME_AVAILABLE = True
    print("✓ Undetected-chromedriver disponível - bypass stealth do Cloudflare ativado")
except ImportError:
    UNDETECTED_CHROME_AVAILABLE = False
    print("⚠ Undetected-chromedriver não instalado. Para bypass stealth do Cloudflare, instale com: pip install undetected-chromedriver selenium")

# Importa requests-html se disponível (alternativa estável ao Chrome)
try:
    from requests_html import HTMLSession
    REQUESTS_HTML_AVAILABLE = True
    print("✓ Requests-html disponível - simulação de navegador estável ativada")
except ImportError:
    REQUESTS_HTML_AVAILABLE = False
    print("⚠ Requests-html não instalado. Para simulação de navegador estável, instale com: pip install requests-html")

# Configuração do FlareSolverr (solução mais robusta para Cloudflare 2025)
FLARESOLVERR_URL = "http://localhost:8191/v1"
FLARESOLVERR_AVAILABLE = False

# Testa se FlareSolverr está disponível
try:
    test_response = requests.get("http://localhost:8191", timeout=5)
    if test_response.status_code == 200:
        FLARESOLVERR_AVAILABLE = True
        print("✓ FlareSolverr detectado - bypass premium do Cloudflare ativado")
except:
    print("⚠ FlareSolverr não detectado. Para bypass premium do Cloudflare, instale FlareSolverr via Docker")

def get_ids(url):
    ids = []
    links = []
    technologies = []
    contact_info = []
    
    try:
        # Adiciona http:// se não estiver presente (prioriza HTTP para evitar problemas SSL)
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        
        # Se a URL original era HTTPS mas tem problemas SSL, tenta HTTP
        original_url = url
        urls_to_try = [url]
        if url.startswith('https://'):
            urls_to_try.append(url.replace('https://', 'http://'))
        elif url.startswith('http://'):
            urls_to_try.append(url.replace('http://', 'https://'))
        
        # Lista de user agents para rotação
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'
        ]
        
        # Headers mais completos para simular um navegador real
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'identity',  # Força conteúdo não comprimido
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache'
        }
        
        # Função para tentar acessar a URL com diferentes configurações
        def try_access_url(current_url, current_headers, is_retry=False):
            try:
                # Adiciona um atraso aleatório para parecer mais humano
                if is_retry:
                    time.sleep(random.uniform(2, 5))
                
                # Configura sessão com retry strategy
                session = requests.Session()
                retry_strategy = Retry(
                    total=3,
                    status_forcelist=[429, 500, 502, 503, 504],
                    allowed_methods=["HEAD", "GET", "OPTIONS"]
                )
                adapter = HTTPAdapter(max_retries=retry_strategy)
                session.mount("http://", adapter)
                session.mount("https://", adapter)
                
                # Headers mais completos para contornar proteções
                enhanced_headers = current_headers.copy()
                enhanced_headers.update({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'identity',  # Força conteúdo não comprimido
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"'
                })
                
                response = session.get(current_url, headers=enhanced_headers, timeout=30, allow_redirects=True)
                response.raise_for_status()
                
                # Força descompressão manual se necessário
                import gzip
                import zlib
                
                content = response.content
                html_text = None
                
                # Tenta diferentes métodos de descompressão
                try:
                    # Primeiro tenta response.text (automático)
                    html_text = response.text
                    if html_text and len(html_text) > 1000 and html_text.startswith('<'):
                        print(f"🔍 DEBUG: Usando response.text automático - {len(html_text)} caracteres")
                        return html_text
                except:
                    pass
                
                # Se response.text falhou, tenta descompressão manual
                try:
                    # Tenta gzip
                    if content[:2] == b'\x1f\x8b':  # Magic number do gzip
                        content = gzip.decompress(content)
                    # Tenta deflate
                    elif response.headers.get('content-encoding') in ['deflate', 'compress']:
                        content = zlib.decompress(content)
                    
                    # Decodifica para texto
                    html_text = content.decode('utf-8', errors='ignore')
                    
                except Exception as decomp_error:
                    # Fallback: tenta decodificar diretamente
                    try:
                        html_text = response.content.decode('utf-8', errors='ignore')
                    except:
                        html_text = response.text
                
                return html_text
                
            except Exception as e:
                if not is_retry:
                    # Tenta com outro User-Agent em caso de falha
                    current_headers['User-Agent'] = random.choice(user_agents)
                    return try_access_url(current_url, current_headers, True)
                raise e
        
        # Função para usar FlareSolverr (solução premium 2025)
        def use_flaresolverr(target_url):
            try:
                print("🚀 Tentativa com FlareSolverr (solução premium 2025)")
                
                payload = {
                    "cmd": "request.get",
                    "url": target_url,
                    "maxTimeout": 60000,
                    "proxy": None
                }
                
                headers = {"Content-Type": "application/json"}
                
                response = requests.post(FLARESOLVERR_URL, headers=headers, json=payload, timeout=70)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('status') == 'ok':
                        solution = result.get('solution', {})
                        html_content = solution.get('response', '')
                        if html_content and len(html_content) > 1000:  # Verifica se obteve conteúdo válido
                            print("✅ FlareSolverr bypass bem-sucedido!")
                            return html_content
                        else:
                            print("⚠️ FlareSolverr retornou conteúdo vazio")
                    else:
                        print(f"⚠️ FlareSolverr falhou: {result.get('message', 'Erro desconhecido')}")
                else:
                    print(f"⚠️ FlareSolverr erro HTTP: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ FlareSolverr falhou: {e}")
            
            return None
        
        # Função para usar requests-html (solução estável)
        def use_requests_html(target_url):
            """Usa requests-html para simular um navegador real e contornar proteções"""
            try:
                print(f"🌐 Iniciando requests-html para {target_url}...")
                
                # Cria uma sessão HTML
                session = HTMLSession()
                
                # Headers realistas
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                }
                
                # Faz a requisição
                response = session.get(target_url, headers=headers, timeout=30)
                
                # Renderiza JavaScript se necessário
                if any(indicator in response.html.html.lower() for indicator in ['cloudflare', 'cf-ray', 'checking your browser']):
                    print("🔄 Detectada proteção Cloudflare, renderizando JavaScript...")
                    response.html.render(timeout=20, wait=3)
                    
                # Tenta obter HTML de diferentes formas para evitar conteúdo comprimido
                html = None
                
                # Primeiro tenta response.text (decodificado automaticamente)
                if hasattr(response, 'text') and response.text:
                    html = response.text
                    print(f"🔍 DEBUG: Usando response.text - {len(html)} caracteres")
                # Se não funcionar, tenta response.html.html
                elif hasattr(response, 'html') and response.html.html:
                    html = response.html.html
                    print(f"🔍 DEBUG: Usando response.html.html - {len(html)} caracteres")
                
                # Verifica se o HTML é válido (não comprimido)
                if html and len(html) > 1000:
                    # Verifica se não é conteúdo binário/comprimido
                    if html.startswith('<') or 'html' in html.lower()[:100]:
                        print(f"✅ Requests-html obteve {len(html)} caracteres de HTML válido")
                        return html
                    else:
                        print(f"⚠️ HTML parece estar comprimido ou corrompido: {html[:50]}")
                        return None
                else:
                    print("⚠️ Requests-html retornou conteúdo insuficiente")
                    return None
                    
            except Exception as e:
                print(f"❌ Erro no requests-html: {str(e)}")
                return None
            finally:
                try:
                    session.close()
                except:
                    pass

        # Função para usar undetected-chromedriver (solução stealth 2025)
        def use_undetected_chrome(target_url):
            driver = None
            try:
                print("🥷 Tentativa com undetected-chromedriver (bypass stealth)")
                
                # Configurações do Chrome para máxima estabilidade e stealth
                options = uc.ChromeOptions()
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-features=VizDisplayCompositor')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-images')
                options.add_argument('--disable-web-security')
                options.add_argument('--disable-background-timer-throttling')
                options.add_argument('--disable-renderer-backgrounding')
                options.add_argument('--disable-backgrounding-occluded-windows')
                options.add_argument('--disable-client-side-phishing-detection')
                options.add_argument('--disable-sync')
                options.add_argument('--disable-field-trial-config')
                options.add_argument('--disable-back-forward-cache')
                options.add_argument('--disable-ipc-flooding-protection')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--no-first-run')
                options.add_argument('--no-default-browser-check')
                options.add_argument('--disable-default-apps')
                options.add_argument('--disable-popup-blocking')
                options.add_argument('--disable-translate')
                options.add_argument('--metrics-recording-only')
                options.add_argument('--no-report-upload')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                # Cria o driver com configurações mais robustas
                driver = uc.Chrome(options=options, version_main=None, headless=True)
                driver.set_page_load_timeout(45)
                driver.implicitly_wait(10)
                
                print(f"Navegando para {target_url}...")
                driver.get(target_url)
                
                # Aguarda o carregamento e possível resolução do Cloudflare
                print("Aguardando resolução do Cloudflare...")
                time.sleep(random.uniform(8, 12))
                
                # Verifica se a página carregou corretamente
                try:
                    WebDriverWait(driver, 25).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )
                except TimeoutException:
                    print("Timeout aguardando carregamento, continuando...")
                
                # Obtém o HTML da página
                html_content = driver.page_source
                
                if html_content and len(html_content) > 1000:
                    # Verifica se ainda há proteção Cloudflare
                    cloudflare_indicators = ['cloudflare', 'cf-browser-verification', 'checking your browser']
                    if not any(indicator in html_content.lower() for indicator in cloudflare_indicators):
                        print("✅ Undetected-chromedriver bypass bem-sucedido!")
                        return html_content
                    else:
                        print("⚠️ Undetected-chromedriver ainda detectou proteção Cloudflare")
                        # Aguarda mais um pouco e tenta novamente
                        time.sleep(5)
                        html_content = driver.page_source
                        if not any(indicator in html_content.lower() for indicator in cloudflare_indicators):
                            print("✅ Undetected-chromedriver bypass bem-sucedido na segunda tentativa!")
                            return html_content
                else:
                    print("⚠️ Undetected-chromedriver retornou conteúdo vazio")
                    
            except Exception as e:
                print(f"❌ Undetected-chromedriver falhou: {e}")
            finally:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
            
            return None
        
        # Função avançada para contornar Cloudflare baseada em pesquisa do Stack Overflow
        def handle_cloudflare_protection(html_content, current_url):
            cloudflare_indicators = [
                'cloudflare', 'cf-browser-verification', 'checking your browser',
                'ddos protection', 'security check', 'ray id', 'cf-ray',
                'please wait', 'browser verification', 'under attack mode',
                'just a moment'  # Indicador mais comum
            ]
            
            # Verifica título da página para detecção mais precisa
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            title_indicates_cloudflare = False
            if title_match:
                title = title_match.group(1).strip().lower()
                title_indicates_cloudflare = 'just a moment' in title or 'cloudflare' in title
            
            # Detecção combinada: indicadores no conteúdo OU título suspeito
            content_has_indicators = any(indicator in html_content.lower() for indicator in cloudflare_indicators)
            
            if content_has_indicators or title_indicates_cloudflare:
                # Debug: mostra o que foi detectado
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
                detected_title = title_match.group(1).strip() if title_match else "Sem título"
                print(f"🛡️ Cloudflare detectado em {current_url}")
                print(f"   Título detectado: '{detected_title}'")
                print(f"   Aplicando técnicas avançadas de bypass...")
                
                # Método 1: FlareSolverr (solução premium 2025)
                if FLARESOLVERR_AVAILABLE:
                    flare_result = use_flaresolverr(current_url)
                    if flare_result:
                        # Verifica se ainda há proteção Cloudflare
                        if not any(indicator in flare_result.lower() for indicator in cloudflare_indicators):
                            return flare_result
                        else:
                            print("⚠️ FlareSolverr retornou conteúdo, mas ainda com proteção")
                
                # Método 2: Undetected-chromedriver (bypass stealth 2025)
                if UNDETECTED_CHROME_AVAILABLE:
                    chrome_result = use_undetected_chrome(current_url)
                    if chrome_result:
                        # Verifica se ainda há proteção Cloudflare
                        if not any(indicator in chrome_result.lower() for indicator in cloudflare_indicators):
                            return chrome_result
                        else:
                            print("⚠️ Undetected-chromedriver retornou conteúdo, mas ainda com proteção")
                
                # Método 3: Cloudscraper (mais eficaz segundo Stack Overflow)
                if CLOUDSCRAPER_AVAILABLE:
                    try:
                        print("📡 Tentativa 1: Usando cloudscraper (recomendado pelo Stack Overflow)")
                        scraper = cloudscraper.create_scraper(
                            browser={
                                'browser': 'chrome',
                                'platform': 'windows',
                                'mobile': False
                            },
                            delay=10,  # Aguarda o desafio do Cloudflare
                            debug=False
                        )
                        
                        response = scraper.get(current_url, timeout=45)
                        if response.status_code == 200:
                            content_check = response.text.lower()
                            # Verificação mais rigorosa de conteúdo real
                            content_size_ok = len(response.text) > 5000
                            no_cloudflare_indicators = not any(indicator in content_check for indicator in cloudflare_indicators)
                            has_real_content = any(word in content_check for word in ['html', 'body', 'div', 'script'])
                            
                            # Verifica título para detecção mais precisa
                            title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                            title_is_clean = True
                            if title_match:
                                title = title_match.group(1).strip().lower()
                                title_is_clean = 'just a moment' not in title and 'cloudflare' not in title
                            
                            if no_cloudflare_indicators and content_size_ok and has_real_content and title_is_clean:
                                print("✅ Cloudscraper bypass bem-sucedido!")
                                return response.text
                            else:
                                print("⚠️ Cloudscraper retornou conteúdo, mas ainda com proteção")
                        else:
                            print(f"⚠️ Cloudscraper retornou status {response.status_code}")
                    except Exception as e:
                        print(f"❌ Cloudscraper falhou: {e}")
                
                # Método 4: Técnicas avançadas baseadas em undetected-chromedriver research
                print("📡 Tentativa 4: Simulação avançada de navegador")
                strategies = [
                    # Estratégia baseada em Chrome com headers completos
                    {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Cache-Control': 'max-age=0',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'DNT': '1',
                        'Connection': 'keep-alive'
                    },
                    # Estratégia Firefox (alternativa eficaz)
                    {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'
                    }
                ]
                
                for i, strategy in enumerate(strategies):
                    try:
                        print(f"Tentativa {i+1}/3 com estratégia {['Chrome', 'Firefox', 'Safari'][i]}")
                        
                        # Delay progressivo
                        delay = random.uniform(5 + i*2, 10 + i*3)
                        print(f"Aguardando {delay:.1f} segundos...")
                        time.sleep(delay)
                        
                        # Configura sessão específica para Cloudflare
                        session = requests.Session()
                        
                        # Headers específicos para contornar Cloudflare
                        enhanced_headers = headers.copy()
                        enhanced_headers.update(strategy)
                        enhanced_headers.update({
                            'Referer': 'https://www.google.com.br/',
                            'Origin': 'https://www.google.com.br'
                        })
                        
                        # Primeira requisição para obter cookies
                        response = session.get(current_url, headers=enhanced_headers, timeout=45, allow_redirects=True)
                        
                        # Se ainda há proteção Cloudflare, aguarda mais
                        if any(indicator in response.text.lower() for indicator in cloudflare_indicators):
                            print("Ainda protegido, aguardando mais tempo...")
                            time.sleep(random.uniform(8, 15))
                            
                            # Segunda tentativa com cookies
                            response = session.get(current_url, headers=enhanced_headers, timeout=45, allow_redirects=True)
                        
                        # Verificação mais rigorosa do sucesso
                        if response.status_code == 200:
                            response_lower = response.text.lower()
                            no_indicators = not any(indicator in response_lower for indicator in cloudflare_indicators)
                            
                            # Verifica título
                            title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                            title_ok = True
                            if title_match:
                                title = title_match.group(1).strip().lower()
                                title_ok = 'just a moment' not in title and 'cloudflare' not in title
                            
                            if no_indicators and title_ok:
                                print(f"Sucesso com estratégia {['Chrome', 'Firefox', 'Safari'][i]}!")
                                return response.text
                            
                    except Exception as e:
                        print(f"Estratégia {i+1} falhou: {str(e)}")
                        continue
                
                print("Todas as estratégias falharam, verificando se ainda há proteção...")
                
                # Verifica se ainda há proteção Cloudflare após todos os métodos
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
                title_indicates_cloudflare = False
                if title_match:
                    title = title_match.group(1).strip().lower()
                    title_indicates_cloudflare = 'just a moment' in title or 'cloudflare' in title
                    print(f"Título detectado após bypass: '{title}'")
                
                # Detecção combinada: indicadores no conteúdo OU título suspeito
                content_has_indicators = any(indicator in html_content.lower() for indicator in cloudflare_indicators)
                
                if content_has_indicators or title_indicates_cloudflare:
                    print("⚠️ Todos os métodos de bypass falharam - site ainda protegido")
                    return None  # Retorna None para indicar falha
                else:
                    print("✅ Verificação final: proteção Cloudflare removida com sucesso")
                    return html_content
            
            # Verifica se ainda há proteção Cloudflare no HTML original (caso não tenha entrado no if acima)
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            title_indicates_cloudflare = False
            if title_match:
                title = title_match.group(1).strip().lower()
                title_indicates_cloudflare = 'just a moment' in title or 'cloudflare' in title
            
            content_has_indicators = any(indicator in html_content.lower() for indicator in cloudflare_indicators)
            
            if content_has_indicators or title_indicates_cloudflare:
                print("⚠️ HTML original ainda contém proteção Cloudflare")
                return None
            
            return html_content
        
        # Tenta acessar com múltiplas URLs (HTTP e HTTPS)
        html = None
        successful_url = None
        
        for test_url in urls_to_try:
            try:
                print(f"Tentando acessar: {test_url}")
                html = try_access_url(test_url, headers)
                successful_url = test_url
                print(f"✅ Acesso bem-sucedido: {test_url}")
                break
            except Exception as e:
                print(f"❌ Falha ao acessar {test_url}: {str(e)}")
                continue
        
        if html is None:
            # Se nenhuma URL funcionou, retorna erro
            ids.append("ERRO_ACESSO")
            ids.append("❌ Não foi possível acessar o site")
            ids.append(f"URLs testadas: {', '.join(urls_to_try)}")
            links.append("❌ Links não extraídos devido a erro de acesso")
            technologies.append("❌ Tecnologias não detectadas devido a erro de acesso")
            return ids, links, technologies, contact_info
        
        # Define soup para o HTML obtido com sucesso
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extrai o domínio base da URL bem-sucedida
            from urllib.parse import urlparse
            parsed_url = urlparse(successful_url)
            base_domain = parsed_url.netloc
            
            # Verifica se há proteção Cloudflare (detecção melhorada)
            cloudflare_result = handle_cloudflare_protection(html, successful_url)
            if cloudflare_result is None:
                # Cloudflare bypass falhou - indica necessidade de análise manual
                ids.append("MANUAL_ANALYSIS_REQUIRED")
                ids.append("⚠️ SITE PROTEGIDO POR CLOUDFLARE")
                ids.append("O site possui proteção avançada que impede a análise automática.")
                ids.append(f"Site: {url}")
                ids.append("Status: Protegido por Cloudflare avançado")
                ids.append("")
                ids.append("💡 TENTATIVAS REALIZADAS:")
                ids.append("1. Acesso direto com headers personalizados")
                ids.append("2. Bypass automático com múltiplas técnicas")
                ids.append("3. Verificação de proteção Cloudflare")
                ids.append("4. Tentativas com diferentes user-agents")
                ids.append("5. Análise de indicadores de proteção")
                
                # Adiciona informação específica para links e tecnologias
                links.append("❌ Links não extraídos devido à proteção Cloudflare")
                technologies.append("❌ Tecnologias não detectadas devido à proteção Cloudflare")
                
                return ids, links, technologies, contact_info
            else:
                html = cloudflare_result
                soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            # Função específica para contornar erro 403 Forbidden
            def handle_403_forbidden(original_url):
                print(f"Erro 403 detectado para {original_url}. Implementando técnicas avançadas de contorno...")
                
                # Método 1: Requests-html (mais estável para 403)
                if REQUESTS_HTML_AVAILABLE:
                    print("🌐 Tentando requests-html para contornar 403...")
                    html_result = use_requests_html(original_url)
                    if html_result:
                        print("✅ Requests-html contornou o 403 com sucesso!")
                        return html_result
                    else:
                        print("⚠️ Requests-html falhou no 403")
                
                # Método 2: Undetected-chromedriver (backup)
                if UNDETECTED_CHROME_AVAILABLE:
                    print("🥷 Tentando undetected-chromedriver para contornar 403...")
                    chrome_result = use_undetected_chrome(original_url)
                    if chrome_result:
                        print("✅ Undetected-chromedriver contornou o 403 com sucesso!")
                        return chrome_result
                    else:
                        print("⚠️ Undetected-chromedriver falhou no 403")
                
                # Método 3: Técnicas tradicionais de contorno
                print("📡 Tentando métodos tradicionais de contorno...")
                
                # Lista de User-Agents mais diversos
                advanced_user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/121.0.0.0'
                ]
                
                # Lista de referrers
                referrers = [
                    'https://www.google.com.br/',
                    'https://www.google.com/',
                    'https://www.bing.com/',
                    'https://duckduckgo.com/',
                    'https://search.yahoo.com/',
                    ''
                ]
                
                # Tenta diferentes combinações
                for attempt in range(6):
                    try:
                        print(f"Tentativa {attempt + 1}/6 para contornar 403...")
                        
                        # Delay progressivo
                        delay = random.uniform(3 + attempt, 8 + attempt * 2)
                        print(f"Aguardando {delay:.1f} segundos...")
                        time.sleep(delay)
                        
                        # Seleciona User-Agent e Referrer aleatórios
                        selected_ua = random.choice(advanced_user_agents)
                        selected_ref = random.choice(referrers)
                        
                        # Configura headers específicos
                        anti_block_headers = {
                            'User-Agent': selected_ua,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'DNT': '1',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'cross-site' if selected_ref else 'none',
                            'Sec-Fetch-User': '?1',
                            'Cache-Control': 'max-age=0'
                        }
                        
                        if selected_ref:
                            anti_block_headers['Referer'] = selected_ref
                            anti_block_headers['Origin'] = selected_ref.rstrip('/')
                        
                        # Tenta com HTTP primeiro, depois HTTPS
                        urls_to_try = [original_url]
                        if original_url.startswith('http://'):
                            urls_to_try.append(original_url.replace('http://', 'https://'))
                        elif original_url.startswith('https://'):
                            urls_to_try.append(original_url.replace('https://', 'http://'))
                        
                        for test_url in urls_to_try:
                            try:
                                print(f"Testando URL: {test_url}")
                                
                                # Configura sessão com retry
                                session = requests.Session()
                                retry_strategy = Retry(
                                    total=2,
                                    status_forcelist=[429, 500, 502, 503, 504],
                                    allowed_methods=["HEAD", "GET", "OPTIONS"]
                                )
                                adapter = HTTPAdapter(max_retries=retry_strategy)
                                session.mount("http://", adapter)
                                session.mount("https://", adapter)
                                
                                response = session.get(test_url, headers=anti_block_headers, timeout=45, allow_redirects=True)
                                
                                if response.status_code == 200:
                                    print(f"Sucesso! Contornado 403 com tentativa {attempt + 1}")
                                    return response.text
                                    
                            except Exception as inner_e:
                                print(f"Falha na URL {test_url}: {str(inner_e)}")
                                continue
                                
                    except Exception as outer_e:
                        print(f"Tentativa {attempt + 1} falhou completamente: {str(outer_e)}")
                        continue
                
                print("Todas as tentativas de contorno do 403 falharam")
                # Adiciona informação sobre Cloudflare para o usuário - indica análise manual
                ids.append("MANUAL_ANALYSIS_REQUIRED")
                ids.append("⚠️ SITE PROTEGIDO POR CLOUDFLARE")
                ids.append("O site possui proteção avançada que impede a análise automática.")
                ids.append("💡 TENTATIVAS REALIZADAS:")
                ids.append("• Múltiplas tentativas de bypass 403")
                ids.append("• Diferentes métodos de acesso")
                ids.append("• Verificação de proteção avançada")
                return None
            
            # Se for erro 403 (Forbidden), usa a função específica
            if hasattr(e, 'response') and hasattr(e.response, 'status_code') and e.response.status_code == 403:
                print("Erro 403 detectado para {}. Implementando técnicas avançadas de contorno...".format(url))
                html_result = handle_403_forbidden(url)
                if html_result:
                    print("HTML obtido após contorno do 403, verificando proteção Cloudflare...")
                    cloudflare_result = handle_cloudflare_protection(html_result, url)
                    if cloudflare_result is None:
                        # Cloudflare bypass falhou após 403 - indica necessidade de análise manual
                        ids.append("MANUAL_ANALYSIS_REQUIRED")
                        ids.append("⚠️ ERRO 403 + CLOUDFLARE DETECTADO")
                        ids.append("Site bloqueado por erro 403 E proteção Cloudflare.")
                        ids.append(f"Site: {url}")
                        ids.append("Status: Dupla proteção ativa")
                        ids.append("")
                        ids.append("💡 TENTATIVAS REALIZADAS:")
                        ids.append("1. Bypass automático com requests-html")
                        ids.append("2. Bypass com undetected-chromedriver")
                        ids.append("3. Múltiplas tentativas tradicionais")
                        ids.append("4. Verificação de proteção Cloudflare")
                        
                        links.append("❌ Links não extraídos - Erro 403 + Cloudflare")
                        technologies.append("❌ Tecnologias não detectadas - Erro 403 + Cloudflare")
                        
                        return ids, links, technologies, contact_info
                    else:
                        print("🔍 DEBUG: Entrando na seção de bypass bem-sucedido após 403")
                        print(f"🔍 DEBUG: Tamanho do HTML obtido: {len(cloudflare_result)} caracteres")
                        print(f"🔍 DEBUG: Primeiros 200 caracteres do HTML: {cloudflare_result[:200]}")
                        
                        # Verificação adicional para confirmar se o bypass realmente funcionou
                        title_match = re.search(r'<title[^>]*>([^<]+)</title>', cloudflare_result, re.IGNORECASE)
                        if title_match:
                            title = title_match.group(1).strip()
                            print(f"Título da página após bypass: '{title}'")
                            if 'just a moment' in title.lower():
                                print("⚠️ ATENÇÃO: Título ainda indica proteção Cloudflare ativa!")
                                # Mesmo assim, continua o processamento para análise
                        else:
                            print("🔍 DEBUG: Nenhum título encontrado no HTML")
                        
                        print("✅ Cloudflare bypass bem-sucedido após 403!")
                        html = cloudflare_result
                        soup = BeautifulSoup(html, 'html.parser')
                else:
                    ids.append(f"Erro ao acessar o site (403 Forbidden): {str(e)}")
                    return ids, links, technologies, contact_info
            # Se não for 403, tenta com HTTPS
            elif url.startswith('http://') and not url.startswith('https://'):
                https_url = 'https://' + url[7:]
                try:
                    html = try_access_url(https_url, headers)
                    soup = BeautifulSoup(html, 'html.parser')
                except Exception as e2:
                    ids.append(f"Erro ao acessar o site (HTTPS): {str(e2)}")
                    return ids, links, technologies, contact_info
            else:
                ids.append(f"Erro ao acessar o site: {str(e)}")
                return ids, links, technologies, contact_info
        
        # base_domain já foi definido dentro do try block usando successful_url
        
        # Extrai IDs únicos de diferentes plataformas
        unique_ids = []
        
        # Google Analytics (UA e GA4)
        ua_pattern = re.compile(r'UA-[\w-]+', re.IGNORECASE)
        ua_matches = ua_pattern.findall(html)
        unique_ids.extend([{'type': 'Google Analytics UA', 'id': match} for match in ua_matches])
        
        ga4_pattern = re.compile(r'G-[A-Z0-9]{10}', re.IGNORECASE)
        ga4_matches = ga4_pattern.findall(html)
        unique_ids.extend([{'type': 'Google Analytics GA4', 'id': match} for match in ga4_matches])
        
        # Google Tag Manager
        gtm_pattern = re.compile(r'GTM-[A-Z0-9]+', re.IGNORECASE)
        gtm_matches = gtm_pattern.findall(html)
        unique_ids.extend([{'type': 'Google Tag Manager', 'id': match} for match in gtm_matches])
        
        # Facebook Pixel
        fb_pixel_pattern = re.compile(r'fbq.*init.*[\d]{15,16}', re.IGNORECASE)
        fb_pixel_matches = fb_pixel_pattern.findall(html)
        unique_ids.extend([{'type': 'Facebook Pixel', 'id': match} for match in fb_pixel_matches])
        
        # Google AdSense
        adsense_pattern = re.compile(r'ca-pub-[\d]+', re.IGNORECASE)
        adsense_matches = adsense_pattern.findall(html)
        unique_ids.extend([{'type': 'Google AdSense', 'id': match} for match in adsense_matches])
        
        # Hotjar
        hotjar_pattern = re.compile(r'hjid[:\s]*[\d]{6,8}', re.IGNORECASE)
        hotjar_matches = hotjar_pattern.findall(html)
        unique_ids.extend([{'type': 'Hotjar', 'id': match} for match in hotjar_matches])
        
        # Remove duplicatas mantendo a estrutura
        seen = set()
        for item in unique_ids:
            identifier = f"{item['type']}:{item['id']}"
            if identifier not in seen:
                seen.add(identifier)
                ids.append(f"{item['type']}: {item['id']}")
        
        # Google Site Verification
        site_verification = soup.find('meta', attrs={'name': 'google-site-verification'})
        if site_verification:
            ids.append(f"Google Site Verification: {site_verification.get('content')}")
        
        # Microsoft Bing Verification
        msvalidate = soup.find('meta', attrs={'name': 'msvalidate.01'})
        if msvalidate:
            ids.append(f"Microsoft Bing Verification: {msvalidate.get('content')}")
        
        # Juicy Ad Code
        juicy_pattern = re.compile(r'juicy_code = \'([0-9]+)\'', re.IGNORECASE)
        juicy_matches = juicy_pattern.findall(html)
        if juicy_matches:
            ids.append(f"Juicy Ad Code: {', '.join(set(juicy_matches))}")
        
        # Detecção avançada de tecnologias usando Wappalyzer
        try:
            from Wappalyzer import Wappalyzer, WebPage
            
            # Cria uma instância do Wappalyzer
            wappalyzer = Wappalyzer.latest()
            
            # Cria um WebPage a partir do HTML obtido
            webpage = WebPage(url, html, {})
            
            # Analisa as tecnologias
            detected_technologies = wappalyzer.analyze_with_versions_and_categories(webpage)
            
            # Processa os resultados
            for tech_name, tech_info in detected_technologies.items():
                categories = tech_info.get('categories', [])
                versions = tech_info.get('versions', [])
                
                # Formata a informação da tecnologia
                tech_display = tech_name
                if versions:
                    tech_display += f" {versions[0]}"  # Mostra apenas a primeira versão
                if categories:
                    tech_display += f" ({', '.join(categories[:2])})"  # Mostra até 2 categorias
                
                technologies.append(tech_display)
            
            print(f"✅ Wappalyzer detectou {len(detected_technologies)} tecnologias")
            
        except ImportError:
            print("⚠️ Wappalyzer não disponível, usando detecção manual")
            # Fallback para detecção manual (código original)
            # WordPress
            if 'wp-content' in html or 'wp-includes' in html:
                technologies.append("WordPress")
            
            # Joomla
            if 'joomla' in html.lower():
                technologies.append("Joomla")
            
            # Drupal
            if 'drupal' in html.lower():
                technologies.append("Drupal")
            
            # Bootstrap
            if 'bootstrap' in html.lower():
                technologies.append("Bootstrap")
            
            # jQuery
            if 'jquery' in html.lower():
                technologies.append("jQuery")
            
            # React
            if 'react' in html.lower() or '_reactRootContainer' in html:
                technologies.append("React")
            
            # Angular
            if 'ng-' in html or 'angular' in html.lower():
                technologies.append("Angular")
            
            # Vue.js
            if 'vue' in html.lower() or 'v-' in html:
                technologies.append("Vue.js")
            
            # PHP
            if 'php' in html.lower():
                technologies.append("PHP")
                
            # Laravel
            if 'laravel' in html.lower():
                technologies.append("Laravel")
                
            # Django
            if 'django' in html.lower():
                technologies.append("Django")
                
            # Node.js
            if 'node' in html.lower() or 'nodejs' in html.lower():
                technologies.append("Node.js")
        
        except Exception as e:
            print(f"⚠️ Erro na detecção de tecnologias com Wappalyzer: {e}")
            print("Usando detecção manual como fallback")
            # Fallback para detecção manual em caso de erro
            if 'wp-content' in html or 'wp-includes' in html:
                technologies.append("WordPress")
            if 'vue' in html.lower() or 'v-' in html:
                technologies.append("Vue.js")
            if 'jquery' in html.lower():
                technologies.append("jQuery")
            if 'bootstrap' in html.lower():
                technologies.append("Bootstrap")
        
        # Extração de informações de contato
        # E-mails
        email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}', re.IGNORECASE)
        email_matches = email_pattern.findall(html)
        if email_matches:
            unique_emails = list(set(email_matches))
            contact_info.append(f"E-mails: {', '.join(unique_emails[:5])}")
            if len(unique_emails) > 5:
                contact_info.append(f"... e mais {len(unique_emails) - 5} e-mails")
        
        # Telefones (formato brasileiro)
        phone_pattern = re.compile(r'\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}', re.IGNORECASE)
        phone_matches = phone_pattern.findall(html)
        if phone_matches:
            unique_phones = list(set(phone_matches))
            contact_info.append(f"Telefones: {', '.join(unique_phones[:5])}")
            if len(unique_phones) > 5:
                contact_info.append(f"... e mais {len(unique_phones) - 5} telefones")
        
        if contact_info:
            ids.append("Informações de contato:")
            ids.extend(contact_info)
        
        # Extrai todos os links de forma mais robusta
        social_links = []
        external_links = []
        internal_links = []
        
        # Encontra todos os elementos <a> com href
        all_links = soup.find_all('a', href=True)
        
        for i, link in enumerate(all_links):
            href = link['href'].strip()
            if not href or href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                continue
                
            # Normaliza o link
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                href = f"https://{base_domain}{href}"
            elif not href.startswith('http'):
                href = f"https://{base_domain}/{href}"
            
            # Categoriza os links
            if any(social in href.lower() for social in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'tiktok.com', 'whatsapp.com', 'telegram.org']):
                social_links.append(href)
            elif base_domain in href:
                internal_links.append(href)
            else:
                external_links.append(href)
        
        # Extrai links de JavaScript e atributos data
        js_link_patterns = [
            # r'window\.open\(["\'].*["\'\)]', # REMOVIDO - REGEX PROBLEMÁTICO
            # r'location\.href\s*=\s*["\'].*["\'\]', # REMOVIDO - REGEX PROBLEMÁTICO
            # r'data-href=["\'].*["\'\]', # REMOVIDO - REGEX PROBLEMÁTICO
            # r'data-url=["\'].*["\'\]' # REMOVIDO - REGEX PROBLEMÁTICO
        ]
        
        for pattern in js_link_patterns:
            js_matches = re.findall(pattern, html, re.IGNORECASE)
            for match in js_matches:
                if match and not match.startswith('#') and not match.startswith('javascript:'):
                    # Normaliza o link
                    if match.startswith('//'):
                        match = 'https:' + match
                    elif match.startswith('/'):
                        match = f"https://{base_domain}{match}"
                    elif not match.startswith('http'):
                        match = f"https://{base_domain}/{match}"
                    
                    # Categoriza
                    if any(social in match.lower() for social in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'tiktok.com', 'whatsapp.com', 'telegram.org']):
                        social_links.append(match)
                    elif base_domain not in match:
                        external_links.append(match)
                    else:
                        internal_links.append(match)
        
        # Remove duplicatas
        social_links = list(set(social_links))
        external_links = list(set(external_links))
        internal_links = list(set(internal_links))
        
        # Formata os links para exibição
        for href in social_links:
            links.append(f"[SOCIAL] {href}")
        for href in external_links:
            links.append(f"[EXTERNO] {href}")
        for href in internal_links:
            links.append(f"[INTERNO] {href}")
    
    except Exception as e:
        print(f"❌ ERRO CRÍTICO na extração de dados: {str(e)}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        ids.append(f"Erro ao processar o site: {str(e)}")
        import traceback
        print("❌ TRACEBACK COMPLETO:")
        traceback.print_exc()
        # Não retorna aqui para permitir que continue e mostre os links encontrados até agora
        pass
    
    # Verifica se encontrou algum link
    if not links:
        links.append("Nenhum link encontrado ou erro na extração de links")
    
    # Inicializa contact_info se não foi definido
    if 'contact_info' not in locals():
        contact_info = []
    
    return ids, links, technologies, contact_info