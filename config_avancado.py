#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração Avançada do Sistema F.T.M Otimizado

Este arquivo contém todas as configurações personalizáveis do sistema
de bypass avançado, permitindo ajustes finos para diferentes cenários.

Autor: F.T.M Team
Versão: 2.0 - Otimizada
Data: 2024
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum

class LogLevel(Enum):
    """Níveis de log disponíveis"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ProxyType(Enum):
    """Tipos de proxy suportados"""
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"

@dataclass
class TimeoutConfig:
    """Configurações de timeout para diferentes operações"""
    connect: int = 10  # Timeout de conexão
    read: int = 30     # Timeout de leitura
    total: int = 60    # Timeout total por tentativa
    between_retries: int = 2  # Delay entre tentativas

@dataclass
class RetryConfig:
    """Configurações de retry e backoff"""
    max_retries: int = 3
    backoff_factor: float = 1.5
    max_backoff: int = 30
    retry_on_status: List[int] = field(default_factory=lambda: [429, 502, 503, 504])
    retry_on_exceptions: List[str] = field(default_factory=lambda: [
        'ConnectionError', 'Timeout', 'ReadTimeout', 'ConnectTimeout'
    ])

@dataclass
class UserAgentConfig:
    """Configurações do sistema de User-Agent"""
    rotation_enabled: bool = True
    use_real_stats: bool = True
    custom_agents: List[str] = field(default_factory=list)
    browsers: List[str] = field(default_factory=lambda: ['chrome', 'firefox', 'safari', 'edge'])
    platforms: List[str] = field(default_factory=lambda: ['windows', 'macos', 'linux'])
    cache_size: int = 100
    update_interval_hours: int = 24

@dataclass
class ProxyConfig:
    """Configurações de proxy"""
    enabled: bool = False
    rotation_enabled: bool = False
    proxy_list: List[str] = field(default_factory=list)
    proxy_type: ProxyType = ProxyType.HTTP
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    test_url: str = "http://httpbin.org/ip"
    max_failures: int = 3
    health_check_interval: int = 300  # segundos

@dataclass
class CloudflareConfig:
    """Configurações específicas para bypass do Cloudflare"""
    challenge_timeout: int = 30
    wait_for_challenge: bool = True
    solve_captcha: bool = False
    captcha_service: Optional[str] = None  # '2captcha', 'anticaptcha', etc.
    captcha_api_key: Optional[str] = None
    browser_profile_path: Optional[str] = None
    headless_mode: bool = True
    window_size: Tuple[int, int] = (1920, 1080)
    disable_images: bool = True
    disable_css: bool = False
    disable_javascript: bool = False

@dataclass
class DetectionConfig:
    """Configurações de detecção de proteções e conteúdo"""
    # Detecção de proteções
    protection_detection_enabled: bool = True
    protection_indicators: Dict[str, List[str]] = field(default_factory=lambda: {
        'cloudflare': [
            'cf-ray', 'cloudflare', '__cf_bm', 'cf_clearance',
            'checking your browser', 'ddos protection by cloudflare',
            'attention required', 'cloudflare ray id'
        ],
        'incapsula': [
            'incap_ses', 'visid_incap', 'incapsula',
            'request unsuccessful', 'incident id'
        ],
        'akamai': [
            'akamai', '_abck', 'ak_bmsc',
            'reference #', 'access denied'
        ],
        'ddos_guard': [
            'ddos-guard', '__ddg1', '__ddg2',
            'ddos protection', 'checking your browser'
        ],
        'sucuri': [
            'sucuri', 'access denied',
            'blocked by sucuri', 'sucuri cloudproxy'
        ]
    })
    
    # Detecção de IDs de rastreamento
    tracking_patterns: Dict[str, str] = field(default_factory=lambda: {
        'google_analytics': r'UA-\d+-\d+|G-[A-Z0-9]+',
        'google_tag_manager': r'GTM-[A-Z0-9]+',
        'facebook_pixel': r'fbq\([^)]*["\']([0-9]{15,16})["\']',
        'hotjar': r'hjid["\']?:\s*["\']?([0-9]{6,8})',
        'google_ads': r'AW-[0-9]+',
        'yandex_metrica': r'ym\([^)]*([0-9]{8,9})',
        'mixpanel': r'mixpanel\.init\(["\']([a-f0-9]{32})["\']',
        'segment': r'analytics\.load\(["\']([a-zA-Z0-9]{20,})["\']'
    })
    
    # Detecção de tecnologias
    technology_patterns: Dict[str, str] = field(default_factory=lambda: {
        'react': r'react|__REACT_DEVTOOLS_GLOBAL_HOOK__|_reactInternalFiber',
        'angular': r'angular|ng-version|__ng_|ngDevMode',
        'vue': r'vue\.js|__VUE__|Vue\.config',
        'jquery': r'jquery|\$\.fn\.jquery',
        'bootstrap': r'bootstrap|btn-primary|container-fluid',
        'wordpress': r'wp-content|wp-includes|wordpress',
        'drupal': r'drupal|sites/default|sites/all',
        'joomla': r'joomla|com_content|option=com_'
    })
    
    # Detecção de contatos
    contact_patterns: Dict[str, str] = field(default_factory=lambda: {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone_br': r'\(?\d{2}\)?\s?9?\d{4}-?\d{4}',
        'phone_us': r'\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}',
        'whatsapp': r'wa\.me/\d+|whatsapp.*\d+'
    })

@dataclass
class CacheConfig:
    """Configurações de cache"""
    enabled: bool = True
    cache_dir: str = field(default_factory=lambda: os.path.join(os.getcwd(), '.ftm_cache'))
    max_size_mb: int = 100
    ttl_seconds: int = 3600  # 1 hora
    cleanup_interval: int = 300  # 5 minutos
    cache_responses: bool = True
    cache_user_agents: bool = True
    cache_proxy_health: bool = True

@dataclass
class LoggingConfig:
    """Configurações de logging"""
    enabled: bool = True
    level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    max_file_size_mb: int = 10
    backup_count: int = 5
    log_to_console: bool = True
    log_requests: bool = True
    log_responses: bool = False  # Pode ser muito verboso
    log_performance: bool = True

@dataclass
class SecurityConfig:
    """Configurações de segurança"""
    verify_ssl: bool = True
    allow_redirects: bool = True
    max_redirects: int = 10
    cookie_jar_enabled: bool = True
    cookie_persistence: bool = True
    cookie_file: Optional[str] = None
    headers_blacklist: List[str] = field(default_factory=lambda: [
        'authorization', 'x-api-key', 'x-auth-token'
    ])
    sanitize_urls: bool = True
    max_content_length: int = 50 * 1024 * 1024  # 50MB

@dataclass
class PerformanceConfig:
    """Configurações de performance"""
    max_concurrent_requests: int = 10
    connection_pool_size: int = 20
    adaptive_delays: bool = True
    min_delay_seconds: float = 0.5
    max_delay_seconds: float = 5.0
    success_rate_threshold: float = 0.8
    performance_monitoring: bool = True
    memory_limit_mb: int = 500
    cpu_limit_percent: int = 80

@dataclass
class AdvancedConfig:
    """Configuração principal que agrupa todas as outras"""
    # Configurações básicas
    debug_mode: bool = False
    dry_run: bool = False
    
    # Sub-configurações
    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    retries: RetryConfig = field(default_factory=RetryConfig)
    user_agent: UserAgentConfig = field(default_factory=UserAgentConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    cloudflare: CloudflareConfig = field(default_factory=CloudflareConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Configurações de bypass method priority
    bypass_method_priority: List[str] = field(default_factory=lambda: [
        'requests', 'cloudscraper', 'tls_client', 'curl_cffi', 
        'requests_html', 'undetected_chrome'
    ])
    
    # Configurações específicas por domínio
    domain_specific_config: Dict[str, Dict] = field(default_factory=dict)
    
    def get_domain_config(self, domain: str) -> Dict:
        """Retorna configuração específica para um domínio"""
        return self.domain_specific_config.get(domain, {})
    
    def set_domain_config(self, domain: str, config: Dict):
        """Define configuração específica para um domínio"""
        self.domain_specific_config[domain] = config
    
    def to_dict(self) -> Dict:
        """Converte a configuração para dicionário"""
        import json
        from dataclasses import asdict
        
        def enum_serializer(obj):
            if isinstance(obj, Enum):
                return obj.value
            raise TypeError(f"Object {obj} is not JSON serializable")
        
        return json.loads(json.dumps(asdict(self), default=enum_serializer))
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AdvancedConfig':
        """Cria configuração a partir de dicionário"""
        # Implementação simplificada - em produção seria mais robusta
        config = cls()
        
        # Atualiza campos básicos
        if 'debug_mode' in data:
            config.debug_mode = data['debug_mode']
        if 'dry_run' in data:
            config.dry_run = data['dry_run']
        
        # Atualiza bypass method priority
        if 'bypass_method_priority' in data:
            config.bypass_method_priority = data['bypass_method_priority']
        
        # Atualiza configurações específicas por domínio
        if 'domain_specific_config' in data:
            config.domain_specific_config = data['domain_specific_config']
        
        return config
    
    def save_to_file(self, filepath: str):
        """Salva configuração em arquivo JSON"""
        import json
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'AdvancedConfig':
        """Carrega configuração de arquivo JSON"""
        import json
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)

# Configurações pré-definidas para diferentes cenários
class PresetConfigs:
    """Configurações pré-definidas para cenários comuns"""
    
    @staticmethod
    def development() -> AdvancedConfig:
        """Configuração para desenvolvimento - mais verbosa e permissiva"""
        config = AdvancedConfig()
        config.debug_mode = True
        config.logging.level = LogLevel.DEBUG
        config.logging.log_to_console = True
        config.cloudflare.headless_mode = False
        config.timeouts.total = 120
        config.retries.max_retries = 5
        return config
    
    @staticmethod
    def production() -> AdvancedConfig:
        """Configuração para produção - otimizada e silenciosa"""
        config = AdvancedConfig()
        config.debug_mode = False
        config.logging.level = LogLevel.WARNING
        config.logging.log_to_console = False
        config.logging.log_file = 'ftm_production.log'
        config.cloudflare.headless_mode = True
        config.performance.max_concurrent_requests = 20
        config.cache.enabled = True
        return config
    
    @staticmethod
    def stealth() -> AdvancedConfig:
        """Configuração para máximo stealth - mais lenta mas mais eficaz"""
        config = AdvancedConfig()
        config.user_agent.rotation_enabled = True
        config.proxy.enabled = True
        config.proxy.rotation_enabled = True
        config.performance.adaptive_delays = True
        config.performance.min_delay_seconds = 2.0
        config.performance.max_delay_seconds = 10.0
        config.cloudflare.wait_for_challenge = True
        config.cloudflare.challenge_timeout = 60
        return config
    
    @staticmethod
    def fast() -> AdvancedConfig:
        """Configuração para velocidade máxima - menos stealth"""
        config = AdvancedConfig()
        config.timeouts.total = 30
        config.retries.max_retries = 2
        config.performance.adaptive_delays = False
        config.performance.min_delay_seconds = 0.1
        config.performance.max_concurrent_requests = 50
        config.cloudflare.headless_mode = True
        config.cloudflare.disable_images = True
        config.cloudflare.disable_css = True
        return config
    
    @staticmethod
    def research() -> AdvancedConfig:
        """Configuração para pesquisa acadêmica - máxima detecção"""
        config = AdvancedConfig()
        config.detection.protection_detection_enabled = True
        config.logging.level = LogLevel.INFO
        config.logging.log_performance = True
        config.cache.enabled = True
        config.cache.ttl_seconds = 7200  # 2 horas
        config.performance.performance_monitoring = True
        return config

# Instância global da configuração (pode ser sobrescrita)
GLOBAL_CONFIG = AdvancedConfig()

def get_config() -> AdvancedConfig:
    """Retorna a configuração global atual"""
    return GLOBAL_CONFIG

def set_config(config: AdvancedConfig):
    """Define a configuração global"""
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = config

def load_config_from_env() -> AdvancedConfig:
    """Carrega configuração a partir de variáveis de ambiente"""
    config = AdvancedConfig()
    
    # Exemplos de variáveis de ambiente
    if os.getenv('FTM_DEBUG', '').lower() == 'true':
        config.debug_mode = True
    
    if os.getenv('FTM_LOG_LEVEL'):
        try:
            config.logging.level = LogLevel(os.getenv('FTM_LOG_LEVEL').upper())
        except ValueError:
            pass
    
    if os.getenv('FTM_TIMEOUT'):
        try:
            config.timeouts.total = int(os.getenv('FTM_TIMEOUT'))
        except ValueError:
            pass
    
    if os.getenv('FTM_PROXY_LIST'):
        config.proxy.proxy_list = os.getenv('FTM_PROXY_LIST').split(',')
        config.proxy.enabled = True
    
    return config

# Exemplo de uso
if __name__ == "__main__":
    # Demonstra diferentes configurações
    print("🔧 F.T.M - CONFIGURAÇÕES AVANÇADAS")
    print("=" * 50)
    
    # Configuração padrão
    print("\n📋 Configuração Padrão:")
    default_config = AdvancedConfig()
    print(f"   • Debug Mode: {default_config.debug_mode}")
    print(f"   • Timeout Total: {default_config.timeouts.total}s")
    print(f"   • Max Retries: {default_config.retries.max_retries}")
    
    # Configuração de produção
    print("\n🏭 Configuração de Produção:")
    prod_config = PresetConfigs.production()
    print(f"   • Log Level: {prod_config.logging.level.value}")
    print(f"   • Log File: {prod_config.logging.log_file}")
    print(f"   • Max Concurrent: {prod_config.performance.max_concurrent_requests}")
    
    # Configuração stealth
    print("\n🥷 Configuração Stealth:")
    stealth_config = PresetConfigs.stealth()
    print(f"   • User-Agent Rotation: {stealth_config.user_agent.rotation_enabled}")
    print(f"   • Proxy Enabled: {stealth_config.proxy.enabled}")
    print(f"   • Min Delay: {stealth_config.performance.min_delay_seconds}s")
    
    # Salva exemplo de configuração
    print("\n💾 Salvando configuração de exemplo...")
    example_config = PresetConfigs.development()
    example_config.save_to_file('config_exemplo.json')
    print("   ✅ Salvo em: config_exemplo.json")
    
    print("\n" + "=" * 50)
    print("✨ Configurações prontas para uso!")