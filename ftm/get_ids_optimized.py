import random
import time
import urllib.request
import gzip
import re
import json
import hashlib
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, urljoin
import logging
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importações avançadas para bypass
try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
    logger.info("✓ Cloudscraper disponível - bypass avançado do Cloudflare ativado")
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False
    logger.warning("⚠ Cloudscraper não instalado. Para melhor bypass do Cloudflare, instale com: pip install cloudscraper")

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    # Auto-instalador do ChromeDriver para resolver incompatibilidades
    try:
        import chromedriver_autoinstaller
        chromedriver_autoinstaller.install()
        logger.info("✓ ChromeDriver atualizado automaticamente")
    except ImportError:
        logger.warning("⚠ chromedriver-autoinstaller não instalado - versões podem ser incompatíveis")
    UNDETECTED_CHROME_AVAILABLE = True
    logger.info("✓ Undetected-chromedriver disponível - bypass stealth do Cloudflare ativado")
except ImportError:
    UNDETECTED_CHROME_AVAILABLE = False
    logger.warning("⚠ Undetected-chromedriver não instalado")

try:
    from requests_html import HTMLSession
    REQUESTS_HTML_AVAILABLE = True
    logger.info("✓ Requests-html disponível - simulação de navegador estável ativada")
except ImportError:
    REQUESTS_HTML_AVAILABLE = False
    logger.warning("⚠ Requests-html não instalado")

try:
    import httpx
    HTTPX_AVAILABLE = True
    logger.info("✓ HTTPX disponível - cliente HTTP moderno ativado")
except ImportError:
    HTTPX_AVAILABLE = False
    logger.warning("⚠ HTTPX não instalado")

try:
    from curl_cffi import requests as cf_requests
    CURL_CFFI_AVAILABLE = True
    logger.info("✓ curl_cffi disponível - máxima compatibilidade TLS ativada")
except ImportError:
    CURL_CFFI_AVAILABLE = False
    logger.warning("⚠ curl_cffi não instalado")

try:
    import tls_client
    TLS_CLIENT_AVAILABLE = True
    logger.info("✓ tls_client disponível - JA3 fingerprint spoofing ativado")
except ImportError:
    TLS_CLIENT_AVAILABLE = False
    logger.warning("⚠ tls_client não instalado")

try:
    from fake_useragent import UserAgent
    FAKE_USERAGENT_AVAILABLE = True
    logger.info("✓ fake_useragent disponível - rotação inteligente de User-Agents ativada")
except ImportError:
    FAKE_USERAGENT_AVAILABLE = False
    logger.warning("⚠ fake_useragent não instalado")

try:
    import browser_cookie3
    BROWSER_COOKIE3_AVAILABLE = True
    logger.info("✓ browser_cookie3 disponível - cookies reais do navegador ativados")
except ImportError:
    BROWSER_COOKIE3_AVAILABLE = False
    logger.warning("⚠ browser_cookie3 não instalado")

# Enums para tipos de proteção
class ProtectionType(Enum):
    NONE = "none"
    CLOUDFLARE = "cloudflare"
    INCAPSULA = "incapsula"
    AKAMAI = "akamai"
    DDOS_GUARD = "ddos_guard"
    SUCURI = "sucuri"
    UNKNOWN = "unknown"

class BypassMethod(Enum):
    REQUESTS = "requests"
    CLOUDSCRAPER = "cloudscraper"
    TLS_CLIENT = "tls_client"
    CURL_CFFI = "curl_cffi"
    REQUESTS_HTML = "requests_html"
    UNDETECTED_CHROME = "undetected_chrome"
    HTTPX = "httpx"

@dataclass
class BypassResult:
    success: bool
    html: Optional[str]
    method: BypassMethod
    protection_detected: ProtectionType
    response_time: float
    status_code: Optional[int]
    error: Optional[str]
    metrics: Dict[str, Any]

class AdvancedUserAgentRotator:
    """Sistema avançado de rotação de User-Agents baseado em estatísticas reais"""
    
    def __init__(self):
        # User-Agents baseados em estatísticas reais de uso (2024)
        self.chrome_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        self.firefox_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        ]
        
        self.safari_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        ]
        
        self.edge_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        ]
        
        # Pesos baseados em estatísticas reais de mercado
        self.browser_weights = {
            'chrome': 0.65,  # 65% do mercado
            'firefox': 0.15, # 15% do mercado
            'safari': 0.12,  # 12% do mercado
            'edge': 0.08     # 8% do mercado
        }
        
        self.fake_ua = None
        if FAKE_USERAGENT_AVAILABLE:
            try:
                self.fake_ua = UserAgent()
            except:
                pass
    
    def get_random_agent(self, browser_hint: Optional[str] = None) -> str:
        """Obtém um User-Agent aleatório baseado em estatísticas reais"""
        if self.fake_ua and random.random() < 0.3:  # 30% chance de usar fake_useragent
            try:
                return self.fake_ua.random
            except:
                pass
        
        if browser_hint:
            agents_map = {
                'chrome': self.chrome_agents,
                'firefox': self.firefox_agents,
                'safari': self.safari_agents,
                'edge': self.edge_agents
            }
            return random.choice(agents_map.get(browser_hint, self.chrome_agents))
        
        # Seleção ponderada baseada em estatísticas de mercado
        rand = random.random()
        if rand < self.browser_weights['chrome']:
            return random.choice(self.chrome_agents)
        elif rand < self.browser_weights['chrome'] + self.browser_weights['firefox']:
            return random.choice(self.firefox_agents)
        elif rand < self.browser_weights['chrome'] + self.browser_weights['firefox'] + self.browser_weights['safari']:
            return random.choice(self.safari_agents)
        else:
            return random.choice(self.edge_agents)
    
    def get_matching_headers(self, user_agent: str) -> Dict[str, str]:
        """Gera headers compatíveis com o User-Agent fornecido"""
        base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'User-Agent': user_agent
        }
        
        # Headers específicos por navegador
        if 'Chrome' in user_agent:
            base_headers.update({
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })
        elif 'Firefox' in user_agent:
            base_headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            })
        elif 'Safari' in user_agent:
            base_headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
        
        return base_headers

class ProtectionDetector:
    """Detector avançado de diferentes tipos de proteção anti-bot"""
    
    def __init__(self):
        self.cloudflare_indicators = [
            'cloudflare', 'cf-ray', 'checking your browser', 'just a moment',
            '__cf_bm', 'cf_clearance', 'challenge-platform', 'cf-browser-verification',
            'turnstile', 'cf-challenge', 'cf-under-attack'
        ]
        
        self.incapsula_indicators = [
            'incapsula', '_incap_ses', 'visid_incap', 'incap_ses',
            'generated by cloudflare', 'incapsula incident id'
        ]
        
        self.akamai_indicators = [
            'akamai', '_abck', 'ak_bmsc', 'bm_sz', 'reference #18'
        ]
        
        self.ddos_guard_indicators = [
            'ddos-guard', 'ddosguard', '__ddg1', '__ddg2'
        ]
        
        self.sucuri_indicators = [
            'sucuri', 'access denied - sucuri', 'sucuri cloudproxy'
        ]
    
    def detect_protection(self, html: str, headers: Dict[str, str], status_code: int) -> ProtectionType:
        """Detecta o tipo de proteção baseado no conteúdo HTML e headers"""
        html_lower = html.lower()
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        
        # Detecção Cloudflare
        if any(indicator in html_lower for indicator in self.cloudflare_indicators):
            return ProtectionType.CLOUDFLARE
        if 'cf-ray' in headers_lower or 'cloudflare' in headers_lower.get('server', ''):
            return ProtectionType.CLOUDFLARE
        
        # Detecção Incapsula
        if any(indicator in html_lower for indicator in self.incapsula_indicators):
            return ProtectionType.INCAPSULA
        
        # Detecção Akamai
        if any(indicator in html_lower for indicator in self.akamai_indicators):
            return ProtectionType.AKAMAI
        
        # Detecção DDoS-Guard
        if any(indicator in html_lower for indicator in self.ddos_guard_indicators):
            return ProtectionType.DDOS_GUARD
        
        # Detecção Sucuri
        if any(indicator in html_lower for indicator in self.sucuri_indicators):
            return ProtectionType.SUCURI
        
        # Detecção genérica de proteção
        generic_indicators = ['access denied', 'blocked', 'forbidden', 'security check']
        if any(indicator in html_lower for indicator in generic_indicators) and status_code in [403, 429, 503]:
            return ProtectionType.UNKNOWN
        
        return ProtectionType.NONE

class AdaptiveDelayManager:
    """Gerenciador de delays adaptativos baseado no comportamento do servidor"""
    
    def __init__(self):
        self.domain_delays = {}  # Armazena delays por domínio
        self.success_rates = {}  # Taxa de sucesso por domínio
        self.rate_limit_detected = {}  # Detecção de rate limiting
    
    def get_delay(self, domain: str) -> float:
        """Calcula delay adaptativo baseado no histórico do domínio"""
        base_delay = 1.0
        
        if domain in self.domain_delays:
            # Ajusta delay baseado na taxa de sucesso
            success_rate = self.success_rates.get(domain, 1.0)
            if success_rate < 0.5:  # Taxa de sucesso baixa
                base_delay *= 2.0
            elif success_rate > 0.8:  # Taxa de sucesso alta
                base_delay *= 0.5
        
        # Adiciona variação humana
        human_variation = random.uniform(0.5, 1.5)
        return base_delay * human_variation
    
    def record_attempt(self, domain: str, success: bool, response_time: float):
        """Registra tentativa para ajuste adaptativo"""
        if domain not in self.success_rates:
            self.success_rates[domain] = []
        
        self.success_rates[domain].append(1.0 if success else 0.0)
        
        # Mantém apenas os últimos 10 registros
        if len(self.success_rates[domain]) > 10:
            self.success_rates[domain] = self.success_rates[domain][-10:]
        
        # Calcula taxa de sucesso média
        avg_success = sum(self.success_rates[domain]) / len(self.success_rates[domain])
        self.success_rates[domain] = avg_success
    
    def detect_rate_limit(self, status_code: int, headers: Dict[str, str]) -> bool:
        """Detecta rate limiting baseado em status code e headers"""
        if status_code == 429:
            return True
        
        rate_limit_headers = ['x-ratelimit-remaining', 'retry-after', 'x-rate-limit-remaining']
        return any(header in headers for header in rate_limit_headers)

class CookieManager:
    """Gerenciador avançado de cookies com persistência"""
    
    def __init__(self):
        self.domain_cookies = {}
        self.browser_cookies = {}
        
        # Tenta carregar cookies reais do navegador
        if BROWSER_COOKIE3_AVAILABLE:
            self._load_browser_cookies()
    
    def _load_browser_cookies(self):
        """Carrega cookies reais dos navegadores instalados"""
        try:
            # Chrome cookies
            chrome_cookies = browser_cookie3.chrome()
            for cookie in chrome_cookies:
                domain = cookie.domain
                if domain not in self.browser_cookies:
                    self.browser_cookies[domain] = {}
                self.browser_cookies[domain][cookie.name] = cookie.value
        except:
            pass
        
        try:
            # Firefox cookies
            firefox_cookies = browser_cookie3.firefox()
            for cookie in firefox_cookies:
                domain = cookie.domain
                if domain not in self.browser_cookies:
                    self.browser_cookies[domain] = {}
                self.browser_cookies[domain][cookie.name] = cookie.value
        except:
            pass
    
    def get_cookies_for_domain(self, domain: str) -> Dict[str, str]:
        """Obtém cookies para um domínio específico"""
        cookies = {}
        
        # Cookies do navegador real
        if domain in self.browser_cookies:
            cookies.update(self.browser_cookies[domain])
        
        # Cookies salvos de sessões anteriores
        if domain in self.domain_cookies:
            cookies.update(self.domain_cookies[domain])
        
        return cookies
    
    def save_cookies(self, domain: str, cookies: Dict[str, str]):
        """Salva cookies para uso futuro"""
        if domain not in self.domain_cookies:
            self.domain_cookies[domain] = {}
        self.domain_cookies[domain].update(cookies)

class AdvancedCloudflareBypass:
    """Sistema avançado de bypass para Cloudflare e outras proteções"""
    
    def __init__(self):
        self.ua_rotator = AdvancedUserAgentRotator()
        self.protection_detector = ProtectionDetector()
        self.delay_manager = AdaptiveDelayManager()
        self.cookie_manager = CookieManager()
        self.session_cache = {}  # Cache de sessões por domínio
        self.bypass_stats = {method: {'attempts': 0, 'successes': 0} for method in BypassMethod}
    
    def _create_session(self, domain: str) -> requests.Session:
        """Cria sessão otimizada com configurações avançadas"""
        if domain in self.session_cache:
            return self.session_cache[domain]
        
        session = requests.Session()
        
        # Configuração de retry avançada
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 523, 524],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
            respect_retry_after_header=True
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Carrega cookies salvos
        cookies = self.cookie_manager.get_cookies_for_domain(domain)
        for name, value in cookies.items():
            session.cookies.set(name, value, domain=domain)
        
        self.session_cache[domain] = session
        return session
    
    def _method_requests(self, url: str, timeout: int = 30) -> BypassResult:
        """Método 1: Requests padrão com headers otimizados"""
        start_time = time.time()
        method = BypassMethod.REQUESTS
        self.bypass_stats[method]['attempts'] += 1
        
        try:
            domain = urlparse(url).netloc
            session = self._create_session(domain)
            
            user_agent = self.ua_rotator.get_random_agent('chrome')
            headers = self.ua_rotator.get_matching_headers(user_agent)
            
            # Delay adaptativo
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            response = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response_time = time.time() - start_time
            
            # Salva cookies
            if response.cookies:
                cookie_dict = {cookie.name: cookie.value for cookie in response.cookies}
                self.cookie_manager.save_cookies(domain, cookie_dict)
            
            protection = self.protection_detector.detect_protection(
                response.text, dict(response.headers), response.status_code
            )
            
            success = response.status_code == 200 and protection == ProtectionType.NONE
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=response.text if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=response.status_code,
                error=None,
                metrics={'content_length': len(response.text)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
    
    def _method_cloudscraper(self, url: str, timeout: int = 45) -> BypassResult:
        """Método 2: Cloudscraper com configurações avançadas"""
        if not CLOUDSCRAPER_AVAILABLE:
            return BypassResult(
                success=False, html=None, method=BypassMethod.CLOUDSCRAPER,
                protection_detected=ProtectionType.UNKNOWN, response_time=0,
                status_code=None, error="Cloudscraper não disponível", metrics={}
            )
        
        start_time = time.time()
        method = BypassMethod.CLOUDSCRAPER
        self.bypass_stats[method]['attempts'] += 1
        
        try:
            domain = urlparse(url).netloc
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            # Configuração avançada do cloudscraper
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                },
                delay=10,
                debug=False,
                captcha={
                    'provider': '2captcha',  # Pode ser configurado
                    'api_key': None  # Adicionar se necessário
                }
            )
            
            # Headers customizados
            user_agent = self.ua_rotator.get_random_agent('chrome')
            headers = self.ua_rotator.get_matching_headers(user_agent)
            
            response = scraper.get(url, headers=headers, timeout=timeout)
            response_time = time.time() - start_time
            
            protection = self.protection_detector.detect_protection(
                response.text, dict(response.headers), response.status_code
            )
            
            success = (
                response.status_code == 200 and 
                len(response.text) > 5000 and
                protection == ProtectionType.NONE
            )
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=response.text if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=response.status_code,
                error=None,
                metrics={'content_length': len(response.text)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
    
    def _method_tls_client(self, url: str, timeout: int = 30) -> BypassResult:
        """Método 3: TLS Client com JA3 fingerprint spoofing"""
        if not TLS_CLIENT_AVAILABLE:
            return BypassResult(
                success=False, html=None, method=BypassMethod.TLS_CLIENT,
                protection_detected=ProtectionType.UNKNOWN, response_time=0,
                status_code=None, error="TLS Client não disponível", metrics={}
            )
        
        start_time = time.time()
        method = BypassMethod.TLS_CLIENT
        self.bypass_stats[method]['attempts'] += 1
        
        try:
            domain = urlparse(url).netloc
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            # Cria sessão TLS com fingerprint do Chrome
            session = tls_client.Session(
                client_identifier="chrome_120",
                random_tls_extension_order=True
            )
            
            user_agent = self.ua_rotator.get_random_agent('chrome')
            headers = self.ua_rotator.get_matching_headers(user_agent)
            
            response = session.get(url, headers=headers, timeout=timeout)
            response_time = time.time() - start_time
            
            protection = self.protection_detector.detect_protection(
                response.text, dict(response.headers), response.status_code
            )
            
            success = response.status_code == 200 and protection == ProtectionType.NONE
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=response.text if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=response.status_code,
                error=None,
                metrics={'content_length': len(response.text)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
    
    def _method_curl_cffi(self, url: str, timeout: int = 30) -> BypassResult:
        """Método 4: curl_cffi para máxima compatibilidade"""
        if not CURL_CFFI_AVAILABLE:
            return BypassResult(
                success=False, html=None, method=BypassMethod.CURL_CFFI,
                protection_detected=ProtectionType.UNKNOWN, response_time=0,
                status_code=None, error="curl_cffi não disponível", metrics={}
            )
        
        start_time = time.time()
        method = BypassMethod.CURL_CFFI
        self.bypass_stats[method]['attempts'] += 1
        
        try:
            domain = urlparse(url).netloc
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            user_agent = self.ua_rotator.get_random_agent('chrome')
            headers = self.ua_rotator.get_matching_headers(user_agent)
            
            # Usa curl_cffi com impersonate Chrome
            response = cf_requests.get(
                url, 
                headers=headers, 
                timeout=timeout,
                impersonate="chrome120"
            )
            response_time = time.time() - start_time
            
            protection = self.protection_detector.detect_protection(
                response.text, dict(response.headers), response.status_code
            )
            
            success = response.status_code == 200 and protection == ProtectionType.NONE
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=response.text if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=response.status_code,
                error=None,
                metrics={'content_length': len(response.text)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
    
    def _method_requests_html(self, url: str, timeout: int = 30) -> BypassResult:
        """Método 5: Requests-HTML com renderização JavaScript"""
        if not REQUESTS_HTML_AVAILABLE:
            return BypassResult(
                success=False, html=None, method=BypassMethod.REQUESTS_HTML,
                protection_detected=ProtectionType.UNKNOWN, response_time=0,
                status_code=None, error="Requests-HTML não disponível", metrics={}
            )
        
        start_time = time.time()
        method = BypassMethod.REQUESTS_HTML
        self.bypass_stats[method]['attempts'] += 1
        
        session = None
        try:
            domain = urlparse(url).netloc
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            session = HTMLSession()
            
            user_agent = self.ua_rotator.get_random_agent('chrome')
            headers = self.ua_rotator.get_matching_headers(user_agent)
            
            response = session.get(url, headers=headers, timeout=timeout)
            
            # Detecta se precisa renderizar JavaScript
            initial_protection = self.protection_detector.detect_protection(
                response.html.html, dict(response.headers), response.status_code
            )
            
            if initial_protection != ProtectionType.NONE:
                logger.info(f"Detectada proteção {initial_protection.value}, renderizando JavaScript...")
                response.html.render(timeout=20, wait=3, sleep=2)
            
            response_time = time.time() - start_time
            
            protection = self.protection_detector.detect_protection(
                response.html.html, dict(response.headers), response.status_code
            )
            
            success = (
                response.status_code == 200 and 
                len(response.html.html) > 1000 and
                protection == ProtectionType.NONE
            )
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=response.html.html if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=response.status_code,
                error=None,
                metrics={'content_length': len(response.html.html)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
        finally:
            if session:
                try:
                    session.close()
                except:
                    pass
    
    def _method_undetected_chrome(self, url: str, timeout: int = 45) -> BypassResult:
        """Método 6: Undetected Chrome com máximo stealth"""
        if not UNDETECTED_CHROME_AVAILABLE:
            return BypassResult(
                success=False, html=None, method=BypassMethod.UNDETECTED_CHROME,
                protection_detected=ProtectionType.UNKNOWN, response_time=0,
                status_code=None, error="Undetected Chrome não disponível", metrics={}
            )
        
        start_time = time.time()
        method = BypassMethod.UNDETECTED_CHROME
        self.bypass_stats[method]['attempts'] += 1
        
        driver = None
        try:
            domain = urlparse(url).netloc
            delay = self.delay_manager.get_delay(domain)
            time.sleep(delay)
            
            # Configurações stealth máximas
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
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-field-trial-config')
            options.add_argument('--disable-back-forward-cache')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-default-apps')
            options.add_argument('--disable-sync')
            options.add_argument('--disable-translate')
            options.add_argument('--hide-scrollbars')
            options.add_argument('--mute-audio')
            options.add_argument('--no-first-run')
            options.add_argument('--safebrowsing-disable-auto-update')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-update')
            options.add_argument('--disable-domain-reliability')
            
            # User agent customizado
            user_agent = self.ua_rotator.get_random_agent('chrome')
            options.add_argument(f'--user-agent={user_agent}')
            
            # Força uso da versão 138 do Chrome para compatibilidade
            driver = uc.Chrome(options=options, version_main=138)
            
            # Simula comportamento humano
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            driver.get(url)
            
            # Aguarda carregamento e possível challenge
            time.sleep(5)
            
            # Verifica se há challenge do Cloudflare
            try:
                WebDriverWait(driver, 15).until(
                    lambda d: 'checking your browser' not in d.page_source.lower()
                )
            except TimeoutException:
                pass
            
            # Simula movimento humano
            driver.execute_script("""
                // Simula movimento de mouse
                var event = new MouseEvent('mousemove', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': Math.random() * window.innerWidth,
                    'clientY': Math.random() * window.innerHeight
                });
                document.dispatchEvent(event);
                
                // Simula scroll
                window.scrollTo(0, Math.random() * 100);
            """)
            
            time.sleep(2)
            
            html = driver.page_source
            response_time = time.time() - start_time
            
            protection = self.protection_detector.detect_protection(
                html, {}, 200  # Assume 200 para Selenium
            )
            
            success = len(html) > 1000 and protection == ProtectionType.NONE
            
            if success:
                self.bypass_stats[method]['successes'] += 1
            
            self.delay_manager.record_attempt(domain, success, response_time)
            
            return BypassResult(
                success=success,
                html=html if success else None,
                method=method,
                protection_detected=protection,
                response_time=response_time,
                status_code=200,
                error=None,
                metrics={'content_length': len(html)}
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            return BypassResult(
                success=False,
                html=None,
                method=method,
                protection_detected=ProtectionType.UNKNOWN,
                response_time=response_time,
                status_code=None,
                error=str(e),
                metrics={}
            )
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def advanced_cloudflare_bypass(self, url: str, max_retries: int = 3) -> Optional[str]:
        """
        Sistema avançado de bypass para Cloudflare e outras proteções
        
        Hierarquia de fallback inteligente:
        1. Requests padrão com headers otimizados
        2. Cloudscraper com configurações avançadas
        3. TLS Client com JA3 fingerprint spoofing
        4. curl_cffi para máxima compatibilidade
        5. Requests-HTML com renderização JavaScript
        6. Undetected Chrome com stealth máximo
        """
        logger.info(f"🚀 Iniciando bypass avançado para: {url}")
        
        # Métodos em ordem de prioridade (mais rápido para mais lento)
        methods = [
            self._method_requests,
            self._method_cloudscraper,
            self._method_tls_client,
            self._method_curl_cffi,
            self._method_requests_html,
            self._method_undetected_chrome
        ]
        
        results = []
        
        for attempt in range(max_retries):
            logger.info(f"🔄 Tentativa {attempt + 1}/{max_retries}")
            
            for method_func in methods:
                try:
                    result = method_func(url)
                    results.append(result)
                    
                    logger.info(
                        f"📊 {result.method.value}: "
                        f"{'✅ Sucesso' if result.success else '❌ Falha'} "
                        f"({result.response_time:.2f}s) "
                        f"Proteção: {result.protection_detected.value}"
                    )
                    
                    if result.success:
                        logger.info(f"🎉 Bypass bem-sucedido com {result.method.value}!")
                        self._log_success_stats()
                        return result.html
                    
                    # Se detectou proteção específica, ajusta estratégia
                    if result.protection_detected == ProtectionType.CLOUDFLARE:
                        logger.info("🛡️ Cloudflare detectado, priorizando métodos stealth...")
                        # Reordena métodos para priorizar stealth
                        methods = [
                            self._method_undetected_chrome,
                            self._method_requests_html,
                            self._method_cloudscraper,
                            self._method_curl_cffi,
                            self._method_tls_client,
                            self._method_requests
                        ]
                        break
                    
                except Exception as e:
                    logger.error(f"❌ Erro no método {method_func.__name__}: {e}")
                    continue
            
            # Delay entre tentativas
            if attempt < max_retries - 1:
                delay = (attempt + 1) * 2  # Backoff exponencial
                logger.info(f"⏳ Aguardando {delay}s antes da próxima tentativa...")
                time.sleep(delay)
        
        logger.error(f"💥 Falha em todos os métodos de bypass para {url}")
        self._log_failure_stats(results)
        return None
    
    def _log_success_stats(self):
        """Log das estatísticas de sucesso"""
        logger.info("📈 Estatísticas de Bypass:")
        for method, stats in self.bypass_stats.items():
            if stats['attempts'] > 0:
                success_rate = (stats['successes'] / stats['attempts']) * 100
                logger.info(f"  {method.value}: {success_rate:.1f}% ({stats['successes']}/{stats['attempts']})")
    
    def _log_failure_stats(self, results: List[BypassResult]):
        """Log das estatísticas de falha"""
        logger.error("💔 Análise de Falhas:")
        
        protection_counts = {}
        for result in results:
            prot = result.protection_detected.value
            protection_counts[prot] = protection_counts.get(prot, 0) + 1
        
        logger.error(f"  Proteções detectadas: {protection_counts}")
        
        errors = [r.error for r in results if r.error]
        if errors:
            logger.error(f"  Erros comuns: {set(errors)}")

# Instância global do bypass avançado
advanced_bypass = AdvancedCloudflareBypass()

def get_ids(url):
    """
    Função principal otimizada para detecção de IDs com bypass avançado do Cloudflare
    
    Mantém compatibilidade com a versão original mas com capacidades muito superiores
    """
    ids = []
    links = []
    technologies = []
    contact_info = []
    
    try:
        # Normaliza URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"🎯 Iniciando análise avançada de: {url}")
        
        # Usa o sistema avançado de bypass
        html = advanced_bypass.advanced_cloudflare_bypass(url, max_retries=2)
        
        if not html:
            logger.error(f"❌ Falha ao obter conteúdo de {url}")
            # Retorna dicionário para compatibilidade com testes
            return {
                'tracking_ids': len(ids),
                'links': len(links),
                'technologies': len(technologies),
                'contacts': len(contact_info),
                'ids_list': ids,
                'links_list': links,
                'technologies_list': technologies,
                'contacts_list': contact_info
            }
        
        logger.info(f"✅ Conteúdo obtido: {len(html)} caracteres")
        
        # Parse do HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # === DETECÇÃO DE IDs DE RASTREAMENTO ===
        
        # Google Analytics (Universal e GA4)
        ga_patterns = [
            r'UA-\d+-\d+',  # Universal Analytics
            r'G-[A-Z0-9]{10}',  # GA4
            r'gtag\(["\']config["\'],\s*["\']([^"\'\']+)["\']',  # gtag config
            r'ga\(["\']create["\'],\s*["\']([^"\'\']+)["\']'  # ga create
        ]
        
        for pattern in ga_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match not in ids:
                    ids.append(match)
                    logger.info(f"🔍 Google Analytics detectado: {match}")
        
        # Google Tag Manager
        gtm_patterns = [
            r'GTM-[A-Z0-9]{6,8}',
            r'googletagmanager\.com/gtm\.js\?id=([^"\'\'&]+)'
        ]
        
        for pattern in gtm_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match not in ids:
                    ids.append(match)
                    logger.info(f"🔍 Google Tag Manager detectado: {match}")
        
        # Facebook Pixel
        fb_patterns = [
            r'fbq\(["\']init["\'],\s*["\']([0-9]{15,16})["\']',
            r'facebook\.com/tr\?id=([0-9]{15,16})',
            r'_fbp["\']?:\s*["\']([^"\'\']+)["\']'
        ]
        
        for pattern in fb_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match not in ids:
                    ids.append(match)
                    logger.info(f"🔍 Facebook Pixel detectado: {match}")
        
        # Hotjar
        hotjar_patterns = [
            r'hjid["\']?:\s*["\']?([0-9]{6,8})',
            r'hotjar\.com/c/hotjar-([0-9]{6,8})',
            r'hj\(["\']identify["\'],\s*["\']([^"\'\']+)["\']'
        ]
        
        for pattern in hotjar_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match not in ids:
                    ids.append(match)
                    logger.info(f"🔍 Hotjar detectado: {match}")
        
        # Google Ads
        gads_patterns = [
            r'AW-[0-9]{9,11}',
            r'googleadservices\.com/pagead/conversion/([0-9]{9,11})'
        ]
        
        for pattern in gads_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match not in ids:
                    ids.append(match)
                    logger.info(f"🔍 Google Ads detectado: {match}")
        
        # === DETECÇÃO DE LINKS ===
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith(('http://', 'https://')):
                if href not in links:
                    links.append(href)
        
        # === DETECÇÃO DE TECNOLOGIAS ===
        
        # JavaScript frameworks
        js_frameworks = {
            'React': [r'react', r'_react', r'__REACT_DEVTOOLS_GLOBAL_HOOK__'],
            'Vue.js': [r'vue\.js', r'__VUE__', r'vue-'],
            'Angular': [r'angular', r'ng-', r'_angular'],
            'jQuery': [r'jquery', r'\$\(document\)\.ready'],
            'Bootstrap': [r'bootstrap', r'btn-', r'container-fluid']
        }
        
        for framework, patterns in js_frameworks.items():
            for pattern in patterns:
                if re.search(pattern, html, re.IGNORECASE):
                    if framework not in technologies:
                        technologies.append(framework)
                        logger.info(f"🔧 Tecnologia detectada: {framework}")
                    break
        
        # CMS Detection
        cms_indicators = {
            'WordPress': [r'wp-content', r'wp-includes', r'/wp-json/'],
            'Drupal': [r'drupal', r'sites/default/files'],
            'Joomla': [r'joomla', r'option=com_'],
            'Shopify': [r'shopify', r'cdn\.shopify\.com'],
            'Magento': [r'magento', r'mage/cookies']
        }
        
        for cms, patterns in cms_indicators.items():
            for pattern in patterns:
                if re.search(pattern, html, re.IGNORECASE):
                    if cms not in technologies:
                        technologies.append(cms)
                        logger.info(f"🔧 CMS detectado: {cms}")
                    break
        
        # === DETECÇÃO DE INFORMAÇÕES DE CONTATO ===
        
        # Emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        for email in emails:
            if email not in contact_info:
                contact_info.append(email)
                logger.info(f"📧 Email detectado: {email}")
        
        # Telefones
        phone_patterns = [
            r'\+?\d{1,3}[\s.-]?\(?\d{2,3}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}',
            r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, html)
            for phone in phones:
                if phone not in contact_info and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) >= 10:
                    contact_info.append(phone)
                    logger.info(f"📞 Telefone detectado: {phone}")
        
        logger.info(f"🎉 Análise concluída: {len(ids)} IDs, {len(links)} links, {len(technologies)} tecnologias, {len(contact_info)} contatos")
        
    except Exception as e:
        logger.error(f"💥 Erro na análise: {str(e)}")
    
    # Retorna dicionário para compatibilidade com testes
    return {
        'tracking_ids': len(ids),
        'links': len(links),
        'technologies': len(technologies),
        'contacts': len(contact_info),
        'ids_list': ids,
        'links_list': links,
        'technologies_list': technologies,
        'contacts_list': contact_info
    }

# Função de compatibilidade para manter a interface original
def advanced_cloudflare_bypass(url: str, max_retries: int = 3) -> Optional[str]:
    """
    Função standalone para bypass avançado do Cloudflare
    
    Args:
        url: URL para fazer bypass
        max_retries: Número máximo de tentativas
    
    Returns:
        HTML da página ou None se falhar
    """
    return advanced_bypass.advanced_cloudflare_bypass(url, max_retries)

if __name__ == "__main__":
    # Teste da funcionalidade
    test_url = "https://httpbin.org"
    logger.info(f"🧪 Testando bypass avançado com: {test_url}")
    
    result = get_ids(test_url)
    logger.info(f"📊 Resultado do teste: {len(result[0])} IDs encontrados")